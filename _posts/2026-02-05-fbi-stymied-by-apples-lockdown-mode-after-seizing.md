---
layout: post
title: "FBI stymied by Apple’s Lockdown Mode after seizing journalist’s iPhone - FBIが記者のiPhoneを押収するもAppleの「ロックダウンモード」に阻まれる"
date: 2026-02-05T00:33:06.072Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://arstechnica.com/tech-policy/2026/02/fbi-stymied-by-apples-lockdown-mode-after-seizing-journalists-iphone/"
source_title: "FBI stymied by Apple&#039;s Lockdown Mode after seizing journalist&#039;s iPhone - Ars Technica"
source_id: 410361377
excerpt: "AppleのロックダウンモードがFBIの端末解析を阻み、記者の取材源保護と法的論争を浮き彫りに"
image: "https://cdn.arstechnica.net/wp-content/uploads/2026/02/iphone-and-macbook-pro-1152x648-1770243377.jpg"
---

# FBI stymied by Apple’s Lockdown Mode after seizing journalist’s iPhone - FBIが記者のiPhoneを押収するもAppleの「ロックダウンモード」に阻まれる
思わず押したくなる見出し：取材源を守る“防弾スイッチ”――AppleのロックダウンモードがFBIの解析を止めた理由と、日本の記者・技術者が知るべき対策

## 要約
米当局がワシントン・ポスト記者ハンナ・ナタンソン氏の自宅を捜索した際、押収したiPhoneは事前に「Lockdown Mode（ロックダウンモード）」が有効であったため、FBIが端末からデータを抽出できなかった。一方で、指紋で解除したMacBookからは一部のSignalメッセージが確認された。

## この記事を読むべき理由
ジャーナリストや情報管理に関わる技術者、セキュリティに敏感なビジネス層にとって、端末防御の実効性と法執行機関との境界線（技術＋法的対応）が実際の捜査でどう作用するかを示す重要な実例だからです。

## 詳細解説
- 事案の概要：2026年1月14日、ペンタゴンの請負業者による機密流出疑惑で捜索。押収物はiPhone 13（ポスト所有）、MacBook Pro（ポスト所有と個人所有）、外付け1TB、ボイスレコーダー、Garmin等。
- Lockdown Modeの効果：Appleが2022年に導入した強化モードで、メッセージ添付や未知のFaceTime発信、特定のブラウザ技術、写真共有などを制限して攻撃面を縮小する。端末ごとに手動で有効化が必要（iPhone: 設定→プライバシーとセキュリティ→Lockdown Mode）。
- 抽出の結果：FBIのCARTチームは、iPhoneは「Lockdown Mode」表示かつ通電中であったため物理イメージ（bit単位の完全複製）を取得できず、SIMの電話番号のみ抽出できた。ポスト所有のMacは指紋認証で解除され、一部のSignalメッセージは閲覧・写真保存された。個人のMacは電源オフで暗号化されており未解析。
- 法的背景（米国）：捜索令状はバイオメトリの使用を許可。捜索時に協力して指紋で解除された例があり、5th修正条項（自己負罪拒否）との関係は場面により異なる。捜査の妥当性を巡り公権力と報道の自由の対立が続く。
- 信号（Signal）について：自動消去設定のメッセージは消えるが、捜査官がスクリーン写真や音声で保存する可能性があるため「完全な自動消去＝安全」ではない。

## 実践ポイント
- すぐやること：
  - Lockdown Modeを必要な端末に有効化（iPhone/iPad: 設定→プライバシーとセキュリティ→Lockdown Mode、Mac: Appleメニュー→システム設定→プライバシーとセキュリティ）。
  - 重要データは定期的に暗号化されたオフラインバックアップを作成（ただし捜査令状がある場合、提出・保全義務に注意）。
  - バイオメトリ（指紋/顔認証）は利便性と法的リスクのトレードオフがあるため、機密性の高い端末では無効化を検討。
- 運用上の注意：
  - メッセージの自動消去は便利だが、捜査でスクリーンショット等により保存される可能性を意識すること。
  - 法的リスクがある場合は弁護士と連携し、端末保全ポリシーを社内・編集部で整備する。
- 日本向けの視点：
  - 日本でも捜査で端末押収は起こり得るため、報道機関やスタートアップは端末管理・取材源保護の手順を事前に定めておくべき。

必要であれば、読者向けに「Lockdown Modeを有効化する手順（スクリーンショット付き）」や、記者向けの端末保全チェックリストを短く作成しますか？
