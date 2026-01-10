---
layout: post
title: "Instagram Data Leak Exposes Sensitive Info of 17.5M Accounts - Instagramのデータ流出で1,750万アカウントの機密情報が露出"
date: 2026-01-10T17:44:18.734Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://cybersecuritynews.com/instagram-data-leak-exposes-sensitive-info-of-17-5m-accounts/"
source_title: "Instagram Data Leak Exposes Sensitive Info of 17.5M Accounts"
source_id: 467413821
excerpt: "Instagramで1,750万件の連絡先が流出、乗っ取りや標的型攻撃の詳報と今すぐ有効な対策"
image: "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEj6dyXXTkEzf5uICN2f4AYB7XUALI7vSF4W3keCjHOuB3kV9MoknkIPevSOneD8tPqzJwo6W7-mpb14FuGhPrhu41TOQHuD7iNXCsBO1EEpWbkfj0B7xRLM4hG-coiPz2-_cyZz1LnznQtjVXnedw6cR3hhZZkwWqH9-mdQsU9Pdx0LvgqPnfDzGA46TJgV/s1600/Data%20Leak%20Exposes%20Sensitive%20Info%20of%2017.5M%20Accounts%20%281%29.webp"
---

# Instagram Data Leak Exposes Sensitive Info of 17.5M Accounts - Instagramのデータ流出で1,750万アカウントの機密情報が露出
魅力釣りタイトル: 「あなたのインスタが狙われているかも？1,750万件流出の中身と今すぐできる防御」

## 要約
2024年末にスクレイピングで収集されたとされるInstagramユーザー約1,750万件分の個人情報（ユーザー名、メール、電話、住所の一部など）がダークウェブに出回り、アカウント乗っ取りや標的型フィッシングが現実に起き始めています。

## この記事を読むべき理由
日本でもインフルエンサーや企業のInstagram活用が進む中、連絡先や住所が漏れると個人・企業ともに被害リスクが高まります。エンジニアも運用担当も、被害を防ぐ実践的な対策を今すぐ確認すべきです。

## 詳細解説
- 何が起きたか：セキュリティ企業の調査で、17.5M件分のInstagram関連データがダークウェブで販売されていると確認されました。出品者は「Subkek」と名乗り、2024年後半にパブリックAPIや国別の情報源からスクレイピングしたと主張しています。
- 流出データの種類：ユーザー名、メールアドレス、電話番号、部分的な住所（国や市区レベル）、サンプルレコードがリストに含まれているとの報告。これらが揃うと、なりすましやフィッシング、個人情報を用いたソーシャルエンジニアリングの成功率が高まります。
- 実際の悪用の兆候：漏洩後、複数ユーザーに対して正当な「パスワードリセット」通知が届いており、乗っ取りの試行が行われている事例が確認されています。
- どこが原因か：Instagram／Meta側の公式コメントはまだ出ていません。外部サービスやパブリックAPIのスクレイピング、あるいはサードパーティー経由の情報流出が疑われています。調査は継続中です。

## 実践ポイント
- 一般ユーザー向け
  - 2段階認証を即有効化（認証アプリ推奨、SMSはリスクあり）
  - パスワードをユニークかつ複雑にし、パスワードマネージャーを利用
  - 不審なメールやDMのリンクは開かない。Instagramからの通知か公式アプリで確認する習慣を
  - アカウントのログイン履歴と接続アプリを確認して、不審なセッションを削除
  - メールや電話番号が漏れていないか、「Have I Been Pwned」などで確認（英語サイト）

- 企業・運用担当向け
  - 影響が疑われるビジネスアカウントはすぐに全担当者の認証設定を見直す
  - インフルエンサーや代理店と共有している連絡先管理の運用ルールを厳格化
  - 被害発生時の対応フロー（通知、ログ保存、法的相談）を整備
  - 個人情報を扱う際はAPPI（個人情報保護法）に基づく対応と、必要に応じた関係当局への届出を準備

- 開発者／セキュリティ担当向け
  - 自社が公開するAPIに対しレート制限・スクレイピング検知を強化
  - 第三者連携サービスのデータ保護体制を監査・評価
  - 大量のデータ取得やパターンを検出するためのログ監視とアラート設計
  - ユーザーデータの最小化（必要以上に保持しない）と暗号化

最後に：個人情報の流出は「他人事」ではありません。まずは自身のアカウント設定と企業の運用を今すぐ点検してください。
