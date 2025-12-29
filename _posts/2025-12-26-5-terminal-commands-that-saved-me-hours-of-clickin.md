---
layout: post
title: 5 Terminal Commands That Saved Me Hours of Clicking
date: 2025-12-26 03:59:51.972000+00:00
categories:
- tech
- world-news
tags:
- tech-news
- japan
source_url: https://dev.to/maame-codes/5-terminal-commands-that-saved-me-hours-of-clicking-4mfn
source_title: 5 Terminal Commands That Saved Me Hours of Clicking - DEV Community
source_id: 3114994
---
# クリック地獄から解放される5つのターミナル技—マウス依存を一気に断つ方法

## 要約
GUIでの無駄なクリックを減らし、作業速度と正確性を劇的に上げるターミナルの五つの基本コマンドを実例とともに解説する。

## この記事を読むべき理由
プロジェクト作成・ファイル操作・検索といった日常タスクを短いコマンドで終わらせることで、日本の現場でも生産性向上とタイムログ削減に直結するため。

## 詳細解説
- 1) テレポートする感覚: cd + Tab補完  
  Terminal:
  ```bash
  # フォルダ名の先頭だけ入力してTabで補完
  cd ~/Doc[TAB]/Proj[TAB]/web-app
  ```
  解説: cdでディレクトリ移動。Tab補完を使えば深い階層をクリックで辿る必要がなく、タイプ数と時間を劇的に削減できる。

- 2) 一発でディレクトリ構造を作る: mkdir -p とブレース展開  
  Terminal:
  ```bash
  mkdir -p my-app/{src/components,assets,tests}
  ```
  解説: `-p` は親ディレクトリもまとめて作成。ブレース展開 `{a,b}` を組み合わせれば、複数のサブフォルダを一行で生成できる。テンプレートプロジェクト作成がすばやく行える。

- 3) 保険をかけてコピー: cp -r（再帰コピー）  
  Terminal:
  ```bash
  # ディレクトリを丸ごとコピー（上書きに注意）
  cp -r original_project backup_project
  ```
  解説: GUIでフォルダをドラッグするより迅速。大きなフォルダを丸ごと複製するときに有効。重要ファイルのバックアップを自動化するスクリプトにも組み込みやすい。

- 4) 名前の移動・整理は一行で: mv と -v（詳細表示）  
  Terminal:
  ```bash
  # ファイルやディレクトリの移動・リネーム
  mv -v src/old_component.js src/components/new_component.js
  ```
  解説: GUIで切り取り→貼り付けする操作をコマンドで一発に。`-v` を付ければ何がどう変わったかログが出るためCIスクリプトやデプロイ前の確認にも便利。

- 5) プロジェクト全体を素早く検索: grep -R / ripgrep (rg) の利用  
  Terminal:
  ```bash
  # grepで再帰検索（出力を絞る）
  grep -Rn "TODO" ./my-app

  # もし導入済みならripgrepは高速
  rg "TODO" ./my-app
  ```
  解説: GUIの検索は遅く、設定が面倒。`grep -R` や `rg`（ripgrep）を使うと大規模リポジトリでも高速に文字列を見つけられる。正規表現や行番号オプションで精度を高める。

## 実践ポイント
- Tab補完は設定不要。まずは意識して使い、筋肉記憶にする。  
- プロジェクト初期化スクリプトに `mkdir -p` とブレース展開を組み込むと新人教育の時間が削減できる。  
- コピーや移動はスクリプト化してログを残す（`-v`、`--backup` 等）。誤操作のリスク管理につながる。  
- 大規模検索には ripgrep（rg）を導入すると体感速度が大幅向上。パイプで `less -R` と組み合わせて使う。  
- VS Codeユーザならターミナルを統合して、ショートカット（Ctrl+`）で即利用できるように習慣化する。

