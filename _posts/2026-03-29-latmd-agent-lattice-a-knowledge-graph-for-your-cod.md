---
layout: post
title: "Lat.md: Agent Lattice: a knowledge graph for your codebase, written in Markdown - コードベースの知識グラフをMarkdownで作る（Agent Lattice）"
date: 2026-03-29T12:22:20.280Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/1st1/lat.md"
source_title: "GitHub - 1st1/lat.md: Agent Lattice: a knowledge graph for your codebase, written in markdown. · GitHub"
source_id: 47561496
excerpt: "Markdownでコード知識グラフを作りCIとエージェントで保守するlat.md"
image: "https://opengraph.githubassets.com/ee3535aa8945568950feb740d92e8443f38b62358c7884673e20f9906ab727bf/1st1/lat.md"
---

# Lat.md: Agent Lattice: a knowledge graph for your codebase, written in Markdown - コードベースの知識グラフをMarkdownで作る（Agent Lattice）
ドキュメント地獄を終わらせる：Markdownで作る“読み書きできる”コード知識グラフ、lat.md

## 要約
lat.mdはプロジェクト内にlat.md/というディレクトリを置き、相互リンクされたMarkdownファイルとソース注釈で「コードの知識グラフ」を構築するツールです。リンク検証、検索（ファジー／意味検索）、エージェント連携機能を備え、ドキュメントの陳腐化を防ぎます。

## この記事を読むべき理由
日本でも大規模化するモノレポやリモート開発で「設計意図が埋もれる」問題が深刻です。lat.mdはエンジニアの引き継ぎ・レビュー効率を高め、CIやエディタ連携でドキュメント品質を保てる現実的な手法を提供します。

## 詳細解説
- 基本コンセプト：lat.md/配下に分割したMarkdownセクション（設計、認証、テスト仕様など）をwikiリンク（[[file#Section]]）で結び、ソース側に // @lat: コメント（Pythonなら # @lat:）で実装→概念を紐付ける。  
- スケーラビリティ：単一のAGENTS.mdの代替として、関心ごとにファイルを分けられるため、大規模プロジェクトでも扱いやすい。  
- 検証機能：lat checkでwikiリンクやソース参照の整合性を自動検証し、ドリフトを防ぐ。CIに組み込める。  
- 検索とエージェント：lat searchは埋め込みによる意味検索をサポート（OpenAIキーまたはVercel AI Gatewayが必要）。lat expandなどでエージェント用のコンテキスト展開も可能。  
- CLI例（代表コマンド）:
```bash
npm install -g lat.md
lat init        # lat.md/ をスキャフォールド
lat check       # リンクとコード参照を検証
lat search "how do we auth?"
lat section "auth#OAuth Flow"
```
- 実装注釈例（TypeScript / Python）:
```typescript
// src/auth.ts
// @lat: [[auth#OAuth Flow]]
```
```python
# src/auth.py
# @lat: [[auth#OAuth Flow]]
```
- エディタ連携：MarkdownなのでVS Code/Obsidianでそのまま編集でき、lat CLIやMCPサーバでツールやエージェントと連携可能。

## 日本市場との関連性
- 引き継ぎ・オンボーディングの短縮：新人や外注が増える現場で、設計意図を素早く参照できる。  
- ドキュメント品質が求められる業界（金融・医療・製造）の規格対応や説明責任にも有利。  
- 日本語ドキュメントと混在してもMarkdownベースなので多言語運用が容易。

## 実践ポイント
- まず試す：プロジェクトで `npm install -g lat.md` → `lat init` → 重要なコンポーネントから少しずつ文書化。  
- CIに組み込む：`lat check` をビルドパイプラインに追加してドリフト防止。  
- コードに注釈を入れる：実装箇所に `// @lat:` を付けてトレーサビリティを確保。  
- 意味検索を使う：OpenAIやVercel AIキーを設定して `lat search` を有効化すれば、ドキュメントを自然言語で探索可能。  
- スタイルを決める：セクション命名規則と必須フィールド（例：require-code-mention）をチームで定める。

短時間で価値を出せる導入パスがあり、大規模リポジトリや分散チームの「知識の一元化」に即効性があります。興味があればまず小さなモジュールで試してみてください。
