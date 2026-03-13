---
layout: post
title: "Reinventing Python's AsyncIO - PythonのAsyncIOを再発明する"
date: 2026-03-13T18:07:17.322Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://blog.baro.dev/p/reinventing-pythons-asyncio"
source_title: "Reinventing Python&#x27;s AsyncIO | Fluxus by gi0baro"
source_id: 1167612052
excerpt: "Event/WaiterでGILを回避しAsyncIOを2倍超高速化するTonIO"
---

# Reinventing Python's AsyncIO - PythonのAsyncIOを再発明する
PythonのAsyncIOはこう変わるかもしれない — GILを捨て、単純な「Event/Waiter」設計で高速化を狙うTonIOの試み

## 要約
既存のAsyncIOの複雑さと「メインスレッド原理」を捨て、EventとWaiterという極めて単純な原理で非同期ランタイムを再設計したTonIO（Rust実装）は、単純ベンチでAsyncIO比2〜3倍程度の高速化を示している。

## この記事を読むべき理由
Async/awaitが普及する中で「何を覚えればいいのか分からない」や「GILが足枷になる」という問題意識は日本の現場でも共通です。TonIOの考え方は、学習コスト・実装コスト・性能のトレードオフに関して実践的な示唆を与えます。特にマルチコアを活かした高速I/Oや、新規サービスの設計を検討する技術者に有益です。

## 詳細解説
- 問題意識：AsyncIOはプロトコル／トランスポートやHandleなど多くのプリミティブがあり、設計の複雑さとGIL周りの奇妙さ（メインスレッド依存）がある。結果、理解・移行コストやランタイムオーバーヘッドが常につきまとう。
- TonIOの核心アイデア：非同期は本質的に「停止（suspend）」と「再開（resume）」の仕組みであると定義し、全てをEvent（原子フラグ）とWaiter（待ちポイント）に帰着させるシンプル設計。コルーチンがWaiterをyieldすると待ち登録され、Event.set()で関連Waiterをwakeして再スケジュールする。
  - イメージ（簡略化した擬似コード）：

```python
class Event:
    flag: bool = False
    waiters: list = []
    def wait(self): return Waiter(self)
    def set(self):
        self.flag = True
        for w in self.waiters: w.wake()

class Waiter:
    def __init__(self, ev): self.event = ev
    def register(self, origin): self.origin = origin; self.event.waiters.append(self)
    def wake(self): self.origin.resume()
```

- マルチスレッド化とGIL：TonIOはRustでコアを実装し「free-threaded Python」向けに設計。メインスレッドを低レベルI/O用に限定し、アプリコードは同等のワーカースレッド群で実行することで「メインスレッド特権」を排除する。これにより、Rustの原子操作やスレッド安全性を活かして高並列化が可能になる。
- 性能：単純なCPU-boundな軽作業を多数回まわすベンチや小さなTCP echoで、AsyncIOより2倍〜3倍超の改善が報告されている（実装が単純なためオーバーヘッドが少ない）。
- 限界と現実：TonIOはまだ初期段階で互換性が低く、既存のAsyncIOエコシステム（httpx, asyncpg等）へそのまま置き換えられるわけではない。ストリームAPIの追加や既存ライブラリのラッパ／モンキーパッチが普及の鍵。

## 実践ポイント
- 新規サービスやパフォーマンスが重要な処理では、Rustでコアを実装したランタイム（TonIO的アプローチ）を評価対象に入れる。
- 既存コードを即置き換えるのは困難：まずは小さなモジュールや新規マイクロサービスで試験導入する。
- 学習用に「Event/Waiter」モデルを自前で実装してみると、Asyncの本質理解が深まる（上の擬似コードを参考に）。
- 今後のエコシステム（AnyIOの対応、httpx等のラッパ）を追い、互換層が整った段階で導入検討する。

以上。元記事はGiovanni Barillari氏の実装試行で、TonIOはRustベースの試作プロジェクトです。興味があるなら元記事（リンク）を参照してソースやベンチ詳細を確認してください。
