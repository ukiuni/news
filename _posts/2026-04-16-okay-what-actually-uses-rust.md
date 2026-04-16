---
layout: post
title: "Okay, what actually uses Rust - Rustは実際にどこで使われているのか"
date: 2026-04-16T21:20:40.233Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://blog.goose.love/posts/what-actually-uses-rust/"
source_title: "Ok, what ACTUALLY uses Rust? | BLOG.GOOSE.LOVE"
source_id: 1328629456
excerpt: "Linuxカーネルからクラウド・WASMまで、実運用で採用されるRust事例と導入の要点"
---

# Okay, what actually uses Rust - Rustは実際にどこで使われているのか
いま本当に「現場」で使われているRust——業界の主要プロジェクトから学ぶ実用性

## 要約
近年Rustは研究的関心から実運用へ移行しており、OSカーネル、ブラウザ、クラウド、開発ツール、WASMなど幅広い分野で採用例が増えている。

## この記事を読むべき理由
Rustの「話題性」だけでなく、実際にどの大手プロジェクトや企業が生産環境で使っているかを知ることで、日本のプロダクト開発やレガシー置換・安全性向上の判断材料になるため。

## 詳細解説
- OS・低レイヤ：Linuxカーネルは6.1以降でRustを受け入れ（6.19で安定採用）、coreutilsの書き直しやRedoxのような実験的OSも存在する。メモリ安全が求められる領域で注目される。
- ブラウザ・レンダリング：Servo（Mozilla発）や、ChromiumへRust統合の動き、Firefoxの一部コンポーネント採用など、レンダリングやセキュリティ重視の領域で使われる。
- クラウド・インフラ：AWS（Lambda/Firecracker）、Cloudflare、Microsoft、Appleのクラウド/サーバー周りで採用実績。政府機関（NSAやホワイトハウス）もメモリ安全の観点からRustを推奨している。
- 開発ツール・言語エコシステム：ripgrep（高速grep）、swc（JSコンパイラ／バンドラ）、ruff（Pythonリンター）、turborepo、Denoなど、ビルドやツールチェーンの高性能実装に使われる例が多い。
- アプリ・デスクトップ：Tauri（Electron代替）、Zed（エディタ）、Alacritty（端末）など、ユーザー向けアプリでも採用が進む。
- ゲーム・マルチメディア・その他：DiscordがGoからRustへ一部移行、Valve Protonにも利用。WASMターゲットとしてはRustが人気で、Web向け高速処理に貢献している。
- AI・ブロックチェーン・検索：Meilisearch、各種AI／ブロックチェーン実装など、性能や安全性が重要な新領域でも採用が増えている。

## 実践ポイント
- 小さく試す：まずはripgrepやruffなど既存のRust製ツールを導入して体感する。  
- レガシー置換は段階的に：性能や安全性が必要なモジュール単位でRustに置き換える。FFIで既存コードと共存可能。  
- WASM活用：フロントエンドの計算負荷を下げたいならRust→WASMを検討する。  
- 学習リソース：所有するプロジェクトのCIにClippyやMIRツールを入れて、借用チェッカーに慣れる。  
- コミュニティ活用：国内外の事例（Linux、AWS、Cloudflareなど）を調査し、実運用でのトレードオフを学ぶ。

以上。この記事で挙げた領域を起点に、自社の課題（性能・安全・運用性）に合う使いどころを検討してみてください。
