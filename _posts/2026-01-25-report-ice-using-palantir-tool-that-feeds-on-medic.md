---
layout: post
title: "Report: ICE Using Palantir Tool That Feeds On Medicaid Data - レポート：ICEがメディケイド（Medicaid）データを吸い上げるPalantirツールを使用中"
date: 2026-01-25T20:13:32.361Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.eff.org/deeplinks/2026/01/report-ice-using-palantir-tool-feeds-medicaid-data"
source_title: "Report: ICE Using Palantir Tool That Feeds On Medicaid Data | Electronic Frontier Foundation"
source_id: 417778159
excerpt: "ICEがMedicaid住所をPalantirで解析し摘発候補を地図化、個人情報流用と誤検知の恐れ"
image: "https://www.eff.org/files/banner_library/surveillance-og-2.png"
---

# Report: ICE Using Palantir Tool That Feeds On Medicaid Data - レポート：ICEがメディケイド（Medicaid）データを吸い上げるPalantirツールを使用中
ICEが「住所データで人を地図化」するAIツールで摘発候補を割り出す──あなたの個人情報はどこまで繋がるか？

## 要約
米国移民税関取締局（ICE）が、Palantir製のELITEというツールで保健福祉局（HHS）のメディケイドなどの住所データを取り込み、潜在的な摘発対象の位置を地図上にプロットし「信頼度スコア」を付与していると報じられました。

## この記事を読むべき理由
行政が本来の目的（医療や福祉）で集めたデータを捜査・摘発目的に再利用すると、プライバシー侵害や誤検知による人権侵害が起きます。日本でも行政データの連携や民間製解析ツールの導入が進む中、同種のリスクと対策を知っておく必要があります。

## 詳細解説
- ツールの概要：ELITE（Enhanced Leads Identification & Targeting for Enforcement）はPalantirが構築した分析プラットフォームで、住所データを含む複数ソースを統合し、地図表示・個人ごとの「ドシエ（プロファイル）」生成・住所の「confidence score（信頼度）」を算出して摘発候補を抽出する機能を持つとされます。
- データ流れ：HHS（Medicaidを含む）などの政府データが入力され、Palantirの検索可能なインターフェイスで個人の移動履歴や居住可能性を推定している点が問題視されています。
- 技術的リスク：
  - データ統合による目的外利用：各部署が収集したデータを横断照合すると本来想定されない用途に使われる。
  - 誤検知とバイアス：住所更新の遅れ、共有住所、データ欠落により高い誤検知率が生じやすく、スコアは誤った行動につながる可能性がある。
  - 監査不在：商用プラットフォームによるブラックボックス化で意思決定過程の説明責任が低下する。
- 法的・社会的対応：EFFなど市民団体は訴訟やアミカスブリーフで異議を申し立て、行政データ活用の透明性と制約を求めています。

## 実践ポイント
- 自治体・企業向け
  - データ最小化：収集と共有は目的限定で行う。住所など敏感情報は必要最小限に。
  - PIA（プライバシー影響評価）を実施し、外部監査を義務化する。
  - アルゴリズムの説明可能性と誤判定対策（ヒューマン・レビュー）を導入する。
- 個人向け
  - 行政に提出する住所情報の扱いについて開示請求や問合せを行う。
  - 市民団体や議員に透明性・法的規制の強化を求める。
- 日本市場への示唆
  - 日本の個人情報保護法（APPI）や自治体のデータ連携の運用は今後ますます注視が必要。調達時にプライバシー条項と監査権を入れることを推奨。

出典：Electronic Frontier Foundation（報道要旨に基づく要約）。
