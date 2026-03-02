---
layout: post
title: "Notes on Lagrange Interpolating Polynomials - ラグランジュ補間多項式のメモ"
date: 2026-03-02T16:43:10.388Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://eli.thegreenplace.net/2026/notes-on-lagrange-interpolating-polynomials/"
source_title: "Notes on Lagrange Interpolating Polynomials - Eli Bendersky's website"
source_id: 47219688
excerpt: "ラグランジュ補間の理論と数値的不安定性、実務で使える安定手法を具体例付きで解説"
---

# Notes on Lagrange Interpolating Polynomials - ラグランジュ補間多項式のメモ
ゼロからわかるラグランジュ補間 — データ点を「ぴったり」結ぶ多項式の仕組みと現場での使いどころ

## 要約
ラグランジュ補間は、与えられた異なる $n+1$ 個の点 $(x_i,y_i)$ をちょうど通る多項式を構成する手法で、基底多項式 $l_i(x)$ を使うと簡潔に表現できる。理論上は一意で存在するが、数値実装では注意が必要。

## この記事を読むべき理由
多項式補間はデータ近似・軌道生成・信号処理など日本のエンジニアが直面する場面で頻出する基礎技術。理論の理解と数値的注意点（不安定性や代替手法）を押さえれば、実務での誤差トラブルを防げます。

## 詳細解説
- 問題設定: 異なる $n+1$ 点
  $$ (x_0,y_0),\dots,(x_n,y_n) $$
  に対し、次数 $\le n$ の多項式
  $$ p(x)=a_0+a_1 x+\cdots+a_n x^n $$
  で $p(x_i)=y_i$ を満たす係数を求める。

- Vandermonde 行列による線形代数的存在証明:  
  系は
  $$
  \begin{bmatrix}
  1 & x_0 & x_0^2 & \dots & x_0^n\\
  1 & x_1 & x_1^2 & \dots & x_1^n\\
  \vdots & \vdots & \vdots & \ddots & \vdots\\
  1 & x_n & x_n^2 & \dots & x_n^n
  \end{bmatrix}
  \begin{bmatrix} a_0\\ \vdots\\ a_n \end{bmatrix}
  =
  \begin{bmatrix} y_0\\ \vdots\\ y_n \end{bmatrix}
  $$
  この行列の行列式は
  $$\det(V)=\prod_{0\le i<j\le n}(x_j-x_i)$$
  であり $x_i$ が互いに異なれば非零 → 一意解が存在。

- ラグランジュ基底と補間式:  
  各基底多項式を
  $$l_i(x)=\prod_{j\ne i}\frac{x-x_j}{x_i-x_j}$$
  と定義すると、$l_i(x_j)=\delta_{ij}$ により補間多項式は
  $$p(x)=\sum_{i=0}^n y_i\, l_i(x)$$
  と書ける。各 $l_i$ の次数は $\le n$、よって $p$ の次数も $\le n$。

- 一意性の理由:  
  もし別の補間多項式 $q(x)$ があれば $r(x)=p(x)-q(x)$ は次数 $\le n$ で $n+1$ 個の根を持つため、零多項式。したがって一意。

- 数値的注意点と現実的代替:  
  Vandermonde の逆行列を直接求めると数値的に不安定（条件数が大きくなる）ことが多い。実務では
  - バリセントリック（barycentric）ラグランジュ形式（高速で安定）、
  - ニュートンの差商（分割差）形式（追加点の拡張が容易）、
  - 区間分割してスプライン補間（高次数の副作用回避）
  を用いるのが一般的。また等間隔ノードで高次補間を行うと Runge 現象による振動が生じるため、Chebyshev ノードやスプライン化が推奨される。

## 実践ポイント
- 小さめの次数（例 3〜10）で十分ならバリセントリック形式を使う。ライブラリでは SciPy / NumPy や Eigen（C++）が便利。
- ノードが等間隔で多項式次数を上げすぎない。振動が出たらスプラインや Chebyshev ノードを検討。
- Vandermonde を使う実装では行列の条件数をチェックし、高条件数なら別手法へ切り替える。
- 追加入力点が動的に増える場面ではニュートンの分割差を使うと効率的。

以上を押さえれば、理論の理解と実装上の落とし穴の両方をカバーできます。
