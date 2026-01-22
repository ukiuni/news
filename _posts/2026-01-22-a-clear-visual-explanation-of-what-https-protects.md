---
layout: post
title: "A clear visual explanation of what HTTPS protects - HTTPSが何を守っているかの分かりやすい図解"
date: 2026-01-22T11:45:01.838Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://howhttps.works/why-do-we-need-https/"
source_title: "Why do we need HTTPS? - How HTTPS works"
source_id: 420460788
excerpt: "HTTPSが守る「見られない・改ざん防止・相手確認」を図で直感解説"
image: "https://howhttps.works/assets/images/how-https-works-open-graph.png"
---

# A clear visual explanation of what HTTPS protects - HTTPSが何を守っているかの分かりやすい図解
HTTPSで“何が守られているか”を3つの視点で直感的に解説する記事

## 要約
HTTPSが守るのは「プライバシー（盗み見防止）」「整合性（改ざん防止）」「認証（相手確認）」の3点。これらがそろうことで、安全にウェブを使える。

## この記事を読むべき理由
日本でもネットバンキング、電子申請、リモートワークの増加で通信の安全性は日常的な関心事。基本概念を簡潔に押さえておけば、サービス設計や運用、個人利用でのリスク回避に直結します。

## 詳細解説
- プライバシー（Privacy）  
  平文HTTPだと通信内容が第三者に覗かれる（例：パスワードやフォーム内容）。HTTPSは通信を暗号化して「盗み見」を防ぐ。ブラウザの鍵アイコンは「暗号化されている」目印。

- 整合性（Integrity）  
  中間で通信を改ざんされると、送信した内容と受信した内容が一致しなくなる（マン・イン・ザ・ミドル攻撃）。TLSは通信の改ざんを検出・阻止して、データが途中で書き換えられていないことを保証する。

- 認証（Identification）  
  そのサーバーが本当に期待する相手かを証明するのがSSL/TLS証明書。信頼できる認証局（CA）が発行した証明書を使うことで、「本物のサイト」に接続していることを確認できる（なりすまし防止）。

- 仕組みの概略（次のステップ）  
  実際は「対称鍵暗号」と「公開鍵暗号」を組み合わせ、ハンドシェイクで安全なセッション鍵を共有してから高速暗号で通信する。TLS 1.2/1.3が現在の主流。

## 実践ポイント
- サイト運営者向け  
  - 常にHTTPSを有効化し、HTTPはHTTPSへリダイレクトする（HSTSの導入を検討）。  
  - TLSは最新バージョン（可能なら1.3）を使い、弱い暗号スイートを無効化。  
  - 証明書は期限前に更新。Let's Encryptなどで自動更新を導入すると便利。

- 一般ユーザー向け  
  - 鍵アイコン／証明書情報を確認：怪しいと感じたらURLや証明書の発行元をチェック。  
  - 公衆Wi‑Fiでは特にHTTPSサイトのみ扱う。ブラウザ拡張やOSのアップデートで最新のTLSサポートを保つ。

短くまとめると、HTTPSは「見られない・変えられない・相手が確かである」ことを同時に提供する基礎技術です。これを理解しておけば、安全設計と日常利用の判断がぐっと楽になります。
