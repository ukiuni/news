---
layout: post
title: "Building Docs Like a Product - ドキュメントをプロダクトのように作る"
date: 2026-01-29T23:46:30.077Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://emschwartz.me/building-docs-like-a-product/"
source_title: "Building Docs Like a Product | Evan Schwartz"
source_id: 802646319
excerpt: "ドキュメントを実際に触れる製品化し、実装共有や型付きリンクで体験と保守性を両立する"
image: "https://bear-images.sfo2.cdn.digitaloceanspaces.com/emschwartz-1723634231.webp"
---

# Building Docs Like a Product - ドキュメントをプロダクトのように作る
ドキュメントを「読むマニュアル」から「触れるアプリ」に変える、実践的ドキュメント設計テクニック

## 要約
Scour（個人向けコンテンツフィード）の事例から、ドキュメントをインタラクティブで製品の一部のように作る方法を解説。実例・コンポーネント共用・リンクの型安全化でメンテ性とユーザー体験を高める。

## この記事を読むべき理由
良いドキュメントは導入障壁を下げ、プロダクトの採用率を上げる。日本のSaaSや開発チームでも「使える・試せる」ドキュメントは差別化要素になるため、今日すぐ取り入れられる手法を知る価値がある。

## 詳細解説
- インタラクティブ化：Scourは単なる説明文ではなく、ドキュメント内に実際の検索バーや購読ボタンなど「動く部品」を埋め込んでいる。読者がその場で試せると理解が早い。
- 見せる（Show）ことの優先：設定や推薦の説明をテキストで書く代わりに、ログインユーザーには実際の推薦や設定トグルを表示して操作させる。実例は学習効率を飛躍的に上げる。
- 実コンポーネントの再利用：例示用に別実装を作らず、実際のUIコンポーネントをドキュメントでも使う。こうすると実装とドキュメントが乖離しにくい。
- ドキュメントから設定変更：設定ページへのリンクだけでなく、ドキュメント内でオン・オフできるとユーザーは即座に効果を確認できる。
- リンクの壊れ対策（型で守る）：Rustのaxumを例に、ルーティングを構造体（TypedPath）で定義しておけば、パス変更時にリンク切れが起きにくい。小規模でも型安全な参照は有効。

参考コード（Rust + axum の例）:
```rust
// rust
use axum::Router;
use axum_extra::routing::{TypedPath, RouterExt};
use serde::Deserialize;

#[derive(Deserialize, TypedPath)]
#[typed_path("/docs/interests")]
pub struct InterestsPath;

async fn interests(_path: InterestsPath) { /* ... */ }

#[tokio::main]
pub async fn main() {
    let router = Router::new().typed_get(interests);
}
```
- この型を利用して別箇所からパス文字列を生成すれば、パス変更時にコンパイルで検出できる。

## 実践ポイント
- ドキュメントに「触れる」要素を1つ入れる（例：簡易検索・トグル）。
- UIコンポーネントは本番と同じ実装を流用する。例示用コピーは作らない。
- 設定や購読をドキュメント内で切り替えられるようにして、即時フィードバックを与える。
- ルートやリンクはコード側で型にして管理（使用している言語/フレームワークに合わせる）。
- ユーザーフィードバックを定期的に反映し、ドキュメントをプロダクトの一部として運用する。
