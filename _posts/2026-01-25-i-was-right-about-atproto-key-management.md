---
layout: post
title: "I Was Right About ATProto Key Management - ATProtoの鍵管理について私が正しかった理由"
date: 2026-01-25T20:15:32.670Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://notes.nora.codes/atproto-again/"
source_title: "I Was Right About ATProto Key Management - nora's notes"
source_id: 1625415167
excerpt: "ATProto自前PDSで鍵管理の現実に直面、文書不足とAPI差異で完全分散は難航"
---

# I Was Right About ATProto Key Management - ATProtoの鍵管理について私が正しかった理由
Blueskyを“自前で”使おうとしたらドメインと朝を失った話 — 自分で鍵を持つ分散化の現実

## 要約
著者はATProto/Blueskyでdid:webを使って自前のPDS（Personal Data Server）上に完全分散のアカウントを作ろうとしたが、ドキュメント不足・微妙なAPI挙動・運用上のブラックリストで頓挫し、「ユーザーにPKIを丸投げするのは現実的でない」と結論付けた。

## この記事を読むべき理由
日本でも分散SNSや自前サーバ運用への関心が高まる一方、実際に個人や小規模チームが安全に鍵管理・認証を扱えるかは別問題です。本件は「分散化の理想」と「現場の運用コスト」を如実に示します。

## 詳細解説
- やったことの流れ：NixOS上でPDSを立て、did:web用の公開/秘密鍵ペアを作成、did.jsonを公開しDNSとCORSを設定、PDS上でアカウントを作成。
- 問題点1 — ドキュメント不足：各エンドポイントの説明はあるものの、アカウント作成の一連手順をまとめた公式なガイドはなく、主要情報はクローズドなGitHubコメントやDiscordに散在。
- 問題点2 — 鍵の不整合：getRecommendedDidCredentialsが返すJSONとDID文書のフォーマットが微妙に違い、手動でキーを編集する必要があった。API説明は「マイグレーション用」と書かれており、新規作成ケースは想定外。
- 問題点3 — アカウント状態とブラックリスト：途中でアカウントを削除したらAppView側でdid:webが使えなくなり、結果的に公式サポート（中央管理）に頼らざるを得ない状況に。完全分散の「体験」は事実上成立していない。
- 本質的示唆：鍵管理（PKI）はユーザーに委ねられるとエラーや運用負荷が爆発する。Mastodonの初期セットアップより難しい、という現場感が出ている。

## 実践ポイント
- 初めてPDS/did:webを触る人は、本番移行前に検証用ドメインで手順を何度も試す。削除は慎重に。  
- getRecommendedDidCredentialsの出力とDIDフォーマットの違いを確認し、必要な変換を自動化するスクリプトを用意する。  
- CORSやDNSなどの環境設定は想定より重要。did.json配信時のHTTPヘッダ確認を忘れずに。  
- 公式ドキュメントが不十分な場合は、DiscordやGitHubの議論を追い、作業ログ（curlコマンドやサーバログ）を残す。  
- 小規模運用者は、今のところ完全自前運用よりも信頼できるホスト／コミュニティPDSの利用を検討するのが現実的。

（参考：元記事は作者の実体験レポートで、ATProtoの現状運用コストを率直に指摘しています。）
