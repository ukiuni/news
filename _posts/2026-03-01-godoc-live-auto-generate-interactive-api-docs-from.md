---
layout: post
title: "GoDoc Live — Auto-generate interactive API docs from Go source code (no annotations needed) - GoDoc Live — 注釈不要でGoソースから対話式APIドキュメントを自動生成"
date: 2026-03-01T13:17:33.664Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/syst3mctl/godoclive"
source_title: "GitHub - syst3mctl/godoclive: GoDoc Live statically analyzes your Go HTTP services — extracts route definitions, request/response contracts, and authentication patterns — then generates beautiful, interactive API documentation."
source_id: 393596459
excerpt: "注釈不要で既存Goコードを静的解析し、即試せる対話式APIドキュメントを自動生成"
image: "https://opengraph.githubassets.com/5433c1164836dc3d92e7dce9ecef39fe46810bd88f05c760f4fa75ffe8ae7113/syst3mctl/godoclive"
---

# GoDoc Live — Auto-generate interactive API docs from Go source code (no annotations needed) - GoDoc Live — 注釈不要でGoソースから対話式APIドキュメントを自動生成
魅せるAPIドキュメントがコードから勝手に生まれる。注釈ゼロ、既存のハンドラを解析して即「Try itできる」ドキュメントを作るツールの話。

## 要約
GoのHTTPサービス（chi / gin）を静的解析してルート、パラメータ、リクエスト/レスポンス、認証パターンを抽出し、対話式HTMLドキュメントを自動生成するCLI／ライブラリ。注釈不要で既存コードに手を加えず使える。

## この記事を読むべき理由
日本でもマイクロサービスや社内APIの増加でAPIドキュメント整備が課題。手作業でOpenAPIを書かずに、安全で最新のドキュメントを自動生成できれば、オンボーディングや開発効率が大きく改善します。

## 詳細解説
- 何をするか  
  - go/ast と go/types による静的解析で、ルート登録（chi, gin）、パス/クエリパラメータ、リクエストボディ、レスポンス、ファイルアップロード、認証（JWT/APIキー/Basic）を抽出。
  - ハンドラ内のjson.DecodeやShouldBindJSON解析で構造体を復元し、ステータスコードは条件分岐を追跡して割り当てる。

- サポート状況（Phase 1）  
  - 対応：chi、gin（ルート・グループ・ミドルウェアなど）  
  - 精度（テストデータ上）：ルート/パス/クエリ/レスポンス/認証は高精度。詳細はREADMEのAccuracy参照。今後 gorilla/mux、echo、fiber と OpenAPI出力を予定。

- 使い方（代表的CLI）  
  - インストール: go install github.com/syst3mctl/godoclive/cmd/godoclive@latest  
  - ドキュメント生成: godoclive generate ./...  → docs/index.html を開く  
  - ライブ監視: godoclive watch ./... --serve :8080（保存で自動再生成＋ブラウザ自動リロード）  
  - 分析のみ: godoclive analyze ./...（--json, --verbose有り）  
  - 検証: godoclive validate ./...（カバレッジ確認）

- カスタム化  
  - .godoclive.yaml でタイトル、バージョン、base_url、除外パス、認証ヘッダ、オーバーライド(説明・タグ・追加レスポンス)が設定可能。ゼロ設定でも動く点が魅力。

- ライブラリ利用  
  - Goライブラリとして組み込み可能。Analyze / Generate のAPIが提供されるためCIやカスタムパイプラインへの組み込みが容易。

## 実践ポイント
- 今すぐ試す（3コマンド）  
  1. go install github.com/syst3mctl/godoclive/cmd/godoclive@latest  
  2. godoclive generate ./...  
  3. open docs/index.html（または godoclive watch ./... --serve :8080）

- CI導入案  
  - PRで godoclive validate を実行し、ドキュメント化カバレッジを阻止条件にする（未解決エンドポイントをFail条件に）。

- 日本市場での活用ポイント  
  - 社内APIやレガシーGoサービスのドキュメント不足を短期間で解消。API仕様書作成の工数削減や、社内向けSDK/フロント実装の品質向上に直結。

- 注意点  
  - 現状は chi/g

in が主対象。特殊なルーターや極端に複雑なハンドラでは解析が未解決になる可能性あり。必要なら .godoclive.yaml で手動オーバーライドを使う。

以上を踏まえ、既存のGo HTTPコードベースに手を入れず「見た目も使い勝手も良い」APIドキュメントを手早く作りたい現場には強くおすすめです。
