---
layout: post
title: "docrawl: Rust CLI that crawls documentation sites and converts to clean Markdown - docrawl：ドキュメントサイトをクリーンなMarkdownに変換するRust製CLI"
date: 2026-02-17T23:23:18.063Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/neur0map/docrawl"
source_title: "GitHub - neur0map/docrawl: Docs‑focused crawler that converts documentation sites to clean Markdown."
source_id: 439109560
excerpt: "ドキュメントサイトを構造維持で即Markdown化しLLM学習や移行を劇的に簡単化するCLI"
image: "https://opengraph.githubassets.com/143362499d5a33f478bfeb6d17b0ffc815cdd0c470c9e42a99138e2be6f59026/neur0map/docrawl"
---

# docrawl: Rust CLI that crawls documentation sites and converts to clean Markdown - docrawl：ドキュメントサイトをクリーンなMarkdownに変換するRust製CLI

一瞬で技術ドキュメントを丸ごとMarkdown化——移行、バックアップ、LLM向けデータ準備に便利な「docrawl」の魅力と使い所

## 要約
docrawlはドキュメント特化のRust製クローラーで、Docusaurus/MkDocs/Sphinxなどを自動検出して構造を保ったままクリーンなMarkdownへ変換します。robots.txtやレート制御、サニタイズ、疑わしいコンテンツの隔離など「礼儀」と安全を重視しています。

## この記事を読むべき理由
日本の開発チームがドキュメントの移行、オフライン配布、検索インデックス作成、あるいはLLM学習データ整備を考えるとき、手作業を大幅に減らせる実用的なツールだからです。

## 詳細解説
- 主目的：ドキュメントサイトをクローリングして、フォルダ構造をURLパスに合わせてmirrorしつつindex.mdを生成。コードブロック、表、YAMLフロントマター（title, source_url, fetched_at）を保持します。  
- フレームワーク対応：Docusaurus、MkDocs、Sphinx、Next.js docsなどを自動検出するビルトインセレクタを搭載。カスタムCSSセレクタの指定も可能。  
- 出力例：出力ディレクトリは hostベースの構成（例: output/example.com/guide/index.md）とassets管理、manifest.jsonを生成。  
- 性能と挙動：並列ワーカー、スマートなレート制御、永続キャッシュ、ストリーミング処理で大規模サイトにも対応。`--fast`でアセットを省いた高速スキャンが可能。  
- セキュリティ：HTMLのサニタイズ、プロンプトインジェクション検知と隔離、URL検証、ファイルシステムのサンドボックス化で安全性を確保。  
- 運用：CLIはdepth、rate、concurrency、resume、silenceなど多彩なオプション。出力ディレクトリやカスタム設定はdocrawl.config.jsonで管理（CLI優先）。

インストールと簡単な使い方例：
```bash
# インストール
cargo install docrawl

# 例: 浅くクロール
docrawl "https://nextjs.org/docs" --fast

# 例: フルサイト（深さ2）
docrawl "https://react.dev" --depth 2
```

ライブラリとして組み込み（Rust）:
```rust
# rust
#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let cfg = docrawl::CrawlConfig {
        base_url: url::Url::parse("https://example.com/docs")?,
        output_dir: std::path::PathBuf::from("./out"),
        max_depth: Some(3),
        ..Default::default()
    };
    let stats = docrawl::crawl(cfg).await?;
    println!("Crawled {} pages", stats.pages);
    Ok(())
}
```

主要なCLIオプション（抜粋）:
- --depth <n>（デフォルト10）
- --all（サイト全体）
- --output <dir>
- --rate（リクエスト/s）
- --concurrency（同時ワーカー数）
- --selector（カスタムセレクタ）
- --fast / --resume / --silence / --update

## 実践ポイント
- 小さめサイトでまず `--fast` を試し、期待するセレクタで正しくテキスト抽出できるか確認する。  
- CIで定期的にミラーを作るなら `--resume` と低い `--rate` を併用してサーバ負荷を抑える。  
- カスタム選択が必要なら `--selector` や docrawl.config.json に抽出セレクタを設定する。  
- 生成されたYAMLフロントマターやmanifest.jsonを使って静的サイトジェネレータや検索インデックスへ流し込むと効率的。  
- セキュリティ機能で隔離されたページは必ず目視確認してから公開或いは学習データに使うこと。

短時間でドキュメントを整理・移行したい開発チームにとって、docrawlは実務に直結するシンプルかつ安全な選択肢です。
