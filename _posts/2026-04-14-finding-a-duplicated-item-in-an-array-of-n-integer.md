---
layout: post
title: "Finding a duplicated item in an array of N integers in the range 1 to N − 1 - 長さNの配列から1〜N−1の重複を見つける"
date: 2026-04-14T11:22:17.114Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://devblogs.microsoft.com/oldnewthing/20260413-00/?p=112227"
source_title: "Finding a duplicated item in an array of N integers in the range 1 to N &minus; 1 - The Old New Thing"
source_id: 363186688
excerpt: "配列を壊さず$O(N)$・$O(1)$で重複を発見するFloyd巡回検出法を実装で解説する記事。"
image: "https://devblogs.microsoft.com/oldnewthing/wp-content/uploads/sites/38/2019/02/ShowCover.jpg"
---

# Finding a duplicated item in an array of N integers in the range 1 to N − 1 - 長さNの配列から1〜N−1の重複を見つける
魅力タイトル: 配列を壊さずに重複をO(N)で見つける方法 — 面接で差がつく「巡回検出」テクニック

## 要約
配列長 $N$、要素が $1\ldots N-1$ のとき必ず存在する重複値を、配列を変更せずに線形時間・定数追加空間で見つける方法（Floydの巡回検出）を解説します。

## この記事を読むべき理由
日本でもコーディング面接や組み込み系で「追加メモリを使わずに重複を探せ」という問いは頻出。配列をポインタ列と見なす発想は実務・面接双方で即戦力になります。

## 詳細解説
問題設定：長さ $N$ の配列 A（1-based）で各要素は $1\ldots N-1$。鳩ノ巣原理により少なくとも1つ重複がある。重要点は「配列の値をインデックスとして見る」こと：

- 各添字 i（1..N）をノードとし、i → A[i] の有向辺を張ると、値が $N$ を取らないためノード $N$ は入ってこない（出はある）。従ってノード $N$ から辿ると必ず既存のサイクルに合流する。この「合流点（サイクルの始点）」が重複値を指します。
- Floydの巡回検出（ウサギとカメ法）で、配列を一切変更せずにそのサイクル開始点を線形時間・定数空間で検出できます。計算量は $O(N)$、追加メモリは $O(1)$。

補足として：
- 「要素を負にして訪問済みを示す」手法もあり（配列を書き換える、または符号ビットをフラグに使う）が配列の変更を許さない場合に不適。
- 重複が「ちょうど1つ」だけなら和を利用して $ \text{duplicate} = \sum A - \frac{N(N-1)}{2} $ と算出可能（ただしオーバーフローや複数重複に非対応）。

簡潔な実装例（配列は0ベースで受け取り、値は1..N-1）：

```python
# python
def find_duplicate(arr):
    n = len(arr)  # N
    # start from index N (1-based) -> 0-based は n-1
    def nxt(i): return arr[i] - 1  # 値を0ベースのインデックスに変換
    # 1. 出会い点を見つける
    tortoise = nxt(n-1)
    hare = nxt(nxt(n-1))
    while tortoise != hare:
        tortoise = nxt(tortoise)
        hare = nxt(nxt(hare))
    # 2. サイクルの始点（重複値）を見つける
    tortoise = n-1
    while tortoise != hare:
        tortoise = nxt(tortoise)
        hare = nxt(hare)
    return hare + 1  # 1-based の重複値を返す
```

## 実践ポイント
- 実装時は「1-based ↔ 0-based」を正確に変換すること。ミスると無限ループや範囲外参照に。
- 配列を書き換え可能ならシンプルに訪問フラグ（符号反転など）で早く書けるが、元データ復元が必要なら注意。
- 重複が必ず1つとは限らない場合、和による解法は使えない。Floyd法は「任意の重複のうちの1つ」を見つける保証がある。
- 組み込みや低メモリ環境では追加空間が小さいFloyd法が有効。面接では考え方（配列をグラフと見る）が問われることが多いので説明できると高評価。
