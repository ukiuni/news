---
layout: post
title: "I used a new go version manager govm - 新しい Go バージョンマネージャ govm を使ってみた"
date: 2026-01-21T03:57:20.408Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/maneeshsagar/govm"
source_title: "GitHub - maneeshsagar/govm"
source_id: 421520751
excerpt: "依存ゼロの単一バイナリで瞬時にGo切替、プロジェクト固定も簡単なgovm"
image: "https://opengraph.githubassets.com/ce35e827fee33425f565c4cc55ce8c1a88685dafc7701f26d1c50c67d0607197/maneeshsagar/govm"
---

# I used a new go version manager govm - 新しい Go バージョンマネージャ govm を使ってみた
面倒なGoのバージョン管理を「依存ゼロ・単一バイナリ」で解決するgovm――手軽に試せるローカル開発の新定番

## 要約
govm は依存関係ゼロの単一バイナリで動作する Go バージョンマネージャ。シンプルなコマンドでバージョン切替やプロジェクト単位の固定ができ、手軽に導入できる点が特徴。

## この記事を読むべき理由
日本でも複数プロジェクトや古いサービスの保守で Go のバージョン差分に悩む場面は多い。複雑なセットアップを避けつつ素早く切り替えたいエンジニアや、社内PCで余計なパッケージを入れられない開発環境を使う人に特に有用。

## 詳細解説
- 目標と設計思想  
  既存の gvm 等は Git/Mercurial/GCC 等の依存が必要で導入が面倒。govm は「単一バイナリ」で依存を持たないことを狙いとしており、インストール後すぐ使えるシンプルさが売り。

- 主な動作原理（shims）  
  govm は go / gofmt などの呼び出しを「shim（小さなラッパースクリプト）」で横取りします。shim はまず以下の優先順位で使う Go バージョンを決定します：  
  1. 環境変数 GOVM_VERSION  
  2. カレントまたは親ディレクトリの .go-version ファイル（プロジェクト指定）  
  3. グローバルデフォルト（~/.govm/version）  
  決定後、該当バージョンの実バイナリを実行します。

- 主要コマンド（使い方）  
  - govm list-remote：入手可能な Go バージョン一覧を表示  
  - govm use <version>：指定バージョンに切替（必要ならインストールも行う）  
  - govm use <version> --local：カレントディレクトリでのローカル固定（.go-version を作成）  
  - govm install <version>：インストールのみ  
  - govm versions：インストール済み一覧表示  
  - govm uninstall <version>：バージョン削除  
  - govm prune：古いバージョンのクリーンアップ

- インストール方法とソースからのビルド  
  手軽に試すなら公式インストールスクリプトを実行：
  ```bash
  curl -fsSL https://raw.githubusercontent.com/maneeshsagar/govm/main/install.sh | bash
  ```
  セキュリティを重視するならリポジトリをクローンして Rust のビルドツールでビルドできます（govm は Rust で実装されています）：
  ```bash
  git clone https://github.com/maneeshsagar/govm.git
  cd govm
  cargo build --release
  ./install.sh
  ```

- アンインストール  
  ~/.govm を削除し、シェルの設定から govm 関連の行を取り除くことでアンインストール可能。

- ライセンス  
  MIT ライセンスのため社内利用やカスタムは比較的自由。

## 実践ポイント
- まずは試す：ローカルで一度インストールして、プロジェクトディレクトリで以下を実行して切替を確認する。
  ```bash
  govm use 1.22.0
  go version
  ```
- プロジェクト固定：チームでバージョンを揃えたいならリポジトリに .go-version をコミットする。CI でも govm をインストールしてそのファイルを読み込めばローカルと同じ環境に。
- セキュリティ注意：curl | bash での即導入は便利だが、内部スクリプトは目で確認してから実行するか、ソースからビルドすることを推奨。
- 制限事項の確認：govm はローカルの shim ベースの切替を想定しているため、Docker イメージ内や特殊な PATH 設定の CI では挙動を検証すること。CI では必要な Go を直接インストールする方が安定する場合もある。
- 保守運用：複数バージョンを長期間使う場合は govm prune で不要なものを整理してディスクを節約する。

短くまとめると、govm は「導入の敷居をグッと下げた Go バージョン管理ツール」。軽量で依存が気になる環境や、素早く試したい場面でまず試す価値がある。
