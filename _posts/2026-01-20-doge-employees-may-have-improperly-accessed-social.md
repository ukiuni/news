---
layout: post
title: "DOGE employees may have improperly accessed social security data, DOJ says - DOGE職員が社会保障情報へ不正アクセスか、米司法省が提出書類で指摘"
date: 2026-01-20T22:37:10.921Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.axios.com/2026/01/20/doge-employees-social-security-information-court-filing?utm_campaign=editorial&amp;utm_sf_cserv_ref=1830665590513511&amp;utm_sf_post_ref=655924993&amp;utm_source=facebook&amp;utm_medium=organic_social&amp;fbclid=IwdGRzaAPcyahleHRuA2FlbQIxMQBzcnRjBmFwcF9pZAwzNTA2ODU1MzE3MjgAAR54FH-rFK-TRMAdA-zEbNq8tCvH6acdR4sm-g-Wvcp4h7iKrfx5YfB9i1ie3A_aem_41toMhiB9Cuo6IcEJ-zqLQ"
source_title: "DOGE employees may have improperly accessed social security data, DOJ says"
source_id: 421756516
excerpt: "DOGE職員が裁判制限を破りSSA個人データを外部サーバーに移した疑い"
---

# DOGE employees may have improperly accessed social security data, DOJ says - DOGE職員が社会保障情報へ不正アクセスか、米司法省が提出書類で指摘

マイナンバー級の“個人情報”が外部サーバーに流出した可能性――米政府の内部データ取扱いで浮上した重大な統制欠陥

## 要約
米司法省の裁判提出書類によれば、DOGEチームの少なくとも数名が社会保障局（SSA）のデータへ裁判所の制限に反してアクセスし、未承認の外部サーバーにデータを置いた可能性があると報告されました。さらに一部職員は政治団体と接触しており、職務と政治活動の境界も問題視されています。

## この記事を読むべき理由
個人情報を扱うシステムの運用ミスは、技術的な問題だけでなく法的・政治的リスクを同時に生む点は日本の企業・自治体にも他山の石です。マイナンバーや住民情報を扱う組織の担当者や開発者は、実務で直ちに確認すべきポイントが含まれています。

## 詳細解説
- 何が起きたか：米司法省の提出によると、DOGEチームの職員がSSAの制限下にあるデータにアクセスしたり、第三者のサーバーにデータを保存した疑いがあると明記されました。SSA側はどのデータが共有されたか、サーバー上にデータが残っているかを特定できていません。
- 政治的関与：少なくとも2名の職員は、選挙結果覆す目的で州の有権者名簿データ解析を依頼した政治団体と接触。1名は「Voter Data Agreement」に署名したとされ、ハッチ法（公務員の政治活動制限）違反の可能性でSSAは調査を進めています。
- 法的・運用上の問題点：
  - 裁判所の使用制限を超えたデータ利用（契約・裁判所命令の違反）
  - 未承認の第三者サーバー利用による管理外流出リスク
  - 監査証跡（ログ）やチェーン・オブ・カストディの欠如で影響範囲が不明瞭
  - 政治的活動との利害衝突で内部統制が弱体化
- 影響：法的責任、信頼失墜、追加の監査や制裁、データ主体への被害（不正利用や識別の危険）など。米側での“訂正”提出が示すように、記録や説明責任が曖昧になれば裁判や監査での不利が拡大します。

## 実践ポイント
- アクセス制御の見直し：最小権限（least privilege）を徹底し、役割ベースのアクセス管理（RBAC）を導入する。
- 外部サーバー禁止と例外管理：敏感データの外部アップロードを禁止し、例外は文書化・承認・期限付きで管理する。
- ログと監査：アクセスログを完全に保持し、定期的に自動で分析（SIEM/DLP）して異常を早期検知する。
- データ分類と暗号化：個人識別情報（マイナンバー等）は保存時・転送時ともに強力に暗号化する。
- 利害関係と政治活動のルール化：公務や業務データと個人的・政治的活動を厳格に分離するポリシーを整備する。
- 事前評価と契約管理：外部ベンダー利用時はセキュリティ評価と明確な契約（データ保持・削除条項、監査権限）を必須にする。
- 迅速な対応計画：インシデントレスポンス、法務・広報との連携、関係当局への報告フローを準備しておく。

米国のケースは、技術的対策だけでなく組織文化・法令順守の欠如が重大事故につながる好例です。日本でも同様のリスクが現実的に存在するため、エンジニア／運用担当者は今回の教訓を基に今すぐ社内ルールと実装を点検してください。
