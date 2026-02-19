---
layout: post
title: "Show HN: Ghostty-based terminal with vertical tabs and notifications - Ghosttyベースのターミナル（縦タブ＋通知付き）"
date: 2026-02-19T22:12:02.511Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/manaflow-ai/cmux"
source_title: "GitHub - manaflow-ai/cmux: Ghostty-based macOS terminal with vertical tabs and notifications for AI coding agents"
source_id: 47079718
excerpt: "縦タブ・通知リングで複数AIエージェントの応答待ちを一目で把握できる高速軽量macOS端末"
image: "https://opengraph.githubassets.com/f234bebbe1d0a84b96aad9ec85b43a7bef230d2eaafdbf5bedd31752294aa4c1/manaflow-ai/cmux"
---

# Show HN: Ghostty-based terminal with vertical tabs and notifications - Ghosttyベースのターミナル（縦タブ＋通知付き）

魅せるターミナル — macOSネイティブでAIエージェントの「待ち」を一目で分かるcmux

## 要約
cmuxはGhosttyレンダリングを使ったmacOSネイティブ端末アプリで、縦型タブ・通知リング・スクリプタブルなブラウザを備え、複数のAIコーディングエージェントの管理を高速かつ視覚的に行えます。

## この記事を読むべき理由
- Macで複数のAIエージェントやターミナル分割を扱う開発者にとって作業見通しが劇的に改善されるため。  
- Electron系ツールより軽く起動が速く、既存のGhostty設定（テーマ/フォント）もそのまま使える点は日本のMacユーザーに刺さります。

## 詳細解説
- ネイティブ実装：Swift + AppKitで構築。Electron/Tauriより低メモリ・高速起動を目指している。  
- Ghostty互換：libghosttyでGPUアクセラレーションされた滑らかな端末描画。既存の~/.config/ghostty/configを読みテーマ/フォントを継承。  
- 縦タブ＋サイドバー：ワークスペースごとに縦タブ表示。各タブはgitブランチ、作業ディレクトリ、リッスン中ポート、直近通知の概要を表示。  
- 通知システム：ターミナルの特殊シーケンス（OSC 9/99/777）や付属のCLI（cmux notify）経由で通知を拾い、該当ペインに青いリングやタブのハイライトで可視化。Cmd+Shift+Uで未読にジャンプ。これにより「どのエージェントが応答待ちか」が一目で分かる。  
- スクリプタブルブラウザ：agent-browser由来のAPIでアクセシビリティツリーのスナップショット、要素参照、クリック、フォーム入力、JS評価が可能。端末横にブラウザをスプリットして、AIが開発中のサーバと直接やり取りするワークフローを作れる。  
- 自動化API：CLIとソケットAPIでワークスペース作成、分割、キーストローク送信、URLオープンなどを制御可能。  
- インストール：公式DMGまたはHomebrew cask。AGPL-3.0ライセンス。

## 実践ポイント
- まずはDMGかbrewでインストールして普段のGhostty設定を読み込ませるだけで即導入可能。  
- Claude Code等のエージェントにcmuxのCLI通知フック（cmux notify）を組み込み、エージェント待ちの視認性を確保する。  
- ブラウザ分割＋スクリプトAPIを使えば、AIにローカル開発サーバ上で操作させるプロトタイプ自動化が簡単に試せる。  
- 企業利用時はAGPLの影響（派生物の公開義務など）を法務と確認すること。

興味があれば公式リポジトリ（https://github.com/manaflow-ai/cmux）をチェックして、リリースとショートカット一覧を確認してみてください。
