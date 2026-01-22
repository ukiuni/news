---
layout: post
title: "Playdate supports Go language. Compiler, SDK Bindings, Tools and Examples ⚒️ - PlaydateがGo言語をサポート。コンパイラ、SDKバインディング、ツール、サンプルを公開"
date: 2026-01-22T18:35:15.005Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://devforum.play.date/t/playdate-supports-go-language-compiler-sdk-bindings-tools-and-examples/24919"
source_title: "Golang support for Playdate. Compiler, SDK Bindings, Tools and Examples ⚒️ - Playdate Developer Forum"
source_id: 421531126
excerpt: "実機でGopher描画！PdGoでPlaydateをGoで開発、コンパイラ・SDK・サンプル公開"
image: "https://devforum-cdn.play.date/optimized/3X/d/5/d5988954ce5ccff2ea223d37b9bf764c33aaadd9_2_768x1024.jpeg"
---

# Playdate supports Go language. Compiler, SDK Bindings, Tools and Examples ⚒️ - PlaydateがGo言語をサポート。コンパイラ、SDKバインディング、ツール、サンプルを公開

Playdateで「Go（Golang）」が使える！かわいいGopherが実機に描画された初公開リリース。

## 要約
Playdate向けのオープンソースプロジェクト「PdGo」が公開され、GoでPlaydate向けゲーム・ツールを書けるコンパイラ、SDKバインディング、ツール類、サンプルが揃っています。

## この記事を読むべき理由
日本でもインディーゲーム／ハードウェア愛好者やGoを主戦力にする開発者が増えています。慣れた言語でPlaydateを触れることで、プロトタイプ作成や小規模ゲーム開発の敷居が下がります。

## 詳細解説
- PdGoはGo言語からPlaydate向けバイナリへ変換するためのツール群とSDKバインディングを提供します。公式サポート言語だったLua・C（後にSwift/Rust/Nimも登場）に続く選択肢です。  
- リポジトリにはコンパイラ周りの実装（ラッパー／ツールチェーン）、Playdate APIへのバインディング、動作確認用のサンプルが含まれており、実機でGopherが描画されるなど実用段階の成果が報告されています。  
- READMEにHow‑to、APIドキュメント、ツール内部の解説がまとまっており、導入〜デバッグの手順が参照できます。プロジェクトはまだ開発中ながら第一公開版として公開済みです。

## 実践ポイント
- リポジトリを取得してREADMEを読み、サンプルを動かすのが最短の入門方法：
```bash
git clone https://github.com/playdate-go/pdgo
cd pdgo
# READMEの手順に従ってセットアップ・サンプル実行
```
- 日本の小規模チームや個人開発者は、Goでの素早いプロトタイプ→Playdate実機検証のワークフローを試してみてください。問題やフィードバックはリポジトリやPlaydate開発フォーラムに投稿するとコミュニティ貢献になります。
