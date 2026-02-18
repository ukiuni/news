---
layout: post
title: "Show HN: Echo, an iOS SSH+mosh client built on Ghostty - Echo：Ghosttyを活用したiOS向けSSHクライアント"
date: 2026-02-18T19:14:56.108Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://replay.software/updates/introducing-echo"
source_title: "Introducing Echo — Replay Software"
source_id: 47064787
excerpt: "外出先でAIエージェントやtmuxを快適に操作、FaceID対応の高速iOSSSHクライアント"
image: "https://replay.software/echo/opengraph-blog.png"
---

# Show HN: Echo, an iOS SSH+mosh client built on Ghostty - Echo：Ghosttyを活用したiOS向けSSHクライアント
外出先でエージェントを操る——iPhone/iPadを本気で開発マシンにするターミナルアプリ「Echo」

## 要約
EchoはGhosttyの端末エンジンを組み込んだネイティブiOS/iPadOS向けのSSHクライアント。Metal描画やKeychain/Face ID連携、iPadのマルチウィンドウ対応などで、TUIやAIエージェントとのリモート作業を快適にする設計です。

## この記事を読むべき理由
日本の通勤・モバイルワーク事情やiPad開発需要を踏まえ、外出先でリモートマシンやAIコーディングエージェントを扱う具体的な選択肢が分かります。

## 詳細解説
- なぜ今ターミナルか：最近のTUI（lazygit、lazydocker、Bubbletea/Ink/Textualなど）やAIコーディングエージェント（Claude Code、Codex等）が端末上で高度な対話を要求するようになり、単なる文字端末ではなく「リッチなインタラクティブ環境」が必要になっています。  
- Ghosttyの採用：EchoはGhosttyの高速で正確な端末レンダリングエンジンを組み込み、TUIの複雑なUI（シンタックスハイライト、インタラクティブな差分表示、進捗表示など）を正しく表示します。Ghosttyは埋め込み可能なオープンソースの端末エンジンです。  
- ネイティブ設計の利点：WebViewラップではなく完全ネイティブ。Metalアクセラレーションで描画が高速、iOSのKeychainでSSH鍵を安全に管理、Face IDで接続ロックをかけられます。  
- iPhone向けUX：キーボード上部の専用ツールバーやジェスチャベースの矢印移動など、タッチ操作でのコマンド入力を快適にする工夫があります。  
- iPad向けUX：ハードウェアキーボードのショートカット完全サポート、Split View/Slide Over、Stage Manager対応により複数セッションを並べて作業可能。iPadが実用的な開発端末になります。  
- エージェント運用に最適：tmux等でセッションをアタッチすれば、外出先からAIエージェントが生成したコードやビルド状況、インタラクティブな差分をそのまま操作・承認できます。  
- カスタマイズ：テーマコレクションを同梱し見た目を調整可能。  
- 価格と配布：App Storeで一度きりの有料（$2.99）、サブスクリプションなし。

日本語ローカルのニーズとの親和性：電車やカフェで短時間に承認や確認をする文化、iPad Pro／Magic Keyboardでの開発需要、企業のセキュリティ要件（鍵管理・生体認証）に合致します。サブスク嫌いの傾向が強いユーザーにも受け入れやすい価格モデルです。

## 実践ポイント
- まずはApp Storeで購入して試す（$2.99、一度きり）。  
- 常用するリモートホストはtmuxでセッションを維持しておくと外出先で続きから作業しやすい。  
- KeychainにSSH鍵を入れ、Face IDロックを有効にしてセキュリティ確保。  
- iPhoneではツールバー／ジェスチャを活用して入力効率を上げる。  
- iPadではハードウェアキーボード＋Stage Managerで複数セッション並列作業を試す。  
- TUIツール（lazygit等）やAIエージェントとの組合せで、レビュー・承認フローを短縮できるか確認する。
