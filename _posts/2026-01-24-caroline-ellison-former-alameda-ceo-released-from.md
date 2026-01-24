---
layout: post
title: "Caroline Ellison, Gary Wang, and Nishad Singh - キャロライン・エリソン、ゲイリー・ワン、ニシャド・シンに関するSEC裁判報告"
date: 2026-01-24T04:00:15.556Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.sec.gov/enforcement-litigation/litigation-releases/lr-26450"
source_title: "Caroline Ellison Former Alameda CEO Released from Prison After 440 Days"
source_id: 46740644
excerpt: "元Alameda CEOエリソンらがSECと和解、顧客資金流用と役員禁止の詳細判明"
---

# Caroline Ellison, Gary Wang, and Nishad Singh - キャロライン・エリソン、ゲイリー・ワン、ニシャド・シンに関するSEC裁判報告
元FTX/Alamedaで何が起きたのか——顧客資金が「例外扱い」としてソフトウェアで流用された疑惑の全貌

## 要約
SECは、FTXとその関連ヘッジファンドAlamedaに関する訴訟で、元Alameda CEOのCaroline Ellison、元FTX CTOのGary Wang、元エンジニアのNishad Singhに対する最終合意判決を提出。彼らは顧客資金の不正な流用などを巡るSECの主張を争わずに和解（同意判決）に応じた。

## この記事を読むべき理由
暗号資産サービスの裏で「技術とガバナンスの欠陥」が資金流出を招く事例は、プロダクト開発者やインフラ担当者、投資家すべてにとって他人事ではない。日本でも仮想通貨交換業やブロックチェーンプロジェクトの安全設計と信頼確保が重要だからです。

## 詳細解説
- 争点の概要：SECは2019年5月〜2022年11月の間に、FTXが「顧客資産を保護する高度なリスク管理機能を持つ安全な取引所」として資金を約18億ドル超集めたが、実際にはAlamedaに特別扱い（リスク緩和を適用しない、事実上の無制限の与信）をして顧客資金を移転していたと主張。  
- 役割分担：Ellison（元Alameda CEO）は流用された資金をAlamedaの取引に使用したとされ、WangとSinghは顧客資金をAlamedaへ振り向けるソフトウェアコードを作成したとされる。Samuel Bankman‑Friedの指示の下、複数の幹部に資金が回っていたとSECは述べる。  
- 法的結末：当事者らはSECの主張を否認せず最終合意判決に同意（裁判所承認待ち）。結果として、詐欺禁止規定（Securities Exchange Act §10(b), Rule 10b‑5 等）違反を禁じる恒久的差止め、5年の行動制限的差止め、さらにEllisonは10年、WangとSinghは8年の役員・取締役就任禁止などが科される見込み。  
- 技術的ポイント：指摘されるのは「コードレベルでのアクセス制御と業務分離の欠如」「リスク緩和ルールの例外化を可能にする設定／権限設計」「監査証跡（ログ）や独立した監督の不在」。これがあれば、運用側の恣意的な資金移動が技術的に実行可能になってしまう。

## 実践ポイント
- 開発者/エンジニア向け：権限分離（least privilege）、コードレビュー、自動化された監査ログ、異常検知ルールを設計段階で組み込む。重要処理は複数署名・多段認可にする。  
- プロダクト/運用責任者向け：リスク緩和ルールを明文化し、例外運用の承認プロセスを独立部門で実施する。外部監査・第三者の定期レビューを導入。  
- 投資家/一般利用者向け：取引所やカストディアンの「顧客資産分別管理」「外部監査」「規制当局への登録状況」を確認する。約束されたリスク管理の具体的実装（例：独立した保管方法や証跡）を問いただす。

（出典：U.S. Securities and Exchange Commission Litigation Release No. 26450）
