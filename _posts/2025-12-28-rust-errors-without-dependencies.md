---
layout: post
title: Rust Errors Without Dependencies - 依存関係なしのRustエラー処理
date: 2025-12-28T07:15:42.895Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://vincents.dev/blog/rust-errors-without-dependencies/"
source_title: "Rust Errors Without Dependencies"
source_id: 764775186
excerpt: "依存ゼロで学ぶ、標準ライブラリだけでエラー連鎖と文脈を保持するRust実践法"
---

# Rust Errors Without Dependencies - 依存関係なしのRustエラー処理

## 要約
標準ライブラリだけで実用的なエラー型を作る手法を解説。依存を減らしつつ、エラーの連鎖（chaining）や文脈（context）を保持する実装パターンを示す。

## この記事を読むべき理由
サプライチェーン事故や企業ポリシーで外部クレートの導入に慎重な日本の現場に最適。組み込みやミッションクリティカル領域、または大規模コードベースで「依存を最小化」しつつ堅牢なエラー処理をしたいエンジニア向け。

## 詳細解説
Rustは例外を持たず、Resultを返すことで呼び出し側にエラー処理を委ねる設計です。この「即時に扱う」スタイルは安全性と合成性を高めますが、エラー文脈やチェーンをどう扱うかが設計上のポイントになります。多くの人は anyhow/thiserror/eyre のようなクレートを使いますが、標準ライブラリだけでも十分にまともなエラー設計が可能です。

基本パターンは次の通り：
- エラー用のenumを定義して、外部の具体的なエラー型（例: ParseIntError）をラップする。
- Fromトレイトを実装して `?` 演算子で自動変換できるようにする。
- Displayを実装してユーザー向けメッセージを用意し、Errorトレイトを実装してチェーン元を公開する（source）。

例：
```rust
// rust
use std::error::Error;
use std::fmt;

#[derive(Debug)]
pub enum DemoError {
    ParseErr(std::num::ParseIntError),
    IoErr(std::io::Error),
    // 必要に応じて他のケースを追加
}

impl From<std::num::ParseIntError> for DemoError {
    fn from(err: std::num::ParseIntError) -> Self {
        DemoError::ParseErr(err)
    }
}

impl From<std::io::Error> for DemoError {
    fn from(err: std::io::Error) -> Self {
        DemoError::IoErr(err)
    }
}

impl fmt::Display for DemoError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            DemoError::ParseErr(e) => write!(f, "parse error: {}", e),
            DemoError::IoErr(e) => write!(f, "io error: {}", e),
        }
    }
}

impl Error for DemoError {
    fn source(&self) -> Option<&(dyn Error + 'static)> {
        match self {
            DemoError::ParseErr(e) => Some(e),
            DemoError::IoErr(e) => Some(e),
        }
    }
}
```

この構成だと、`?` を使うだけで下位のエラーが自動でラップされ、Display/Debugで適切に情報を出力できます。必要なら `std::backtrace::Backtrace` をエラー構造体に含めて、発生時のバックトレースを保持することもできます（環境変数やRustバージョンに依存する点に注意）。

unwrap/expectに関しては「完全に禁止」する立場もありますが、設計上絶対に起こり得ないと保証できる箇所では適切に使うこともひとつの選択です。ただし運用上の想定外入力が発生するとサービス停止に直結するため、慎重な判断が必要です（Cloudflareの事例が示すように）。

## 実践ポイント
- 小さくて明確なエラーenumを作る：外部型をラップしてFromを実装する。
- Displayはユーザー／ログ向けの簡潔なメッセージに。内部デバッグには Debug や source() を使う。
- エラーに「文脈」を付けたいときは map_err でラップするか、専用のケースをenumに追加する。
  例: `.map_err(|e| DemoError::ParseErr(e))`
- unwrap/expectは本当に不変な前提の時だけ使う。運用の監査とドキュメントを残す。
- テストでエラー経路も必ずカバーする（異常系のインテグレーションテスト含む）。
- 企業や組み込み環境では依存を減らすことで監査負荷やバイナリサイズ、攻撃面を減らせる。

