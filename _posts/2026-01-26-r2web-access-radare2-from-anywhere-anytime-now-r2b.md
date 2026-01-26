---
layout: post
title: "R2web: Access radare2 from anywhere, anytime. Now r2become more easier to be accessible than before, no local installation required use it anytime, anywhere from any device - ブラウザで動くradare2「r2web」を今すぐ試すべき理由"
date: 2026-01-26T04:39:50.569Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/radareorg/r2web"
source_title: "GitHub - radareorg/r2web: Access radare2 from anywhere, anytime."
source_id: 418592996
excerpt: "ブラウザでradare2が動く！インストール不要で即解析できるr2web"
image: "https://opengraph.githubassets.com/60e8832a43aae6d6e03aa4d9dec035fc82f039951d753f046edfa9dfd1ce3b25/radareorg/r2web"
---

# R2web: Access radare2 from anywhere, anytime. Now r2become more easier to be accessible than before, no local installation required use it anytime, anywhere from any device - ブラウザで動くradare2「r2web」を今すぐ試すべき理由

魅力的な一言タイトル：ブラウザだけで逆アセンブルと解析ができる時代が来た — r2webでどこでもradare2

## 要約
r2webはradare2をWASM/WASI上でブラウザ実行するフロントエンドで、ローカルインストール不要でバイナリ解析をどのデバイスからでも行えるようにするプロジェクトです。

## この記事を読むべき理由
日本でも組込み・ファームウェア解析、セキュリティ教育、インシデント対応の現場で手軽に使えるツールが求められています。r2webは環境構築のハードルを下げ、BYODや共有端末でも解析ワークフローを始められる点で価値があります。

## 詳細解説
- 実行環境：radare2はr2wasmとしてWASMバイナリ化され、Wasmer（WASIサポート）でブラウザ上で動作。フロントはReact + TypeScript + Vite、端末表示はxterm.jsを採用しており、インタラクティブにr2コマンドを実行できます。  
- クロスプラットフォーム：モダンブラウザがあればWindows/Mac/Linux/タブレット/スマホから利用可能。ただしWASI/WASM未対応の古いブラウザや、Firefoxでの既知問題があります。安定性はChromium系（Chrome/Edge/Brave）で良好。  
- 機能面：端末インターフェース、ショートカット（例：Ctrl+Gでシーク）、大出力の検索、グラフ表示、pd/px/iz等のコマンドボタンなど。グラフ表示やファイル保存はradare2のバージョン依存（保存は≥6.0.3、グラフは≥6.0.9）。  
- バイナリ取得とキャッシュ：初回アクセス時にradare2のWASMバイナリをダウンロードしローカルにキャッシュ可能。プライバシーやディスクを気にする場合はキャッシュ無効化オプションあり。  
- 開発とデプロイ：ローカル起動はリポジトリをクローン後、bun（またはnpm/yarn）で依存を入れ bun dev で起動。ブラウザのCORS回避のために小さなプロキシ（api/wasm.cjs）を立てる必要あり（proxyは複数バージョン対応時のみ必須）。本番ビルドは bun run build、サブディレクトリ配信時は VITE_BASE_URL を設定。静的ホスティング（GitHub Pages/Netlify/Vercel等）推奨。  
- 開発ポリシー：依存を極力減らす方針。外部UIボイラープレートを避ける設計。

## 実践ポイント
- まずはデモサイト（r2.revengi.in）で触ってみる。  
- Chromium系ブラウザで利用する。Firefoxで問題が出たらブラウザ切替を検討。  
- 必要機能（保存／グラフ）が使えるかはradare2のバージョン要件を確認する（保存≥6.0.3、グラフ≥6.0.9）。  
- ローカルで動かす場合：git clone → bun install（またはnpm/yarn）→ bun dev、プロキシは api/wasm.cjs を起動。  
- 公開するなら静的ホスティング＋VITE_BASE_URLの設定でサブパス配信に対応。  
- プライバシー重視ならキャッシュ無効化オプションを使う。  
- 日本の教育機関やセキュリティチームでは、OSやツールチェーンを揃えずに短期間でワークショップを開ける利点がある。

興味があればリポジトリをチェックして、必要なr2バージョンやブラウザ互換性を確認してみてください。
