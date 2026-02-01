---
layout: post
title: "Match, Hinge, OkCupid, and Panera Bread breached by ransomware group - Match、Hinge、OkCupid、Panera Breadがランサムウェア集団により侵害"
date: 2026-02-01T16:10:48.722Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.malwarebytes.com/blog/news/2026/01/match-hinge-okcupid-and-panera-bread-breached-by-ransomware-group"
source_title: "Match, Hinge, OkCupid, and Panera Bread breached by ransomware group | Malwarebytes"
source_id: 413256582
excerpt: "Match/Hinge/OkCupidとPaneraで計数千万件、住所や交際履歴流出の恐れ"
image: "https://www.malwarebytes.com/wp-content/uploads/sites/2/2026/01/match.jpg"
---

# Match, Hinge, OkCupid, and Panera Bread breached by ransomware group - Match、Hinge、OkCupid、Panera Breadがランサムウェア集団により侵害
数千万件規模の流出——デート履歴と住所情報、あなたにとってどちらが危険か？

## 要約
ShinyHuntersというランサムウェアグループが、Match Group（Tinder/Match/Hinge/OkCupid等）から約1,000万件、Panera Breadから約1,400万件のデータ流出を主張。両社は調査中で、ログイン情報や金融情報の流出は確認されていないとしていますが、PII（個人を特定できる情報）やトラッキングデータは含まれる可能性があります。

## この記事を読むべき理由
デートアプリ利用が増える日本でも「プライバシーや身元露見（doxxing）」や「ターゲット型フィッシング」が現実的脅威になっており、SSOや音声合成（ボイスクローン）など新たな攻撃手法の登場は国内企業・利用者双方に影響します。

## 詳細解説
- 攻撃主体と被害の範囲：攻撃はShinyHuntersが主張。Match側はAppsflyer等のトラッキングデータや内部文書が対象になった可能性を示しています。Paneraは住所などのPIIが含まれるとされます。両社は現在調査・通知対応中。  
- 手口の特徴：報告ではSSO（シングルサインオン）経由のアクセス取得や、音声合成を使ったなりすましが観測されています。SSOの突破は複数サービス横断で影響を拡大させ、ボイスクローンは電話確認やサポート窓口の信頼を悪用します。  
- データの性質と影響：  
  - デートアプリのデータ流出は「個人の交際状況」「利用履歴」「追跡データ」による露見・恐喝・社会的被害につながるリスクが高い。  
  - 飲食チェーンの注文・住所データは、既存データと突合されて精度の高いフィッシングやなりすましに悪用される。  
- 企業側声明：現時点でログイン資格情報やクレジット情報の流出は確認されていないとする報告が多いが、調査は継続中のため念のための対応が必要。

## 実践ポイント
- 公式発表を先に確認：被害連絡は公式サイト／メールで真偽を確認する。  
- パスワードを変更：被害が疑われるサービスはすぐに強力で固有のパスワードに。パスワードマネージャー推奨。  
- 2要素認証を有効化：可能ならFIDO2対応のハードウェアキーを使う（SMSのみの2FAは脆弱）。  
- SSO設定を見直す：企業利用のSSOログや権限設定、ログイン通知を確認。  
- フィッシング警戒：受信メール／SMSで急を要する要求やリンクは疑って別経路で確認。  
- カード情報の扱いを再検討：通販でカード情報を保存している場合は見直す。  
- 身元監視サービスを検討：必要に応じてダークウェブ監視やクレジットモニタリングを利用。  
- 日本向けの注意点：国内でもデーティングアプリやフードデリバリ利用者は多く、個人情報が断片的に結びつくと被害が拡大するため、日頃から二段階認証・支払い情報管理を徹底すること。

以上。
