---
layout: post
title: "Schedule tasks on the web - ウェブ上でのスケジュール実行"
date: 2026-03-27T15:41:06.768Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://code.claude.com/docs/en/web-scheduled-tasks"
source_title: "Schedule tasks on the web - Claude Code Docs"
source_id: 47539188
excerpt: "毎朝自動でPRレビューや脆弱性検査を実行しCI集約まで自動化するClaude Codeのスケジュール術"
image: "https://claude-code.mintlify.app/_next/image?url=%2F_mintlify%2Fapi%2Fog%3Fdivision%3DClaude%2BCode%2Bon%2Bthe%2Bweb%26appearance%3Dsystem%26title%3DSchedule%2Btasks%2Bon%2Bthe%2Bweb%26description%3DAutomate%2Brecurring%2Bwork%2Bwith%2Bcloud%2Bscheduled%2Btasks%26logoLight%3Dhttps%253A%252F%252Fmintcdn.com%252Fclaude-code%252Fc5r9_6tjPMzFdDDT%252Flogo%252Flight.svg%253Ffit%253Dmax%2526auto%253Dformat%2526n%253Dc5r9_6tjPMzFdDDT%2526q%253D85%2526s%253D78fd01ff4f4340295a4f66e2ea54903c%26logoDark%3Dhttps%253A%252F%252Fmintcdn.com%252Fclaude-code%252Fc5r9_6tjPMzFdDDT%252Flogo%252Fdark.svg%253Ffit%253Dmax%2526auto%253Dformat%2526n%253Dc5r9_6tjPMzFdDDT%2526q%253D85%2526s%253D1298a0c3b3a1da603b190d0de0e31712%26primaryColor%3D%25230E0E0E%26lightColor%3D%2523D4A27F%26darkColor%3D%25230E0E0E%26backgroundLight%3D%2523FDFDF7%26backgroundDark%3D%252309090B&amp;w=1200&amp;q=100"
---

# Schedule tasks on the web - ウェブ上でのスケジュール実行
魅力的タイトル: もう忘れない！毎朝自動でPRレビューや脆弱性チェックを走らせる“Claude Code”のスケジュール術

## 要約
AnthropicのClaude Codeが提供する「クラウドスケジュール機能」は、クラウド上で定期的にAIプロンプトを実行してリポジトリや外部サービスを自動操作できる機能です。PCがオフでも安定稼働し、PR点検やCI解析、ドキュメント同期などを自動化します。

## この記事を読むべき理由
日本の開発現場でも、毎朝のPR確認や夜間のCI集約、週次の依存関係チェックは手間になりがちです。Claudeのスケジュール機能を使えば、人的コストを下げつつ開発フローの品質と速度を向上できます。

## 詳細解説
- 使えるスケジューリング方式  
  - Cloud（Anthropic管理クラウド）：マシン不要で永続稼働（最小間隔1時間）。信頼性重視の定期処理向け。  
  - Desktop：自分のマシン上で実行。ローカルファイルやツールにアクセス可能（最小間隔1分）。  
  - /loop（CLI内）：セッション中の軽いポーリング用（最小間隔1分、セッション依存）。  

- タスク作成の流れ（Web画面の手順）  
  1. 名前とプロンプト：自律実行なので「何をして、成功の条件は何か」を明確に書く。モデル選択あり。  
  2. リポジトリ選択：実行時にリポジトリをクローン（デフォルトブランチ開始）。デフォルトではclaude/プレフィックスのブランチにしかプッシュしない。必要なら「Allow unrestricted branch pushes」を有効化。  
  3. 環境選択：ネットワークアクセス、環境変数（APIキー等）、セットアップスクリプト（依存インストール）を指定。カスタム環境作成でAPIアクセス等を与えられる。  
  4. スケジュール設定：プリセット（毎日9:00等）を選択。タイムゾーンはローカル時計に合わせて動作。細かい間隔はCLIの/schedule updateで調整可。  
  5. コネクタ確認：SlackやGoogle Drive等の接続（MCPコネクタ）をタスクに紐づけられる。不要なコネクタは外して権限を絞る。  
  6. 作成後：次回の実行でセッションが作られ、実行ログや変更（PR作成など）を確認可能。詳細画面から「Run now」「一時停止」「編集」「削除」ができる。  

- 実行ログと操作  
  各ランは通常のセッションとして開け、実行内容のレビュー、変更の確認、PR作成やセッションの名前変更・アーカイブが可能。CLIからは /schedule list /schedule run /schedule update 等で操作できる。

## 実践ポイント
- 信頼性重視ならCloud、ローカルファイルやビルドツールが要るならDesktopを選ぶ。  
- プロンプトは「自己完結」で成功基準を明記する（例：未処理PR一覧を10件以内にまとめ、重要な差分を要約）。  
- 環境変数とセットアップスクリプトで実行前準備（依存インストールやAPIキー注入）を済ませる。  
- コネクタは最小限に：不要な外部アクセスを外して権限を最小化する。  
- ブランチ保護を壊さないためデフォルトのclaude/プレフィックスを活かし、どうしても直接pushが必要なら限定的に許可する。  
- 細かいスケジュール調整や即時実行はCLIの /schedule コマンドで行う。

以上を踏まえれば、毎朝のPRチェックや夜間のCIサマリ、週次の依存監査といった定常作業を安全かつ自動化でき、日本のチーム運用での工数削減に直結します。
