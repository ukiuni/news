---
layout: post
title: "Microsoft Outlook and Teams are down | Thousands of outages reported - Microsoft Outlook と Teams がダウン | 数千件の障害報告"
date: 2026-01-23T02:03:00.901Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.wcnc.com/article/news/nation-world/is-microsoft-outlook-down-teams-outage/507-8eee4961-fa15-4dd5-9330-19ff85a81b37"
source_title: "Are Microsoft Outlook and Teams down? | Thousands of outages reported | wcnc.com"
source_id: 421302679
excerpt: "Microsoft 365で大規模障害、Outlook/Teamsが全国で接続不能—原因と即時対策"
image: "https://media.wcnc.com/assets/CCT/images/c8e6b95a-d0c5-43cb-bc2c-18f8d24c303c/20250710T142701/c8e6b95a-d0c5-43cb-bc2c-18f8d24c303c_1140x641.jpg"
---

# Microsoft Outlook and Teams are down | Thousands of outages reported - Microsoft Outlook と Teams がダウン | 数千件の障害報告
魅力的なタイトル: 「国内企業も他人事じゃない——Microsoft 365大規模断続障害、対策と現場で今すぐできること」

## 要約
2026年1月22日、北米のインフラ不具合によりMicrosoft 365（Outlook・Teams含む）で数万件規模の接続障害が発生。Microsoftはトラフィックの再振り分けとインフラ復旧を実施している。

## この記事を読むべき理由
Outlook/Teamsは日本の企業でも業務基盤として広く使われており、停止は業務継続に直結します。原因と復旧方針を理解し、現場で取るべき対策を知ることは今すぐ役立ちます。

## 詳細解説
- 発生状況：現地時間2026年1月22日午後3時ごろ、DownDetectorなどに数万件の障害報告が集約。報告内訳は Microsoft 365 関連で約1.5万件、Outlookで約1.2万件、Teamsで約500件（ピーク時）。その後報告数は段階的に減少し、夕方には約3,000件まで落ち着いた。  
- 原因：Microsoftは「北米の一部サービスインフラが期待どおりにトラフィックを処理していない」と述べ、インフラ側の問題と発表。インシデントIDは MO1221364、詳細は status.cloud.microsoft に掲載。  
- 対応：当初は「該当インフラを健全な状態に戻す」作業を行い、その後トラフィックを代替インフラに迂回（ロードバランシング／リバランシング）して復旧を図った。前日（1/21）にもサードパーティのネットワーク問題で短時間の障害が発生しており、続発している点は注目に値する。  
- 技術的視点：クラウドサービスはリージョン/インフラの冗長化で回復力を高めるが、トラフィック制御（ロードバランス、ルーティング）と依存するネットワーク経路の問題が複合すると短時間で広域障害を招く。サービスヘルスやインシデントIDを追跡し、テナント側でのメッセージセンターやログ確認が重要。

## 実践ポイント
- 緊急連絡経路を確保する：社内で別のチャネル（Slack、SMS、電話、社内ポータル）を事前に合意しておく。  
- 管理者が確認すべき項目：Microsoft 365 管理センターの Service health、Message center、Azure status、インシデントID（MO1221364）を監視。  
- ユーザー向け指示：Outlookで送受信できない場合はWeb版やキャッシュ（OST/PST）からの作業、Teamsが使えない場合は代替ツールで会議やチャットを実施する。  
- 予防措置：重要ワークフロー（認証、メール配信、会議）はマルチプロバイダー冗長化を検討。外部接続やプロキシ、NWベンダー依存の影響を洗い出す。  
- 事後対応：障害ログ、影響範囲、業務影響報告をまとめ、BCP/改善策（SLA見直し、フェイルオーバー設計）を更新する。

短時間で復旧したケースでも、継続的な依存度の見直しと具体的な代替手順の用意が日本の現場には不可欠です。
