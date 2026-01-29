---
layout: post
title: "Looi — A Minimal, Customisable New Tab page for Firefox, Chrome(with Widgets & GitHub Sync) - Looi — 最小限でカスタマイズ可能な新しいタブページ（ウィジェット＆GitHub同期）"
date: 2026-01-29T15:58:36.562Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/prinzpiuz/looi"
source_title: "GitHub - prinzpiuz/looi: A Minimal, Customisable New Tab page for Firefox, Chrome, and Edge."
source_id: 919965989
excerpt: "Looi：GitHub同期で設定共有できる軽量ウィジェット新タブ"
image: "https://repository-images.githubusercontent.com/1026031526/60da93de-eead-400f-b59f-52ceb730733a"
---

# Looi — A Minimal, Customisable New Tab page for Firefox, Chrome(with Widgets & GitHub Sync) - Looi — 最小限でカスタマイズ可能な新しいタブページ（ウィジェット＆GitHub同期）
新しいタブが“ただの白紙”から、シンプルで拡張可能な個人ダッシュボードに変わる — 開発者にも一般ユーザーにも使いやすい軽量拡張

## 要約
LooiはTypeScriptで作られた軽量な新しいタブ拡張で、カレンダー・ToDo・速度チェック・ブックマーク等のウィジェットを備え、設定をGitHubで同期できる。Chrome/Firefox/Edgeに対応し、カスタマイズ性とシンプルさを両立している。

## この記事を読むべき理由
日本ではブラウザの新しいタブを生産性向上や個人ダッシュボードに活用したいユーザーが増えている。Looiは軽量でプライバシー配慮しやすく、開発者向けにソースが公開されているため職場や個人利用での導入・カスタマイズがしやすい。

## 詳細解説
- 主要機能  
  - ウィジェット：カレンダー、To-Do、スピードチェッカー、ブックマークなど必要最小限のパーツを提供。  
  - カスタマイズ：表示のオンオフやレイアウト調整で自分好みに簡単に変更可能。  
  - GitHub同期：設定をGitHub上で同期・バックアップでき、複数環境で同じ設定を使える（ローカルのみの利用も可能）。  
- 技術スタックと配布方法  
  - 実装は主にTypeScript（約77%）＋CSSで管理され、オープンソース（GPL‑3.0）。  
  - ローカル開発はnpmベースで、開発用サーバ起動とビルドスクリプト（Firefox/Chrome向けビルド）が用意されている。  
- セキュリティ／ライセンスの観点  
  - GPL‑3.0のため派生配布時は同じライセンスでの公開義務が生じる点に注意。  
  - GitHub同期は利便性が高いが、設定をクラウドに置くため機密情報は避けること。

## 実践ポイント
- 試しに動かす（ローカル開発）:
```bash
# リポジトリをクローンして依存を入れ、開発サーバ起動
git clone https://github.com/prinzpiuz/looi
cd looi
npm install
npm run start
```
- 本番ビルドとブラウザへの読み込み:  
  npm run build:chrome / npm run build:firefox を実行し、出力をブラウザの開発者モードで「拡張機能の読み込み（アンパック）」で読み込む。  
- カスタマイズと運用のコツ  
  - CSSやウィジェット設定を編集して自分用ダッシュボードを作成。  
  - 設定のバックアップや複数端末同期はGitHubに任せるが、トークンや個人情報は含めない。  
  - 日本語化やローカルのカレンダー連携など、ニーズに応じてフォークして拡張すると実用性が高まる。

興味がある場合はGitHubリポジトリをチェックして、ローカルで起動 → 小さなカスタマイズから始めることをおすすめする。
