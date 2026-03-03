---
layout: post
title: "OAuth Redirect Abuse Lets Attackers Bypass MFA Without Stealing Tokens - OAuth リダイレクト悪用で多要素認証を回避、トークンは奪われない手口"
date: 2026-03-03T13:05:50.156Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://threatroad.substack.com/p/oauth-redirect-abuse-lets-attackers"
source_title: "OAuth Redirect Abuse Lets Attackers Bypass MFA Without Stealing Tokens"
source_id: 391955195
excerpt: "OAuthのリダイレクト仕様を悪用しMFAを回避、誘導でマルウェア配布や端末侵害に至る新手口"
image: "https://substackcdn.com/image/fetch/$s_!9WB7!,w_1200,h_675,c_fill,f_jpg,q_auto:good,fl_progressive:steep,g_auto/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fac3ac172-5d58-490e-a489-9429a5ddc689_686x386.jpeg"
---

# OAuth Redirect Abuse Lets Attackers Bypass MFA Without Stealing Tokens - OAuth リダイレクト悪用で多要素認証を回避、トークンは奪われない手口
魅せるタイトル: 「OAuthの“仕様”を悪用する新手口 — 多要素認証をすり抜け、マルウェアを配布する攻撃の正体」

## 要約
攻撃者はOAuthの“エラー時リダイレクト”機能を悪用し、ユーザーを誘導してマルウェアを配布する手口を実行。アクセス・トークンを盗まなくても、多要素認証（MFA）を迂回して端末侵害に至る事例が報告された。

## この記事を読むべき理由
多くの日本企業・公的機関がMicrosoft Entra/Azure ADやOAuthを利用しており、仕様どおり動作する機能を逆手に取られると従来の検知やMFAだけでは防げないため、即時の対策と運用見直しが必要になるから。

## 詳細解説
- 攻撃の核心  
  攻撃者は正規のOAuth認可URL風に見えるリンクを作成するが、scopeなど一部パラメータを不正に設定して認可エラーを発生させる。OAuth仕様ではエラー時に指定のredirect_uriへ遷移するため、これを攻撃者管理下のURLに向けてユーザーを誘導する。  
  例: https://login.microsoftonline.com/common/oauth2/v2.0/authorize?client_id=<app_id>&response_type=code&scope=<invalid_scope>&prompt=none&state=<value>

- なぜMFAを“回避”できるのか  
  ユーザーがトークンや権限を承認していない状況でも、仕様に沿ったエラー→リダイレクトの流れでブラウザを攻撃者サイトに遷移させられるため、認証フロー自体が悪用されている。攻撃は「認証欠陥」ではなく「仕様の正しい使われ方の悪用」。

- マルウェア配布と侵害チェーン  
  攻撃サイトはHTMLスムッギングやZIP内のLNK（ショートカット）を介してPowerShellを実行させ、正規プロセスを使ったDLLサイドローディングや暗号化済みペイロードの復号→C2接続といった手順で完全侵害に至らせる。EvilProxyやTycoonのようなプロキシ型ツールで認証情報やセッションクッキーを中間で傍受する事例も確認されている。

- 攻撃の社会的文脈  
  Microsoftは政府・公的機関を標的とするキャンペーンを観測しており、標的型・諜報目的の可能性が高い。会議招待やe-signatureといった信頼されやすい文脈を使い、メールフィルタをすり抜ける工夫も行われている。

## 実践ポイント
- Azure/Entra管理者向け  
  - ユーザー同意権限を最小化し、アプリ権限を定期レビューする。  
  - 未使用・過剰権限のOAuthアプリは即削除。  
  - 外部ドメインを指す疑わしいredirect_uriを監視・ブロック。  
  - OAuthアプリ作成を信頼できるアカウントに限定する条件付きアクセスを導入。

- セキュリティ運用（SOC）向け  
  - 不審なサインインプロパティ（匿名IP、異常なUser-Agent）をフラグ。  
  - Mail.SendやMail.ReadWriteなど過剰な権限要求の監視。  
  - OAuthリダイレクト先での自動ファイルダウンロードをブロック。

- エンドユーザー向け（簡潔）  
  - 不意なOAuth承認リンクはクリックしない。redirect_uriを確認し、不明なドメインなら中止。  
  - PDF/ICSや会議リンク経由の不審な添付ファイルは開かない。

- 日本市場への示唆  
  - 地方自治体、教育機関、ヘルスケアなど公的部門が標的になりやすく、委託ベンダーや外部連携アプリの権限管理を見直す必要あり。

今回のポイントは「ソフトウェア脆弱性の悪用ではなく、設計された動作の“仕様的悪用”」であること。仕様を理解した上で運用・検知ルールを強化することが最も有効な対策になる。
