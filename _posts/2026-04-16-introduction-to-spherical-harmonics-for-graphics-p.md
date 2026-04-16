---
layout: post
title: "Introduction to Spherical Harmonics for Graphics Programmers - グラフィックスプログラマのための球面調和関数入門"
date: 2026-04-16T02:07:16.218Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://gpfault.net/posts/sph.html"
source_title: "Introduction to Spherical Harmonics for Graphics Programmers"
source_id: 47749548
excerpt: "9つの係数でモバイルやVR向けに高品質な拡散照明を軽量化する球面調和関数入門"
---

# Introduction to Spherical Harmonics for Graphics Programmers - グラフィックスプログラマのための球面調和関数入門
ゲームやリアルタイムレンダリングの「照明表現」を劇的に簡潔にする、9つの係数で雰囲気を再現する方法

## 要約
球面調和関数（Spherical Harmonics, SH）は、球面上の任意の連続関数を無限個の直交基底で表現する方法で、低周波の環境光や拡散照明の近似に特に有効です。少ない係数で複雑な方向依存情報を扱えるため、リアルタイム描画やテクスチャベイクで重宝されます。

## この記事を読むべき理由
日本のゲーム／リアルタイムCG開発では、モバイルやVRなど計算・メモリ制約が厳しい環境で質の高い照明を実現する必要があります。SHは「軽量に現実っぽい拡散光を得る」定番テクニックで、エンジニア／テク愛好者が実装と原理を押さえておく価値があります。

## 詳細解説
- 基本概念  
  方向は単位ベクトルで表され、その端点は単位球面上の点です。方向依存の量（例：点で入射する放射輝度 $L_i(p,\vec\omega)$）は球面上の関数と考えられます。SHはその関数空間の直交正規基底で、任意の連続関数 $f(\omega)$ を
  $$f(\omega)=\sum_{l=0}^{\infty}\sum_{m=-l}^{l} c_{lm}Y_l^m(\omega)$$
  の形で表します。係数は内積で求められます：
  $$c_{lm}=\langle f, Y_l^m\rangle=\int f(\omega)Y_l^m(\omega)\,d\omega.$$
  内積は球面上の積分で定義され、基底は
  $$\langle Y_i,Y_j\rangle=\delta_{ij}$$
  を満たします（直交正規性）。
- 次と位相（degree / order）  
  各バンドは次数 $\ell\in\{0,1,2,\dots\}$ を持ち、バンド $\ell$ は $2\ell+1$ 個の関数（$m=-\ell\ldots\ell$）を含みます。低い $\ell$ は低周波（広域の変化）、高い $\ell$ は高周波（細かい変化）を表現します。
- 切り捨てと実用性  
  無限和は計算上不可能なので切り捨てます。実務では $\ell\le2$（合計9係数）が拡散環境照明の多くに十分使えますが、高周波（鏡面反射など）には不向きです。
- 係数計算（実装面）  
  内積は環境マップやキューブマップをサンプリングしてモンテカルロ積分で近似します。数式どおりに実装するか、既存の基底定義（Peter-Pike Sloan 等）を利用して係数を求めます。基底関数は多くの公開実装にあるためコピペして使われますが、直交性を数値で検証するのが安全です（Monte-Carlo で $\langle Y_i,Y_j\rangle$ を確認）。
- 用途例  
  - 拡散irradianceの事前計算（PRT/環境光の簡易近似）  
  - メッシュ厚さの方向依存近似をテクスチャにベイクしてサブサーフェスに利用  
  - ランタイムでの軽量な環境照明合成（RGBそれぞれに係数を持つ）

- 実際の基底（参考）  
  実装例として次数 $\ell\le2$ の基底を評価する関数（JavaScript）：
  ```javascript
  // javascript
  const RECIP_PI = 1/Math.PI;
  const C = [
    Math.sqrt(RECIP_PI)*0.5,
    Math.sqrt(3*RECIP_PI)*0.5,
    Math.sqrt(15*RECIP_PI)*0.5,
    Math.sqrt(5*RECIP_PI)*0.25,
    Math.sqrt(15*RECIP_PI)*0.25
  ];
  function y00(x,y,z){ return C[0]; }
  function y_11(x,y,z){ return C[1]*y; }
  function y01(x,y,z){ return C[1]*z; }
  function y11(x,y,z){ return C[1]*x; }
  function y_22(x,y,z){ return C[2]*y*x; }
  function y_12(x,y,z){ return C[2]*y*z; }
  function y02(x,y,z){ return C[3]*(3*z*z-1); }
  function y12(x,y,z){ return C[2]*x*z; }
  function y22(x,y,z){ return C[4]*(x*x - y*y); }
  function evalSHBasis(d){
    const [x,y,z]=d;
    return new Float32Array([
      y00(x,y,z),
      y_11(x,y,z), y01(x,y,z), y11(x,y,z),
      y_22(x,y,z), y_12(x,y,z), y02(x,y,z), y12(x,y,z), y22(x,y,z)
    ]);
  }
  ```

## 実践ポイント
- 拡散環境光ならまずは $\ell\le2$（9係数／色）を試す：画質とコストの良いトレードオフ。  
- 環境マップ→係数計算はサンプリング（Monte-Carlo）で行い、サンプル数を増やして収束を確認する。  
- 基底定義は信頼できるソースから流用し、直交性（$\langle Y_i,Y_j\rangle$ がほぼ $\delta_{ij}$）を数値検証する習慣をつける。  
- 高周波が重要なシーン（鏡面・輝点）には別手法（スペキュラ用のラフネス別アプローチやBRDF分解）を併用する。  
- 実装では各係数をRGBで保持してシェーダーで線形結合すると高速に評価できる。

短くまとめると、SHは「球面上の低周波情報を少数の係数で表現する強力なツール」であり、特にモバイルやリアルタイム環境での拡散照明表現に即効性のある実装パターンです。興味があれば、係数の計算（サンプリング）とシェーダー側での合成を試してみてください。
