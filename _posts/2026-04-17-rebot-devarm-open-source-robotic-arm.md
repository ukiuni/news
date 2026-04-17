---
layout: post
title: "ReBot-DevArm: open-source Robotic Arm - ReBot-DevArm：オープンソース ロボットアーム"
date: 2026-04-17T06:31:49.299Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/Seeed-Projects/reBot-DevArm"
source_title: "GitHub - Seeed-Projects/reBot-DevArm: Open Source Robotic Arm for All Developers · GitHub"
source_id: 47750600
excerpt: "設計図・SDK付きのデスクトップ6軸アームでEmbodied AIやROS連携を実機で学べる"
image: "https://opengraph.githubassets.com/116c983a4fd9d7c52a78449a4a0dfb07c8567c574a761a571df482a7574f64b9/Seeed-Projects/reBot-DevArm"
---

# ReBot-DevArm: open-source Robotic Arm - ReBot-DevArm：オープンソース ロボットアーム
デスクトップで学べる“本物の”オープンソース6軸アーム — reBotでEmbodied AIを始めよう

## 要約
SeeedのreBot-DevArmは、ハードからソフトまで完全オープンソースで公開されたデスクトップ向け6軸ロボットアームプロジェクト。設計図・BOM・SDK・ROS連携・シミュレーション対応まで揃い、学習・プロトタイプ・研究に使える。

## この記事を読むべき理由
日本のスタートアップ／教育機関／メイカーズにとって、実機でEmbodied AIやロボティクス制度を学べる低障壁なプラットフォーム。ROSやIsaac Sim、Hugging Face LeRobotなど主流ツールと連携予定で、国内開発や授業教材に適する。

## 詳細解説
- バリエーション：reBot Arm B601-DM（Damiao）とB601-RS（Robstride）の2型。見た目は同一で内部仕様や対応パーツが異なる。  
- 完全オープン：板金・3Dプリントのソース、STEPファイル、ボルト一本単位までのBOM、ソフト（Python SDK、ROS1/2対応ドライバ、Isaac Sim対応データ、LeRobot対応）を公開。  
- 主要スペック：6 DOF + 1グリッパ、連続推奨荷重 ≲1.5 kg（有効作業域の70%内）、最大到達約650 mm、重量 約4.5 kg、繰返し精度 <0.2 mm、供給電圧 DC24V。  
- ソフトエコシステム：既にPython SDKや一部コアドライバが完成。ROS2（Humble）やMoveIt2最適化、Isaac Sim USDインポート、Pinocchioによる順逆運動学／重力補償、LeRobot統合は順次対応中（ロードマップあり）。  
- ラーニング＆コミュニティ：組立動画・チュートリアル群、センサー・モータのサンプル、教育用コース展開予定。Seeedがキット（部品単位〜フルキット、完成品）を販売。  
- ライセンス／利用制限：Creative Commons BY‑NC‑SA 4.0。個人学習・研究は自由、商用展開は原則支援（一定の商用行為は申請やルールあり）、単なるリバンドや低改変での独自ブランド化は制限。

## 実践ポイント
- まずはフルキットかボディ＋モーターキットを購入して組み立てドキュメントを追う。  
- Python SDKで基本動作→ROS2/MoveIt2（対応済みor順次公開）で軌道制御へ移行。  
- Isaac SimのUSDモデルが揃ったら、実機前にシミュレーションで検証すると安全かつ高速。  
- 教育／ワークショップ用途では、BOMと設計図を利用してカスタム改造や教材化が容易。  
- 商用利用を検討する場合はライセンス条項を確認し、Seeedに相談（商用支援体制あり）。

参考：GitHubリポジトリ（Seeed-Projects/reBot-DevArm）および公式Wikiで設計図・BOM・SDK・チュートリアルを確認可能。
