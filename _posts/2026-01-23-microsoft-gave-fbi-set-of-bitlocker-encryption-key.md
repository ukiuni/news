---
layout: post
title: "Microsoft gave FBI set of BitLocker encryption keys to unlock suspects' laptops - マイクロソフトがFBIにBitLocker回復キーを提供、容疑者のノートPCを解除"
date: 2026-01-23T18:14:13.379Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://techcrunch.com/2026/01/23/microsoft-gave-fbi-a-set-of-bitlocker-encryption-keys-to-unlock-suspects-laptops-reports/"
source_title: "Microsoft gave FBI a set of BitLocker encryption keys to unlock suspects&#039; laptops: Reports | TechCrunch"
source_id: 46735545
excerpt: "マイクロソフトが保管するBitLocker回復キーをFBIに提供し、クラウド鍵の開示リスクが浮上"
image: "https://techcrunch.com/wp-content/uploads/2025/07/microsoft-store-1185699758.jpg?resize=1200,800"
---

# Microsoft gave FBI set of BitLocker encryption keys to unlock suspects' laptops - マイクロソフトがFBIにBitLocker回復キーを提供、容疑者のノートPCを解除

魅力的なタイトル: 「あなたのWindowsは本当に“自分だけ”を守るのか？　マイクロソフトがFBIにBitLocker回復キーを渡した件の意味」

## 要約
報道によると、マイクロソフトは連邦捜査でFBIにBitLockerの回復キーを提供し、3台の暗号化されたノートPCを解除した。BitLockerの回復キーは既定でマイクロソフトのクラウドに保存されるため、法執行機関やクラウド侵害のリスクが問題になっている。

## この記事を読むべき理由
多くの日本の個人・企業が標準で有効なBitLockerやMicrosoftアカウントを使っており、キー管理と法的要求が直接データ保護やコンプライアンスに影響するため。クラウドに預けた鍵が第三者（捜査機関や攻撃者）に利用される可能性は、日本でも無視できない問題です。

## 詳細解説
- 何が起きたか：Forbes報道によれば、グアムでの不正受給事件の捜査で、マイクロソフトはFBIへ3台分のBitLocker回復キーを提供。回復キーは暗号化解除に使えるマスターキー。
- なぜ可能か：多くのWindowsデバイスではBitLocker回復キーが既定でユーザーのMicrosoftアカウントやAzure ADにアップロードされるため、マイクロソフト側にキーのコピーが存在する。法的根拠があれば企業は当該キーを当局に渡すことがある。
- セキュリティの懸念：暗号化の主目的は「デバイス紛失時に第三者が読めないこと」だが、クラウド保存によりクラウド事業者や要求側がアクセス可能となる。暗号鍵がクラウドで管理されることは、クラウド侵害や法的開示のリスクを伴う。暗号専門家はマイクロソフトの鍵管理を他業界と比較して問題視している。
- 制約：仮にクラウドから回復キーが漏洩しても、攻撃者は物理ドライブへのアクセスが必要（盗難や押収）が前提。だが物理アクセスと鍵の組合せでデータが復元され得る。

## 実践ポイント
- 個人：Microsoftアカウントに保存された回復キーを確認・削除する（account.microsoft.com → デバイス管理）し、アカウントに強力なMFAを設定する。
- 企業：BitLocker鍵管理ポリシーを見直す（Azure AD/Intuneの既定動作、キーのバックアップ先、顧客管理キーの採用）。法務と連携して法執行機関からの開示要求に備える。
- 技術対策：TPM + PINなど物理的アクセスと別要素を組み合わせる、顧客管理型のキー管理（HSM／KMS）を検討する。
- コンプライアンス観点：APPIや社内機密基準に照らし、クラウド保存の鍵が与える法的・運用リスクを評価する。

以上。
