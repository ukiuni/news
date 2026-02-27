---
layout: post
title: "Tenth Circuit: 4th Amendment Doesn't Support Broad Search of Protesters' Devices - 第10巡回控訴裁判所：第4修正は抗議者のデバイスの広範な捜索を支持しない"
date: 2026-02-27T16:18:50.710Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.eff.org/deeplinks/2026/02/victory-tenth-circuit-finds-fourth-amendment-doesnt-support-broad-search-0"
source_title: "Victory! Tenth Circuit Finds Fourth Amendment Doesn’t Support Broad Search of Protesters’ Devices and Digital Data | Electronic Frontier Foundation"
source_id: 47181391
excerpt: "第10巡回、抗議者の端末丸ごと捜索を違法と断じ、令状の範囲に判例的制限"
image: "https://www.eff.org/files/banner_library/protest-2024-2.jpg"
---

# Tenth Circuit: 4th Amendment Doesn't Support Broad Search of Protesters' Devices - 第10巡回控訴裁判所：第4修正は抗議者のデバイスの広範な捜索を支持しない

デバイス丸ごと捜索は許されない――米控訴裁判所が示した「デジタル時代の捜索の線引き」

## 要約
米国の第10巡回控訴裁判所が、抗議参加者や団体のデバイス・ソーシャルメディアを対象とした「無制限かつ広範な」捜索令状を問題ありと判断し、下級審の却下を覆しました。

## この記事を読むべき理由
デジタルデータが刑事捜査で頻繁に対象になる今、捜査令状の範囲や捜査機関の免責（qualified immunity）がどこまで許されるかは、プライバシーやプロダクト設計、企業対応に直結します。日本でも捜査時のデータ提出要請や事業者対応が増える中、設計や運用の指針になります。

## 詳細解説
- 事件名と経緯：Armendariz v. City of Colorado Springs。2021年の住宅抗議で逮捕された参加者に対し、警察は写真・動画・メール・メッセージ・位置情報を2か月分捜索する令状と、「bike」「assault」「right」など26語を無期限で検索する令状を取得。団体（Chinook Center）のFacebookページも捜索対象に。
- 裁判所の判断：第10巡回は、令状が「特定性（particularity）」を欠き過度に広範（overbroad）であると指摘。各令状について詳細に検討し、顔ぶれや期間・キーワードの範囲が問題であると認め、下級審の却下を取り消し訴訟継続を命じた。
- 重要な法的ポイント：
  - 第4修正（不当な捜索・押収の禁止）の観点で、デジタルデータでも令状の範囲は厳格に問われる。
  - 「明確に確立された法（clearly established law）」に反する行為と判断され、令状発行時の捜査官はqualified immunity（公務員免責）を認められないとした点が稀で重い意味を持つ。
  - 第1修正（表現の自由）については結論を出していないが、捜索の背景にある警察の敵意（animus）に言及している。
- 意味合い：控訴裁のこの判断は、デバイス全体の「丸ごと捜索」や時間無制限でのキーワードスキャンに歯止めをかける先例になり得る。

## 実践ポイント
- プロダクト設計：最小限のデータ保持とアクセス分離、ログの粒度を下げる（不要なメタデータを保存しない）。
- 暗号化：端末側／エンドツーエンド暗号化を採用し、企業がアクセスできない設計を検討する。
- 法務・対応フロー：捜査要請を受けた際の社内プロセスを整備し、過度に広い要求には法的異議申立てを検討する。
- 透明性：透明性レポートやユーザー通知ポリシーを整え、信頼を維持する。
- コミュニティ対応：市民権・表現の自由に関わる案件ではNGOや弁護団と連携する準備をしておく。

この記事は、データ保護と捜査のバランスを考える上で、日本の開発者・事業者にも直接役立つ教訓を含んでいます。
