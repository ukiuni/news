---
layout: post
title: "A new California law says all operating systems need to have age verification - カリフォルニア州の新法、全OSに年齢確認を義務化"
date: 2026-02-27T22:55:13.817Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.pcgamer.com/software/operating-systems/a-new-california-law-says-all-operating-systems-including-linux-need-to-have-some-form-of-age-verification-at-account-setup/"
source_title: "A new California law says all operating systems, including Linux, need to have some form of age verification at account setup | PC Gamer"
source_id: 47181208
excerpt: "カリフォルニア新法で全OSに年齢確認義務化—LinuxやIoTまで実務対応が必須に"
image: "https://cdn.mos.cms.futurecdn.net/Z9XbAPKf32a28g9TdTi8dG-1920-80.jpg"
---

# A new California law says all operating systems need to have age verification - カリフォルニア州の新法、全OSに年齢確認を義務化
全OS対象の年齢確認義務化が意味するもの：Linuxまで影響、あなたのPCやアプリはどう変わるか？

## 要約
カリフォルニア州の法案（AB 1043）が2027年1月1日施行され、OS提供者はアカウント作成時に年齢情報を取得し、開発者に年齢区分を返すためのAPIを用意することを義務付けます。

## この記事を読むべき理由
カリフォルニア発の規制はグローバルなサービス運用に波及しやすく、日本のOSベンダーやアプリ開発者、オープンソースコミュニティにも実務的・法務的影響が出るため、早めの準備が必要です。

## 詳細解説
- 法的要件：AB 1043はOS提供者に対し、アカウント作成で生年月日や年齢の入力インターフェイスを設け、開発者が要求した場合に「未満13歳／13～15歳／16～17歳／18歳以上」の4区分の年齢シグナルをリアルタイムAPIで返せることを求めます。  
- 実装の範囲：生体認証（顔スキャン等）を直接義務化しているわけではありませんが、年齢確認の「何らかの形」を収集・伝達する責務があります。  
- 技術的課題：オープンソースOS（多くのLinux配布物）はユーザベースの特定や地域別適用が難しく、どのように「カリフォルニア居住者だけ」に適用するか、あるいはグローバルに適用するかで議論が分かれる可能性があります。  
- プライバシー懸念：UKの事例やDiscordの年齢認証で問題になったように、第三者プロバイダによる過剰なデータ収集・利用や、個人データ保持のリスクが指摘されています。  
- 影響範囲：デスクトップOSに限らず、スマホ系OS、組み込み機器、IoTデバイス、そしてアプリストアの運営側も年齢シグナルを受け取って表示や機能を変える必要が出てきます。

## 実践ポイント
- プロダクト担当者：アカウント作成フローを見直し、日付/年齢入力と年齢区分を返すAPI設計を検討。法務と連携し規約とデータ保持方針を更新。  
- 開発者：年齢シグナルを受け取る想定でアプリ側のアクセス制御・コンテンツフィルタを実装。最小限のデータ利用設計（目的限定・短期保持）を採用。  
- OSS/ディストリビューション管理者：カリフォルニア特有の対応案（地域限定の表示や注意書き、構築済みオプションの提供）を検討。コミュニティで方針を早めに決定する。  
- プライバシー保護派：より侵襲の少ない手法（自己申告の年齢区分、ゼロ知識証明など）の採用や、外部認証プロバイダの監査を要求する。

この法は現時点でカリフォルニア州法ですが、実務コストとリスクを最小化するために、関連する事業者は今すぐ影響評価と対応計画を始めるべきです。
