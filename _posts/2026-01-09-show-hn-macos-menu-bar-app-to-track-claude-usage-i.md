---
layout: post
title: "Show HN: macOS menu bar app to track Claude usage in real time - macOSメニューバーでClaudeの利用状況をリアルタイム表示するアプリ"
date: 2026-01-09T01:46:53.363Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/richhickson/claudecodeusage"
source_title: "GitHub - richhickson/claudecodeusage"
source_id: 46544524
excerpt: "メニューバーでClaudeのAPI使用量をリアルタイム監視し、閾値で警告するmacOSアプリ"
image: "https://opengraph.githubassets.com/5ebcc08358f71ffd4503fd0cbbb176c21206aa22244c5e23963dfe7fe6f35937/richhickson/claudecodeusage"
---

# Show HN: macOS menu bar app to track Claude usage in real time - macOSメニューバーでClaudeの利用状況をリアルタイム表示するアプリ
魅力的なタイトル: 「MacのメニューバーでClaudeのAPI利用を一目管理 — 無駄なコストを防ぐ軽量トラッカー」

## 要約
macOS向け軽量アプリ「Claude Usage」は、メニューバーからAnthropic Claude Codeのセッション／週間利用量をリアルタイムに表示し、色付きインジケータで利用率の危険域を知らせるツール。ローカルでKeychainからOAuth情報を読み取り、利用APIを叩く設計。

## この記事を読むべき理由
Claude（Anthropic）のAPIを使う開発者やコスト管理が必要なチームにとって、手元で簡単に利用状況を監視できるツールは即効性が高い。macOSを使う日本のエンジニアやデザイナーにとって導入ハードルが低く、無駄な課金防止や運用の可視化に役立つ。

## 詳細解説
- 主要機能
  - メニューバー表示でセッションと週次の使用量を同時表示
  - 2分ごとに自動更新（手動リフレッシュも可）
  - 色分けステータス：緑 (OK)、黄 (>70%)、赤 (>90%)
  - リセットまでの残り時間表示
  - ネイティブSwiftで軽量に動作

- 技術的なポイント
  - macOS KeychainからClaude CodeのOAuth資格情報を読み取り、Anthropicの利用状況エンドポイントに問い合わせる
  - 利用APIエンドポイント: api.anthropic.com/api/oauth/usage（非公開仕様のAPIを利用しているため将来的に変わる可能性あり）
  - 要件: macOS 13.0 (Ventura) 以降、Claude Code CLIがインストール済みでログインされていること
  - オープンソース（MITライセンス）なのでコードを確認・改造可能

- インストールとビルド
  - リリースからClaudeUsage.zipをダウンロードしてApplicationsに移動して起動
  - ソースからビルドする場合:
```bash
git clone https://github.com/richhickson/claudecodeusage
cd claudecodeusage
open ClaudeUsage.xcodeproj
# Xcodeで⌘B、実行は⌘R
```
  - Claude CLIの導入:
```bash
npm install -g @anthropic-ai/claude-code
claude   # 初回はログインフローを完了する
```

- プライバシーと注意点
  - 資格情報はローカルKeychainからのみ読み取られ、アプリ自体はAnthropic以外にデータを送らない（テレメトリ無し）
  - ただし「非公開API」を利用しているため、Anthropic側の変更で動作が停止するリスクあり。運用時はその点を考慮すること。

## 実践ポイント
- 今すぐ試す手順
  1. Claude CLIをインストールして `claude` を実行、ログインする
  2. GitHubのReleasesからClaudeUsage.appをダウンロードしてApplicationsへ
  3. 起動してメニューバーに常駐させ、2分ごとの自動更新で利用状況を確認

- 運用上の活用例
  - API利用課金が気になるプロジェクトで逐次監視し、閾値（70%/90%）に達したらアラートや利用制限を掛ける運用ルールを作る
  - チームでの推奨ツールとして配布し、各自のKeychain認証で安全に使わせる
  - 同様の仕組みを社内でカスタム実装（SwiftUIやElectronなど）する際のサンプルとして参照

- トラブルシュート（よくある事例）
  - 「Not logged in to Claude Code」→ ターミナルで `claude` を実行して再ログイン
  - メニューバーに出ない→ Activity Monitorでアプリが動作しているか確認して再起動
  - 数値が古い/おかしい→ ドロップダウンの↻を押す、ダメなら再ログイン（セッション切れの可能性）

最後に一言：非公式ツールである点と非公開API利用のリスクを理解した上で、まずはローカル環境で試し、費用管理やデバッグの効率化に役立てるのが現実的な使い方。
