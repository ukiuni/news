---
layout: post
title: "Faster asin() Was Hiding In Plain Sight - 見落とされていた高速 asin() の正体"
date: 2026-03-12T14:29:46.860Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://16bpp.net/blog/post/faster-asin-was-hiding-in-plain-sight/"
source_title: "16BPP.net: Blog / Faster asin() Was Hiding In Plain Sight"
source_id: 1377873564
excerpt: "std::asinを簡潔なCg近似に置換し、実レンダリングを約8–10%高速化する手法"
---

# Faster asin() Was Hiding In Plain Sight - 見落とされていた高速 asin() の正体
asin() を置き換えるだけでレンダリングが速くなる――古い Cg 実装に隠れていた「実用的で速い近似」を掘り出した話

## 要約
元記事は、三角関数 asin(x) の高速近似を試行錯誤し、Padé や半角変換を組み合わせたアプローチを経て、最終的に NVIDIA/Cg にある極めてシンプルな近似（Abramowitz & Stegun 系の多項式）を使うことで実レンダリングが約8–10%速くなった、という検証報告です。

## この記事を読むべき理由
- グラフィックスや物理シミュレーションなどで asin がホットスポットになっている場合、簡単に置き換えて実効速度を稼げる可能性があるため。
- 日本の開発現場（レンダラー、ゲーム、数値計算ライブラリ）でもすぐに試せる実践的な手法が示されています。

## 詳細解説
- 問題意識：高頻度で呼ばれる std::asin() はコストが高く、近似で「十分な精度」を維持しながら高速化できるなら有益。
- 初手：テイラー級数（4次）で近似すると実行速度は向上（≈+5%）したが、|x|>0.8 付近で誤差が大きく実関数にフォールバックする必要があった。
- Padé 近似：テイラーから [3/4] や [5/4] の Padé を作り、中心域で精度改善。さらに半角変換（端付近を内部の小さい値へ「写像」して計算 → 結果を戻す）を導入すると端域の誤差が大幅に減る。
  - 半角変換の要点（概念式）: $$\operatorname{asin}(x)\approx\operatorname{sign}(x)\left(\frac{\pi}{2}-2\operatorname{asin}\Big(\sqrt{\frac{1-|x|}{2}}\Big)\right)$$
  - この考えで端域をより良い近似対象に変換できるため、Padé を内外で使い分けるのが有効。
- 最終解：NVIDIA の Cg ドキュメントにある古典的な近似（Abramowitz & Stegun に基づくミニマックス風多項式）を採用すると、計算が非常にシンプルかつブランチが少なく、プラットフォームによっては std::asin より大きく速い。元検証では：
  - レンダリング（PSRayTracing）：std::asin 110.9s → Taylor 104.7s → Cg 101.5s（約8.5%短縮）
  - マイクロベンチでも CPU によっては 1.4–1.9x の高速化を確認（Intel で顕著、Apple M4 では小幅）。

- 近似の式（概念）：|x| を使った多項式 p(|x|) を sqrt(1-|x|) に掛け，π/2 から引いて符号を戻す、という非常に短い評価ルーチン。

簡潔な C++ 実装例（元記事ベース）:
```cpp
// cpp
constexpr double HalfPi = 3.1415926535897932385 / 2.0;
double fast_asin_cg(double x) {
    constexpr double a0 = 1.5707288;
    constexpr double a1 = -0.2121144;
    constexpr double a2 = 0.0742610;
    constexpr double a3 = -0.0187293;
    double ax = std::fabs(x);
    double p = ((a3 * ax + a2) * ax + a1) * ax + a0; // Horner
    double res = HalfPi - std::sqrt(1.0 - ax) * p;
    return std::copysign(res, x);
}
```

## 実践ポイント
- まずプロファイル：asin が本当にボトルネックか確認する（レンダラならサンプルのテクスチャ計算周り）。
- 精度チェック：近似を導入したら視覚差分・数値差分で問題がないか確認（特に端域）。
- ハードごとの挙動：CPU/コンパイラで差が出るので、ターゲット環境でベンチすること（Intel で効果大、ARM/M シリーズは差が小さいことあり）。
- 段階導入：まずブランチ少ない Cg 風近似を試し、必要なら Padé＋半角補正で精度向上、そしてフォールバックを最小化する設計にする。
- ライブラリ化：ユーティリティ関数として切り出し、テストスイートを付けて切り替えられるようにする。

短いまとめ：asin の「劇的な改良」は新発見ではないが、実用上はいまでも有効。ホットパスに入れて検証する価値は大いにあります。
