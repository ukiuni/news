---
layout: post
title: "Discord faces backlash over age checks after data breach exposed 70,000 IDs - Discord、7万人分のID流出を受け年齢確認で反発"
date: 2026-02-09T21:05:24.755Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://arstechnica.com/tech-policy/2026/02/discord-faces-backlash-over-age-checks-after-data-breach-exposed-70000-ids/"
source_title: "Discord faces backlash over age checks after data breach exposed 70,000 IDs - Ars Technica"
source_id: 445799936
excerpt: "Discordが7万人のID流出を受け、顔写真で年齢確認を義務化し波紋"
image: "https://cdn.arstechnica.net/wp-content/uploads/2026/02/GettyImages-2225503659-1024x648.jpg"
---

# Discord faces backlash over age checks after data breach exposed 70,000 IDs - Discord、7万人分のID流出を受け年齢確認で反発

顔写真で年齢を判定する新方針――プライバシーと安全、どちらを取るべきか？

## 要約
Discordが成人向けコンテンツにアクセスする際、セルフィーや政府発行IDで年齢確認を必須化。だが以前に第三者サービス経由で7万人分のID流出が起きており、ユーザーの反発が強まっている。

## この記事を読むべき理由
日本でも個人情報（運転免許やマイナンバー等）の取り扱いは敏感なテーマ。オンデバイスAI・外部業者の利用・過去の流出という組み合わせは、日本のユーザーやサービス運営者に直接関係する問題です。

## 詳細解説
- 仕組み：Discordはセルフィーを端末内でAIが年齢推定する「オンデバイス処理」と、政府IDを第三者業者で照合する2経路を提示。セルフィーは端末外へ送られないと説明されている一方、ID照合はオフデバイス処理だと明言されている。  
- ベンダー：Discordはk‑IDやPrivatelyといった外部プロバイダを使う。これらは「端末で推定を完結する」「結果のみ受け渡す」と主張するが、プライバシーポリシーの表現が曖昧だと指摘されている。  
- 過去の流出：以前に第三者サービスから英国・豪州のユーザー約70,000件の政府IDが盗まれ、身元情報の悪用や身代金要求が懸念された経緯がある。  
- 精度と脆弱性：オンデバイス推定でも18・19歳付近の判定誤差や、AI動画での迂回など実運用での問題が報告されている。年齢確認の「訴訟リスク回避」と「ユーザー信頼」のバランスも問われている。  
- 運用方針：段階的なグローバル展開で全ユーザーは初期状態で“ティーン向け”になり、アクセスには年齢推定が必要になる。メタデータ-basedの年齢推定（プレイ履歴や行動）も併用するため、一部ユーザーは確認を求められない場合がある。

## 実践ポイント
- 個人ユーザー向け：
  - IDや顔写真を提出する前に、各社（Discord／k‑ID／Privately）の最新プライバシーポリシーを確認する。  
  - 本当に必要でなければ公的IDのアップロードは控える。代替手段（オンデバイス推定や年齢推測）があるか確認。  
  - アカウントに強力なパスワードと二段階認証を設定し、身元詐取のリスクに備える。  
  - 万が一IDを提出したら、定期的に不正利用の監視（クレジットや行政通知）を行う。  
- 企業／開発者向け：
  - 年齢確認を導入するなら、オンデバイス処理・データ最小化・透明性（処理ログ・削除方針）を優先する。  
  - 外部ベンダー採用時は責任範囲と侵害時の対応プロセスを契約で明確化する。日本の法規（個人情報保護法）準拠も確認する。

（出典：Ars Technica記事の要約）
