---
layout: post
title: "US reportedly investigate claims that Meta can read encrypted WhatsApp messages - メタが暗号化されたWhatsAppメッセージを読めるとする主張を米当局が調査か"
date: 2026-01-31T16:00:36.009Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.theguardian.com/technology/2026/jan/31/us-authorities-reportedly-investigate-claims-that-meta-can-read-encrypted-whatsapp-messages"
source_title: "US authorities reportedly investigate claims that Meta can read encrypted WhatsApp messages | WhatsApp | The Guardian"
source_id: 46836487
excerpt: "米当局が調査、メタのWhatsApp暗号解読疑惑とクラウド漏洩リスク"
image: "https://i.guim.co.uk/img/media/3b2d9e5704aa4cc63dbc19f3e9679f9ee8501778/886_311_2237_1789/master/2237.jpg?width=1200&height=630&quality=85&auto=format&fit=crop&precrop=40:21,offset-x50,offset-y0&overlay-align=bottom%2Cleft&overlay-width=100p&overlay-base64=L2ltZy9zdGF0aWMvb3ZlcmxheXMvdGctZGVmYXVsdC5wbmc&enable=upscale&s=09d4a0edadd7040772a41a23cc8ee90a"
---

# US reportedly investigate claims that Meta can read encrypted WhatsApp messages - メタが暗号化されたWhatsAppメッセージを読めるとする主張を米当局が調査か
WhatsAppの“完全な秘密”が揺らぐか？──暗号化の限界と実務的な備え

## 要約
米裁判で「MetaがWhatsAppのエンドツーエンド（E2E）暗号化メッセージを読める」とする訴訟が提起され、Bloomberg報道を受けて米当局が調査したと伝えられる。Metaは全面否定し、政府側は主張を裏付ける証拠は不確かだと述べている。

## この記事を読むべき理由
日本でもLINEやWhatsAppを使う個人・企業が多く、暗号化やメタデータの扱いに関する国際的な議論はそのまま国内のプライバシー設計や法規制に影響します。特に報道関係者や研究者、国際取引をする企業は注視すべきテーマです。

## 詳細解説
- 何が問題になっているか：原告が「Metaはほぼ全てのWhatsAppの‘私的’通信にアクセスできる」と主張。訴訟は匿名の内部告発者らの証言に基づく。Metaは「断固として事実無根」と反論している。
- 技術的核心：WhatsAppはE2E暗号化を採用しており、理論上メッセージ本文は送信者と受信者のみが復号可能。サーバー側で復号するには利用者の秘密鍵が必要で、これを無断で取得・保持するのは「数学的に不可能」に近いと専門家は指摘する。
- ただし例外と懸念点：端末側でのバックアップ（クラウド保存）、バックドア的なクライアント改変、メタデータ収集（誰が誰といつ話したか、プロフィール、連絡先同期など）は実際に可能で、プライバシーリスクを残す。訴訟ではNSOなどスパイウェア事案との関連も議論されている。
- 信頼性の争点：専門家は内部告発の真偽と証拠に懐疑的であり、米商務省からは「立証不十分」との反応もある。つまり技術的には「可能性」と「実行性／証拠」が分かれている。

## 実践ポイント
- 一般利用者
  - アプリとOSを常に最新に保つ。
  - 連絡先の自動同期やクラウドバックアップの設定を見直す（クラウドに暗号化されず保存されると本文が漏れる可能性）。
  - 高度な機密通信にはSignalなど検証済みのクライアントを検討する。
- 企業・開発者
  - データ最小化とメタデータ管理方針を明確化する。
  - 暗号仕様の第三者監査や透明性レポートを導入するようベンダーに求める。
  - 自社アプリでは端末側の鍵管理とバックアップ設計に注意し、フォワードシークレシーを確保する。
- ジャーナリスト／活動家
  - 通信の脅威モデルを再評価し、必要に応じて端末の物理保全や専用端末の運用を行う。

（元記事：The Guardian / Bloomberg 報道を基に要約・再解説）
