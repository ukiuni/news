---
layout: post
title: Detect memory leaks of C extensions with psutil and psleak - psutilとpsleakでC拡張のメモリリークを検出する
date: 2025-12-27 15:40:12.764000+00:00
categories:
- tech
- world-news
tags:
- tech-news
- japan
source_url: https://gmpy.dev/blog/2025/psutil-heap-introspection-apis
source_title: Detect memory leaks of C extensions with psutil and psleak
source_id: 46376608
excerpt: psutilとpsleakで隠れたC拡張のネイティブヒープ漏れを自動検出する方法を紹介
---
# Detect memory leaks of C extensions with psutil and psleak - psutilとpsleakでC拡張のメモリリークを検出する

## 要約
psutil 7.2.0 が提供するネイティブヒープ向けAPI（heap_info / heap_trim）を使えば、pymalloc の上に隠れた C レイヤーのメモリリークを直接検出できる。psleak はこれを自動化して単体テストに組み込めるツールだ。

## この記事を読むべき理由
NumPy、pandas、PyTorch、psycopg、独自 C 拡張など C 層を持つライブラリは日本のプロダクトでも多用されている。RSS が安定しているのにプロセスが徐々にメモリを消費している場合、原因は C の malloc()/mmap() 側にあることが多く、従来の tracemalloc や参照カウントだけでは発見できない。これは本番運用や CI での安定性に直結する問題なので、早期検出手段を知る価値が高い。

## 詳細解説
- 問題の本質：CPython は小さな Python オブジェクト管理に pymalloc を使うが、C 拡張が直接 malloc()/mmap() を使うと、その割当ては Python の統計（sys.getrefcount, tracemalloc, gc）や時に RSS に現れにくい。結果として「メモリが増えているのに原因が見えない」状況が起きる。
- psutil の新API：
  - heap_info(): プラットフォームのネイティブアロケータを直接調べ、現在 malloc()／mmap() によって実際に使われているバイト数を返す。主なフィールドは heap_used（小さめの malloc）、mmap_used（大きな malloc/mmap）、Windows では heap_count（HeapCreate の数）。
  - heap_trim(): アロケータに未使用領域の解放を試みさせ、測定ノイズを減らす。実際の RSS を大きく減らすことが保証されるわけではないが、差分測定の精度向上に有用。
- 検出手順（概念）：
  1. heap_trim() でノイズを下げる
  2. baseline を取得（heap_info()）
  3. 疑わしい C 関数を大量に実行
  4. 再度 heap_info() を取得して差分を評価
  5. 値が継続的に増えるならネイティブリークの可能性が高い
- 実際のツール：psleak は上記の手順を自動化し、複数回のリトライや統計的判定を行って「一貫して増加する領域」をリークとして報告する。

コード例（簡潔）
```python
# python
import psutil

psutil.heap_trim()           # ノイズ抑制
before = psutil.heap_info()
for _ in range(200):
    my_cext_function()       # 問題の C 拡張を繰り返し呼ぶ
after = psutil.heap_info()
print("delta heap_used =", after.heap_used - before.heap_used)
print("delta mmap_used =", after.mmap_used - before.mmap_used)
```

psleak の最小例
```python
# python
from psleak import MemoryLeakTestCase

class TestLeaks(MemoryLeakTestCase):
    def test_fun(self):
        self.execute(some_c_function)
```

## 実践ポイント
- まず psutil >= 7.2.0 を入れる（pip install psutil）。psleak は PyPI から取得可能。
- テストは複数回（回数を増やして）実行し、heap_trim() を毎回行って測定ノイズを減らす。
- 増加が観測されたら、該当 C 拡張側で malloc/free の不整合、malloc と対応する free の欠損、Py_DECREF の忘れ等を疑う。可能なら AddressSanitizer や Valgrind と併用して特定を進める。
- CI に psleak ベースのテストを組み込み、リリース前にネイティブリークの回帰を検出する。
- Windows は heap_count 等の特殊フィールドがあり挙動が異なる点に注意する。

