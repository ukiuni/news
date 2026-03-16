---
layout: post
title: "Ten years late to the dbt party (DuckDB edition) - dbtパーティーに10年遅れて（DuckDB編）"
date: 2026-02-23T16:04:44.250Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://rmoff.net/2026/02/19/ten-years-late-to-the-dbt-party-duckdb-edition/"
source_title: "Ten years late to the dbt party (DuckDB edition)"
source_id: 398572544
excerpt: "DuckDB＋dbtで小規模チーム向け高速再現パイプライン構築法（実践）"
image: "https://rmoff.net/images/2026/02/h_IMG_4249.webp"
---

# Ten years late to the dbt party (DuckDB edition) - dbtパーティーに10年遅れて（DuckDB編）
遅れてきたけど目から鱗：DuckDBで始めるdbt入門 — 小規模データワークフローを一気に現代化する方法

## 要約
dbtをDuckDBと組み合わせて、APIやCSVからの取り込み→ステージング→マート→増分ロード／バックフィル／テストまでをシンプルかつ再現可能に構築した実践レポート。

## この記事を読むべき理由
dbtはデータ変換のベストプラクティス（ソース定義、ステージング、マート、テスト、ドキュメント、増分処理）を提供するため、日本の少人数チームやプロトタイプ開発で「素早く確実な」データパイプラインを作る際に即戦力になるから。

## 詳細解説
- 全体像  
  - 著者はUKの環境庁API（気象・河川など）をデータ源に、従来の手書きSQLパイプラインからdbtへ移行。DuckDBは軽量な実行エンジン／ストレージとして使い、dbtは変換ロジックと運用ルールを担う構成。

- ソースと分離（抽出 vs 変換）  
  - dbtのsource定義で「取り込み元」を宣言し、抽出（API呼び出しやCSV取得）と変換（ステージング→マート）を明確に分離。これによりオフライン用の静的データ差し替えやデータ鮮度チェックが容易に。

  例：sources.yml（抜粋）
  ```yaml
  # yaml
  - name: env_agency
    schema: main
    description: Raw data from the Environment Agency API
    tables:
      - name: raw_readings
        loaded_at_field: _latest_reading_at
        freshness:
          warn_after: {count: 24, period: hour}
          error_after: {count: 48, period: hour}
  ```

- DuckDBを使った抽出の実装（マクロ）  
  - dbtのJinjaマクロでDuckDBのread_json/read_csvを実行し、取り込みテーブル(raw_readings)を作成。取り込み時に最新タイムスタンプを列として保存しておくことで、dbtのfreshnessチェックや増分判定に利用する。

  例：マクロ（抜粋）
  ```sql
  -- sql
  {% raw %}
  {% macro load_raw_readings() %}
  {% set endpoint = var('api_base_url') ~ '/data/readings?latest' %}
  {% set sql %}
  CREATE OR REPLACE TABLE raw_readings AS
  SELECT *, list_max(list_transform(items, x -> x.dateTime)) AS _latest_reading_at
  FROM read_json('{{ endpoint }}');
  {% endset %}
  {% do run_query(sql) %}
  {% endmacro %}
  {% endraw %}
  ```

- ステージング / マート設計  
  - ステージングでデータクレンジング（URL除去、配列→値変換、型キャストなど）を行い、マート（fct_readings）はstgテーブルとアーカイブstgのUNIONで構築。責務を分離するとデバッグやバックフィルが容易。

- 増分ロード（incremental）  
  - dbtのmaterialized='incremental'とunique_key指定で、既存テーブルへの差分挿入を自動化。is_incremental()条件で「高水位（max日時）以降」をWHEREに入れて処理するのが定石。

  例：増分設定
  ```sql
  -- sql
  {{ config(materialized='incremental', unique_key=['dateTime','measure']) }}
  SELECT * FROM {{ ref('stg_readings') }}
  {% if is_incremental() %}
  WHERE dateTime > (SELECT MAX(dateTime) FROM {{ this }})
  {% endif %}
  ```

- バックフィルと履歴取り込み  
  - 日毎CSVをgenerate_seriesやlist_transformで列挙し、read_csvでアーカイブを取り込みつつ別ステージ（stg_readings_archive）で整形。マートはstgとstg_archiveをUNIONするだけで済む。

- SCD（徐々に変化する次元）の扱い  
  - 単純に上書き（SCD Type1）するのではなく、履歴管理（Type2相当）や更新キーの設計を考慮することで分析上の価値を維持できる。

- テスト・チェック・オーケストレーション  
  - dbtのtests・freshness・ドキュメント生成機能で品質管理。抽出は外部（Airbyteやカスタムジョブ）で行い、DagsterやAirflowでdbt実行をオーケストレーションするのが現実的。

## 実践ポイント
- 今すぐ試す手順（小さく始める）
  1. DuckDBをローカルに用意し、簡単なread_json/read_csvでAPI/CSVを取り込む。  
  2. dbtプロジェクトを作成し、sources.ymlで取り込み先を定義する。  
  3. ステージング→マートの分離を意識してモデルを作る。  
  4. materialized='incremental'とunique_keyで増分処理を設定。  
  5. freshnessルールと基本的なtests（nullチェック、一意性）を追加。  
  6. 歴史データはバックフィル用マクロで取り込み、別stgで扱う。

- 日本の現場での有用性  
  - ローカル／オンプレ環境や小規模チーム、IoT・環境センサーデータなど断続的に到着するデータのプロトタイピングに最適。DuckDBは軽量でローカル解析に向くため、クラウド移行前の開発・検証コストを抑えられる。

- 注意点
  - DuckDBのAPI取り込みは便利だが、リトライやタイムアウトなど運用面は外部ツールで補完するのが安全。dbtは「変換」に集中するツールである点を忘れないこと。

以上を踏まえ、dbt＋DuckDBは「小さく始めて堅牢に育てる」データ基盤づくりに非常に強力な組み合わせ。まずは1本のデータパイプラインをdbtで組んでみて、ドキュメントとテストの恩恵を体感してほしい。
