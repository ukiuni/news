---
layout: post
title: "Even Faster Asin() Was Staring Right At Me - さらに高速な asin() は目の前にあった"
date: 2026-03-16T16:40:03.451Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://16bpp.net/blog/post/even-faster-asin-was-staring-right-at-me/"
source_title: "16BPP.net: Blog / Even Faster asin() Was Staring Right At Me"
source_id: 47398080
excerpt: "Estrin変形でasin近似がCPUのILPを引き出し、実機で最大1.8倍高速化を実現する手法"
---

# Even Faster Asin() Was Staring Right At Me - さらに高速な asin() は目の前にあった
CPUの並列実行を引き出す「Estrinの式変形」で、近似asin()をさらに高速化するテクニック

## 要約
Cgのasin近似をHorner法からEstrinの形に変えるだけで、依存チェーンが短くなりモダンCPUで並列実行され、実機ベンチで最大1.8倍程度の高速化を確認したという話。

## この記事を読むべき理由
少しの数式整理でランタイムが実際に改善する実例は、レンダラーやゲーム、数値処理で「ちょっと速くしたい」日本のエンジニアにとってすぐ使える知識だからです。

## 詳細解説
元の近似はMinimax係数を使った多項式近似（Horner評価）で、典型的な実装は次の流れ：
- 絶対値を取り、$\sqrt{1-|x|}$ を用いた補正を行い $\frac{\pi}{2}$ から引き戻す
- 多項式は Horner 法で評価

多項式（係数は元記事）を展開すると、
$$p = a_3 x^3 + a_2 x^2 + a_1 x + a_0$$
これを Estrin のスキームでグループ化すると、
$$p = (a_3 x + a_2) x^2 + (a_1 x + a_0)$$
となり、$(a_3 x + a_2)$ と $(a_1 x + a_0)$ を独立に評価できるため、命令レベル並列（ILP）をCPUに活かせます。結果として依存チェーン長が短くなり、特にインテル系のCPUで大きな効果が出ました。

簡潔なコード比較（概念）：

```cpp
// 元: Horner
double asin_cg(double x) {
    constexpr double a0=1.5707288, a1=-0.2121144, a2=0.0742610, a3=-0.0187293;
    double ax = fabs(x);
    double p = ((a3*ax + a2)*ax + a1)*ax + a0; // Horner
    double xd = sqrt(1.0 - ax);
    double r = (M_PI/2.0) - xd * p;
    return copysign(r, x);
}
```

```cpp
// 改良: Estrin
double asin_cg_estrin(double x) {
    constexpr double a0=1.5707288, a1=-0.2121144, a2=0.0742610, a3=-0.0187293;
    double ax = fabs(x);
    double x2 = ax * ax;
    double p = (a3 * ax + a2) * x2 + (a1 * ax + a0); // Estrin
    double xd = sqrt(1.0 - ax);
    double r = (M_PI/2.0) - xd * p;
    return copysign(r, x);
}
```

ベンチマーク結果の要点：
- Intel（例: i7）で最大1.8xの高速化（コンパイラ依存あり）
- AMDではほとんど効果なし（影響小）
- Apple Mシリーズはclangでやや効果、GCCでは差が小さい
- 実アプリ（レイトレーサ）ではasin呼び出しが全体で小比率なので数%の改善に留まる

注意点：これは近似式であり誤差がある。グラフィックス用途では許容されることが多いが、用途により精度確認が必須。

## 実践ポイント
- 単純に式を書き換えてEstrinにするだけで効果が出る可能性が高い（特にIntel + 最適化コンパイラ）。
- 実装時は定数をconstにし、コンパイラ最適化フラグ（-O3 等）でテストする。
- マイクロベンチマークを取り、ターゲットCPU/コンパイラで必ず検証する（ARM/モバイルでは結果が異なる）。
- 精度が重要な用途では誤差評価を行い、必要なら標準関数に戻す。
- さらに速くしたければSIMD化やアーキテクチャ別最適化を検討。ただし設計次第では恩恵が限定的。

（短くまとめると）目の前にある数式の「書き方」を変えるだけで、コンパイラとCPUが仕事をしやすくなり、実運用でも意味のある改善が得られる――日本のレンダリング／ゲーム開発現場でも試す価値があります。
