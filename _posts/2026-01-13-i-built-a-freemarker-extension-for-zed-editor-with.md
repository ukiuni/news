---
layout: post
title: "I built a FreeMarker extension for Zed editor (with tree-sitter grammar) - Zed向け FreeMarker 拡張を作った（tree-sitter 文法で）"
date: 2026-01-13T17:33:58.984Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/debba/zed-freemarker"
source_title: "GitHub - debba/zed-freemarker: Freemarker Template Language support for Zed editor with tree-sitter-based syntax highlighting"
source_id: 427921105
excerpt: "ZedでFTL編集が劇的に快適化—tree-sitterで高精度ハイライトと括弧補完を実現"
image: "https://opengraph.githubassets.com/725d116c884e5623f33f1037c8058f9a627e7f5dd17573aea4905816a28b0f71/debba/zed-freemarker"
---

# I built a FreeMarker extension for Zed editor (with tree-sitter grammar) - Zed向け FreeMarker 拡張を作った（tree-sitter 文法で）
魅力タイトル: ZedでFTLが生き返る！小さな拡張でテンプレート編集が劇的に快適になる理由

## 要約
Zedエディタ向けに、tree-sitterベースの完全なFreeMarker（.ftl）対応拡張が公開されました。構文ハイライトから括弧補完、HTML埋め込みの扱いまでカバーし、将来的なLSP連携も計画されています。

## この記事を読むべき理由
日本ではJavaベースのテンプレート（特に既存の業務システムやECサイト）でFreeMarkerが今も使われています。軽量で高速なZed上でFTL編集を快適にすると、保守性向上やデバッグ時間の短縮に直結します。初学者にも扱いやすい導入方法と、開発者向けのビルド手順が整理されています。

## 詳細解説
- 何ができるか  
  - tree-sitterによる正確な構文解析で、FreeMarkerのディレクティブ（if/else、list、foreach など）や式、コメント形式（角括弧／角かっこ型どちらも）を正しくハイライトします。  
  - HTMLテンプレート内でのハイライト統合、スマートな括弧自動閉鎖、コメントのトグル（Cmd/Ctrl+/）等、日常の編集で役立つ機能を揃えています。

- 技術スタックと設計ポイント  
  - 文法は tree-sitter による独自の grammar（Rust と Node.js を使ってビルド）で定義。これによりパーサが軽量かつ正確に動作します。  
  - Zed の拡張構造（extension.toml や languages/config.toml）に沿ってインストール・公開される設計です。将来的にはLSP連携（補完、定義ジャンプ、参照検索、ホバー）を目指しています。

- 開発者向け情報（要点）  
  - 必要環境：Rust（tree-sitterのネイティブビルド）、Node.js、tree-sitter CLI。  
  - ビルドの流れ（リポジトリをクローン → grammarフォルダで npm install / npm run build → Zed拡張フォルダへコピー）。  
  - テストは tree-sitter test や playground を使って文法を検証します。

## 実践ポイント
- 今すぐ試す（Zedの拡張ギャラリー推奨）：Zedで拡張検索 -> 「Freemarker」 をインストールして .ftl ファイルを開くだけで有効化。  
- 手元で開発版を試す（ローカルインストール例）:
```bash
# リポジトリをクローン
git clone https://github.com/debba/zed-freemarker.git
cd zed-freemarker

# tree-sitter grammar をビルド
cd grammars/freemarker
npm install
npm run build

# Zed の拡張フォルダにコピー（Linux/macOSの例）
cp -r .. ~/.config/zed/extensions/freemarker
```
- 日本の現場での使いどころ：Springや独自フレームワークでFreeMarkerを使っているプロジェクトに導入すると、テンプレートの可読性向上とバグ発見が早まります。既存のFTL大量ファイルを保守する際の効率化に直結します。  
- 貢献のすすめ：LSP対応やスニペット、カスタムディレクティブのサポートは今後の主要な拡張点。日本ユーザー特有のユースケース（社内共通タグ、ローカルビルド手順の改善）でコントリビュートすると役立ちます。

短めのまとめ：Zed上でFTL編集を本気で快適にしたいなら、この拡張はすぐに試す価値あり。開発環境が整っていれば自分でビルドしてカスタマイズするのも簡単です。
