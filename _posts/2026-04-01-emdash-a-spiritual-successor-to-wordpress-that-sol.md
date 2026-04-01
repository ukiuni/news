---
layout: post
title: "EmDash – a spiritual successor to WordPress that solves plugin security - EmDash — WordPressの精神的後継でプラグインの安全性を解決するCMS"
date: 2026-04-01T17:16:42.254Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://blog.cloudflare.com/emdash-wordpress/"
source_title: "Introducing EmDash — the spiritual successor to WordPress that solves plugin security"
source_id: 47602832
excerpt: "EmDashはプラグインをサンドボックスで隔離し安全性を高めるTypeScript製CMS"
image: "https://cf-assets.www.cloudflare.com/zkvhlag99gkb/hBSrp5YJXIsn2IwBqdg2m/a22cf1285db3826ca159d83ab81076e0/EmDash-OG.png"
---

# EmDash – a spiritual successor to WordPress that solves plugin security - EmDash — WordPressの精神的後継でプラグインの安全性を解決するCMS
魅力的な日本語タイトル: 「WordPressの次を担う？EmDashが“危ないプラグイン”問題を技術で封じる理由」

## 要約
EmDashはTypeScript製のオープンソースCMSで、プラグインを隔離して最小権限で動かすことでWordPressが抱えるプラグイン安全性問題を根本的に改善することを目指すプロジェクトです。

## この記事を読むべき理由
日本の多くの企業・個人サイトは未だWordPressに依存しており、プラグイン由来の脆弱性や運用コストに悩んでいます。EmDashは保守性・セキュリティ・サーバレス運用・収益化（x402）を同時に提供し、日本の制作会社やメディア事業者に現実的な代替案を示します。

## 詳細解説
- 基本設計：EmDashは完全TypeScriptで書かれ、Astroをフロントエンド基盤に採用。サーバレス向け設計で、CloudflareのV8アイソレート（Dynamic Workers）など上で瞬時にスケールし、使わないときはゼロに戻ります。
- プラグインの隔離：従来のWordPressはPHPプラグインがサイトのDB/ファイルに直接アクセスでき、96%の脆弱性がプラグイン由来でした。EmDashは各プラグインを独立したサンドボックス（Dynamic Worker）で動かし、マニフェストで宣言した「capabilities（権限）」のみを付与します。これにより、事前に何を許可するかを明確に把握できます。
- 権限ベースの例（TypeScriptでのプラグイン定義）：

```typescript
import { definePlugin } from "emdash";

export default () => definePlugin({
  id: "notify-on-publish",
  version: "1.0.0",
  capabilities: ["read:content","email:send"],
  hooks: {
    "content:afterSave": async (event, ctx) => {
      if (event.content.status !== "published") return;
      await ctx.email!.send({ to: "editor@example.com", subject: `New: ${event.content.title}` });
    },
  },
});
```

- マーケットプレイスとライセンス：プラグインはEmDash本体と分離して動くため、作者は任意のライセンスを選べます（GPL縛りからの解放）。またコードを見せずに動作させられるので、中央集権的な市場依存を減らせます。
- 収益化（x402）：エージェントやクローラ中心の未来でも、x402によるオンデマンド課金で従量課金のアクセス制御が可能。購読を使わずにPay-per-use型ビジネスを作れます。
- テーマと移行：テーマはAstroプロジェクトとして作成。テーマはDB操作できないため安全性が高く、既存WordPressテーマの移行にはツールとエージェント支援が用意されます。

## 実践ポイント
- 小規模で試す：EmDash v0.1のプレビューをCloudflareまたはNode.js環境で動かして、既存サイトの部分的移行を試してみる。
- プラグイン設計を見直す：新規プラグインは必須のcapabilitiesだけを明示し、権限を最小化する運用ルールを導入する。
- ライセンス戦略：日本の開発チームや制作会社は、配布・商用化の自由度を高めるためにプラグインのライセンス選択を検討する。
- 収益化の実験：x402を使ったマイクロ課金（記事単位・API単位）を試し、AIエージェント時代の新しい収益モデルを模索する。
- ホスティング方針：法令やデータ保護で国内サーバが必要な場合はNode.js版で運用可能。Cloudflare上のサーバレス利点と国内ホスティングのトレードオフを評価する。

短期的には「試して学ぶ」姿勢で、長期的には安全で拡張しやすいCMS設計への移行を検討する価値があります。
