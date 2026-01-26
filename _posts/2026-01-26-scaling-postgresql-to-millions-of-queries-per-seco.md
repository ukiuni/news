---
layout: post
title: "Scaling PostgreSQL to Millions of Queries Per Second: Lessons from OpenAI - PostgreSQLをミリオンQPSへ拡張する：OpenAIの教訓"
date: 2026-01-26T09:54:02.570Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.rajkumarsamra.me/blog/scaling-postgresql-to-millions-of-queries-per-second"
source_title: "Scaling PostgreSQL to Millions of Queries Per Second: Lessons from OpenAI | Rajkumar"
source_id: 417251757
excerpt: "OpenAIが単一プライマリ＋50レプリカで数百万QPSを達成した実践的手法と即効改善策を公開"
image: "https://rajkumarsamra.me/favicon_io/android-chrome-512x512.png"
---

# Scaling PostgreSQL to Millions of Queries Per Second: Lessons from OpenAI - PostgreSQLをミリオンQPSへ拡張する：OpenAIの教訓
クリックせずにはいられない！「単一プライマリPostgreSQL」でChatGPT級トラフィックをさばいた現場の最前線

## 要約
OpenAIは単一プライマリ＋約50台のリードレプリカで数百万QPSを実現した。鍵は「書き込みを減らし、読みを最適化する」一貫した工夫と運用だ。

## この記事を読むべき理由
日本のプロダクトでもトラフィック急増やコスト制約に直面する場面が増えている。OpenAIの実践は「すぐに試せる対策」と「運用上の落とし穴」を具体的に示してくれる。

## 詳細解説
- 問題の本質：書き込み（writes）がボトルネック  
  PostgreSQLのMVCCは整合性に強いが、更新のたびに行がコピーされるため書き込みが多いと「書き込み増幅」と「不要な死行（dead tuple）スキャン」が発生する。

- 戦略：書きを最小化、読みを最大化  
  - 書きの多い・分割可能なワークロードはシャーディングされたストア（例：Cosmos DB相当）へ移行。新規テーブルはまずシャード前提で検討。  
  - 読みは可能な限りレプリカへオフロード。プライマリは書き込みトランザクションに専念させる。

- クエリ最適化の重要性  
  - 複雑な多テーブルJOINやORM生成SQLがパフォーマンス事故の典型。クエリプランを確認し、必要ならJOINを分解してアプリ側で処理。  
  - 長時間のidle transactionはautovacuum阻害になるため、タイムアウト（例：idle_in_transaction_session_timeout）を設定。

- 接続プーリング（PgBouncer）  
  PostgreSQLインスタンスあたりの接続限界（例：Azureの5,000）に達するリスクを防ぐため、PgBouncerでステートメント/トランザクションプーリングを導入。レイテンシは大幅に改善する。プロキシ・クライアント・レプリカは同一リージョンに共置するのが重要。

- キャッシュミスの嵐対策（Cache locking/leasing）  
  同一キーのキャッシュミスが同時発生するとDBへ大量リクエストが行くため、取得権を1つに絞るロック機構でミス嵐を防ぐ。

- リードレプリカの拡張とWALの課題  
  50台以上のレプリカへWALを直接配信するとプライマリ負荷が高まる。中継レプリカによるカスケードレプリケーションでスケールを確保するが、フェイルオーバー運用は複雑化する。

- レート制御・スキーマ管理  
  多層でのレートリミット、リトライ間隔の設計、スキーマ変更（フルテーブル書き換えを避ける）に対する厳格なルールが必須。

## 実践ポイント
- まずやること（低コストで効果大）
  1. PgBouncerを導入して接続をプーリング。アプリと同一リージョンに配置。  
  2. 重いクエリを洗い出す（EXPLAIN/pg_stat_statements）→ ORM生成SQLの見直し。  
  3. idle_in_transaction_session_timeout等のタイムアウトを設定。

- 中期施策
  4. キャッシュにロック/リースを導入してキャッシュミス嵐を防ぐ。  
  5. 書き込みホットスポットを特定し、可能ならシャーディングへ移行。  
  6. ワークロードを高/低優先度で分離しインスタンスを分ける。

- 長期/運用
  7. レプリカ拡張はカスケード方式を検討。フェイルオーバー手順を自動化・検証。  
  8. スキーマ変更ポリシーを定め、フルリライトを伴う変更は厳格に制限。  
  9. クラウドベンダー（Azure/AWS/GCPの東京リージョン）と連携し、プロバイダ固有の限界や機能を活用する。

これらは「日本の現場」にも直接応用可能。小規模でもまず接続管理とクエリ可視化から始め、段階的に書き込み削減やレプリカ戦略へ進めることが現実的な道筋となる。
