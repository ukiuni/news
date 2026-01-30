---
layout: post
title: "cli-stash: TUI tool to save and recall shell commands - シェルコマンドを保存・再呼び出しするTUIツール"
date: 2026-01-30T17:32:04.670Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/itcaat/cli-stash"
source_title: "GitHub - itcaat/cli-stash: Terminal UI for saving and recalling shell commands"
source_id: 690189687
excerpt: "TUIでファジー検索→即プロンプト挿入、コピペ不要のコマンド備忘庫"
image: "https://opengraph.githubassets.com/0fe1be863fcd7e3c490d794a3c757f581727e52db948abeef66230f026c88186/itcaat/cli-stash"
---

# cli-stash: TUI tool to save and recall shell commands - シェルコマンドを保存・再呼び出しするTUIツール
もうコピペ不要！キーボードだけで過去コマンドを検索・挿入する「コマンド備忘庫」

## 要約
cli-stashはBubble Teaで作られたターミナルUIツールで、シェル履歴や保存したコマンドをファジー検索し、選んだコマンドを即座にプロンプトへ挿入できます。使用頻度で自動ソートされ、日常のコマンド作業を高速化します。

## この記事を読むべき理由
- 毎日ターミナルを使う日本の開発者・運用担当者が、単純作業（複雑なコマンドのコピペや履歴探索）を劇的に短縮できるため。  
- VS Code等の統合端末とも相性が良く、ローカル作業効率が上がる実用ツールだから。

## 詳細解説
- 実装と依存：Go製、TUIはBubble Teaを利用。macOS/Linux向けにHomebrewパッケージやGoからのインストールが可能。  
- 主要機能：
  - 保存：Ctrl+Aでシェル履歴を参照して保存。
  - 検索：リアルタイムのファジー検索で目的のコマンドを素早く絞り込める。
  - ソート：利用頻度が高い順に表示（Smart sorting）。
  - 挿入：Enterで選択したコマンドがターミナルプロンプトに挿入される（実行前に編集可）。
  - 削除：Ctrl+Dで保存コマンドを削除。
- キーバインド（主なもの）：↑/↓（移動）、Enter（選択/保存）、Ctrl+A（履歴から追加）、Ctrl+D（削除）、Esc（キャンセル）。
- ストレージ：保存データは ~/.stash/commands.json に格納されるためバックアップや共有が容易。
- 安全性と運用：コマンドは挿入されるだけで即実行されないので、実行前に編集・確認可能。秘匿情報を扱うコマンドは保存に注意。

## 実践ポイント
- インストール例：
```bash
brew install itcaat/tap/cli-stash
```
または
```bash
go install github.com/itcaat/cli-stash@latest
```
- 起動：
```bash
cli-stash
```
- まずはCtrl+Aで履歴からよく使うコマンドを保存し、ファジー検索→Enterで挿入→編集→実行、の流れを試して習慣化する。  
- ~/.stash/commands.json を定期的にバックアップ／チームで共有すれば、共通の運用スニペット集として活用できる。  
- VS Codeの統合ターミナルで使えば、エディタ作業から離れずにコマンドを再利用できる点が便利。

以上。試してみて、よく使うコマンド群を「備忘庫」にしてみてください。
