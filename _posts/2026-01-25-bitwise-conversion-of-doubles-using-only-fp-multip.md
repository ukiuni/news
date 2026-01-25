---
layout: post
title: "Bitwise conversion of doubles using only FP multiplication and addition - 浮動小数(double)を乗算＋加算だけでビット列に変換する方法"
date: 2026-01-25T23:10:05.985Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://dougallj.wordpress.com/2020/05/10/bitwise-conversion-of-doubles-using-only-floating-point-multiplication-and-addition/"
source_title: "Bitwise conversion of doubles using only floating-point multiplication and addition | dougallj"
source_id: 46754522
excerpt: "乗算と加算だけでdoubleのビット列を取り出す実用的な数学トリック"
image: "https://s0.wp.com/i/blank.jpg?m=1383295312i"
---

# Bitwise conversion of doubles using only FP multiplication and addition - 浮動小数(double)を乗算＋加算だけでビット列に変換する方法
乗算と加算だけで「doubleの内部ビット」を取り出す――冗談のようで実用的な、数学的トリックの完全解説

## 要約
IEEE‑754の64ビット浮動小数（double）を、ビット操作や分岐・比較・除算を使わずに、乗算と加算だけで上位/下位の2つのuint32（をdoubleに格納）へ変換し、逆変換も行える手法を示す。NaN/±Infや-0は扱えない制約がある。

## この記事を読むべき理由
- JSや限定された組み込み言語、C++のconstexprなど「ビット操作が使えない環境」でdoubleのビット表現が必要になる場面がある（デバッグ、シリアライズ、ポータブル実装など）。  
- IEEE‑754の丸め性質と最小非零量を利用する発想は、数値処理を理解するうえで良い学習になる。

## 詳細解説
ポイントは「乗算・加算だけで条件判定やビット抽出を再現する」アイデア群。

- doubleの構造は sign(1) + exponent(11) + fraction(52) の合計 $64$ ビット。通常値は $s\times(1+f\times 2^{-52})\times2^{e-1023}$、サブノーマルは暗黙1がない。
- 制約：比較・ビット演算・除算・累乗・分岐を使えない。加減乗のみ。丸めは標準の $round\ to\ nearest,\ ties\ to\ even$ に依存する。
- ブール表現：真を $1.0$、偽を $0.0$ として
  - AND = 乗算、NOT = $1-x$、OR = $x + y - x*y$ で実装可能。
- 無限大（Inf）生成を避けるため、乗算係数は絶対値 $\le 1$ に抑え、加算では許容される定数範囲内にする必要がある。
- 最小非零サブノーマル $2^{-1074}$（記事では p2(-1074)）を使ったトリック：$x + 2^{-1074} - x$ の結果は丸めに依存して離散的な値になり、これをスケールして $-1,0,1$ などの小さな集合に落とし込み、そこからビットに相当する情報（指数が小さいかどうかなど）を取り出す。
- こうして「指数が0か1か／特定範囲か」を判定し、さらに乗算によるスケーリングと再帰的組合せで52ビットの仮数部や符号ビットを分解していく。
- 最終的に得られるのは、2つのdoubleに格納した「低位32ビット」「高位32ビット」。逆変換も、固定係数の加算と乗算の組合せで元のdoubleを復元する。
- 制約・注意点：
  - NaNや±Infを正確に扱えない（変換不可）。  
  - -0 と +0 を区別できない（加減乗のみでは符号付きゼロの判別不能）。  
  - IEEE‑754の通常丸めモードかつコンパイラの「unsafe math 最適化」が無効であることが前提（シェーダーや /fp:fast のような設定では破綻する可能性）。

## 実践ポイント
- 用途例：DataView やビットキャストが使えない環境（古い埋め込みインタプリタ、限定的なconstexpr環境、教育的実験）でのビット列取得や復元に使える。  
- 実装時の注意：丸めモードと最適化オプションを固定してテストを行う。NaN/Inf/-0 の要件がある場合は別途処理を用意する（本手法では不可）。  
- テスト：境界（最大/最小ノーマル、サブノーマル、ゼロ、極端な指数）で結果を確認し、復元誤差がないことを確かめる。  
- ポーティング：元記事の実装は多数の定数を使うが、原理はどの言語にも移植可能。まずは小さなユニットで「p2(-1074) を使った判定」から試すと理解しやすい。

この記事は「無茶な制約下でも諦めない」数値処理の一例で、実務よりは教育・研究性が高いが、限定環境での実装ニーズには確実に役立ちます。
