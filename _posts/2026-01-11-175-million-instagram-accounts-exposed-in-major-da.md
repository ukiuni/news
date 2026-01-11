---
layout: post
title: "17.5 Million Instagram Accounts Exposed in Major Data Leak - 1,750万のInstagramアカウントが大規模流出"
date: 2026-01-11T12:23:44.372Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://cyberpress.org/instagram-data-leak/"
source_title: "17.5 Million Instagram Accounts Exposed in Major Data Leak"
source_id: 465589429
excerpt: "1,750万件のInstagram連絡先が流出、SIM乗っ取りや巧妙なフィッシング被害が急増の懸念"
image: "https://i3.wp.com/blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEj-Z7qQM8UfQAe_l1HdQ0FxDAjzMtSS2z4cpOw-UswlZ1qWnYN5ZHECRLQ4PgGepKzJjY2gKLamylj_VRPCCOtcqWBZ-bcMocqlHr_GEhLcMdqwXU5tna-jN3n-8PEwKnIwsCd9qNIKxunUPu22VcLeyyg775l7LfusmCWbctyb5Xjn9jdguDSHbCT-OdxO/s16000/BreachForums%20Hack%20(1).webp?w=1600&resize=1600,900&ssl=1"
---

# 17.5 Million Instagram Accounts Exposed in Major Data Leak - 1,750万のInstagramアカウントが大規模流出
日本のユーザーも標的に—個人情報が暗号市場に流出、今すぐできる対策はこれだ

## 要約
約1,750万件分のInstagramアカウント情報（氏名・ユーザ名・メール・電話番号・国情報など）がダークウェブに出回り、既にパスワードリセット通知の急増など実害の兆候が出ています。流出は「APIのスクレイピング（API漏えい）」とされ、Metaは当該漏えいについて明確なコメントを出していません（記事出典：Cyber Press）。

## この記事を読むべき理由
日本でもInstagramユーザーは多く、流出した連絡先情報があればSIM乗っ取りや精巧なフィッシングで被害に遭うリスクが高まります。技術的背景と実践的な防御策を押さえておけば被害を防げます。

## 詳細解説
- 流出経緯：攻撃者は「Solonik」と名乗る人物がハッキングフォーラムに「2024 API LEAK」として17.5Mのデータを掲載。データはJSON/TXT形式で、公開APIの大量照会（スクレイピング）により収集された可能性が高いと報告されています。
- 含まれる情報：氏名・ユーザ名・確認済みメールアドレス・電話番号・ユーザーID・国・部分的な位置情報など。パスワード自体は含まれていないとされますが、メールと電話番号の組合せだけで攻撃者が信頼を築ける点が危険です。
- なぜ危険か：メールや電話番号が流出すると（1）フィッシングの標的が絞られ成功率が上がる、（2）SMSベースの2要素認証（2FA）を狙ったSIMスワップ（電話番号の不正移転）で認証コードを奪われる、（3）サポート窓口を偽るソーシャルエンジニアリングで追加情報を引き出される、という被害が現実化します。
- 技術的含意：今回の分類は「サーバ侵入」ではなく「スクレイピング」ですが、APIのレート制限や認証・プライバシー設定に抜けがあった可能性を示唆します。大規模な自動照会を見逃した点はプラットフォーム側の検出体制の課題でもあります。
- 現状：記事時点（2026年1月10日）でMetaからの正式声明は確認されていません。セキュリティ専門家はアプリ型の認証器でのMFA利用を推奨しています。

## 実践ポイント
- すぐにやること
  - Instagramで二段階認証を有効化：SMSではなくAuthenticatorアプリ（Google AuthenticatorやAuthy等）を使う。
  - メールとInstagramアカウントのパスワードを強力かつ一意に設定し、パスワードマネージャーを利用する。
  - 不審なパスワードリセットやログイン通知は無視し、正規サイトで直接確認する（メール内リンクはクリックしない）。
- 電話番号に関する対策（日本向け）
  - キャリアで「第三者による番号移転ロック（MNPロック）」「なりすまし防止」サービスを有効にする。各社の窓口で設定可能。
  - SIM再発行やMNP手続き時の追加本人確認を求める。
- 継続的にやること
  - 登録済みサードパーティ連携アプリの見直しと不要アプリの解除。
  - アカウントのログイン履歴・接続端末を定期チェック。
  - 金融情報や重要情報はSNSに紐づけず、メールや電話のセキュリティも強化する（2段階認証を設定）。
  - 万が一被害に遭ったら、Instagramのヘルプセンター、キャリア、警察相談（サイバー犯罪相談窓口）に速やかに連絡する。

この事案は「自分ごと化」して対策を講じる価値があります。まずは二段階認証の設定と電話番号保護の確認から。
