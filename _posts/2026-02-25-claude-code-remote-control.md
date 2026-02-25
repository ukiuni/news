---
layout: post
title: "Claude Code Remote Control - Claude Code リモートコントロール"
date: 2026-02-25T12:00:15.786Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://code.claude.com/docs/en/remote-control"
source_title: "Continue local sessions from any device with Remote Control - Claude Code Docs"
source_id: 47148454
excerpt: "ローカル環境をそのままスマホや別PCで安全に続行できる新機能—データは端末に残る"
image: "https://claude-code.mintlify.app/_next/image?url=%2F_mintlify%2Fapi%2Fog%3Fdivision%3DPlatforms%2Band%2Bintegrations%26appearance%3Dsystem%26title%3DContinue%2Blocal%2Bsessions%2Bfrom%2Bany%2Bdevice%2Bwith%2BRemote%2BControl%26description%3DContinue%2Ba%2Blocal%2BClaude%2BCode%2Bsession%2Bfrom%2Byour%2Bphone%252C%2Btablet%252C%2Bor%2Bany%2Bbrowser%2Busing%2BRemote%2BControl.%2BWorks%2Bwith%2Bclaude.ai%252Fcode%2Band%2Bthe%2BClaude%2Bmobile%2Bapp.%26logoLight%3Dhttps%253A%252F%252Fmintcdn.com%252Fclaude-code%252FTBPmHzr19mDCuhZi%252Flogo%252Flight.svg%253Ffit%253Dmax%2526auto%253Dformat%2526n%253DTBPmHzr19mDCuhZi%2526q%253D85%2526s%253Dd535f2e20f53cd911acc59ad1b64b2e0%26logoDark%3Dhttps%253A%252F%252Fmintcdn.com%252Fclaude-code%252FTBPmHzr19mDCuhZi%252Flogo%252Fdark.svg%253Ffit%253Dmax%2526auto%253Dformat%2526n%253DTBPmHzr19mDCuhZi%2526q%253D85%2526s%253D28e49a2ffe69101f4aae9bfa70b393d0%26primaryColor%3D%25230E0E0E%26lightColor%3D%2523D4A27F%26darkColor%3D%25230E0E0E%26backgroundLight%3D%2523FDFDF7%26backgroundDark%3D%252309090B&amp;w=1200&amp;q=100"
---

# Claude Code Remote Control - Claude Code リモートコントロール
魅力：作業中のローカル環境をそのままスマホや別PCで続けられる—「家で始めた作業を外でそのまま再開」する新しいワークフロー

## 要約
Claude CodeのRemote Controlは、ローカルで動くClaude Codeセッションをブラウザやモバイルから遠隔で操作できる機能で、作業データはクラウドに移動せず端末上に残ります。

## この記事を読むべき理由
日本の開発者・プロダクト担当者にとって、ローカル依存のツールやMCPサーバー、設定を手元に残したまま別端末で作業継続できる点は、生産性とセキュリティの両面で魅力的だからです。

## 詳細解説
- 何ができるか  
  - デスクで始めた会話やタスクを、スマホや別のPCのclaude.ai/codeやClaudeアプリでそのまま続行できる。会話は全端末で同期。
- 実行場所の違い（重要）  
  - Remote Control：実行はあなたのマシン上。ローカルファイル・MCPやツールにそのままアクセス可能。  
  - Claude Code on the web：Anthropicのクラウド上で実行され、ローカル環境は参照できない。
- 要件と制限  
  - 利用プラン：ProまたはMax（Team／Enterpriseは非対応）。APIキー不可。  
  - ワークスペース信頼を承認し、/loginで認証済みであること。  
  - セッションはローカルプロセスとして動作するため、ターミナルを閉じると終了。1セッションにつき1リモート接続。長時間ネットワーク断（約10分）でタイムアウト。
- セキュリティと接続  
  - ローカルは着信ポートを開かず、アウトバウンドHTTPSでAnthropic APIをポーリング。通信はTLSで保護され、短命のスコープ付き認証を使用。
- セッション開始と接続方法（要点）  
  - 新規セッション（プロジェクトディレクトリで実行）:
  ```bash
  claude remote-control
  ```
  - 既存セッションを継続（会話中に実行）:
  ```bash
  /remote-control
  ```
  - 接続手段：端末に表示されるセッションURLをブラウザで開く、表示されるQRコードをスマホでスキャン、またはclaude.ai/code・アプリのセッション一覧から選択。/mobileでアプリダウンロードQRを表示可能。セッション名は最後のメッセージか /rename で設定。
- オプション  
  - --verbose（ログ表示）、--sandbox／--no-sandbox（ファイル/ネットワークの隔離）※/remote-controlコマンドではこれらは不可。/configで全セッション自動有効化も可能。

## 実践ポイント
- まずはローカルのプロジェクトで一度claudeを起動し、ワークスペース信頼と/loginを済ませておく。  
- デスクで作業を始めるときは:
  ```bash
  cd path/to/project
  claude remote-control
  ```
  QRをスキャンしてスマホで続行。  
- セッション名は /rename でわかりやすくしておく（複数端末で見つけやすい）。  
- ローカル機密データを扱う場合は--sandboxで隔離を検討（デフォルトはオフ）。  
- ターミナルを閉じると終了するため、長時間離席する際はセッションの再開手順を確認しておく。  

関連リンク（公式ドキュメント参照を推奨）：claude.ai/codeのRemote Controlドキュメント。
