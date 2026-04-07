---
layout: post
title: "Floating point from scratch: Hard Mode - 浮動小数点を根本から理解する：ハードモード"
date: 2026-04-07T15:23:56.021Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://essenceia.github.io/projects/floating_dragon/"
source_title: "Floating point from scratch: Hard Mode &#183; Tales on the wire"
source_id: 1595685294
excerpt: "浮動小数点の+0/-0やNaN、丸め誤差が生む落とし穴を実装者向けに解説必読"
image: "https://essenceia.github.io/projects/floating_dragon/feature.gif"
---

# Floating point from scratch: Hard Mode - 浮動小数点を根本から理解する：ハードモード
ゼロが二つある世界、NaNは感染する――実装者が直面する浮動小数点の“地獄”をやさしく解説

## 要約
Julia Desmazes の深掘り記事を基に、IEEE754準拠の浮動小数点で起きる奇妙な振る舞い（+0/-0、NaNの種類、無限大、デノーマル／漸近的アンダーフロー、丸めモードや比較の非順序性）を初心者にも分かりやすく整理。

## この記事を読むべき理由
浮動小数点はどのプログラミング言語でも当たり前に使われる一方、実装と挙動の微妙な違いがバグや性能問題を生む。特に組込みや数値ライブラリ、機械学習での型（bfloat16 など）の利用が増える日本の現場では必須の知識です。

## 詳細解説
- 表現の基本：正規化数は
  $$(-1)^S \times 2^{E-b} \times (1 + T\cdot 2^{1-p})$$
  と表され、$S$（符号）、$E$（バイアス付き指数）、$T$（有効数字の下位ビット）で構成される。簡約して $(-1)^S \times 2^e \times m$ とも書く。  
- +0 / -0：符号ビットがあるため $+0.0$ と $-0.0$ が共存。演算規則により例えば $X-X=+0.0$ など結果の符号が決まる。等価比較や符号依存の処理で落とし穴になる。  
- NaN：qNaN（quiet）と sNaN（signaling）があり、qNaN は「伝染」して以降の演算も qNaN を返す。メモリ上は指数ビットが全て1、仮数に非ゼロビットで表現される。  
- Infinity：$+\infty$ / $-\infty$ も指数全1で仮数ゼロ。数ではなく“極限”として扱われる。  
- デノーマル（subnormal）：正規化で隠し1が使えない最小領域を埋め、漸近的アンダーフロー（gradual underflow）により極小差の消失を緩やかにする。実装・性能コストが高く、古いFPUではソフトウェア処理されることも。  
- 丸めモード：IEEE は主に5種を規定（RD, RU, RZ, RN_even, RN_away）。丸めモードによってはオーバーフローが $\pm\infty$ に到達する/しない等の境界挙動が異なる（例：RU では $-\infty$ に到達しない、RZ は両極に到達しない等）。  
- 比較の「非順序性」：片方が NaN の比較は「unordered」となり、すべての NaN は自分自身とも unordered。単純な <, == に頼ると意図せぬ分岐を招く。

## 実践ポイント
- 等価比較は避け、差の絶対値と ULP（または相対誤差）で比較する。  
- NaN/Inf の判定を明示的に行い、伝播や例外を想定したテストを追加する。  
- デノーマルは性能問題の原因になり得る。性能重視なら「フラッシュ・トゥ・ゼロ（FTZ）」設定やコンパイラ/ハードのオプションを検討。  
- 丸めモードはデフォルト（近傍偶数）以外を使うと演算境界が変わるため、意図的に変更する場合は境界ケースの検証を行う。C/C++では fesetround 等で制御可能：
```cpp
// cpp
#include <cfenv>
fesetround(FE_UPWARD); // RU
```
- プラットフォーム依存（libstdc++/MSVCの実装差や bfloat16 の取り扱い）を疑い、クロスプラットフォームの単体テストとリファレンス実装で検証すること。

元記事は実装者視点で深く掘り下げた良記事なので、実装や検証に携わる技術者は原文も合わせて読むことを推奨します（著者：Julia Desmazes）。
