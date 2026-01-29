---
layout: post
title: "Narwhal: an extensible pub/sub messaging server for edge applications - Narwhal：エッジ向け拡張可能なPub/Subメッセージングサーバー"
date: 2026-01-29T19:14:02.778Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/narwhal-io/narwhal"
source_title: "GitHub - narwhal-io/narwhal: An extensible pub/sub messaging server for edge applications"
source_id: 1194268796
excerpt: "Modulatorで認可や検証を委譲する軽量Rust製Pub/Sub、エッジ向け"
image: "https://opengraph.githubassets.com/73c5eaa880331430d5b803f18cc8c4f07a2e571d666edd875d21919c3c29301d/narwhal-io/narwhal"
---

# Narwhal: an extensible pub/sub messaging server for edge applications - Narwhal：エッジ向け拡張可能なPub/Subメッセージングサーバー
軽量×拡張性で「チャット機能やIoT同期を手早く実装」——Narwhalでリアルタイムをシンプルに作る

## 要約
NarwhalはRust製の非同期Pub/Subサーバーで、メッセージルーティングは軽量に保ちつつ、認証・認可・検証などのアプリ固有ロジックを外部サービス（Modulator）に委譲することで柔軟な拡張を実現します。エッジやモバイル、IoT用途を想定した設計です。

## この記事を読むべき理由
日本でもモバイルアプリ、ゲーム、産業IoT、チャット機能など低遅延で柔軟なメッセージングが求められています。Narwhalは「軽さ」と「カスタム性」を両立するアプローチで、既存のMQTTやXMPPでは難しい細かな認可やメッセージ検証をアプリ側で簡単に実装できます。

## 詳細解説
- コアアイデア  
  Narwhalはメッセージの受け渡しを高速に行う「サーバー本体」と、認証やバリデーションなどを担当する「Modulator」を分離。サーバーは1つのModulatorに接続し、Modulatorが“頭脳”として振る舞います。これによりサーバーは軽量で運用しやすく、アプリごとのポリシーはModulatorで自由に実装できます。

- Modulatorの役割（代表例）  
  - カスタム認証（JWT/OAuth/独自スキーム）  
  - 細かなアクセス制御（チャネル毎の権限ルール）  
  - メッセージスキーマ検証やサイズ制限  
  - メッセージ変換（暗号化・圧縮・付加情報）  
  - 外部サービス連携（DB／APIブリッジ）

- 接続モデル  
  - C2S（Client-to-Server）: クライアント→Narwhal  
  - S2M（Server-to-Modulator）/M2S（Modulator-to-Server）: Narwhal↔Modulator（操作委譲とプライベート送信）

- 実装と性能  
  Rustの非同期実装で高スループットを目指し、開発用は自動証明書生成（TLS）などセキュアなデフォルトを提供。ベンチマークツールでスループットやp99レイテンシを計測できます。

- 開発体験  
  リポジトリにModulatorのサンプル（簡易認証、JSON/CVS検証、プライベート送信など）があり、TOMLで設定、cargoでビルド／テストが可能。現状はv0.4.0のアルファ段階のため、APIの変更や本番運用前の評価が推奨されています。

- 将来ロードマップ（予定）  
  メッセージ永続化、観測性の強化（メトリクス／トレース）、WebSocket等の追加トランスポート、フェデレーション（複数サーバー間でのメッセージ共有）など。

- すぐ触れるコマンド例
```bash
# リポジトリ取得とビルド
git clone https://github.com/narwhal-io/narwhal.git
cd narwhal
cargo build --release

# サーバ起動（開発用）
cargo run --bin narwhal

# 接続確認（OpenSSLでTLS接続テスト）
openssl s_client -connect 127.0.0.1:22622 -ign_eof
```

## 実践ポイント
- まずはサンプルModulatorを動かして、認証／検証フローを理解する。  
- チャットやプレゼンス、ゲームの同期など、状態管理が分離できるユースケースにマッチ。  
- 既存の認証基盤（OAuth/JWT、社内ID）をModulatorに組み込めば柔軟に統合可能。  
- ベンチマークツールで自分の想定負荷を計測し、アルファ段階のAPI変化に備える。  
- 日本のネットワーク条件（モバイル回線、キャリアNAT）やデータ所在地要件を考慮してエッジ配置やフェデレーションの検討を。  
- 本番利用前はメッセージ永続化や監視機能の要件を満たす設計を計画する（現状はロードマップ参照）。

興味が湧いたらリポジトリのexamplesを触って、Modulator側で小さな認証／検証ロジックを作ってみるのがおすすめです。
