---
layout: post
title: "Show HN: A Unix environment in a single HTML file (420 KB) - 単一HTMLファイルで動くUnix環境（420KB）"
date: 2026-02-18T16:58:11.216Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://shiro.computer/show"
source_title: "Shiro — A Unix environment in one HTML file"
source_id: 47062726
excerpt: "420KB単一HTMLでオフライン動作するブラウザ内Unix環境、npmやgitも完備で即配布可能"
image: "https://shiro.computer/og.png"
---

# Show HN: A Unix environment in a single HTML file (420 KB) - 単一HTMLファイルで動くUnix環境（420KB）
驚きの「ブラウザだけで動くUnix環境」が1ファイルで完結する理由

## 要約
420KBの自己完結HTMLで、シェル・ファイルシステム・git・npm・viなど200+コマンドをブラウザだけで動かせるプロジェクト。IndexedDBで永続化し、サーバー不要でオフライン動作する点が特徴。

## この記事を読むべき理由
日本の開発現場や教育現場で「手軽にデモ・ワークショップ・検証環境を配布」したいとき、ブラウザだけで完全再現できる手段は非常に有用。社内ネットワークやChromebook環境でも即座に試せます。

## 詳細解説
- アーキテクチャ
  - 単一の自己完結HTMLにJS/CSSが埋め込まれ、配布はGitHub PagesやS3などどこでも可能。約420KB（gzipped）。
  - ファイル保存はIndexedDBを使い、POSIXライクなAPI（stat, readdir, readFile, writeFile, mkdir, symlink, chmod, glob）を提供。ページを再読み込みしてもファイルが残る。
- シェル機能
  - パイプ、リダイレクト、環境変数、&& / ||、クォーティング、ヒアドキュメントなど、実用的なPOSIX互換性を実装し、スクリプトが動くレベル。
- パッケージと実行
  - 実際のnpmタールボールを利用してnodeモジュールをインストール可能。node互換の実行系やesbuildによるTypeScriptバンドルも動作。require()はnode_modulesを解決する。
- git対応
  - isomorphic-git等を用いてローカルでinit/add/commit/diffなどのGit操作を完全クライアント側で実行できる（サーバ不要）。
- 便利な機能
  - ファイルシステム全体をGIFにスナップショットして別インスタンスへドラッグで復元するユニークなエクスポート/インポート機構。
- セキュリティと制約
  - ブラウザ沙汰のサンドボックス内で動作するため、ネイティブシステムのリソースには直接触れない。重いビルドや長時間プロセスはブラウザ依存の制約あり。

## 実践ポイント
- まずは試す: shiro.computer（またはGitHubリポジトリ）を開いて、`npm init -y` → `npm install` → `node` → `git init` の流れをブラウザで体験してみる。
- 教育／ワークショップで活用: インターネット接続不要で配れる教材イメージとして最適（Chromebookやネットワーク制限下でも動作）。
- デモ配布: 420KBの単一ファイルなのでGitHub PagesやS3に置くだけで配布可能。オフライン配布用にGIFスナップショットを作っておくと再現性が高い。
- ソース確認: 実装はオープンなので、コマンド実装やIndexedDBの抽象化を学ぶ教材としても有用。
