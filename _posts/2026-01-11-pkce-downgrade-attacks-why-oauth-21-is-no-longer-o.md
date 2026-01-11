---
layout: post
title: "PKCE Downgrade Attacks: Why OAuth 2.1 is No Longer Optional - PKCEダウングレード攻撃：OAuth 2.1がもはや任意でない理由"
date: 2026-01-11T12:26:17.834Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://instatunnel.my/blog/pkce-downgrade-attacks-why-oauth-21-is-no-longer-optional"
source_title: "PKCE Downgrade Attacks: Why OAuth 2.1 Is Now Mandatory | InstaTunnel Blog"
source_id: 465535129
excerpt: "PKCE未実装で認可コードが丸ごと盗まれる危険—OAuth2.1必須化の理由と対策"
image: "https://i.ibb.co/9k3ddMrB/PKCE-Downgrade-Attacks-Why-OAuth-2-1-is-No-Longer-Optional.png"
---

# PKCE Downgrade Attacks: Why OAuth 2.1 is No Longer Optional - PKCEダウングレード攻撃：OAuth 2.1がもはや任意でない理由
あなたのアプリの「認可コード」が丸ごと盗まれる前に読むべき、実務的でわかりやすい解説

## 要約
OAuth 2.1 は PKCE（Proof Key for Code Exchange）を全クライアントで必須化し、従来の認可コードフローの「ダウングレード経路」を断ち切ります。PKCE未適用だと、モバイルのカスタムURLスキームやSPAのリファラ／履歴漏洩を使って認可コードが盗まれ、アクセストークン取得につながる危険があります。

## この記事を読むべき理由
日本のスタートアップや企業アプリ（モバイル・SPA・FinTech・SaaS）はOAuthに依存しています。個人情報保護やサービス信頼性を守るため、攻撃者が手軽に使う「PKCEダウングレード攻撃」の仕組みと対策を押さえることは必須です。実装ミスでユーザーのセッションが丸ごと乗っ取られるリスクを未然に防げます。

## 詳細解説
1. OAuth 2.1 が何を変えたか（要点）
   - PKCE を Authorization Code フローで全クライアントに必須化。
   - Implicit Grant と ROPC（パスワード受け取り型）は廃止。
   - リダイレクトURIは完全一致を要求（ワイルドカード禁止）。
   - 結果：認可コードをフロントチャネルで盗んでも使えないようにする防御線を標準化。

2. PKCE の仕組み（初級者向け）
   - code_verifier：クライアントが毎回作るランダム文字列（秘密、外に出さない）。
   - code_challenge：code_verifier を SHA-256 等でハッシュした値を最初に送る。
   - 認可サーバは発行した認可コードをこのチャレンジに「紐付け」し、トークン交換時に verifier を検証する。
   - つまり、認可コードだけを盗まれても、対応する verifier を知らなければ無効になる。

3. PKCE ダウングレード攻撃とは
   - 攻撃者が初期リクエストの code_challenge を削り（中間改変）、認可サーバがPKCEを必須にしていないと非PKCEフローでコードを発行してしまう。
   - そのコードをカスタムURLスキームの横取りやブラウザ履歴／Referer経由で奪取すると、攻撃者がそのままトークンを取得できる。
   - 根本対策は「認可サーバ側で code_challenge が無いリクエストを拒否する」こと（＝OAuth 2.1の主旨）。

4. client_secret は“見せかけ”の防御
   - サーバ側（Confidential）なら意味はあるが、SPAやモバイル（Public）に埋めた client_secret は簡単に取り出せる。
   - 静的な秘密は一度漏れると永続的に悪用されるが、PKCE の verifier は1回限りの動的値でありより安全。

5. さらに進んだ防御策（近年の攻撃に対応）
   - Refresh Token Rotation：リフレッシュ毎に新しいトークンを発行して古いものを無効化。
   - DPoP（DPoP等のProof-of-Possession）：トークンを発行したデバイスだけで使えるようにする。
   - 正確な redirect_uri マッチング、レガシーモードの無効化、ライブラリの最新化。

## 実践ポイント
- Authorization Server（Auth0, Okta, Keycloak 等）を監査して、PKCE を全クライアントで必須に設定する。
- ライブラリ／SDK を最新版に上げ、PKCE（S256）をデフォルトで使わせる。plain法は使わない。
- SPA / モバイルに client_secret を置かないこと。フロントに秘密をハードコーディングしているなら直ちに除去。
- リダイレクトURIはワイルドカード禁止、完全一致を設定。不要なエントリは削除。
- リフレッシュトークンは回転（Rotation）を有効化し、発行ポリシーを見直す。
- DPoP や Sender-Constrained Tokens の採用を検討し、トークンが使える端末を制限する。
- 日本市場向け注意点：Android のカスタムスキームや共有ブラウザ環境（端末貸し借り、端末診断ツール）を想定した脅威モデルを作る。特に金融系や個人情報を扱うサービスは法令対応（個人情報保護法）も含め早急に対策を。
- 最低限のテスト：認可フローを中間改変して code_challenge を除去した場合に認可サーバがリクエストを拒否することを確認する。

OAuth 2.1 は「オプション」ではなく「新しい基準」です。今すぐ設定とライブラリを見直し、PKCE を全フローで厳格に運用してください。
