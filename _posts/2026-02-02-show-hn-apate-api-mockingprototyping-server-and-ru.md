---
layout: post
title: "Show HN: Apate API mocking/prototyping server and Rust unit test library - Apate: APIモック／プロトタイピングサーバとRustテストライブラリ"
date: 2026-02-02T11:39:43.808Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/rustrum/apate"
source_title: "GitHub - rustrum/apate: API prototyping/mocking server &amp; rust unit tests library to mimic external 3rd party API endpoints with Rhai scripting capabilities"
source_id: 46845097
excerpt: "Rust製ローカルAPIモックApateで外部依存を切り、テストとプロトタイプを高速化"
image: "https://repository-images.githubusercontent.com/1075241504/8a0f09c1-6904-421f-a349-75c9b698af84"
---

# Show HN: Apate API mocking/prototyping server and Rust unit test library - Apate: APIモック／プロトタイピングサーバとRustテストライブラリ
「外部APIに悩まされない」ローカルで使える軽量モックサーバ — Rust製でテスト向け機能が豊富なApate

## 要約
Apateはローカルで動くAPIプロトタイピング／モックサーバと、Rust向けのユニットテスト用ライブラリ。RhaiスクリプトやJinjaテンプレート、メモリ永続化などで柔軟に応答を定義でき、Dockerやcargoで手軽に使える。

## この記事を読むべき理由
外部APIの不安定さや開発環境の差分でCIや統合テストが壊れる課題は日本の開発現場でも共通。Apateを使えば外部依存を切り離して安定したテスト／プロトタイプ環境を素早く作れます。

## 詳細解説
- アーキテクチャ: 独立したサーバ（Web UIあり）として動作し、TOMLで仕様を読み込む。ランタイムはRust。
- レスポンス定義: 平文／バイナリ（HEX/BASE64）／minijinjaテンプレート／Rhaiスクリプトで出力を生成可能。テンプレートやスクリプト内でリクエスト情報（メソッド、パス、ヘッダ、ボディ）にアクセスできる。
- 条件判定と拡張: “Matchers”でリクエストマッチ条件を定義（すべてtrueならマッチ）。“Processors”でRhaiを使って応答後処理やボディ修正が可能。カスタムRustプロセッサも埋め込み可。
- 振る舞いの保持: メモリ上の簡易永続化でカウンタやストレージ読み書きができ、ステートフルなモックが作れる。
- テスト向け統合: RustのテストでApateを起動して、本番と同じHTTP呼び出しでクライアントロジックを検証できる。テスト中にサーバを起動・破棄するだけで完結。
- 運用: Dockerイメージが公開されており、ENVで仕様ファイルを渡すかUI/API経由でランタイム編集可能。

## 実践ポイント
- 最速起動（Docker）:
```bash
docker run --rm -p 8228:8228 ghcr.io/rustrum/apate:latest
```
- ローカル開発（cargo）:
```bash
cargo install apate
apate -p 8228 ./examples/apate-specs.toml
```
- Rustテストでの使い方（概略）:
```rust
// テスト内でApateサーバを起動して実APIと同じURLに対して検証する
let config = DeceitBuilder::with_uris(&["/user/check"])
    .require_method("POST")
    .add_response(DeceitResponseBuilder::default()
        .code(200)
        .with_output(r#"{"message":"Success"}"#)
        .build())
    .to_app_config();
let _apate = ApateTestServer::start(config, 0);
// ここで http://localhost:8228/user/check を呼んでアサート
```
- 日本市場での活用例: 外部決済／SNS認証／サードパーティ通知APIの開発・E2Eテスト、CIでの安定化、プロダクト開発初期のAPIプロトタイプ共有。
- 注意点: Rhaiやテンプレートで複雑にすると保守コストが上がるため、まずはシンプルなモックから導入し必要に応じて拡張するのがおすすめ。

以上を踏まえ、外部API依存でテストが壊れる現場や、迅速なAPIプロトタイピングが必要なプロジェクトはApateを試してみてください。
