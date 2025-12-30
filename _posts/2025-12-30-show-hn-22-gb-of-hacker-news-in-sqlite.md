---
layout: post
title: "Show HN: 22 GB of Hacker News in SQLite - 22 GBのHacker NewsをSQLiteで手元に"
date: 2025-12-30T19:37:19.297Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://hackerbook.dosaygo.com"
source_title: "Show HN: 22 GB of Hacker News in SQLite"
source_id: 46435308
excerpt: "22GBのHN全投稿をSQLite化、全文検索と時系列分析で国内トレンドを先読み可能"
---

# Show HN: 22 GB of Hacker News in SQLite - 22 GBのHacker NewsをSQLiteで手元に
22GBのHNアーカイブをSQLite化して「ローカルで全文検索・集計」ができる──研究・プロダクト開発に刺さる究極のデータセット

## 要約
Hacker BookはHacker Newsの投稿・コメントを2006〜2025年分まとめて22GBのSQLiteデータベースとして提供し、オフライン解析や全文検索、可視化に即使える形で公開しているプロジェクトです。

## この記事を読むべき理由
国内のプロダクト開発者や研究者が、グローバルな技術トレンドや議論の流れを定量的に捉えるための即戦力データセットだからです。日本語キーワードや「Japan」タグでの時系列解析を行えば、国内採用や投資トレンドの先読みにも使えます。

## 詳細解説
- データ規模と形式: 提供されるデータは合計約22GBの単一SQLiteファイル。テーブルは投稿(posts)、コメント(comments)、ユーザ(users)、リンクやメタ情報などで構成される想定（一般的なHNダンプの構成に準拠）。
- 取得手法: 作者はHNの公開アーカイブやスクレイピング／APIを組み合わせて収集し、整形・正規化してSQLiteに格納したと考えられます（詳細は配布ページを参照）。
- 検索と索引: 大量テキストを扱うため、SQLiteのFTS5（全文検索拡張）やインデックスが設定されている可能性が高く、キーワード検索やフレーズ検索が高速に行えます。
- 実用ユースケース:
  - トレンド分析: 時系列でのトピック出現頻度、急上昇ワード検出。
  - ネットワーク解析: 投稿→コメントのスレッド深さ、ユーザ間のやり取り解析。
  - コンテンツ抽出: 特定ドメインやURLの被リンク数、人気スニペットの抽出。
  - モデル学習データ: コミュニティ言語・応答例のコーパスとして（利用規約・ライセンスを確認のこと）。
- 注意点:
  - 22GBのDBはディスク・バックアップ・メモリの要件に注意。軽量解析はDuckDBやsqlite-utilsへの変換も検討。
  - データ利用はHNの利用規約／著作権・プライバシーに従うこと。

## 実践ポイント
- VS Codeでの即活用:
  - SQLite拡張を入れてDBを開き、クエリを試す。統合ターミナルで簡単にバックアップや変換を実行できる。
- 最初にやるべきクエリ例（人気ドメイン上位）:
```sql
-- sql
SELECT url_host, COUNT(*) AS cnt
FROM posts
GROUP BY url_host
ORDER BY cnt DESC
LIMIT 20;
```
- 日本関連のポスト抽出（タイトル・本文に「Japan」や「日本」を含むもの）:
```sql
-- sql
SELECT id, title, created_at
FROM posts
WHERE body LIKE '%Japan%' OR body LIKE '%日本%'
ORDER BY created_at DESC
LIMIT 100;
```
- Pythonでの取り回し例（pandasで集計）:
```python
# python
import sqlite3
import pandas as pd
con = sqlite3.connect("hackerbook.db")
df = pd.read_sql_query("SELECT created_at, COUNT(*) AS cnt FROM posts GROUP BY date(created_at)", con)
print(df.tail())
```
- パフォーマンスTips:
  - FTS5テーブルがあるならそちらを使う（全文検索はFTSが圧倒的に早い）。
  - 大きなJOINやOLAP処理はDuckDBにインポートすると高速。
  - WALモードや適切なインデックス、VACUUMでレスポンスを改善。

## 引用元
- タイトル: Show HN: 22 GB of Hacker News in SQLite
- URL: https://hackerbook.dosaygo.com
