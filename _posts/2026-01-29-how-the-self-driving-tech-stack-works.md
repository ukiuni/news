---
layout: post
title: "How the Self-Driving Tech Stack Works - 自動運転の技術スタックの仕組み"
date: 2026-01-29T18:06:02.833Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://cardog.app/blog/autonomous-driving-stack-technical-guide"
source_title: "How the Self-Driving Tech Stack Works"
source_id: 414400630
excerpt: "openpilotとAutowareで学ぶ、センサ〜制御までの実践自動運転解説"
image: "https://digitalassets.tesla.com/tesla-contents/image/upload/f_auto,q_auto/Robotaxi-Hero-Desktop.jpg"
---

# How the Self-Driving Tech Stack Works - 自動運転の技術スタックの仕組み
AIやセンサーだけじゃ語れない――生データからハンドル制御まで、openpilot と Autoware の実装を例に「実際に動く」自動運転スタックを読み解く

## 要約
センサー→ローカライゼーション→知覚→計画→制御の各層で何が起きているかを、open-source 実装のコード・アーキテクチャを元に具体的に解説する。

## この記事を読むべき理由
日本の開発者が「理屈だけでなく実装を想像できる」ようになるため。左側通行や車種ごとの CAN の違いなど日本固有の課題も絡め、現場で使える知識を短時間で得られます。

## 詳細解説
- ハードウェア層（センサー）
  - カメラ（20–60Hz, 〜200m）、LiDAR（10–20Hz, 3D点群）、レーダー（速度測定、全天候）、IMU（100–200Hz）、GNSS（1–10Hz）など。  
  - openpilot は基本的に「カメラ＋IMU」中心（vision-only）、Autoware は LiDAR＋カメラの冗長センサ融合が基本。

- 車両通信（CAN bus）と DBC
  - 車両状態は CAN メッセージで流れる。DBC ファイルでビット・スケール・単位を定義する（例：STEER_ANGLE は 16bit, scale 0.1）。
  - Python での簡易パーシング例：
```python
python
# cp.vl は opendbc 由来の解析結果を想定
for cp in can_packets:
    steer = cp.vl["STEERING_SENSORS"]["STEER_ANGLE"]   # deg
    speed = cp.vl["ENGINE_DATA"]["XMISSION_SPEED"] * 0.27778  # kph->m/s
```

- セーフティ（Panda 等）
  - CAN 書き込みはハードウェア側でモード・レート・トルクリミットを厳格に制御。誤操作を防ぐウォッチドッグやペダル優先ルールが必須。

- ローカライゼーション（EKF 等）
  - 複数センサーを統合する代表は拡張カルマンフィルタ（EKF）。状態ベクトル例：
$$
x = [x,y,z,v_x,v_y,v_z,roll,pitch,yaw,b_{g_x},b_{g_y},b_{g_z}]
$$
  - 高周波 IMU で予測、低周波 GPS/ビジュアルオドメトリで補正するのが基本。
```python
python
# 極めて簡易な予測・更新の擬似コード
kf.predict(imu_accel, imu_gyro, dt)
if gps_available:
    kf.update(gps_pose, R_gps)
```

- 知覚（Perception）
  - LiDAR 系：PointPillars（点群→柱→2D擬似画像→2D CNN）でリアルタイム検出。
  - カメラ系：openpilot の Supercombo は ViT や FPN + 時系列集約（GRU 等）でパス・車両検出・レーン・信号を同時出力。
```python
python
# 出力例（概念）
path, lanes, lead = model(images_seq, desire, traffic_convention)
```
  - Tesla の Occupancy Network のように、物体クラスではなく 3D 空間の「占有確率」を直接推定する手法が新潮流。

- 計画と制御（MPC 等）
  - 階層構造：ルート→行動選択→軌道生成→軌道最適化。モデル予測制御（MPC）が軌道最適化の主流。
$$
\min_{u_{0:N-1}} \sum_t \|x_t - x^{ref}_t\|^2 + \|u_t\|^2 \quad s.t.\ x_{t+1}=f(x_t,u_t)
$$

## 実践ポイント
- open-source を触る順序：まず opendbc（CAN）→ openpilot の car-interface（ローカルで CAN 解析）→ シミュレータで Supercombo を試す。  
- Autoware は LiDAR 前提。実機で試す前に Docker＋シミュレータ（LGSVL 等）で動作確認を。  
- ローカライズは「IMU 高周波＋低周波 GPS/VO」の組合せを自分で実装してみると理解が深まる（robot_localization パッケージがおすすめ）。  
- 日本向け注意点：左側通行フラグ、独自の ECU/DBC、車検や道路運送法の規制を必ず確認する。  
- 学習リソース：KITTI、nuScenes、Comma2k19 などのデータセットで PointPillars や Occupancy 学習を試す。

短時間で全体像を掴みつつ、実装に触れて理解を深めるのが近道です。
