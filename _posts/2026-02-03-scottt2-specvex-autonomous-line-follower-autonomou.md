---
layout: post
title: "ScottT2-spec/vex-autonomous-line-follower: Autonomous VEX robot capable of line tracking, obstacle detection, and manual override using embedded sensor logic. - 自律型VEXロボット：ライン追跡・障害物検知・手動オーバーライドを組み込んだプロジェクト"
date: 2026-02-03T23:02:39.023Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/ScottT2-spec/vex-autonomous-line-follower"
source_title: "GitHub - ScottT2-spec/vex-autonomous-line-follower: Autonomous VEX robot capable of line tracking, obstacle detection, and manual override using embedded sensor logic."
source_id: 411165357
excerpt: "VEX V5で作る、ライン追跡と障害物回避ができる教材ロボット"
image: "https://opengraph.githubassets.com/4a2e1f691c7802a760c2b806882067075cea27d15b7286a2eacb9dbc7a67e562/ScottT2-spec/vex-autonomous-line-follower"
---

# ScottT2-spec/vex-autonomous-line-follower: Autonomous VEX robot capable of line tracking, obstacle detection, and manual override using embedded sensor logic. - 自律型VEXロボット：ライン追跡・障害物検知・手動オーバーライドを組み込んだプロジェクト

魅力的なタイトル: 教室で使える！VEXで作る「線をたどって避ける」自律ロボの作り方と実践テクニック

## 要約
VEX V5ハードとC++（VEXcode V5）で実装された自律ロボットリポジトリ。ラインセンサーで黒線を追跡し、距離センサーで障害物を検知すると停止してバック。アーム・クローは手動制御に切替可能で、画面にセンサ情報を表示します（MITライセンス）。

## この記事を読むべき理由
教育現場やものづくりコミュニティで「初めての自律制御」を教える・学ぶ際、最小限のハードで実用的な挙動（ラインフォロー + 障害物回避 + 手動オーバーライド）を再現できる設計と実装例は即戦力になります。日本のロボコンや学校教材にも応用しやすい内容です。

## 詳細解説
- ハードウェア構成  
  - VEX V5 Brain & Controller  
  - 4× V5 Smart Motors（左右駆動、アーム、クロー）  
  - V5 距離センサー（レーザー）  
  - V5 ライントラッカー（車体下面）  
  - V5 Clawbot メタルキット

- 接続（リポジトリのREADMEに記載）  
  - Left motor: Port 1  
  - Right motor: Port 10  
  - Arm: Port 8  
  - Claw: Port 3  
  - Distance sensor: Port 5  
  - Line tracker: 3‑Wire Port A

- ソフトウェア概念（C++ / VEXcode V5）  
  - ライントラッカーは床をスキャンし、黒（ライン）を検出すると直進、白地が続くとライン復帰のために旋回するというシンプルな閾値ベースのロジック。  
  - 距離センサーは前方の障害物を常時監視し、閾値未満であれば停止→後退を行う安全処理。  
  - 手動制御への切替はソース内で autonomousMode と usercontrol を差し替える手順で可能。  
  - ロボット画面にセンサ値を表示してデバッグや調整がしやすい実装。

- 実装上のポイント  
  - ライン検出は環境光や床の反射で閾値が変わるため、実機でのキャリブレーションが必要。  
  - 単純な閾値では左右振動しやすいので、PIDや差分制御で滑らかにすると精度が上がる。  
  - 障害物回避は単純な停止＆バックのみだが、回避パターン（左右回避、経路再探索）を足せば自律性が向上する。

## 実践ポイント
- まず揃えるもの：VEX V5本体、ライン用マット（白黒コントラストがはっきりしたもの）、PCとVEXcode V5。  
- 初期セットアップ手順：モータ／センサを指定ポートに接続→READMEのポート設定を確認→VEXcodeで main.cpp をビルドしてアップロード。  
- 調整のコツ：ライン閾値と距離センサー閾値を現場で調整。画面表示でセンサ値を確認しながらチューニングする。  
- 次の一手（発展案）：
  - PIDでライン追従を安定化。  
  - 障害物検知後に左右どちらかに回避してライン復帰するアルゴリズム追加。  
  - データをログして学習ベースの制御に拡張。

元リポジトリはMITライセンスで公開されているため、教育用途や改変・配布がしやすく、日本の学校やメイカースペースでも取り入れやすい教材候補です。
