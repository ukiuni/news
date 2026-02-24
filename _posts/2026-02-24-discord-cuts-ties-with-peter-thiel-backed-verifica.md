---
layout: post
title: "Discord cuts ties with Peter Thiel-backed verification software after code found in US surveillance - Discord、ピーター・ティール支援の本人確認ソフトと決別（コードが米当局関連で発見）"
date: 2026-02-24T12:17:25.432Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://fortune.com/2026/02/24/discord-peter-thiel-backed-persona-identity-verification-breach/"
source_title: "Discord cuts ties with Peter Thiel-backed verification software after code found in US surveillance | Fortune"
source_id: 397852820
excerpt: "DiscordがPersonaと決別—米当局関連で本人確認コード流出、あなたのIDはどこへ？"
image: "https://fortune.com/img-assets/wp-content/uploads/2026/02/GettyImages-2261647012-e1771866643179.jpg?resize=1200,600"
---

# Discord cuts ties with Peter Thiel-backed verification software after code found in US surveillance - Discord、ピーター・ティール支援の本人確認ソフトと決別（コードが米当局関連で発見）

魅力タイトル：Discordの“年齢確認”が炎上——個人情報の行き先が見えた瞬間、あなたのIDはどこへ行く？

## 要約
Discordが、ピーター・ティール系ファンドの支援を受ける本人確認サービス「Persona」との連携を中止。研究者がFedRAMP管理下の政府系エンドポイントでPersonaのフロントエンド関連ファイル約2,500件（約53MB）を発見し、顔認証や多数のスクリーニングが可視化されたことが発端です。

## この記事を読むべき理由
クラウド時代の本人確認は「誰に」「どこで」「どの程度」データが残るかがカギ。日本企業・サービス運営者も外部ベンダー依存で同様のリスクを抱えやすく、顧客データ保護や規制対応（個人情報保護法、取引先監査）の観点で即時の示唆を得られます。

## 詳細解説
- 発見内容：研究者が公開されていたフロントエンド関連ファイル群を指摘。ファイル群は政府承認のFedRAMPエンドポイントにも配置されており、ファイルからはPersonaが実行する処理（年齢確認に加え、政治的に影響力のある人物（PEP）や「テロリズム、諜報」など14カテゴリにわたる“有害メディア”スクリーニング、計269種のチェック、リスク/類似度スコア割当）が読み取れたと報告されています。
- Discordの説明：テストは短期間かつ限定ユーザーで実施され、提出データは最長7日で削除されるとしたが、過去には別ベンダーの侵害で7万人超のIDが影響を受けた前例もあり、ユーザーの不信感が増幅。
- Persona側の反応：CEOは発見は「圧縮前のフロントエンドソースマップ」で脆弱性とは考えていないと主張。一方で同社はKYC/AMLや企業向けのFedRAMP承認取得を目指しており、OpenAIやRobloxなどにもサービス提供している点は注目すべき事実。
- 問題の本質：本人確認は「機能」と「データフロー（どこに何が残るか）」を分けて評価する必要がある。技術的には多様なチェックが可能でも、それをどの顧客がどの用途で使うか・ログや外部共有がどう管理されるかがプライバシーリスクを決める。

## 実践ポイント
- ベンダー契約で「データ保持期間」「削除証跡」「第三者提供の可否」を明確化する。  
- 必要最小限の情報で済む方式（年齢のみの確認はボールド・エッジ検証や端末内処理）を優先する。  
- ベンダーのセキュリティ認証（ISO27001、SOC2、FedRAMP等）と監査報告を確認する。  
- サプライチェーン（委託先→再委託先）を可視化し、脆弱性報告やバグバウンティの有無を確認する。  
- ユーザー向けには選択肢を用意（IDアップロード以外の代替手段、保存期間・目的の透明化）。

短期間の連携でも個人情報リスクは発生します。国内でも外部本人確認を採用する前に、データの「行き先」と「消去の証跡」を厳密に設計してください。
