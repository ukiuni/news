---
layout: post
title: "Memory layout in Zig with formulas - Zigにおけるメモリレイアウト（公式付き）"
date: 2026-01-24T20:39:35.049Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://raymondtana.github.io/math/programming/2026/01/23/zig-alignment-and-sizing.html"
source_title: "Memory Layout in Zig with Formulas - Raymond Tana"
source_id: 46744647
excerpt: "Zigのパディングとアラインメントを数式で解説し、型別サイズ計算と最適化手法が一目で分かる実践ガイド"
---

# Memory layout in Zig with formulas - Zigにおけるメモリレイアウト（公式付き）
Zigで「パディングとアラインメント」を読んで一発で分かる！メモリ配置を数式で扱う実践ガイド

## 要約
Zigの型ごとのアラインメントとサイズを計算するための明確なルールと公式を整理し、プリミティブ／構造体／列挙／配列／スライス／（非）タグ付き共用体ごとにどう決まるかを示します。

## この記事を読むべき理由
メモリ効率は組み込み、ゲーム、モバイル、サーバーパフォーマンスで直結する課題。Zigで確実にバイト数を把握し、データレイアウトを最適化したいエンジニア向けの実践知が得られます。

## 詳細解説
- 共通の不変条件  
  型Tについて常に  
  $@sizeOf(T) \ge @alignOf(T)$  
  かつ $@alignOf(T) \mid @sizeOf(T)$（アラインメントはサイズを割り切る）。

- プリミティブ  
  プリミティブはサイズ＝アラインメント。ビット数をバイト単位に丸める際は「2の冪に切り上げる」。具体的には  
  $$\texttt{bytes(bits)} := \max\{1,\,2^{\lceil\log_2(\frac{\texttt{bits}}{8})\rceil}\}$$  
  で、例えば u17 は 3 バイトではなく 4 バイトになる（次の2の冪へ）。

- 構造体（externでフィールド順固定）  
  - アラインメント：フィールドの最大値  
    $$@alignOf(struct)=\max_{\text{fields}} @alignOf(field)$$  
  - 配置ルール：各フィールドは直前の末尾からそのフィールドのアラインメントの次の倍数位置に置く。切り上げ関数は  
    $$\texttt{next\_mult}(N,m)=\left\lceil\frac{N}{m}\right\rceil\cdot m.$$  
  - サイズ：フィールド全部を収めるのに十分な、構造体アラインメントの最小倍数。Zigはデフォルトでフィールド順を最適化して最小化可能。packed struct はパディングを無くすが性能制約あり。

- 列挙型（enum）  
  インデックス幅に依存。デフォルトは要素数に応じて $b=\lceil\log_2(\text{len})\rceil$ ビットを割り当て、プリミティブと同様にバイトに丸める。

- 配列とスライス  
  $$@alignOf([N]T)=@alignOf(T),\quad @sizeOf([N]T)=N\cdot@sizeOf(T).$$  
  スライスは内部的にポインタ（usize）＋長さ（usize）なので、64bit環境なら align=8, size=16。

- 共用体（union）  
  - bare extern union（順序は外部互換）: アラインメントはフィールドの最大、サイズは最大フィールドサイズをアラインメントの倍数へ切り上げ。  
    $$@alignOf= \max @alignOf(field),\quad @sizeOf=\texttt{next\_mult}(\max @sizeOf(field),\ @alignOf)$$  
  - 通常の（タグなし）union は内部で追加のアラインメント分を消費する（実装上余分になる場合がある）。

- タグ付き共用体（union(enum)）  
  タグ（enum）のサイズを加味して、  
  $$@alignOf=\max\{@alignOf(union),@alignOf(enum)\}$$  
  $$@sizeOf=\texttt{next\_mult}\big(\max_{\text{fields}} @sizeOf(field) + @sizeOf(enum),\ @alignOf\big)$$

- 補足：ポインタはusizeに一致。32/64bitで結果が変わる点に注意。

（参考にZigで型を調べる組み込み：@alignOf, @sizeOf, @offsetOf, std.meta.fields）

コード例（型調査の出力用、抜粋）:
```zig
const std = @import("std");
fn memory_printout(T: type) void {
    std.debug.print("@alignOf({s}): {d}\t@sizeOf({s}): {d}\n", .{@typeName(T), @alignOf(T), @typeName(T), @sizeOf(T)});
}
```

## 実践ポイント
- まず @alignOf/@sizeOf/@offsetOf で型を計測して「期待と違う」場所を探す。  
- 小さなenum（要素数が少ない）を使えばタグコストを下げられる。明示的に幅を指定すると確実。  
- 構造体はフィールド順でサイズが変わる。自分で並べるか Zig に最適化させる（デフォルト）か決める。FFIは extern を使って順序固定。  
- packed struct はメモリ節約に有効だが読み書きコストやアクセス制限のトレードオフあり。  
- 32/64bit 環境で usize／ポインタ幅が変わるため、クロスコンパイルや組込みでは必ず確認する。  

元記事の知見を使えば、Zigでメモリレイアウトを手作業で正確に予測・最適化できます。
