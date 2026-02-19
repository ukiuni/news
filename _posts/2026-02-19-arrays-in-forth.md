---
layout: post
title: "Arrays in Forth - Forthにおける配列設計術"
date: 2026-02-19T18:12:18.672Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.forth.org/svfig/Len/arrays.htm"
source_title: "Arrays in Forth"
source_id: 47022527
excerpt: "限られたメモリで動く製品向けにForthで最適な配列設計を自作する実践ガイド"
---

# Arrays in Forth - Forthにおける配列設計術
魅力的な配列がなくても大丈夫。Forth流に「自分で作る」自由と利点を体感しよう

## 要約
Forthは言語標準で汎用的な配列を持たない代わりに、用途に合わせた「配列的構造」を簡潔に作れるのが強み。バッファ的なunindexed、要素単位で扱うindexed、可変要素長やサブフィールドまで柔軟に実装できる。

## この記事を読むべき理由
日本の組込み・レトロ系開発や教育でForthに触れる機会が増えています。言語仕様に依存せず、効率的にメモリ表現を設計するスキルは、限られた資源で動く製品開発や低レイヤ実装で役立ちます。

## 詳細解説
- unindexed（非添字）配列  
  コンパイル時にバイト数を確保し、起点アドレスを返す「作業領域」。バッファ用途が主。例:
```forth
: unindexed-array ( n -- a ) create allot ;
80 unindexed-array u-foo   \ 80バイトの領域 u-foo
```

- indexed（添字）配列  
  要素長で領域を分割し、インデックスからその要素のアドレスを返す形式。代表例は「セル長（cell）単位」のvariable-like配列。
```forth
: array ( n -- ) create cells allot does> cells + ;
100 array foo    \ セル100個分
3 foo            \ インデックス3の要素のアドレス（4番目）
```
（慣例として0始まり。実装によっては DOES> 内で swap が必要な場合あり。）

- 長要素（複数セル）を持つ配列  
  各要素を任意のセル数とする定義。コンパイル時に要素数と長さを受け、実行時にインデックスから要素アドレスを算出します。
```forth
: long-element-array ( n len -- ) create dup , * cells allot does> dup @ swap * cells + ;
10 5 long-element-array th-room   \ 5セル長×10要素の配列
4 th-room                         \ 4番目の要素アドレス
```

- サブフィールド（フィールドオフセット）  
  レコード内に複数項目がある場合はオフセットで対応。current-offset を使って順にオフセットを定義すると見通しが良くなります。
```forth
variable current-offset
: offset ( n -- ) create current-offset @ , does> @ cells + ;

current-offset off
1 offset }descriptor
1 offset }north
1 offset }east
1 offset }south
1 offset }west

\ 使い方例
3 th-room }north @         \ 部屋3の北の部屋番号を取得
4 th-room }descriptor @ execute \ 描写ルーチンを呼ぶ
```

- シンプルに「偽装」する方法  
  配列が少数なら単純に1つのバッファを作り、インデックス計算用の関数でアドレス計算するだけで十分です。
```forth
create (rooms) 200 allot
: room ( i -- a ) 20 * (rooms) + ;  \ 要素は20バイト固定
```

- ビット配列など特殊用途も容易  
  メモリをビット単位で扱うユーティリティを作れば、ビット配列も実装可能。ANS Forth準拠での実装例も存在します。

## 実践ポイント
- まず用途を決める（作業領域か、添字で要素を扱うか）。  
- 要素長がセル1つで足りるなら単純な array を使う。複数セルなら long-element-array を定義。  
- フィールドが複数あるレコードは offset を使って可読性を確保。  
- 0始まりインデックスが慣習なので、外部仕様と合わせるなら要素数を余分に確保するなどの工夫を。  
- 組込み（MCU）やメモリ制約のある環境では、この「自前で定義する設計」が最も効率的。

以上を押さえれば、Forthで配列が「ない」ことはむしろ自由への扉になります。自分の必要に忠実なデータ構造を設計してみてください。
