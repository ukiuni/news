---
layout: post
title: "jsongrep – Query JSON using regular expressions over paths, compiled to DFAs - パスに正規表現を使ってJSONを検索、DFAにコンパイルされるjsongrep"
date: 2026-02-02T01:06:34.578Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/micahkepe/jsongrep"
source_title: "GitHub - micahkepe/jsongrep: A JSONPath-inspired query language over JSON documents."
source_id: 411597137
excerpt: "jsongrepでパス正規表現を使い、深いネストのJSONをDFA実行で超高速に抽出できる。"
image: "https://repository-images.githubusercontent.com/1034729507/046a4866-e4aa-483d-8993-4190e9bba2f1"
---

# jsongrep – Query JSON using regular expressions over paths, compiled to DFAs - パスに正規表現を使ってJSONを検索、DFAにコンパイルされるjsongrep
魅力的タイトル: 深いネストも一発抽出！パス正規表現でJSONを超高速検索する「jsongrep」の使いどころ

## 要約
jsongrepはJSONの「パス」に対して正規表現ライクなクエリを投げ、NFA→DFAで実行するコマンド＆Rustライブラリ。ネスト深いJSONから欲しい値だけを宣言的に効率抽出できる。

## この記事を読むべき理由
jqのようなフィルタパイプでは探索ロジックを書く必要がある場面で、パスを正規表現で宣言すれば短く・高速に抽出できる。大量ログやAPIレスポンス、多層設定ファイルを扱う日本の現場で即戦力となる。

## 詳細解説
- 基本思想：JSONをツリー（辺はフィールド名や配列インデックス）と見做し、パスに正規表現演算子を適用してマッチ集合を定義する。
- 主要演算子：
  - シーケンス: foo.bar.baz — 順に辿る
  - 連言/和: foo | bar — いずれか
  - クリーンスター（任意深度）: ** — 0階層以上の任意アクセス（任意の深さで一致）
  - 単一ワイルドカード: * または [*] — 単一フィールド／配列要素
  - オプショナル: foo?.bar — fooがあれば続ける
  - 配列指定: [0], [1:3] — インデックスやスライス
  - （実験的）/regex/ — フィールド名に正規表現マッチ（未完）
- 実装の肝：クエリをまずNFAに変換し、さらに決定化してDFAとして実行するため、ドキュメントを一度走査しながら高速にマッチできる。重複する正規表現の問題（例：/a/と/aab/の重なり）は決定化で処理する必要があり、一部実装中の機能あり。
- 使い方（CLI）：コマンドは jg。パイプ入力、ファイル指定、--count、--no-display、--compactなどオプションあり。
- ライブラリ：Cargo依存に追加してQueryBuilderでプログラム的にクエリを構築可能。

例（短い使用例）：
```bash
# インストール
cargo install jsongrep

# 標準入力からネストしたnameを全部抜く
echo '{"users":[{"name":"Alice"},{"name":"Bob"}]}' | jg '**.name'
# 出力: ["Alice","Bob"]

# ファイルから配列中の全メールを数える（表示せずカウントのみ）
jg 'users[*].email' data.json --count --no-display
```

ライブラリ例（Rust）:
```rust
use jsongrep::query::engine::QueryBuilder;

let query = QueryBuilder::new()
    .field("foo")
    .index(0)
    .field("bar")
    .field_wildcard()
    .field("baz")
    .build();
```

## 実践ポイント
- 深いネストや不均一なJSON構造から特定フィールドを取り出すときはまずjsongrepのパス式を試すと短く書ける。
- ログ解析やAPI大量レスポンスの集計では --count／--no-display を使って高速に件数だけ集める。
- Rustプロジェクトに組み込めば、クエリをコード生成的に作り、安全に実行可能。
- 日本語APIフィールドやスペース含むフィールドは "quoted field" を使う（例: "user name"）。
- 実運用で正規表現フィールドマッチが必要な場合は実装状況をチェック（現状実験的）。

参考：公式リポジトリ（インストール・サンプル・詳細仕様）を参照して、既存のjqワークフローに置き換えられる箇所を検討すると良い。
