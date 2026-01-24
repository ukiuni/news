---
layout: post
title: "Microsoft confirms it will give the FBI your Windows PC data encryption key if asked — you can thank Windows 11's forced online accounts for that - マイクロソフト、法的要請があればPCのBitLocker鍵をFBIに提供すると公表 — Windows 11のオンラインアカウント義務が原因"
date: 2026-01-24T03:00:53.496Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.windowscentral.com/microsoft/windows-11/microsoft-bitlocker-encryption-keys-give-fbi-legal-order-privacy-nightmare"
source_title: "Microsoft gave FBI BitLocker keys, raising privacy fears | Windows Central"
source_id: 419140989
excerpt: "Windows11の既定でBitLocker回復キーがMSに保存され、法的要請でFBIへ提供され得る"
image: "https://cdn.mos.cms.futurecdn.net/RR6euwrPY7cVqtXtgx7DMV-2048-80.jpg"
---

# Microsoft confirms it will give the FBI your Windows PC data encryption key if asked — you can thank Windows 11's forced online accounts for that - マイクロソフト、法的要請があればPCのBitLocker鍵をFBIに提供すると公表 — Windows 11のオンラインアカウント義務が原因

Windows 11の既定設定でBitLocker回復キーがMicrosoftアカウントに自動保存されており、法的根拠があればMicrosoftがその鍵をFBIなどに引き渡すと認めた—プライバシー上の大きな懸念。

## 要約
Microsoftは有効な法的命令があればクラウドにバックアップされたBitLocker回復キーを提供すると表明。Windows 11のMicrosoftアカウント必須化が、知らぬ間に鍵をクラウドへ保存させる原因になっている。

## この記事を読むべき理由
日本でもWindows 11導入が進む中、既定の設定で暗号化回復鍵がクラウドへ保存され、捜査機関の要請で共有され得ることは個人・企業いずれにも重要なプライバシー／コンプライアンス問題だから。

## 詳細解説
- BitLockerの回復キーは、暗号化されたドライブを復号するための“最後の手段”で、通常は48桁の回復キー（数字）で管理される。これがあればデータへアクセス可能になる。  
- Windows 11でMicrosoftアカウント（MSA）を使ってセットアップすると、既定でその回復キーがユーザーのMicrosoftアカウントにバックアップされる。これはユーザーがローカルでロックアウトされた際の復旧を容易にするため。  
- MicrosoftはForbesなどへの説明で、法的に有効な要求（FBIからの法的命令等）があれば、クラウド保存されたBitLocker回復キーを提供すると明言した。過去にグアムの捜査でキーが引き渡された事例が報じられている。  
- 同社は年に約20件のリクエストを受けるが、多くはキーがクラウドに存在しないため対応不能だったとも述べている。  
- 技術的には、クラウドに保存された回復キーがサーバー側でさらに暗号化されておらず、Microsoft側で参照可能な状態にある点が問題視されている。対照的にAppleは過去に当局の要求に抵抗した例がある。Metaなどは鍵をサーバー側で暗号化する方式を採ることがある。  
- 企業環境ではAzure AD/Intune等によるキー管理ポリシーが適用され、個人用MSAとは挙動が異なる点に注意。

## 実践ポイント
- まず確認：Microsoftアカウントの回復キー管理ページ（account.microsoft.com/devices/recoverykey）で、自分のデバイスに回復キーが保存されているか確認し、不要なら削除する。  
- 回復キーのクラウド保存を避ける方法：セットアップ時にローカルアカウントを使う（回避が難しい場合は手順を調べる）、またはBitLockerの回復キーをUSBや紙にオフライン保存する。  
- 組織デバイスではIT部門に確認：Azure ADやIntuneを介したキー管理ポリシーがあるため、勝手な変更は避ける。  
- セキュリティ設計：機密データを扱う場合は鍵の管理ポリシー（誰が、どこに、どのように鍵を保管するか）を明確化し、保存先の暗号化やアクセスログの有無を確認する。  

短く言えば、利便性のための自動バックアップが、知らぬ間に法的アクセスの経路を作る可能性がある。まずは自分の回復キーの保存状況を確認して対策を。
