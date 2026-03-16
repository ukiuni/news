---
layout: post
title: "I Built EchoHR: The HR System That Doesn’t Ghost You - ゴーストしないHRシステム「EchoHR」を作った"
date: 2026-03-16T08:04:38.905Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://dev.to/ujja/i-built-echohr-the-hr-system-that-doesnt-ghost-you-1c2i"
source_title: "I Built EchoHR: The HR System That Doesn’t Ghost You - DEV Community"
source_id: 3334932
excerpt: "Notion＋AI連携で採用～退職を自動化し候補者の“ゴースト”を防ぐEchoHR"
image: "https://media2.dev.to/dynamic/image/width=1200,height=627,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2F04qzm8j2sklzgjboos0o.png"
---

# I Built EchoHR: The HR System That Doesn’t Ghost You - ゴーストしないHRシステム「EchoHR」を作った
候補者も社員も放置しない。Notion＋MCP＋AIで組む「人に優しい」HRプラットフォーム

## 要約
Notion MCP上に構築したEchoHRは、採用からオフボーディングまでのライフサイクルを自動化し、候補者や従業員が「連絡が途絶える（ghosting）」ことを防ぐことを目的としたワークスペーステンプレートと自動化群です。

## この記事を読むべき理由
日本でも候補者への応答遅延や評価の透明性不足は採用体験の課題です。EchoHRは既存ツール（Notion、Slack、Figma、カレンダー、OpenAI）をつなぎ、小規模チームでも迅速に「見える化＋通知＋AIサマリ」を試せる点が実務的に有益です。

## 詳細解説
- 構成要素  
  - Notion MCP：CRUDとスキーマ管理の中核。候補者／応募／面接／オファー／オンボーディング〜退職まで20以上の関連データベースを用意。RelationsとRollupsで全ジャーニーを結合。  
  - Automation Server（OpenAI MCP連携）：/webhooks/meeting-notes などのエンドポイントで会議メモを受け取り、AIで候補者向けの安全な要約やマネジャー向けアクションを生成してNotionへ書き戻す。  
  - Slack MCP：重要なアップデート（フォロー期限、オンボーディング通知、フィードバック催促）を人に届く形で通知。  
  - Figma / Calendar MCPパターン：デザインのレビューや面接スケジュールを自動でタスク化・スケジューリング。  
- デモ体験  
  - リポジトリにテンプレートがあり、npm run demoでワンコマンドでワークスペースとデモデータ（約50名規模のスタートアップ想定）をプロビジョニング可能。  
- 独自性（Zero-Ghosting）  
  - 自動SLA・リマインダー・レビュータイムラインで「連絡が途切れる」状況をシステム側から防止する設計思想。  
- 現状の制約（Notion API依存）  
  - APIで作れないビュー（ボード／タイムライン等）や、プロパティ（数式など）の後編集不可、見た目のカスタムCSS非対応などは手動補完が必要。グラフは外部埋め込みで代替。

## 実践ポイント
- まず動かす：リポジトリをクローンしてREADMEの手順で npm run demo を実行し、シードされたワークスペースを確認する。  
- 必要な連携：Slackトークン、OpenAIキー、Notion連携を用意して自動化を有効化する。  
- 小さく試す：採用パイプラインの一部（応募→面接メモ→AI要約→通知）だけを切り出して検証。  
- カスタマイズ：SLA期限や通知文言、オンボーディングチェックリストを自社プロセスに合わせて調整。  
- 注意点：個人情報の扱いと社内規程（日本の個人情報保護法に基づく運用）を必ず確認する。

興味があれば、公式リポジトリ（GitHub: ujjavala/EchoHR）を確認して、まずは小さなパイロットで「ゴーストしない採用」を試してみてください。
