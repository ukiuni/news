---
layout: post
title: "Show HN: Sowbot – open-hardware agricultural robot (ROS2, RTK GPS) - Sowbot：オープンハードウェア農業ロボ（ROS2、RTK GPS）"
date: 2026-02-23T19:18:16.780Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://sowbot.co.uk/"
source_title: "sowbot &#8211; The Open AgBot"
source_id: 47123894
excerpt: "ROS2とRTKで誰でも組める、低コスト小規模圃場向けオープン農業ロボ"
image: "http://nibleyleaves.co.uk/sowbot/wp-content/uploads/sites/10/2026/01/sowbot_sim.png"
---

# Show HN: Sowbot – open-hardware agricultural robot (ROS2, RTK GPS) - Sowbot：オープンハードウェア農業ロボ（ROS2、RTK GPS）
クローズドな農業機器から脱却する「誰でも組める」農業ロボット──Sowbotが示すオープンで再現可能なフィールド自動化

## 要約
Sowbotは、ROS2やRTK GNSSを核にしたオープンハードウェアの農業ロボット参照設計とソフトウェアスタックを公開し、研究者やスタートアップが「プロトタイプの溝」を越えて実運用に移せるようにするプロジェクトです。

## この記事を読むべき理由
日本は高齢化・人手不足が深刻で、狭小・段差の多い圃場に適応する低コストでカスタマイズ可能な自律ロボットが求められています。Sowbotは「部品・回路・ファームウェアを公開」することで、日本の現場事情に合わせた改変・実装を促します。

## 詳細解説
- ハードウェア要点  
  - Open Core（ロボットの「脳」）は10×10cmモジュール基準でAvaota A1 SBC（オクタコア、AIアクセラレータ内蔵）を2枚使用。Board AはROS2ナビ・EKFローカリゼーション・緊急停止等の制御、Board Bはカメラ処理とNN推論（例：YOLO）を担当。ESP32（Lizardファーム）と直結し、リアルタイムモータ制御と安全監視を実現。  
  - 通信はネイティブCANバス、双発のGNSS RTKでセンチメートル級の位置精度を確保。防水アルミ筐体とM12コネクタで屋外長期運用を想定。  
  - シャーシはモジュール式で、ODrive系のCANドライバ、800Wハブモータ（高トルク・高分解能エンコーダ）、12V 80Ahのナトリウムイオン電池×複数などを想定。Sowbot Mini/Picoといった1/4スケール開発プラットフォームも用意。  
- ソフトウェア要点  
  - Lizard（Zauberzeug製）：リアルタイムのロボットオーケストレーション。センサ入力→モータ制御→ナビを統合。  
  - RoSys：asyncioベースのPythonフレームワークで制御ループやUIを簡素化。Field Friendは農業向け実装例。  
  - DevKit ROS：ROS向けの開発キットで、既存のROSエコシステムと容易に接続・シミュレーション可能。  
- 開発哲学  
  - 全設計（回路図・PCB・ファーム）はオープンライセンスで公開。スタートアップは基礎開発時間を短縮、研究者はDockerで実験環境を再現可能。

## 実践ポイント
- まずは公式サイトとGitHubのRoadmap/リポジトリを確認して設計やライセンスを把握する。  
- DevKit ROSやLizardを使ってシミュレーション→小型プラットフォーム（Pico/Mini）で実験する。  
- 日本の狭い畦や段差に合わせたシャーシ改造やセンサ配置を検討し、ローカルな圃場でRTKの挙動を検証する。  
- 商用化を目指す場合は電池の低温充電特性や防水コネクタ仕様を早期確認する。  
- 貢献先：ソースにプルリク、Discord参加、ローカルコミュニティでの検証データ共有を検討する。

（参考）公式：https://sowbot.co.uk/
