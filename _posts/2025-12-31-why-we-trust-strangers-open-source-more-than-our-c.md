---
layout: post
title: "Why we trust strangers’ open source more than our colleagues’ - なぜ私たちは同僚のOSSより他人のOSSを信頼するのか"
date: 2025-12-31T05:37:58.721Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://00f.net/2025/09/01/opensource-by-internal-contributors/"
source_title: "Why we trust strangers’ open source more than our colleagues’"
source_id: 905061257
excerpt: "同僚作の優れた社内OSSが敬遠される心理と具体的対策を解説、採用チェックリストなど実務手法も紹介"
---

# Why we trust strangers’ open source more than our colleagues’ - なぜ私たちは同僚のOSSより他人のOSSを信頼するのか
社内で作られた「いいライブラリ」が敬遠される理由と、それを変えるための実務的対処法

## 要約
チームは必要な機能を外部の星があるライブラリからさっさと取ってくる一方、同じ機能を社内の同僚が公開したOSSだと急に疑念を持つ――この心理的偏向が無駄な再実装や士気低下を生む。

## この記事を読むべき理由
日本の企業は安全志向や階層文化が強く、内製のオープンソースが正当に評価されないケースが多い。採用・管理側も開発側も、判断基準を整えれば時間と信頼を取り戻せる。

## 詳細解説
Frank DENIS氏の観察を日本向けに整理すると、主な心理要因は次の6つ。
- 社会的証明（social proof）：スターや利用実績があると“検証済み”に見える。
- 責任回避（blame avoidance）：外部の不具合なら責任が希釈されるが、社内だと責任が明確になる。
- 利益相反の疑念（conflict-of-interest）：同僚が推すと自己宣伝と受け取られやすい。
- 身近な人物の“聖化されない”効果（prophet without honor）：外部のREADMEは美化され、同僚のコミットは生々しい。
- 実感できるバスファクター（vivid bus factor）：同僚が抜けるリスクは具体的に感じられる。
- プロセスのミスマッチ：社内OSSが「外部OSS」と「内部コード」のあいだに挟まれてしまう。

結果として、有用な社内ライブラリが無視され、同じものを再実装するコストやメンテナーのモチベ低下、時にはセキュリティの逆説（身近なメンテナーを疑って外部に依存）を招く。

## 実践ポイント
- 評価基準を統一する：テストカバレッジ、リリース頻度、ドキュメント、セキュリティポリシーなど、作者ではなく品質で判断するチェックリストを作る。
- 中立的なホスティング：個人アカウントではなく組織（GitHub Org等）へ移行し、複数メンテナーを登録する。
- ガバナンス文書を用意する：貢献ルール、メンテナンス方針、退任時の引き継ぎを明記して「個人資産感」を排除する。
- 提案の切り口を工夫する：導入時は「私のプロジェクト」ではなく「OSSライブラリXの機能と利点」として提示する。
- マネジメントの介入：導入判断を個人の裁量に委ねないため、レビュー委員会やOKRで採用基準を明確にする。
- 見える化で信頼を作る：CI実行履歴、セキュリティスキャン、導入事例をダッシュボードで共有する。

短期的には「採用チェックリスト」を作るだけで導入判断が安定し、中長期では組織的ホスティングとガバナンスが社内OSSを資産に変える。

## 引用元
- タイトル: Why we trust strangers’ open source more than our colleagues’
- URL: https://00f.net/2025/09/01/opensource-by-internal-contributors/
