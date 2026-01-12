---
layout: post
title: "The Three-Body Problem: Agentic AI in Software Engineering - 三体問題：ソフトウェア工学におけるエージェントAI"
date: 2026-01-12T02:12:25.639Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://open.substack.com/pub/serefayar/p/the-three-body-problem-of-ai-software"
source_title: "The Three-Body Problem: Agentic AI in Software Engineering"
source_id: 429100724
excerpt: "AIエージェントが招く三体問題とSpec主導で現場を安定化する方法"
image: "https://substackcdn.com/image/fetch/$s_!6p12!,w_1200,h_675,c_fill,f_jpg,q_auto:good,fl_progressive:steep,g_auto/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8dba639b-c321-4450-b258-73169d3247c3_1400x933.png"
---

# The Three-Body Problem: Agentic AI in Software Engineering - 三体問題：ソフトウェア工学におけるエージェントAI
AIエージェント時代の「三体問題」――開発現場で起きる混沌をどう収めるか

## 要約
AIエージェントが加わることで、従来の「開発者＋IDE」という二体モデルは「人間（意図）＋システム（現実）＋エージェント（確率的）＝三体」になり、些細なズレが大きな混乱を生む。Spec-Driven Development（SDD）がその「人工重力」として安定化に寄与する可能性がある。

## この記事を読むべき理由
日本の開発現場はレガシー資産、堅牢性要求、企業コンプライアンスが強く、AI導入の「楽しさ」だけでは済まない。AIエージェントが勝手にコードを変えるリスクが現実になりつつある今、現場で使える設計法と運用ルールを早めに理解しておくことが重要です。

## 詳細解説
- 三体の構図（簡単解説）
  - 人間（Intent）：自然言語であいまいに指示しがち。「UIを良くして」など。
  - システム（Reality）：コンパイラ、DB、既存コード。厳密で不変な制約を持つ。
  - エージェント（Probability）：AIがあいまいな意図をコードに翻訳するが確率的で誤作動（hallucination）する。
  - 問題点：エージェントが人の期待に合わせるうちにシステム制約を無視したり、逆にシステムエラーに固執して元の意図を見失ったりする。

- なぜ従来の対策が不十分か
  - agents.md や .cursorrules のような「エージェントのアイデンティティ」は行動指針に過ぎず、目的（何を達成するか）を示さない。高品質な「やり方」だけ与えても、目標が曖昧なら良質な混沌が生まれる。

- Spec-Driven Development（SDD）＝「人工重力」
  - Spec（仕様書）をソースオブトゥルースにして、エージェントはまずSpecを読んで理解・更新し、その後でコードを変更する流れにする。こうすることで：
    - アンカー（Spec）がエージェントの軌道を定義し、コンテキストドリフトを防ぐ。
    - Specは外部の「記憶」として働き、エージェントが混乱したら仕様に戻る。
  - ただし、SDDは構文的整合（コードが動く）を保証するが、意味的妥当性（ビジネス要件を本当に満たすか）は保証しない。仕様の不備は上流での重大事故につながる。

- 現実装とツール
  - Kiro、OpenSpec、Spec-kit等が登場し、仕様をAIと人で循環させる仕組みを提供している。CIと連携してSpecの検証→実装→テストのループを組むのが効果的。

- 日本市場における示唆
  - 金融・製造など堅牢性が求められる領域では、SDDは規制対応や監査証跡の面でもメリットが大きい。
  - プロダクトマネージャーやドメイン担当者が「仕様の守護者」になる役割にシフトする必要がある。

## 実践ポイント
- SpecをPR必須にする：コード変更は有効なspec.md/plan.mdの更新がないとマージ不可にする。
- Specテンプレを作る：要件、制約、失敗ケース、データ影響（例：soft-delete 必要性）を明示する項目を用意する。
- エージェントの「行動章典」を用意する：どのAPIを触るか、ログ出力、自己修正の閾値などを定義する（agents.md相当）。
- CIでSpecチェックを自動化：Spec→テストの整合性をCIで検証してからエージェント実行。
- 人間の挟み込み（human-in-the-loop）：重大変更は必ずドメイン担当者の承認を必須にする。
- モニタリングと監査ログ：エージェントの変更履歴と判断根拠（Spec差分）を保存する。
- 小さく始める：非クリティカルなモジュールでSDD＋エージェントのパイロットを回し、学びを次に活かす。

まとめ：AIは魔法ではなく、強力な「第三の力」です。日本の現場ではSpecを中心に据え、役割を再定義しつつ運用ルールを整えることが、混沌を安定させる最短ルートです。
