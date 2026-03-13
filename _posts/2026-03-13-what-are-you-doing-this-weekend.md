---
layout: post
title: "What are you doing this weekend? - 今週末は何をする予定ですか？"
date: 2026-03-13T12:30:09.668Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://lobste.rs/s/jwdr0q"
source_title: "What are you doing this weekend? | Lobsters"
source_id: 1147288036
excerpt: "今週末はZigでSO_SPLICE活用のゼロコピープロキシとSimplenote代替を作る挑戦記"
image: "https://lobste.rs/story_image/jwdr0q.png"
---

# What are you doing this weekend? - 今週末は何をする予定ですか？
週末の個人開発ネタ2本：Zigでゼロコピープロキシに挑む話と、Simplenote代替を作る防衛的プロジェクト

## 要約
Lobstersのスレッドから、FreeBSD/OpenBSDのSO_SPLICEをZigのIo実装に統合する技術的挑戦と、Simplenoteの将来を懸念して個人用メモサービスを作る話が挙がっています。どちらも「日常的な問題を自分で解く」実践的な取り組みです。

## この記事を読むべき理由
日本でも高性能プロキシや自前のクラウドサービス運用は重要です。低レイテンシ／低CPU負荷を狙うゼロコピー設計や、サービス依存を減らす自前ホスティングは、企業・個人問わず実務的価値があります。

## 詳細解説
- SO_SPLICEとゼロコピー: BSD系が提供するsplice系の仕組みは、カーネル内でソケットやファイル間のデータ転送をユーザ空間コピーなしに行えます。プロキシやリバースプロキシでのCPU負荷削減とスループット向上に有効です。  
- ZigのIo設計: ZigにはIo.Threadedのようなスレッドベース実装と、イベントループ（kqueue）ベースのIo.Kqueue（まだネットワーク対応が発展途上）の2方向性があります。コメントの作者は認証処理をスレッド化し、accept／splice／closeをkqueue手動ループで扱う構成にしていて、最終的に単一イベントループでゼロコピーを保ちたいが設計が難しいと述べています。  
- kqueueの課題: kqueueは高性能だが、spliceのようなカーネル機能と非同期イベントループをどう綺麗に組み合わせるか（コールバック設計、状態遷移、エラーハンドリング）が設計上の難所です。  
- Simplenote代替の動機: Automatticの将来に不安を感じ、データ所有権と長期保守性を保つために自分だけのSimplenote類似サービスを「防衛的」に作るという話。これはバックアップ・エクスポート・同期プロトコル（例えば簡易APIやwebdav等）の設計が鍵です。

## 実践ポイント
- プロキシ最適化: まず小さなプロトタイプでsplice系APIを試し、ゼロコピーが本当にボトルネックを改善するか計測する（ベンチマークを必ず取る）。  
- 設計方針: 単一イベントループを目指すなら、kqueueエントリごとに「splice状態」を持つステートマシン設計を検討する。IOライブラリ側にネットワークspliceの抽象を追加できるか設計レビューする。  
- 自前メモサービス: データエクスポート・暗号化・バックアップ・モバイル同期の優先順位を決め、小型MVP（Markdown対応、REST API、SQLiteバックエンド等）から始める。既存OSS（例：JoplinやStandard Notes）を参考にして短期で運用可能な形にする。  
- 日本向け注意点: 国内クラウド／ISPの環境差や法律（個人情報保護）を考慮し、ホスティング先とバックアップ戦略を明確にしておく。

短時間で試せるタスク例：kqueueとspliceの最小実装で1方向のパイプを作り、CPU使用率とスループットを測る。メモサービスはまずローカルで同期可能なノートAPIを作ってみる。
