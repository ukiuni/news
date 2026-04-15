---
layout: post
title: "Cal.com is going closed source - Cal.comがクローズドソースになります"
date: 2026-04-15T19:47:39.255Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://cal.com/blog/cal-com-goes-closed-source-why"
source_title: "Cal.com Goes Closed Source: Why AI Security Is Forcing Our Decision | Cal.com - Scheduling Software for Online Bookings"
source_id: 47780456
excerpt: "AI脅威を受けCal.comが本番コードを非公開化、顧客保護とCal.diy維持"
image: "https://framerusercontent.com/images/kbv1qXf6TM85jTRqb8m0ToBSh8.png?width=1000&amp;height=595"
---

# Cal.com is going closed source - Cal.comがクローズドソースになります
オープンソースを手放した理由：AIが「設計図」を悪用する時代の現実

## 要約
Cal.comは顧客データ保護を優先し、メインのプロダクションコードを非公開化。趣味・自己ホスト向けにMITライセンスの「Cal.diy」は残すと発表した。

## この記事を読むべき理由
AIによる自動的な脆弱性発見が進む中、オープンソースの公開がセキュリティリスクになる可能性は、日本のSaaS導入企業や開発者にも直接関係するため。

## 詳細解説
- 背景：従来は高度なスキルと時間が必要だった脆弱性発見が、現代の大規模言語モデルや自動化ツールで短時間に行えるようになった。公開リポジトリは攻撃者にとって「設計図」になり得る。
- 具体例：Cal.comは過去5年のオープンソース方針を見直し、AIでのプロービングが増えたためプロダクションをプライベートへ移行。認証やデータ処理周りを大幅に書き直したと説明している。
- 対応の二本立て：企業向けにクローズドで安全性を高めつつ、自己ホストや学習用のCal.diy（MIT）をコミュニティ向けに維持することで、オープン精神と顧客保護のバランスを取ろうとしている。
- セキュリティ潮流：自動化されたAIペネトレーションテストやツール群が増え、従来の周期的なセキュリティ検査では追いつかないという業界課題が露呈している。

## 実践ポイント
- Cal.comユーザーは公式の移行・セキュリティ説明を確認し、契約・データ処理の変更点をチェックする。
- 実運用で機密データを扱う場合は、ベンダーのセキュリティ評価（SLA、監査報告、脆弱性対応体制）を必ず確認する。
- 自己検証や学習目的ならCal.diyを試すが、本番用途では認証・データ保護が強化されたプロダクション版を優先すること。
- 開発チームは「シフトレフト」な脆弱性検出（SAST/DAST/SCA）、CIでの自動スキャン、ランタイム監視などを強化しておく。
- 日本企業はデータローカリティや法令（個人情報保護）との整合性を再確認し、必要ならオンプレ／国内リージョン提供の有無を確認する。

（出典：Cal.com公式ブログ「Cal.com is going closed source」）
