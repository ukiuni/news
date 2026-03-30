---
layout: post
title: "Fedware: Government apps that spy harder than the apps they ban - Fedware：禁止アプリ以上にスパイする政府アプリ"
date: 2026-03-30T19:53:03.203Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.sambent.com/the-white-house-app-has-huawei-spyware-and-an-ice-tip-line/"
source_title: "Fedware: 13 Government Apps That Spy Harder Than the Apps They Ban"
source_id: 47577761
excerpt: "ホワイトハウスやICE含む政府公式アプリが位置・生体・端末データを大量収集し密かに追跡"
image: "https://www.sambent.com/content/images/size/w1200/2026/03/feature-final-v2.jpg"
---

# Fedware: Government apps that spy harder than the apps they ban - Fedware：禁止アプリ以上にスパイする政府アプリ
米政府アプリが“スパイ”している？ホワイトハウスからICEまで、隠れた監視パイプラインの全貌

## 要約
米国連邦政府の公式アプリ群が、過剰な権限やサードパーティ追跡を組み込み、公開情報を配信する一方で大量の個人データを収集・共有していると報告されています。

## この記事を読むべき理由
政府アプリ＝安全とは限らない現実は、日本でも他人事ではありません。災害情報や出入国、税・保険など生活に直結するアプリの権限をどう扱うか、実務的な判断力が求められます。

## 詳細解説
- 調査方法と呼称  
  セキュリティ研究者がGoogle Playの連邦政府アプリをExodus Privacyなどで解析し、「Fedware」と命名。トラッカー埋め込みや過剰なAndroid権限のパターンを指摘しています。

- 典型的な技術問題点（例）  
  - ホワイトハウス公式アプリ：位置情報（精密GPS）、指紋などの生体認証、外部ストレージ編集、起動時自動実行、他アプリ上描画、Wi‑Fiスキャン等を要求。HuaweiのSDKなど追跡ライブラリを同梱。  
  - FBIアプリ：複数のトラッカー（例：Google AdMob）を含み、端末IDや利用情報を広告目的で扱う可能性。  
  - FEMA（災害情報）アプリ：28個の権限要求。通知や天気表示だけなら過剰なケース。  
  - CBP（税関入国）系：背景位置追跡、カメラ、生体認証、外部ストレージのフルアクセスを要求。顔情報は最長75年保持とされる資料が示唆。  
  - ICE向けアプリ群（Mobile Fortify、SmartLINK等）：数億件規模の顔画像DBや位置・音声・妊娠情報などセンシティブなデータを収集・共有。外部企業（例：Clearview AI）との契約も報告。  
  - データブローカー（例：Venntel）：多数の民間アプリ経由で毎日数十億の位置データを販売。最高裁判決での保護の抜け道になり得る。

- ガバナンス上の課題  
  GAOの勧告未実施や、IRSとICEのデータ共有ミスなど、監督・透明性不足が構造的な問題を露呈しています。

- なぜアプリが「必要」とされるのか  
  ウェブやRSSで済む情報でも、アプリなら生体・バックグラウンドGPS・端末情報にアクセスできるため、監視・データ収集の手段として使われやすい点が指摘されています。

## 実践ポイント
- まずは疑う：政府公式アプリでも権限を確認し、不要ならインストールしない。  
- 権限を最小化：Androidの権限管理で位置やマイク、生体などをオフにする。  
- 代替手段を使う：公式情報はブラウザやRSS、公式メール配信で受け取れる場合が多い。  
- アプリ解析を活用：Exodus PrivacyやApp permissionsチェッカーで追跡ライブラリと権限を確認。  
- 組織的対応：企業や自治体のIT担当は同様の権限設計を自組織で点検し、APPI（個人情報保護法）等に基づくリスク評価を行う。

短く言えば：公式アプリだから安心、はもう通用しない。まず権限とトラッカーを確認して、必要ならブラウザや安全な手段で情報を受け取りましょう。
