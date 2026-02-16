---
layout: post
title: "Show HN: Simple org-mode web adapter - シンプルな org-mode ウェブアダプター"
date: 2026-02-16T17:21:58.915Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/SpaceTurth/Org-Web-Adapter"
source_title: "GitHub - SpaceTurth/Org-Web-Adapter: A simple view into your org roam notes with editing, backlinks, and rendered math."
source_id: 47036891
excerpt: "単一PythonでローカルOrgをブラウザ閲覧・編集、バックリンクと数式対応"
image: "https://opengraph.githubassets.com/e1c7e89d06404057a5cbbb57444afb3492265a325b77f186e05f208d6e28eeaa/SpaceTurth/Org-Web-Adapter"
---

# Show HN: Simple org-mode web adapter - シンプルな org-mode ウェブアダプター
ローカルのOrg/Org-roamノートをブラウザでサクッと閲覧・編集――最小構成の「Org Web Adapter」

## 要約
Python単一ファイルのローカルWebサーバが、.orgファイルを再帰スキャンして3ペインで表示・編集・バックリンク表示やMathJaxによる数式レンダリングを提供する軽量ツール。

## この記事を読むべき理由
Emacs/Org-modeやOrg-roamでメモ管理しているエンジニアや研究者は多く、日本でも「ローカルで完結する知識基盤」を求める現場が増加中。クラウドに上げずブラウザベースで手軽に閲覧・編集できる点は、社内ナレッジや研究ノートの運用で即戦力になる。

## 詳細解説
- 構成: main.py（サーバ兼パーサ）、templates/index.html（UI＋クライアントJS）、static/style.css（レイアウト）。notesディレクトリ（symlink可）をスキャンして動作する。
- 動作: GET / の度にノートを再スキャン。見出し（*、**…）や段落を簡易にHTML化し、{{NAV_ITEMS}}/{{MAIN_CONTENT}}/{{BACKLINKS}}に注入。クライアント側JSで検索・ソート・シャッフル・テーマ切替を担当。
- リンク処理: file: と id: を解決する resolve_link_target()、逆参照を探す find_backlinks()、バックリンク集計の build_backlink_counts() を備えるため、Org-roamライクな参照関係がブラウザで追える。
- 編集: POST /edit でブラウザからファイルを書き換え。保存成功/失敗のステータス表示あり。
- 数式: MathJax（CDN）で $...$ をレンダリング。オフラインで使うならローカルに置く必要あり。
- 設定と起動: config.yaml（bind_addr, bind_port、デフォルト127.0.0.1:8000）。CLIフラグ --host/--port/--config/--dir で上書き可。実行例: python3 main.py --dir notes
- セキュリティと制約: 認証・暗号化は無し（信頼できるネットワークでのみ使用）。本格的なOrgパーサではなく、簡易レンダリング。大量ノートでは毎リクエスト再スキャンが非効率。
- ライセンス: AGPL-3.0。コードは小さくフォークやカスタマイズが容易。

## 実践ポイント
- すぐ試す: notesディレクトリを用意（または既存Org-roamディレクトリを symlink）、python3 main.py --dir notes で起動。ブラウザで確認。
- ネットワーク注意: 公開サーバにしない。社内LANやローカルで使うこと。必要ならリバースプロキシ＋認証を追加する。
- カスタマイズ案: MathJaxをローカル配布、Orgレンダラの精度向上（リンク・表・リスト対応）、検索インデックス化で大規模ノート対応へ拡張しやすい。
- バックアップ運用: ブラウザ編集でファイルを直接変更するため、運用前にGitや別フォルダでのバックアップを確保する。
- コントリビュートしやすい: 実装が小規模なので、必要機能（認証、差分保存、パフォーマンス改善）を自分で追加して公開するハードルが低い。

元リポジトリ: https://github.com/SpaceTurth/Org-Web-Adapter
