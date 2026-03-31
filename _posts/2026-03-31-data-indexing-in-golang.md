---
layout: post
title: "Data Indexing in Golang - Golangでのデータ索引化"
date: 2026-03-31T16:23:22.690Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://hister.org/posts/data-indexing-in-golang"
source_title: "Hister"
source_id: 785186972
excerpt: "BleveでGoアプリに組み込み可能な高速日本語対応のファイルベース全文検索を実現"
---

# Data Indexing in Golang - Golangでのデータ索引化
Goで自前の全文検索を作る — Bleveで「外部サービス不要」「言語対応」「高速検索」を実現する方法

## 要約
GoライブラリBleveを使えば、Elasticsearchに頼らずファイルベースで大規模な全文インデックスを作れます。言語別解析・フィールド重み付け・カーソル型ページング・マルチインデックス運用が可能です。

## この記事を読むべき理由
日本のプロダクトでも、プライバシーや運用コストの観点から外部検索サービスを避けたいケースが増えています。BleveはGo製アプリに組み込みやすく、日本語を含む多言語対応やゼロダウンタイム切替ができるため、社内検索やローカル検索機能の実装に最適です。

## 詳細解説
- 基本操作：インデックス作成（New/Open）、ドキュメント登録（Index）、検索（Search）。Goの構造体を反射して自動的にフィールドを発見します。
- マッピングとアナライザ：デフォルトのマッピングは英語向けですが、フィールド単位でアナライザ（例：日本語形態素解析器）やインデックス/保存の有無を指定できます。マッピングはインデックス作成時に固定されるため、変更時は再インデックスが必要です。
- クエリ構築：QueryStringQueryでGoogle風構文が使えますが、Match/Wildcard/Booleanなどのクエリを組み合わせて独自の検索ロジック（フィールドごとのブースト、否定語処理など）を作るのが強力です。
- ブーストとスコア調整：タイトルやURLに高いブーストを与えることで関連度を明確にできます（例：titleブースト=50など）。
- ページング：Fromオフセットは深いページでコストが高くぶれるため、SearchAfter/SearchBeforeのカーソル型ページングを推奨。安定ソート（例：["_score","_id"]）が必要です。
- マルチインデックスとAlias：言語別や用途別に複数インデックスを持ち、IndexAliasでまとめて検索。新しいインデックスに切り替える際はAlias.Swapで無停止切替が可能。
- パフォーマンス調整：BoltDBのタイムアウト等、内部設定をOpenUsing/NewUsingで渡してチューニング可能。並行読み書きやホットスワップ下での挙動に注意。

簡単なコード例（概念のみ。実運用では日本語アナライザなど追加してください）:

go
```go
// シンプルなインデックス作成と検索
mapping := bleve.NewIndexMapping()
index, err := bleve.New("example.bleve", mapping)
if err != nil {
    index, _ = bleve.Open("example.bleve")
}
defer index.Close()

type Doc struct{ Title, URL, Text string }
index.Index("id1", Doc{"Go入門", "https://go.dev", "Goは..."})

// 検索
q := bleve.NewMatchQuery("検索ワード")
req := bleve.NewSearchRequest(q)
req.Size = 10
res, _ := index.Search(req)
```

クエリ組み立て（ブースト例）:

go
```go
tq := bleve.NewMatchQuery("kw"); tq.SetField("title"); tq.SetBoost(50)
uq := bleve.NewWildcardQuery("*kw*"); uq.SetField("url"); uq.SetBoost(10)
dis := bleve.NewDisjunctionQuery(uq, bleve.NewMatchQuery("kw"), tq)
boolq := query.NewBooleanQuery([]query.Query{dis}, nil, nil)
```

カーソルページング（SearchAfter）:

go
```go
req := bleve.NewSearchRequest(myQuery); req.Size = 20
req.SortBy([]string{"_score","_id"})
res, _ := index.Search(req)
// 次ページ
last := res.Hits[len(res.Hits)-1].Sort
next := bleve.NewSearchRequest(myQuery); next.Size = 20
next.SortBy([]string{"_score","_id"}); next.SetSearchAfter(last)
```

## 実践ポイント
- まずは小さなインデックスでBleveを試す。デフォルトマッピングで動作確認→必要に応じてフィールド別マッピングを追加。
- 日本語対応は形態素解析器（mecab等の連携）を検討し、ストップワードやステミング設定を調整する。
- ページングは必ずSearchAfterを使う（Fromは深いページで非推奨）。
- 言語ごとにインデックスを分け、IndexAliasで横断検索＆ホットスワップを実装する。
- 本番ではBoltDB等の設定や並行書き込みの挙動をチューニングし、再インデックス戦略を設計する。

元記事の詳細実装やさらに踏み込んだチューニングは公式ドキュメントと実コード（Bleveリポジトリ）を参照してください。
