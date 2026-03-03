---
layout: post
title: "Moldova broke our data pipeline - モルドバがデータパイプラインを壊した"
date: 2026-03-03T06:36:48.573Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.avraam.dev/blog/moldova-broke-our-pipeline"
source_title: "Moldova broke our data pipeline | Avraam Mavridis"
source_id: 47197858
excerpt: "国名の埋め込みカンマでCSV崩壊、境界サニタイズとParquet移行で防ぐ"
image: "https://portfolio-blog-starter.vercel.app/og?title=Moldova%20broke%20our%20data%20pipeline&amp;description=A%20single%20comma%20in%20a%20country%20name%20silently%20corrupted%20our%20Redshift%20pipeline%20for%20weeks.%20One%20country%2C%20one%20comma%2C%20maximum%20chaos%20%E2%80%94%20and%20a%20lesson%20about%20where%20data%20sanitization%20actually%20belongs.&amp;tags=data-engineering%2Caws%2Credshift%2Cpipelines"
---

# Moldova broke our data pipeline - モルドバがデータパイプラインを壊した
国名に含まれる「,」で大事故——Moldova事件から学ぶ「境界での防御」

## 要約
Shopifyから来た国名 "Moldova, Republic of" に含まれるカンマが原因で、AWS DMSが出力したCSVが列ズレを起こしRedshiftのロードが死んだ。根本対処は「境界でのサニタイズ」と「輸送フォーマットの改善」。

## この記事を読むべき理由
外部ソース（SaaSやAPI）を受ける日本の開発チームでも同様の失敗は必ず起きる。小さなデータ形式の想定漏れがBIやレポートを止め、時間と信用を失わせるため、対策を知っておく価値が高い。

## 詳細解説
- 発生原因：Shopifyの配送国フィールドに公式表記 "Moldova, Republic of" のような「埋め込みカンマ」があり、AWS DMSがS3に書き出すCSVでフィールドを適切に引用せず、CSV行が想定列数より増えてRedshiftのCOPYで「invalid column count」になる。
- なぜ起きるか：DMSはRDS→S3→Redshiftの経路でCSVを使う。CSVはデリミタ依存のため、埋め込みデリミタがそのまま残ると列解釈が崩れる。ログ解析（記事ではClaudeでのログ検索が役立った）で原因追跡が行われた。
- 対処の選択肢：
  1. ソースを直す（DB上で手動修正） — 一時復旧するが次回同期で元に戻る可能性があり不安定。
  2. 同期ジョブでサニタイズ（境界で置換） — 例：カンマをハイフンに置換してCSV安全にする。冪等性が保てるため実用的。
  3. DMSのCSVデリミタを変更 — S3ターゲットの接続属性でカンマをパイプやタブに変えれば埋め込みカンマ問題を回避。ただし未知の特殊文字が将来出るリスクは残る。
  4. CSVをやめてParquetにする — Parquetはスキーマ志向で区切り文字問題なし。RedshiftのCOPYはParquetをネイティブサポートし、ロード性能も良い。
- 最善策：輸送層（Parquetやデリミタ変更）で耐性を持たせつつ、最初の取り込み点でデータを検証・正規化・サニタイズする二重防御が推奨される。これが「境界で処理する」原則。

## 実践ポイント
- 同期ジョブで外部文字列を正規化・サニタイズしてからDBに書き込む（例：カンマ置換、正規表現バリデーション）。  
- DMSのS3ターゲットでCSVデリミタを変更する、またはParquet出力に切り替える（性能と堅牢性向上）。  
- 取り込み時のスキーマ検証と異常行のアラート（invalid column countなど）を設定する。  
- 変換は冪等に実装し、元データ（生ログ）を残してデバッグできるようにする。  
- Shopifyなど外部APIからのデータはローカルの慣習（文字エンコーディング、表記揺れ）を前提にテストケースを作る。

外部データは「次のMoldova」を必ず持ってくる。境界で防ぎ、輸送を堅牢にする習慣が事故を防ぐ。
