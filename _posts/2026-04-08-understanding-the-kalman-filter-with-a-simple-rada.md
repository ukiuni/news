---
layout: post
title: "[Understanding the Kalman filter with a simple radar example] - [簡単なレーダー例で理解するカルマンフィルタ]"
date: 2026-04-08T19:20:19.264Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://kalmanfilter.net"
source_title: "Kalman Filter Explained Through Examples"
source_id: 47693153
excerpt: "レーダー例で学ぶカルマンフィルタ：ノイズ下で位置・速度を高精度に予測・更新する直感的入門"
image: "/img/profile.jpg?v=1"
---

# [Understanding the Kalman filter with a simple radar example] - [簡単なレーダー例で理解するカルマンフィルタ]
ノイズだらけの世界で“正確に予測する”技術：レーダー例でわかるカルマンフィルタ入門

## 要約
カルマンフィルタは、ノイズのある観測と不完全な動的モデルから「状態」とその不確かさを同時に推定・予測する線形最適フィルタです。レーダーで飛行機の距離と速度を追跡する直感的な例で、予測（Prediction）と更新（Update）の仕組みをやさしく解説します。

## この記事を読むべき理由
- センサー融合、ロボット、ドローン、自動運転、気象や金融の時系列解析など日本でも応用が広い基礎技術だから。  
- 数式と数値例で直感的に理解でき、実装やチューニングにすぐ活かせる知識が得られるから。

## 詳細解説
- 目的：ノイズを含む観測 $z$ とシステムの動き（動的モデル）から状態 $x$ を推定し、次時刻を予測する。推定と同時に「どれくらい信頼できるか」を共分散 $P$ で示す。
- レーダー例の状態ベクトル（1次元直線運動）：
  $$\boldsymbol{x}=\begin{bmatrix}r\\v\end{bmatrix}$$
  初期観測で $r_{t_0}=10000\ \mathrm{m},\ v_{t_0}=200\ \mathrm{m/s}$ とする。
- 動的モデル（定速モデル, サンプリング間隔 $\Delta t$）：
  $$\boldsymbol{F}=\begin{bmatrix}1 & \Delta t\\0 & 1\end{bmatrix},\qquad \hat{\boldsymbol{x}}_{1|0}=\boldsymbol{F}\,\hat{\boldsymbol{x}}_{0|0}$$
  例：$\Delta t=5\ \mathrm{s}$ のとき予測位置は $10000+200\times5=11000\ \mathrm{m}$。
- 不確かさの扱い：観測ノイズは共分散行列 $\boldsymbol{R}$、モデル誤差はプロセスノイズ共分散 $\boldsymbol{Q}$、状態推定の不確かさは $\boldsymbol{P}$ で表す。予測の共分散は
  $$\boldsymbol{P}_{n+1|n}=\boldsymbol{F}\,\boldsymbol{P}_{n|n}\,\boldsymbol{F}^\top+\boldsymbol{Q}.$$
- 更新ステップ（観測が来たとき）：
  $$\boldsymbol{K}=\boldsymbol{P}_{n+1|n}\boldsymbol{H}^\top\big(\boldsymbol{H}\,\boldsymbol{P}_{n+1|n}\,\boldsymbol{H}^\top+\boldsymbol{R}\big)^{-1}$$
  $$\hat{\boldsymbol{x}}_{n+1|n+1}=\hat{\boldsymbol{x}}_{n+1|n}+\boldsymbol{K}\big(\boldsymbol{z}_{n+1}-\boldsymbol{H}\hat{\boldsymbol{x}}_{n+1|n}\big)$$
  $$\boldsymbol{P}_{n+1|n+1}=(\boldsymbol{I}-\boldsymbol{K}\boldsymbol{H})\boldsymbol{P}_{n+1|n}$$
  ここで $\boldsymbol{H}$ は観測モデル（例では単に $r,v$ を測るので単位行列）。
- 直感：$\boldsymbol{K}$（カルマンゲイン）は「予測をどれだけ観測に合わせるか」を決める重み。観測が信頼できる（$\boldsymbol{R}$ が小さい）ほど観測に強く引き寄せられ、モデル誤差が大きければ（$\boldsymbol{Q}$ が大きい）観測を重視する。
- よくある失敗：モデルが間違っている（加速度を無視する等）・$\boldsymbol{Q},\boldsymbol{R}$ を過小評価すると過度に自信を持ち誤差が拡大する。非線形系は拡張カルマン（EKF）やUnscented KFが必要。

## 実践ポイント
- まずは定速モデル（F）で実装して可視化：状態（位置・速度）と残差（観測−予測）をプロットする。  
- 初期共分散 $\boldsymbol{P}$、観測ノイズ $\boldsymbol{R}$、プロセスノイズ $\boldsymbol{Q}$ を現実的に設定し、ログでチューニングする（残差の平均が0、分散が想定通りか確認）。  
- センサ融合を考える：GNSS＋IMUやレーダー＋カメラでは観測行列 $\boldsymbol{H}$ を設計して統合する。  
- 非線形ならEKF/UKFへ拡張、実装は既存ライブラリ（PythonのFilterPy等）を参考に。  
- 日本の応用例：ドローンの姿勢推定、車載センサー融合、ロボットの自己位置推定、局所天気データの滑らか化など。

短時間で動作確認するなら、観測ノイズを人工的に加えた数値シミュレーションで上記式を実装して挙動を観察すると理解が早まります。
