---
layout: post
title: "Implementing Burger-Dybvig: finding the shortest decimal that round-trips to the original IEEE 754 bits, with ECMA-262 tie-breaking - 最短丸め（Burger–Dybvig）を実装してIEEE 754ビットに戻る最短10進文字列を見つける（ECMA-262準拠）"
date: 2026-03-02T14:37:55.724Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://lattice-substrate.github.io/blog/2026/02/27/shortest-roundtrip-ieee754-burger-dybvig/"
source_title: "Shortest Round-Trip: Implementing IEEE 754 to Decimal Conversion in Go — Lattice Substrate"
source_id: 392711883
excerpt: "Burger–DybvigでIEEE‑754をECMA‑262準拠の最短10進表現に復元する実装手順解説"
---

# Implementing Burger-Dybvig: finding the shortest decimal that round-trips to the original IEEE 754 bits, with ECMA-262 tie-breaking - 最短丸め（Burger–Dybvig）を実装してIEEE 754ビットに戻る最短10進文字列を見つける（ECMA-262準拠）

魅力的な日本語タイトル: 「0.1+0.2の“謎”を解く：IEEE‑754をECMA‑262仕様で最短丸めする方法（実装と要点）」

## 要約
浮動小数点をテキスト化するとき、元のIEEE‑754ビットに復元できる最短の10進表現を求める必要がある。本稿はBurger–Dybvigアルゴリズムを使い、ECMA‑262の偶数丸めルールまで満たす実装の要点を解説する。

## この記事を読むべき理由
RFC 8785（バイト決定論的なJSON）や異なる言語・実装間で「完全に同一の文字列表現」を保証したい場面は増えています。Go標準の出力は高品質でもECMA‑262厳密準拠とは限らないため、日本のサービスやライブラリで互換性を取るなら知っておくべき内容です。

## 詳細解説
- IEEE‑754 binary64 の基礎  
  浮動小数点は64ビットで、構造は符号1ビット・指数11ビット・仮数52ビット。正規化数は値を
  $$(-1)^{\text{sign}}\times 1.\text{mantissa}\times 2^{\text{exponent}-1023}$$
  と表す。非正規化数（subnormal）は暗黙の1が無くなり扱いが変わる。

- なぜ多倍長整数が必要か  
  「最短で元のビットに戻る」10進文字列を決めるには、隣接する表現との境界（半分点）を正確に扱う必要がある。浮動小数点演算では丸め誤差が入るため、$R,S,M_+,M_-$ を大整数で扱って厳密に比較する（$R$：被除数、$S$：除数スケール、$M_\pm$：上下マージン）。

- 状態初期化（スケーリング）  
  指数に応じて $R,S,M_+,M_-$ を2進で構築。パワーオブツー境界（仮数が0かつ指数が最小でない）では下側マージンが上側の半分になり、アルゴリズムは全体を2倍して非対称性を吸収する。

- 10進へのスケーリングと修正  
  最初におおよその桁位置 $k\approx\lceil\log_{10}(f)\rceil$ を当て、$R,S,M_\pm$ を$10^k$でスケール。推定がずれている場合は「高側・低側のfixup」で1桁分だけ調整する。実装では高速化のために700個程度の$10^n$をキャッシュしておく。

- 桁抽出ループ  
  各桁ごとに $R,M_\pm$ を10倍し、$d=\lfloor R/S\rfloor$ を得る。終了判定は2つの条件：
  1. round-down 条件（$R$が下側マージン内）  
  2. round-up 条件（$R+M_+$ が $S$ 以上）  
  両方満たさない限り桁を出力し続ける。

- 偶数丸めによるタイブレーク（ECMA‑262準拠）  
  両方の終了条件が同時に真になる＝ちょうど中点のときは、$2R$ と $S$ を比較して $2R<S$ なら切り下げ、$2R>S$ なら切り上げ、$2R=S$ のときは最終桁を偶数にする（banker’s rounding）。境界比較自体も仮数の偶奇で包摂/厳密を切り替え、ECMA‑262の規定に合うよう微妙に挙動を変える。

- 桁繰り上げと出力形式  
  最終桁で繰り上げが発生するとキャリー伝播が必要（例: 9→10）。結果の桁列と指数 $n$ をECMA‑262の出力ルールに従って4通りの書式（整数固定、小数点、0.x の小さい分数、指数表記）へ整形する。境界（例: $10^{21}$ の扱いなど）は仕様で厳密に決まっている。

短い参考コード（概念示唆）:
```go
// Go: 浮動小数点分解（概念）
func decodeParts(f float64) (mant uint64, exp int, isSubnormal bool) {
    bits := math.Float64bits(f)
    mant = bits & ((1<<52)-1)
    expBits := extractExp(bits) // 11ビットを得る
    if expBits == 0 { /* subnormal */ }
    // 実効仮数/指数を返す
    return
}
```

## 日本市場との関連性
- JSON APIやマイクロサービスで言語や実装が混在する環境（Go / Node / Java等）では、同じ数値の文字列表現不一致がログ比較・署名・テストで問題になる。金融系やブロックチェーン、監査ログなど「バイト単位の決定論」が重要な領域で特に有用です。
- 日本のOSSやライブラリ（Canonical JSON、シリアライザ、検証ツール）を作る/採用する際、ECMA‑262やRFC8785準拠の数値フォーマッタを検討すべきです。

## 実践ポイント
- まずは要件を確認：バイト決定論が必要か（署名・比較・相互運用性）。不要なら標準関数でOK。  
- 必要なら実装を使うか、ECMA‑262準拠を明示するライブラリを選ぶ（Goのstrconvは最短出力だがECMA準拠保証ではない）。  
- テストベクトルを大量に用意して検証する（元記事は約286kベクトルで検証）。  
- pow10キャッシュや多倍長演算のメモリ/速度に注意（実運用では事前キャッシュが効く）。  
- 実装済みのライブラリがあれば、まずそれを使い、互換性試験をCIに組み込むのが現実的な対処。

参考（読みどころ）: IEEE‑754のビット構造、$R,S,M_\pm$ の初期化・スケーリング、偶数丸めの扱い、ECMA‑262の出力区分。元実装はGoで約500行、テストで大規模検証済みです。
