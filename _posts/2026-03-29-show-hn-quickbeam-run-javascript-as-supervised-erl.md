---
layout: post
title: "Show HN: QuickBEAM – run JavaScript as supervised Erlang/OTP processes - QuickBEAM：スーパーバイズされたErlang/OTPプロセスとしてJavaScriptを実行"
date: 2026-03-29T17:45:36.960Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/elixir-volt/quickbeam"
source_title: "GitHub - elixir-volt/quickbeam: JavaScript runtime for the BEAM — Web APIs backed by OTP, native DOM, and a built-in TypeScript toolchain. · GitHub"
source_id: 47558094
excerpt: "QuickBEAMでJSをOTPプロセス化、LiveViewやSSR向けに安全高並列実行"
image: "https://opengraph.githubassets.com/150adc31c7e3758bdf17ad29b4e11274923dcf40fc244132942dfcb1d88fa34d/elixir-volt/quickbeam"
---

# Show HN: QuickBEAM – run JavaScript as supervised Erlang/OTP processes - QuickBEAM：スーパーバイズされたErlang/OTPプロセスとしてJavaScriptを実行
BEAMの監視下で安心してJavaScriptを走らせる時代が来た——QuickBEAMでJSをOTPツリーに組み込む利点とは？

## 要約
QuickBEAMはQuickJSをBEAM上に埋め込み、各JSランタイムをGenServer/OTP子プロセスとして管理できるランタイムです。JSとElixir/Erlang間の双方向ブリッジ、ネイティブDOM、TypeScriptツールチェーンなどを備え、安全かつ高並列にJSを実行できます。

## この記事を読むべき理由
- サーバー側で「ブラウザAPIライク」なJSを実行したい（SSR、LiveView連携、スクリプトサンドボックスなど）日本のPhoenix/Elixir開発者にとって、QuickBEAMは既存のOTP運用慣習でJSを扱える実用的な選択肢です。

## 詳細解説
- アーキテクチャ概要  
  QuickBEAMはQuickJSエンジンをBEAMプロセス（GenServer）として動かす実装。ランタイムはOTPの監視・再起動の恩恵を受け、プロセス間メッセージでJSとBEAMが連携します。Zig（0.15+）をビルド依存に持ち、TypeScriptやブラウザ/Node互換APIのバンドルを提供します。

- BEAMとの統合ポイント  
  - Beam.call / callSyncでElixirハンドラを呼ぶ（DBやキャッシュの橋渡しが容易）。  
  - Beam.send / onMessage / monitorなどでBEAMプロセスと通常のメッセージ連携が可能。  
  - 分散やrpc、プロセス監視（link/demonitor）もサポート。

- DOM & Web API  
  - lexborベースのネイティブDOMを提供し、documentやquerySelectorが動作。Elixir側からDOMをFloki互換タプルで直接読み取れるため、JSを実行せずにHTMLを解析/取得できます（SSRに便利）。  
  - fetch/WebSocket/Worker/BroadcastChannelなどはBEAM実装にバックエンドがあり、純粋なJSポリフィルではない点が特徴。

- 高並列運用向けの工夫  
  - QuickBEAM.ContextPool：軽量なJSコンテキストを多数扱う際にスレッドを共有してスケール。  
  - per-contextリソース制限（memory_limit, max_reductions）でOOMや無限ループを制御。

- モジュール性と軽量化  
  - 必要なAPIグループのみを読み込める（:fetch,:dom,:urlなど）。バンドルサイズを抑え、メモリ効率を改善可能。

- デバッグ／解析機能  
  - QuickJSバイトコードのコンパイル・逆アセンブル、ランタイム診断情報、global一覧などのインスペクション機能を提供。

- 実用ユースケース（想定）  
  - Phoenix LiveViewで接続ごとにJSコンテキストを割り当ててクライアント的ロジックをサーバーで実行。  
  - センドボックス化されたユーザースクリプト実行（監視・再起動・リソース制限あり）。  
  - サーバー側でのHTML生成と直接DOM操作によるSSRパイプライン。  

短いコード例（Elixirでランタイム開始して式を評価）:

```elixir
{:ok, rt} = QuickBEAM.start()
{:ok, 3} = QuickBEAM.eval(rt, "1 + 2")
{:ok, "HI"} = QuickBEAM.eval(rt, "'hi'.toUpperCase()")
QuickBEAM.stop(rt)
```

LiveView連携でContextを作る例:

```elixir
{:ok, pool} = QuickBEAM.ContextPool.start_link(name: MyApp.JSPool, size: 4)
{:ok, ctx} = QuickBEAM.Context.start_link(pool: MyApp.JSPool, handlers: %{"db.query" => &MyApp.query/1})
{:ok, html} = QuickBEAM.Context.eval(ctx, "renderPage()")
```

JS側からBEAMハンドラを呼ぶ例:

```javascript
const rows = await Beam.call("db.query", "SELECT * FROM users LIMIT 5");
```

## 実践ポイント
- 試す手順（短縮）  
  1. mix.exsに {:quickbeam, "~> 0.7"} を追加。Zigが必要（Ziglerで自動取得可）。  
  2. 最初は apis: [:browser] で起動してDOM操作やfetchを確認。  
  3. 高並列なら ContextPool を使い、memory_limit と max_reductions を設定して安全性を確保。  
  4. DBやキャッシュは handlers を通してBridgeする（Beam.call）。  
  5. SSRやLiveViewでDOMをElixir側から読むなら dom_find / dom_html を活用。  
  6. 本番前にAPIグループを絞ってバンドルを小さくする（性能と安全性向上）。

- 注意点  
  - Zigやネイティブ依存があるためCI/CDでビルド手順を整備する。  
  - ランタイムはOTPで再起動される設計なので、状態持ち込みや外部接続のクリーンアップを考慮する。

最後に一言：OTP運用に慣れたチームなら、QuickBEAMは「JSを安全にサーバー実行するための自然な選択肢」になり得ます。まずは小さなPoC（LiveViewの一部レンダリングやユーザースクリプトのサンドボックス）から試してみてください。
