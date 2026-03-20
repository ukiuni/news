---
layout: post
title: "Full Disclosure: A Third (and Fourth) Azure Sign-In Log Bypass Found - Azureサインインログの3つ目（および4つ目）のバイパスが発見された"
date: 2026-03-20T03:17:50.068Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://trustedsec.com/blog/full-disclosure-a-third-and-fourth-azure-sign-in-log-bypass-found"
source_title: "TrustedSec | Full Disclosure: A Third (and Fourth) Azure Sign-In Log…"
source_id: 47448994
excerpt: "Azureのサインインログを回避し有効トークン取得する新たなバイパスが発見、即対策必須"
image: "https://trusted-sec.transforms.svdcdn.com/production/images/Blog-Covers/GraphGoblinAzureLoggingBypass_SEO.jpg?w=1200&amp;h=630&amp;q=82&amp;auto=format&amp;fit=crop&amp;dm=1773775732&amp;s=9e6e76af63714e7757fe4ae6389c0782"
---

# Full Disclosure: A Third (and Fourth) Azure Sign-In Log Bypass Found - Azureサインインログの3つ目（および4つ目）のバイパスが発見された
Azureの「見えない」ログイン：管理者の目をかいくぐる新手法2つ

## 要約
TrustedSecの調査で、Azure Entra IDのサインインログを生成せずに有効トークンを取得できる新たなバイパス（GraphGoblinと未公開名の4番目）が発見され、既に修正は行われたが設計上の弱点が露呈した。

## この記事を読むべき理由
多くの日本企業でAzureを採用しており、サインインログは侵害検知の要です。ログに残らない認証成功は検知回避・情報流出に直結するため、対策と検出方法を知る必要があります。

## 詳細解説
- 背景：攻撃者はHTTP POSTでAzureのトークンエンドポイント（login.microsoftonline.com/.../oauth2/v2.0/token）にユーザー名・パスワード・client_id・scopeを送り、ROPC（Resource Owner Password Credentials）フローでトークンを得られるか検証する手法を多用する。TrustedSecは過去にGraphNinja・GraphGhostというログ非記録の検証手法を報告している。
- GraphNinja（過去）：別テナントのGUIDをエンドポイントに指定すると、パスワードの当たり判定は返るが親テナントのサインインログは生成されなかった（トークンは未取得）。後に追加ログで対処。
- GraphGhost（過去）：無効なclient_id等で後段の検証を失敗させることで、パスワード検証は行われるが「成功ログ」が残らない挙動を利用（トークンは未取得）。修正によりログにパスワード検証結果が付与された。
- GraphGoblin（今回）：scopeパラメータに「openid」を大量に繰り返すなどして、パラメータ自体は「形式上有効」と判定される一方で、内部のログ記録処理（推定：DBのカラム長オーバーフローやINSERT失敗）によりサインインログの書き込みが失敗し、にもかかわらず有効なアクセストークンが返されるケース。実証では返されたトークンでGraph API呼び出しが可能で、AzureポータルのEntra IDサインインログやLog Analyticsに該当イベントは記録されなかった。
- 第4のバイパス：記事では別の手法が示唆されているが詳細は省略。要点は「様々な入力パラメータ処理の盲点でログが抜け落ち得る」こと。

簡潔な例（通常のROPCリクエスト）：
```bash
curl -X POST "https://login.microsoftonline.com/<TENANT>/oauth2/v2.0/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  --data-urlencode "client_id=<CLIENT_ID>" \
  --data-urlencode "grant_type=password" \
  --data-urlencode "username=user@example.com" \
  --data-urlencode "password=YourPass"
```

## 実践ポイント
- すぐやること
  - Azureの最新パッチ適用とMSの緩和措置（TrustedSec報告に対する修正）を確認する。
  - ROPCフローの利用を避け、OAuthの推奨フロー（認可コード＋PKCE等）を採用する。
  - 重要リソースに対して条件付きアクセスと多要素認証（MFA）を必須化する。
- 検出策（SIEM/KQLで実装）
  - サインインログと実際のAPIアクセス（Graph呼び出し等）を相関し、API呼び出しに対応するサインインイベントが存在しないものをアラート化する。
  - tokenエンドポイントへのリクエストで異常に長い/繰り返しのscopeパラメータや異常なリクエストサイズを検出する。
  - トークン発行後の短時間での異常アクセス（地理的不整合・IP変動・過剰権限利用）を監視する。
- 設計上の対策
  - 入力値の長さ・繰り返しに対する堅牢な検証とログ書き込みの障害監視をベンダーに求める。
  - ログ欠損が疑われる場合に備え、ログの二重化（Azure側と自社SIEMへの直接転送）を検討する。

この記事を読んで、まずは自社テナントでROPCや非推奨フローの使用状況を洗い出し、ログ相関ルールとMFA強制を優先してください。
