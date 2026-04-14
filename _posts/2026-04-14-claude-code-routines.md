---
layout: post
title: "Claude Code Routines - Claude Code のルーチン機能"
date: 2026-04-14T18:05:26.272Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://code.claude.com/docs/en/routines"
source_title: "Automate work with routines - Claude Code Docs"
source_id: 47768133
excerpt: "Claude CodeのRoutinesで定期実行やGitHub連携を自動化しPRを無人化"
image: "https://claude-code.mintlify.app/_next/image?url=%2F_mintlify%2Fapi%2Fog%3Fdivision%3DClaude%2BCode%2Bon%2Bthe%2Bweb%26appearance%3Dsystem%26title%3DAutomate%2Bwork%2Bwith%2Broutines%26description%3DPut%2BClaude%2BCode%2Bon%2Bautopilot.%2BDefine%2Broutines%2Bthat%2Brun%2Bon%2Ba%2Bschedule%252C%2Btrigger%2Bon%2BAPI%2Bcalls%252C%2Bor%2Breact%2Bto%2BGitHub%2Bevents%2Bfrom%2BAnthropic-managed%2Bcloud%2Binfrastructur%26logoLight%3Dhttps%253A%252F%252Fmintcdn.com%252Fclaude-code%252Fc5r9_6tjPMzFdDDT%252Flogo%252Flight.svg%253Ffit%253Dmax%2526auto%253Dformat%2526n%253Dc5r9_6tjPMzFdDDT%2526q%253D85%2526s%253D78fd01ff4f4340295a4f66e2ea54903c%26logoDark%3Dhttps%253A%252F%252Fmintcdn.com%252Fclaude-code%252Fc5r9_6tjPMzFdDDT%252Flogo%252Fdark.svg%253Ffit%253Dmax%2526auto%253Dformat%2526n%253Dc5r9_6tjPMzFdDDT%2526q%253D85%2526s%253D1298a0c3b3a1da603b190d0de0e31712%26primaryColor%3D%25230E0E0E%26lightColor%3D%2523D4A27F%26darkColor%3D%25230E0E0E%26backgroundLight%3D%2523FDFDF7%26backgroundDark%3D%252309090B&amp;w=1200&amp;q=100"
---

# Claude Code Routines - Claude Code のルーチン機能
魅力的なタイトル: 「コード自動化を“放置”で回す時代へ：Claude Codeのルーチンで日常作業を自動化する方法」

## 要約
Claude Code の「Routines」は、クラウド上でプロンプト＋リポジトリ＋コネクタをパッケージ化して定期実行・API起動・GitHubイベントで自動実行できる機能です（リサーチプレビュー）。

## この記事を読むべき理由
日本のプロジェクトでも、定型的なバックログ整備、PRの自動チェック、デプロイ後の検証、ドキュメント差分対応などを“人を待たず”に回せれば、品質と速度が同時に向上します。少人数チームやオンコール運用を効率化したい日本のエンジニアに有用です。

## 詳細解説
- 概要：Routines は Anthropic 管理のクラウドで動く自律セッション。プロンプト（自動で行う手順）、対象リポジトリ、環境、コネクタ、トリガーを保存して実行します。実行中はあなたの接続済み GitHub / Slack 等のアカウントでアクションが行われます。
- トリガー種類：
  - Schedule：時刻・周期で定期実行（最短1時間）。タイムゾーンはローカル時刻で指定可能。
  - API：各ルーチンに専用の /fire エンドポイントとベアラートークンが発行され、POST で起動。ペイロードの text をプロンプトに追加可能で、アラート本文やログを渡せます。
  - GitHub：リポジトリのイベント（PR作成、push、merge など）で自動起動。Claude GitHub App のインストールが必要。
- 作成方法：Web（claude.ai/code/routines）、Desktop、CLI（/schedule）から作成可能。Web と CLI は同じアカウントに保存されます。Desktop では「New remote task」を選ぶ点に注意。
- 実行と権限：ルーチンは選んだリポジトリをクローンし、claude/ プレフィックスのブランチを作成可能。環境はネットワークアクセスや環境変数、セットアップスクリプトを制御します。不要な権限やコネクタは外して最小化してください。
- 制限と注意点：研究プレビューのため挙動・API 仕様・レート制限が変わる可能性あり。ルーチンの実行はアカウントの実行枠を消費し、各操作はあなたの連携アカウントとして記録されます（コミットやSlack投稿が本人名義になる）。

## 実践ポイント
1. プロンプトは完全かつ具体的に書く（成功条件とアウトプットを明示）。  
2. 最初は「Run now」で手動実行して挙動を確認する。  
3. トークンはシークレットストアに保管、必要に応じてローテーション／無効化。  
4. 環境とコネクタは最小権限でスコープする（不要なコネクタは外す）。  
5. すぐ試す手順（概略）：
   - claude.ai/code/routines で New routine → 名前・プロンプトを設定  
   - リポジトリと環境を選ぶ（Default 環境でまずは検証）  
   - トリガーを追加（Schedule / API / GitHub）  
   - API トリガーを使う場合はトークンを発行して安全に保存。サンプル呼び出し例:
```bash
curl -X POST https://api.anthropic.com/v1/claude_code/routines/<ROUTINE_ID>/fire \
  -H "Authorization: Bearer sk-xxxx" \
  -H "Content-Type: application/json" \
  -d '{"text":"Sentry alert: ..."}'
```
6. 小さな自動化から始め、実行ログ（session URL）で挙動を確認してから本番化する。

補足：現段階は Pro/Max/Team/Enterprise プランで利用可能。まずは試験的にルーチンを立て、CI/CD や監視アラートとの連携で効果を確かめてください。
