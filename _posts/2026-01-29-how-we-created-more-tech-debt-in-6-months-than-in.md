---
layout: post
title: "How we created more tech debt in 6 months than in a 10-year-old system - 6ヶ月で10年物システムより多くの技術負債を作った話"
date: 2026-01-29T20:25:28.879Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://superkacper4.github.io/portfolio-2023/blog/technical-debt-everyday"
source_title: "How we created more tech debt in 6 months than in a 10-year-old system"
source_id: 414311194
excerpt: "似てるから共通化した設計判断で半年で10年分の技術負債が蓄積、ドメイン分離で回避できた実録"
---

# How we created more tech debt in 6 months than in a 10-year-old system - 6ヶ月で10年物システムより多くの技術負債を作った話
些細な設計判断が半年で雪だるま化する――現場で起きた“日常的な技術負債”の実例と学び

## 要約
小さな判断（似ているから同じテーブルに入れよう）が原因で、半年で既存10年システムより大きな技術負債が発生した。ドメイン分離と早めの切り出しが有効だった、という話。

## この記事を読むべき理由
日常的な「似てるから共通化」判断がプロダクトを破壊する過程は、スピード重視の日本の開発現場でも頻出の失敗例。実務で使える回避策が学べる。

## 詳細解説
- 背景: Next.jsのモノリスで、不動産の「Opinion（意見）」テーブルに広告（Apartment相当）の情報を追加。最初は似ているという理由で新テーブルを作らず拡張を選択。
- 問題の本質: optional（nullable）フィールドが増え、ビジネス上の区別が曖昧になり、isApartmentフラグで状態を判別するような設計に。結果、条件分岐が増え、データ整合性・可読性・保守性が悪化。
- 実際のスキーマ例（抜粋）:

```prisma
model Opinion {
  id String @id @default(cuid())
  building Building? @relation(fields: [buildingId], references: [id])
  buildingId String?
  pricePerSquareMeter Int
  rating Int?
  message String?
  area Float
  opinionDate DateTime @default(now())
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
  // 後から追加された: numberOfRooms?, floor?, height?, isApartment?
}
```

- 対照: 10年稼働のシステムでは、新機能（バウチャー）を将来的な外部連携を見越して最初から専用サービスへ切り出したため、単一ソース・責務分離が保たれた。
- 教訓: 技術負債は「いつかリファクタする」旨の判断や「似てるから共有」で毎日積み重なる。短期のコスト最小化が長期コストを爆発させる。

## 実践ポイント
- ドメインモデリングを優先：似ていても意味が違えば別エンティティにする。
- NULL地獄を避ける：nullableフィールドが多くなる兆候で再設計を検討。
- 境界（Bounded Context）を明確化：将来的な外部連携や責務を早めに想定する。
- 小さく切り出す判断基準：外部連携・異なるライフサイクル・異なるバリデーションがあれば分離。
- 開発チーム向けルール：TODOや「あとで直す」コメントを定期的にレビューし、負債の一覧化と返済計画を作る。

短い判断が半年で何倍ものコストを生む現実を受け止め、設計と境界の判断をチームの習慣にしてください。
