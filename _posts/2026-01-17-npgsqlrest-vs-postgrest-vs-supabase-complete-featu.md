---
layout: post
title: "NpgsqlRest vs PostgREST vs Supabase: Complete Feature Comparison - NpgsqlRest vs PostgREST vs Supabase：完全な機能比較"
date: 2026-01-17T12:56:54.458Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://npgsqlrest.github.io/blog/npgsqlrest-vs-postgrest-supabase-comparison.html"
source_title: "NpgsqlRest vs PostgREST vs Supabase: Complete Feature Comparison | NpgsqlRest"
source_id: 424631011
excerpt: "性能・運用・セキュリティで比較し用途別にNpgsqlRest／PostgREST／Supabaseを推奨"
---

# NpgsqlRest vs PostgREST vs Supabase: Complete Feature Comparison - NpgsqlRest vs PostgREST vs Supabase：完全な機能比較
PostgresをREST化するならどれが正解？性能・運用・セキュリティで選ぶ実務ガイド

## 要約
PostgresをそのままREST API化する代表的な3選を機能・性能・運用観点で比較。軽量で高性能なNpgsqlRest、テーブル中心でシンプルなPostgREST、機能豊富なバックエンドとしてのSupabaseという棲み分けが見える。

## この記事を読むべき理由
- 国内プロジェクトでPostgresをAPI化する際の「どれを選ぶか」が明確になる。  
- 性能や運用コスト、セキュリティ（RLS/認証/データ主権）を踏まえた実務判断に役立つ。  
- 初心者でも理解しやすい運用・導入の第一歩（プロトタイプ〜本番）を示す。

## 詳細解説
- アーキテクチャ
  - NpgsqlRest：単一バイナリ（約30MB）で動く自己完結型。Postgresに直結して関数をエンドポイント化する「function-first」設計。設定はSQLコメントで管理。
  - PostgREST：単一バイナリ（Haskell）。テーブル/ビュー中心で、クライアント側がクエリを組み立てるスタイル。Row Level Security（RLS）と組み合わせる運用が一般的。
  - Supabase：複数サービスから成るフルプラットフォーム（PostgREST, GoTrue, Realtime, Storage 等）。管理コンソールとホスティングを提供するが、セルフホストだと構成が複雑。

- 性能（ベンチマーク要約）
  - NpgsqlRest（JIT）: 約5,177 req/s（100 VU） — 高いスケーラビリティ
  - PostgREST: 約843 req/s（100 VU） — 小〜中規模では十分だが高負荷時の伸びは限定的
  - 大きなペイロード（500レコード）でもNpgsqlRestが低レイテンシで処理数が多い傾向

- 設計思想の違い
  - NpgsqlRest：サーバ側で関数（ストアドプロシージャ）にAPIロジックを閉じる。安全で予測可能、最適化しやすい。
  - PostgREST：テーブルをそのまま公開し、クライアントに柔軟なクエリ構築を許す。迅速なプロトタイピング向け。
  - Supabase：認証・ストレージ・Realtimeを含むフルセット。スタートアップやプロダクト立ち上げに便利。

- 機能差分（要点）
  - 型の取り扱い：複合型やネストJSONは3者とも対応。NpgsqlRestは返却オブジェクトをフラット化／ネスト切替可能でTypeScript生成が強い。
  - 認証：NpgsqlRestはJWT/Cookie/Basic/外部OAuthなど多様。PostgRESTはJWT中心、SupabaseはGoTrueによる多プロバイダ対応。
  - ファイル処理：NpgsqlRestは画像検証・CSV/Excel取り込み・大きなファイル処理までDB連携で強力。PostgRESTは非対応、Supabaseは独自Storageを利用。
  - パフォーマンス機能：NpgsqlRestはメモリ/Redisキャッシュ、スタンペード防止、複数のレート制御、接続リトライ等を備える。
  - リアルタイム：SupabaseはWebSocket/LISTEN-NOTIFY系、NpgsqlRestはSSE＋PostgresのRAISEストリーミングという差。

- 設定・運用
  - NpgsqlRest：API設定をSQLコメントで関数に付与（バージョン管理しやすい）。例：エンドポイント/認可/キャッシュをコメントで指定可能。
  - PostgREST：RLSポリシー＋設定ファイル。APIゲートウェイでパスを整備することが多い。
  - Supabase：ダッシュボード主体、Edge Functionsで拡張可能。ただしセルフホストはサービス多めで運用コスト増。

- 日本市場との関連性
  - データ主権・オンプレ要件がある企業では単一バイナリで簡単に社内運用できるNpgsqlRestやPostgRESTが有利。
  - スタートアップやプロダクトMVPでは認証・ストレージ・Realtimeを一括提供するSupabaseが導入・開発速度で有利。
  - 大手SIや金融分野では「関数を使った明示的なAPI設計（NpgsqlRest）」＋RLS／監査ログが運用上の安心材料になる。
  - 国内クラウド（AWS/Azure/GCPのJPリージョン）との接続、運用自動化やログ集約（OpenTelemetry/Elasticsearch）を考慮すれば選定基準が変わる。

## 実践ポイント
1. 目的で選ぶ
   - 高性能かつDB中心で細かい制御が必要 → NpgsqlRest
   - シンプルにテーブルをAPI化してクライアントに自由度を与えたい → PostgREST
   - 認証・ストレージ・Realtimeを一括で使いたい／早くプロダクトを出したい → Supabase

2. セキュリティ設計
   - 機密データはテーブル全公開より関数経由で制御する（NpgsqlRestの設計思想が有効）。  
   - RLSは必須レベル。PostgREST/SupabaseではRLSとJWTの組合せを検討。

3. 開発ワークフロー
   - DBスキーマとAPI設定を一元管理したければNpgsqlRestのSQLコメント方式が便利。  
   - TypeScript型が欲しいならNpgsqlRestやSupabaseの型生成機能を活用。

4. 運用とスケール
   - 高負荷を想定するならベンチマーク実施（簡単な負荷試験で実乗数を確認）。NpgsqlRestはスケールが良い傾向。  
   - Supabaseをセルフホストする場合は複数サービスのオーケストレーションを忘れずに。

5. すぐ試せるコマンド（NpgsqlRestの例）
```bash
# 直接ダウンロードして実行（例）
wget https://github.com/NpgsqlRest/NpgsqlRest/releases/latest/download/npgsqlrest-linux64
chmod +x npgsqlrest-linux64
./npgsqlrest-linux64 --connection "Host=localhost;Database=mydb;Username=api"
```

6. ヒント：API設計の初手
   - まずは1〜2個の「関数ベースのエンドポイント」を作って性能・権限・レスポンスを確認する。  
   - クライアント側でのクエリ合成が重要か（PostgREST系）、サーバ側で厳格に定義したいか（NpgsqlRest系）を早めに決める。

以上を踏まえ、まずは小さなPoCで性能と運用コストを比較することを推奨。目的に応じて「単一バイナリで高性能を取る」か「フルマネージドで速度重視の開発を取る」か判断するのが実務的。
