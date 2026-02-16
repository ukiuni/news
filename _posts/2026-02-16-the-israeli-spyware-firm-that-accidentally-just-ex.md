---
layout: post
title: "The Israeli spyware firm that accidentally just exposed itself - うっかり自社を暴露したイスラエルのスパイウェア企業"
date: 2026-02-16T14:00:00.783Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://ahmedeldin.substack.com/p/the-israeli-spyware-firm-that-accidentally"
source_title: "The Israeli Spyware Firm That Accidentally Just Exposed Itself"
source_id: 47033976
excerpt: "LinkedIn誤投稿で露見、Graphiteがスマホを無操作で丸裸に"
image: "https://substackcdn.com/image/fetch/$s_!-Wnv!,w_1200,h_675,c_fill,f_jpg,q_auto:good,fl_progressive:steep,g_auto/https%3A%2F%2Fpbs.substack.com%2Fmedia%2FHA5T-uhboAAD2xT.jpg"
---

# The Israeli spyware firm that accidentally just exposed itself - うっかり自社を暴露したイスラエルのスパイウェア企業
LinkedIn写真で明かされた「Graphite」の正体：あなたのスマホが丸見えになる瞬間

## 要約
イスラエルの監視企業ParagonがLinkedInにスパイウェア管理画面の写真を誤投稿し、ゼロクリックで端末を侵害する高精度スパイウェア「Graphite」の実装と運用実態が露呈した。これは商業的な監視産業の構造と、その被害範囲を示す稀な透明化の事例だ。

## この記事を読むべき理由
日本でも政府機関や企業、ニュース関係者が標的になり得るため、端末侵害の実態と対策を理解することは必須。海外で起きた「運用ミス」が示した攻撃手法と流通経路は、日本のセキュリティ対策や調達監査にも直結する問題です。

## 詳細解説
- Graphiteの特徴：ゼロクリックのエクスプロイト連鎖でユーザー操作なしに端末を乗っ取り、OSレベルで永続化して
  - 端末内データ、アプリ内メッセージ（暗号化前後のアクセス含む）
  - マイク・カメラの遠隔起動
  - 連絡先・メディア・アプリアカウント情報の抽出
 という広範な可視化を実現する。
- OPSECの失敗：Paragonの法務担当が投稿した写真に、実際の監視対象番号、アプリ別の取得ステータス、抽出データが写っており、運用インターフェースの構造が暴露された。研究者はこれを“epic OPSEC fail”と評価。
- ベンダーの主張と現実：Paragonは「選択的なアクセス」「アプリ内で完結」と主張したが、Citizen Labなどの調査ではデバイス単位での侵害は結局全てにアクセス可能になると指摘される。
- エコシステムと資金：民間投資による巨額買収（記事は約9億ドル、関係者の巨額報酬を指摘）で監視技術がスケールし、元軍情報組織出身者が人材供給する“監視商業化”が進行している。
- 政府調達と拡散：報道では米国の移民管理機関などへの導入記録が示唆され、軍事・治安用途から民間・行政へ技術が流通するリスクが明示された。

## 実践ポイント
- OS・アプリを常に最新に保ち、ゼロデイ対策のある端末を導入する。  
- 機密性の高い業務は端末分離（業務端末と私用端末を分ける）やハードウェアベースの隔離を検討する。  
- エンドポイント検知（EDR）とサプライチェーン／ベンダー監査を強化し、調達先の透明性を要求する。  
- ジャーナリスト・活動家・ハイリスクユーザーは多層化した運用（物理的隔離、最小権限、定期的なセキュリティチェック）を徹底する。  
- 組織としてはインシデント対応計画・ログ収集・外部の脅威インテリジェンスを整備し、疑わしいベンダー露出（SNSでの機密情報流出など）を監視する。

以上。
