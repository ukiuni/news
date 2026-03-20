---
layout: post
title: "Push events into a running session with channels - 実行中セッションにイベントを流し込む「channels」"
date: 2026-03-20T03:10:29.195Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://code.claude.com/docs/en/channels"
source_title: "Push events into a running session with channels - Claude Code Docs"
source_id: 47448524
excerpt: "監視アラートやチャットを起動中のClaudeへ直送し自動化するchannelsの使い方"
image: "https://claude-code.mintlify.app/_next/image?url=%2F_mintlify%2Fapi%2Fog%3Fdivision%3DAutomation%26appearance%3Dsystem%26title%3DPush%2Bevents%2Binto%2Ba%2Brunning%2Bsession%2Bwith%2Bchannels%26description%3DUse%2Bchannels%2Bto%2Bpush%2Bmessages%252C%2Balerts%252C%2Band%2Bwebhooks%2Binto%2Byour%2BClaude%2BCode%2Bsession%2Bfrom%2Ban%2BMCP%2Bserver.%2BForward%2BCI%2Bresults%252C%2Bchat%2Bmessages%252C%2Band%2Bmonitoring%2Bevents%2Bs%26logoLight%3Dhttps%253A%252F%252Fmintcdn.com%252Fclaude-code%252Fc5r9_6tjPMzFdDDT%252Flogo%252Flight.svg%253Ffit%253Dmax%2526auto%253Dformat%2526n%253Dc5r9_6tjPMzFdDDT%2526q%253D85%2526s%253D78fd01ff4f4340295a4f66e2ea54903c%26logoDark%3Dhttps%253A%252F%252Fmintcdn.com%252Fclaude-code%252Fc5r9_6tjPMzFdDDT%252Flogo%252Fdark.svg%253Ffit%253Dmax%2526auto%253Dformat%2526n%253Dc5r9_6tjPMzFdDDT%2526q%253D85%2526s%253D1298a0c3b3a1da603b190d0de0e31712%26primaryColor%3D%25230E0E0E%26lightColor%3D%2523D4A27F%26darkColor%3D%25230E0E0E%26backgroundLight%3D%2523FDFDF7%26backgroundDark%3D%252309090B&amp;w=1200&amp;q=100"
---

# Push events into a running session with channels - 実行中セッションにイベントを流し込む「channels」
クリックせずにはいられないタイトル: 「監視やチャットを“走るAI”に直送する方法 — Claude Codeのchannelsで自動化を次のレベルへ」

## 要約
Claude Codeの「channels」は、外部イベント（チャット、CI結果、Webhookなど）を“起動中の”Claudeセッションに直接プッシュして、離席中でもAIに自動で反応させる機能です。現在はResearch Previewで、Telegram・Discord・fakechatなどのプラグインが提供されています。

## この記事を読むべき理由
運用や開発の自動化が進む日本の現場では、監視アラートやCI通知を即時に処理できる仕組みが価値を生みます。channelsを使えば、既存のチャットや監視ツールをClaudeと橋渡しして「対話的」な自動化が可能になります。企業での権限管理や安全設定も考慮されている点も重要です。

## 詳細解説
- 概念：channelsはMCP（Model Context Protocol）サーバーとして動作し、外部からメッセージをClaudeの「開いている」セッションへ流し込みます。双方向にでき、Claudeの返信は同じチャネルへ戻ります。ただしイベントはセッションが開いている間のみ受信します（常時稼働させるならバックグラウンドでClaudeを動かす必要あり）。
- 利用条件：Claude Code v2.1.80以降、claude.aiアカウントでログイン必須。Console/APIキー認証は不可。Team/Enterpriseは管理者が明示的に有効化する必要があります。
- プラグイン構造：各チャネルはプラグイン（Bunで実行されるスクリプト）。研究プレビュー中はAnthropic公式の許可済みリストのプラグインのみ有効。
- 代表プラグイン：
  - fakechat：ローカルで動くデモUI。導入ハードルが低く動作確認に最適。
  - Telegram/Discord：ボットを作成し、プラグインをインストール → トークンを設定 → Claudeを--channelsで起動 → ボットとペアリングで送信者を許可するフロー。
- セキュリティ：各チャネルに「送信者の許可リスト（allowlist）」があり、ペアリングで最初のIDを登録。さらにTeam/Enterpriseでは管理者がchannelsの可否を管理（channelsEnabled）。
- 開発・検証：独自チャネルを作る場合はChannelsリファレンスを参照。preview期間は開発チャンネルを読み込むための特別フラグも存在します。

## 実践ポイント
- 準備
  - Claude Codeのバージョン確認・claude.aiでログイン。
  - Bunが必要（bun --versionで確認）。
- ローカルでまず試す（fakechat推奨）
  - インストール:
```bash
/plugin install fakechat@claude-plugins-official
```
  - Claudeをチャンネル付きで起動:
```bash
claude --channels plugin:fakechat@claude-plugins-official
```
  - ブラウザで http://localhost:8787 にアクセスして動作確認。
- Telegram/Discord導入の流れ（要約）
  - Bot作成→トークン取得 → プラグインインストール → トークン設定 → Claudeを--channelsで起動 → ボットにDMでペアリングコードを受け取りClaude側でペアリング → 送信者をallowlist化
- 運用の注意点
  - セッションが閉じているとイベントは届かない。常時受け取りたい場合は常駐プロセスで起動。
  - 権限や組織設定（channelsEnabled）を事前に確認。企業では管理者承認が必要。
  - 自動承認が必要な無人運用ではリスクがあるため、--dangerously-skip-permissions等の危険フラグは限定環境でのみ使用する。

短時間で試せるfakechatから始め、運用目的に応じてTelegram/Discordや独自チャネルへ展開するのが現実的な導入パスです。
