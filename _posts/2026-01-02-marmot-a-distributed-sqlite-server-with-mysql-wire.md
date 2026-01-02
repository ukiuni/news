---
  layout: post
  title: "Marmot – A distributed SQLite server with MySQL wire compatible interface - Marmot — MySQLワイヤ互換の分散SQLiteサーバー"
  date: 2026-01-02T03:13:12.897Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://github.com/maxpert/marmot"
  source_title: "GitHub - maxpert/marmot: A distributed SQLite server with MySQL wire compatible interface"
  source_id: 46460676
  excerpt: "MySQL互換で使えるリーダーレス分散SQLite、Marmotで即時CDCと全ノード書き込みを実現"
  image: "https://opengraph.githubassets.com/535a038d956d0cad9998593e4a20805a00055764fb321f64947e942987b71b9d/maxpert/marmot"
---

# Marmot – A distributed SQLite server with MySQL wire compatible interface - Marmot — MySQLワイヤ互換の分散SQLiteサーバー

魅力的な日本語タイトル: ローカル感覚で分散化するSQLite — MySQLクライアントで使える「Marmot」がインフラを変える理由

## 要約
Marmotは、MySQLのクライアント互換インターフェースを持つ「リーダーレス」な分散SQLiteサーバーで、Gossipベースのクラスタ、2PCによる分散トランザクション、CDC（行単位）レプリケーション、Debezium互換のイベント公開を備えます。どのノードでも書き込み可能で、DDLもクラスタ全体で安全に反映できます。

## この記事を読むべき理由
- 日本のスタートアップや社内システムで「軽量なSQLiteの運用性」と「分散可用性」を同時に求めるケースが増えています。Marmotはそのギャップを埋め、既存のMySQLクライアントやKafkaなどのエコシステムと自然に繋がります。オンプレ／エッジ／クラウド混在環境での採用可能性が高く、日本企業のモダナイズ案件で検討に値します。

## 詳細解説
- アーキテクチャ
  - Leaderless（リーダー不要）設計：Raftのようなリーダー選出を行わず、SWIMスタイルのGossipでクラスタメンバーシップと障害検知を実装。任意ノードでの書き込みを許可するため、単一障害点がない。
  - トランザクション調整：Percolator風の「書き込みインテント」と2フェーズコミット（2PC）で分散コミットを実現。整合性レベルは ONE / QUORUM / ALL といった設定で調整可能。
  - 衝突解決：Last-Write-Wins（LWW）をHLC（Hybrid Logical Clock）タイムスタンプで運用し、競合解消を担保。

- レプリケーションとCDC
  - SQL文の再生ではなく、行レベルのCDCメッセージを用いるため、MySQL→SQLite間の方言差異が問題にならない。行データはバイナリ形式でシリアライズされ、一貫した適用が可能。
  - Debezium互換のイベント形式でKafka/NATS等へ出力でき、既存のデータパイプラインやリアルタイム分析基盤と簡単に接続できる。

- DDL（スキーマ変更）
  - クラスタ全体のロック（デフォルト30秒）で同一DBの同時DDLを防ぎ、DDL文は自動で冪等化（IF NOT EXISTS 等の書き換え）される。ALTER TABLEは再実行で壊れやすいので注意喚起あり。
  - スキーマバージョン管理をgossipで共有し、トランザクション適用の妥当性確認に利用。

- 互換性と制限
  - MySQLプロトコル互換のため、MySQLクライアント（mysql CLI, DBeaver, MySQL Workbench等）でそのまま接続可能。
  - ユーザ管理（CREATE USER等）はノードローカル。分散環境では認証をアプリ側かプロキシで処理することが推奨。
  - LOCK TABLESやXAトランザクションなどはパースされるが、Marmotの分散モデルと完全互換ではないため運用上の注意が必要。

## 実践ポイント
- まず試す：シングルノードで ./marmot-v2 を起動し、mysql CLIで接続してみる（ポート3306互換）。複数ノードの挙動は付属スクリプト（scripts/test-ddl-replication.sh, examples/start-seed.sh 等）で検証可能。
- DDL運用ルール：同一データベースに対するDDLは原則「一接続で順次実行」。ALTER TABLEは慎重に、事前にバックアップと検証を。
- CDC活用：KafkaなどへDebezium互換イベントを流すことで、検索インデックス更新や分析基盤と即時連携できる。フィルタやバッチ設定で負荷を調整。
- 名前空間は明示：db.table のように完全修飾名を使うと、複数DB環境での誤操作を減らせる。
- 運用準備：認証は外部プロキシやアプリレイヤで一元化、監視（クラスタメンバー・ラグ・CDC遅延）と定期バックアップを整備する。

例：DDLロック設定の一部（config.toml）
```toml
[ddl]
lock_lease_seconds = 30
enable_idempotent = true
```

