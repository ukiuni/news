---
layout: post
title: "your agent can think. it can't remember. - エージェントは考えられるが、記憶できない"
date: 2026-03-27T15:41:49.668Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://dev.to/ghostbuild/your-agent-can-think-it-cant-remember-5e1o"
source_title: "your agent can think. it can&#39;t remember. - DEV Community"
source_id: 3403502
excerpt: "Ghostで即時Postgresを作り、時系列メモと安全サンドボックスでエージェント開発を高速化"
image: "https://media2.dev.to/dynamic/image/width=1200,height=627,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2F9tnk8cwhabxhqvffpsf5.png"
---

# your agent can think. it can't remember. - エージェントは考えられるが、記憶できない
エージェントに「居場所」を与えるGhost：瞬時に作れるPostgresでエージェント開発をシンプルに

## 要約
Ghostはエージェント向けに「瞬時で使える、捨てられるPostgresデータベース」を提供し、Memory Engine（時系列メモリ）、pg_textsearch（ハイブリッド検索）、TigerFS（Postgres上のファイルストア）、Ox（サンドボックス実行）と組み合わせて、エージェント基盤の分散化・接着コード問題を解消する。

## この記事を読むべき理由
エージェント系開発は「思考はできるが記憶や安全実行がバラバラ」で破綻しやすい。日本の企業・開発チームに馴染みのあるPostgres上で完結する設計は、運用負荷と統合コストを大幅に下げられるため実務価値が高い。

## 詳細解説
- エフェメラルPostgres：GhostはCLI/MCP経由で即時プロビジョニングできるPostgresインスタンスをブランチ感覚で扱える。数千のフォークや破棄が無料で可能。永久的なRDS的扱いではなく「作って試して捨てる」が前提。
- Git的ワークフロー：データベースをブランチ（fork）して実験→マージ／廃棄。マイグレーションやリスクの隔離が容易。
- Memory Engine：Postgres内で「時間を意識した永続メモリ」を提供。いつ何が真だったかを追跡でき、SQLで直接クエリ可能。ベクトル検索とBM25を組み合わせて検索も行う。
- pg_textsearch：BM25（キーワード精度）とpgvector（意味検索）を組み合わせたハイブリッド検索を標準搭載。外部のElasticsearch/Pineconeが不要。
- TigerFS：Postgresで動くファイルシステム。ファイルをトランザクション管理・メタデータ検索の対象にでき、複数エージェントの同時書き込みに耐える。
- Ox（サンドボックス）：エージェントがデータにアクセスしつつ安全にコードを実行できる隔離環境。実行はブランチ上で行われ、本流を汚さない。
- 統合メリット：すべてPostgresベースで同じトランザクションモデル・認可・SQLを共有するため、接着コードや同期の手間がほぼ不要。既存のPostgres知見が活かせる。

事例（要約）：
- コードレビューエージェント：レビュー用にDBをfork→Oxでテスト実行→結果をTigerFSに保管→Memory Engineで履歴参照。
- 研究エージェント：調査データをGhostに集約→分析はフォーク＋Oxで実行→時系列メモリで比較保存。
- マルチエージェント：複数エージェントが同一Ghost基盤を共有しつつ、個別のサンドボックスで衝突を避ける。
- データ探索：価格モデルのシミュレーションを複数フォークで高速に実行して比較。

## 日本市場との関連性
- Postgresは国内でも採用実績が多く、内製チームの学習コストが低い。  
- 金融や製造などコンプライアンスが厳しい領域でも、データ管理・監査がSQLで追跡しやすい点は評価されやすい。  
- マルチクラウド／オンプレ混在の現場で「サービスごとの接着コード」を減らせば運用コストと障害リスクが下がる。

## 実践ポイント
- まずはローカルで試す：CLIから即起動できる。
```bash
curl -fsSL https://install.ghost.build | sh
```
- Memory Engine と pg_textsearch を組み合わせ、時系列メモ＋ハイブリッド検索を試す。  
- 危険な変更は必ずGhostのフォークで実行し、Oxサンドボックスでテストする。  
- チーム導入時は「DBをブランチ化する運用フロー」を標準プロセスに組み込む。

参考：Ghostは「Postgresネイティブ」のツール群として設計されており、既存のSQLスキルで即活用できる点が最大の強み。
