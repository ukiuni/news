---
layout: post
title: "Convincing Is Not Persuading - 「説得（Convincing）と動かすこと（Persuading）は別物」"
date: 2026-03-22T15:42:40.780Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://blog.alaindichiappari.dev/p/convincing-is-not-persuading"
source_title: "Convincing Is Not Persuading - by Alain Di Chiappari"
source_id: 47477068
excerpt: "正論だけでは通らない理由と相手を動かす実践戦略を具体的に示す"
image: "https://substackcdn.com/image/fetch/$s_!Rw6r!,w_1200,h_675,c_fill,f_jpg,q_auto:good,fl_progressive:steep,g_auto/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb8ddf511-ce4b-4fe8-9027-7756344314fa_1920x1315.webp"
---

# Convincing Is Not Persuading - 「説得（Convincing）と動かすこと（Persuading）は別物」
正論だけでは人は動かない：技術提案が通らない本当の理由

## 要約
論理的に正しい提案（＝説得）は必要だが不十分で、相手の感情・状況・動機に働きかけて行動を引き出す（＝動かすこと／説得とは別物）スキルが決定打になる、という主張。

## この記事を読むべき理由
技術的に正しい設計やRFCを書いても採用されない経験は多いはず。特に日本の保守的な現場や年功的な組織では、正論だけで変化を起こすのは難しいため、本質的な打ち手を知る価値があるから。

## 詳細解説
- 「説得（convincing）」は論理的構成に依拠し、普遍的な合理性（数学的証明やベンチマーク）を目指す。一方「動かすこと（persuading）」は特定の聴衆の不安、利害、経験を狙って行動を促す。
- 古典的修辞学にある3要素：論理（logos）、話者の信頼性（ethos）、聴衆の感情（pathos）が揃って初めて実効性が出る。エンジニアはしばしばlogosに偏りがちで、ethosやpathosを軽視する。
- 「幾何学的思考（axiom→演繹）」と「微妙な感覚（場の空気や未公開の制約を読む）」の違い。優れた意思決定者は正しさを出発点に、相手に合わせて伝え方やタイミングを調整する。
- 具体例：RFCを完璧に作っても、SREは可観測性の不安、プロダクトはスプリントコスト、現場リードはプライドや過去の失敗を基準に判断するため、「理解」は得られても「支持」は得られないことが多い。
- 権限で押し切ると一時的な従順は得られても本当のコミットメントは得られない。逆に真の説得は小さな勝利と信頼を積み上げて変化を定着させる。

## 実践ポイント
- ステークホルダーを洗い出し、それぞれの懸念・利得を明記する（SRE/PM/現場/経営など）。
- 成功指標を相手の言語で示す（例：リリース頻度、MTTR、Q4の納期リスク軽減など）。
- 小さな実験（プロトタイプや段階的マイグレーション）でリスクを可視化し、不安を下げる。
- 信頼を作る：過去の約束を守る、透明に報告する、共通のゴールを強調する。
- タイミングとストーリーを整える：ロジックに加え、なぜ今必要かを具体的事例で伝える。

短く言えば、正しさは基礎。相手の心と利害に働きかけて「動いてもらう」技術を意図的に学び、設計とコミュニケーションを両輪で進めよう。
