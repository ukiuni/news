---
layout: post
title: "nix-run: run nix derivations without nix3 or flakes - nix3やflakesなしでNix派生を実行するnix-run"
date: 2026-02-06T11:54:21.103Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://tangled.org/weethet.bsky.social/nix-run"
source_title: "nix-run: run nix derivations without nix3 or flakes"
source_id: 1288120416
excerpt: "Nix3やflakes不要で既存CIに導入できる軽量なnix run代替"
---

# nix-run: run nix derivations without nix3 or flakes - nix3やflakesなしでNix派生を実行するnix-run
古いNix環境やflakes非対応のプロジェクトでも使える、シンプルで安定した「nix run」代替ツール

## 要約
nix-runは、Nix3やflakesに依存せずにNixのderivation（パッケージ/アプリ）を実行できる軽量ツール。Haskellで実装され、既存のNixワークフローに無理なく導入できるのが特徴です。

## この記事を読むべき理由
日本の現場では企業ポリシーや既存CIで最新のNix/flakesを導入できないケースが多く、互換性のある代替手段は実務的価値が高い。nix-runはそうした制約下でも「nix run」相当の操作を提供します。

## 詳細解説
- 目的：Nix3やflakesに依存せずに、Nix表現（ファイル、attr、式、パッケージ名など）からアプリケーションをビルドして実行する。  
- 実装：Haskellで書かれており、シンプルなCLIを提供。READMEにあるようにリポジトリはクローン可能で、自己ホスト型の環境（Tangledなど）にも対応します。  
- 主な入力形態：ファイルパス、Nix式（-E）、属性パス（-A）、パッケージ名（-p）など複数をサポート。meta.mainProgramを参照するか、--binaryで実行バイナリ名を指定可能。  
- ビルド制御：並列数（-j/--max-jobs）、コア数、タイムアウト、出力抑制（-Q）やログフォーマット指定など、ビルド挙動を細かく制御できる。  
- フォールバックと修復：--fallbackで置換（substitute）が失敗した際にローカルビルドへフォールバック、--repairで壊れたストアパスの再取得や再ビルドを試みるなど運用向け機能を備える。  
- 開発／CI向け：--checkで検証ビルド、--keep-goingや--keep-failedで失敗時の挙動を調整可能。ログや静粛モードもあるためCI統合しやすい。

## 実践ポイント
- リポジトリをクローンして試す：
```bash
git clone https://tangled.org/weethet.bsky.social/nix-run
```
- よく使う例：
```bash
# パッケージ名で実行
nix-run -p hello

# 属性を選んで実行
nix-run -A myPackage

# Nix式を直接評価して実行
nix-run -E 'with import <nixpkgs> {}; hello'
```
- 日本の現場での活用提案：
  - 古いNix環境やflake未導入レポジトリのCIに組み込み、段階的に移行するブリッジとして導入する。  
  - ネットワーク制限下でのビルド運用（--repairや--fallback）やログ制御を活かして安定運用を図る。  

必要なら、導入手順やCIへの組み込み例（GitHub Actions / self-hosted runner向け）を簡潔に作成しますか？
