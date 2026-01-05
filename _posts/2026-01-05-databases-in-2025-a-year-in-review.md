---
  layout: post
  title: "Databases in 2025: A Year in Review - 2025年のデータベース総括"
  date: 2026-01-05T09:08:40.886Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://www.cs.cmu.edu/~pavlo/blog/2026/01/2025-databases-retrospective.html"
  source_title: "Databases in 2025: A Year in Review // Blog // Andy Pavlo - Carnegie Mellon University"
  source_id: 46496103
  excerpt: "Postgresが基盤を制し、MCPでLLM連携が実運用の要に"
  image: "https://www.gravatar.com/avatar/75219a26e1b5940510ad17df0d8c42d3?s=400"
---

# Databases in 2025: A Year in Review - 2025年のデータベース総括
クリック不可避：2025年、データベース界を席巻した「Postgres大航海時代」とMCPの衝撃

## 要約
2025年はPostgreSQLを軸にした商用・分散化の動きが加速し、同時にLLMとデータベースをつなぐ「MCP（Model Context Protocol）」がほぼ全DBMSに浸透した年だった。

## この記事を読むべき理由
日本のプロダクト開発／SRE／データエンジニアは、クラウド提供のPostgres強化やMCPによるAI連携の実運用リスクを今すぐ理解する必要がある。採用するマネージドDBや運用ガードレール設計に直結する潮流です。

## 詳細解説
- PostgreSQLの勢力拡大  
  - 2025年11月リリースのPostgres v18は、非同期I/Oストレージサブシステム（OSページキャッシュ依存を減らす設計）やskip-scanサポート、クエリ最適化改善を搭載。目新しさでは既存DBに遅れを取る面もあるが、エコシステムと商用マネージドの集中投資が注目点。  
  - 商業面ではDatabricksがPostgres DBaaS「Neon」を買収（$1B）、SnowflakeがCrunchyDataを買収（$250M）、MicrosoftはHorizonDBを投入。主要クラウドが強化版Postgresを本気で出してきたことが大きな変化。

- 分散Postgres（スケールアウト）競争  
  - 従来のシングルプライマリ（主従レプリカ）アーキテクチャに対し、水平分割（シャーディング）でPostgresをスケールさせる取り組みが再燃。  
  - SupabaseがSugu（Vitess創設者）を迎えてMultigresを立ち上げ、PlanetScaleはPostgres向けのNekiを発表。これらはVitess的なシャーディングミドルウェアをPostgresへ持ち込み、書き込みスケールを狙う試み。

- MCP（Model Context Protocol）の普及と影響  
  - Anthropicが提唱したMCPはLLMと外部ツール/データの標準的なJSON-RPCゲートウェイ。2025年にOpenAIの対応が後押しし、各DBMSベンダーがMCPサーバを出した（ClickHouse、Snowflake、MongoDB、Redis、各種Postgres DBaaSなど）。  
  - MCPを通じてLLMが直接DB操作やクエリ発行をするケースが増加。利便性は高いが、アクセス権限・クエリ制限・異常検知といったガードレールの重要性が一気に高まった。

- 運用上の事件と学び  
  - 一部ベンダのライセンス変更やベンチマーク不備（例：書き込み未フラッシュで高スコア）など信頼性問題も散見。MongoDB と FerretDBの法的対立など、互換層を巡る摩擦も継続。

## 実践ポイント
- マネージドPostgres選定の視点  
  - 提供アーキテクチャ（シングルプライマリ vs シャード）を明確に把握する。書き込みスケールが要件なら分散Postgresプロジェクトの成熟度を評価する。  
  - 日本リージョンでの運用可否、SLA、サポート体制を優先確認。

- MCP／LLM連携時の必須ガードレール  
  - 最小権限の原則を徹底（エージェント用は読み取り専用など）。  
  - MCPゲートウェイにクエリ上限・タイムアウト・返却行数制限を組み込む（DBHubやいくつかのベンダーが実装例を公開）。  
  - プロキシ／コネクションプール経由で監査・異常検出を行う。Enterprise向け自動検知（例：IBM Guardium等）も検討。

- 開発・テストの迅速化にブランチDBを活用  
  - DBのブランチ機能（Neon等）は、データ構造変更やエージェント動作テストを安全に行える。CIパイプラインに組み込み、実運用へのリスク低減を図る。

- 法務・信頼性観点  
  - 中間ミドルウェアや互換レイヤー利用時はライセンス・特許リスクを確認（FerretDB事例）。ベンチマークやバックアップ設計の妥当性も第三者で検証する。

まとめ：2025年は「Postgresが世界のデータ基盤の中心に立つ」年となり、同時にLLM時代のDB接続標準であるMCPが現場に速やかに浸透した。日本の企業はマネージドDBやMCP導入を機敏に評価し、特にアクセス制御と自動化ガードレールの整備を最優先にすべきだ。
