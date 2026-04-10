---
layout: post
title: "Zero-build privacy policies with Astro - Astroで「ビルド不要」のプライバシーポリシー生成"
date: 2026-04-10T09:16:03.053Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.openpolicy.sh/blog/no-build-astro"
source_title: "Zero-build privacy policies with Astro — OpenPolicy"
source_id: 47715088
excerpt: "Astroでプラグイン不要、ビルド時に静的なプライバシーポリシーを生成してJSゼロの軽量運用を実現"
image: "https://openpolicy.sh/og/no-build-astro.png"
---

# Zero-build privacy policies with Astro - Astroで「ビルド不要」のプライバシーポリシー生成
Astroサイトにプラグイン不要で静的なプライバシーポリシーを組み込む、シンプルでメンテナンス負荷の低い新しい方法。

## 要約
OpenPolicyがAstro向けに、ファイル生成やViteプラグインを使わずにページ内でポリシーをコンパイルして静的HTMLを出力するワークフローを提供。結果はクライアントに余分なJSを送らない、安全で軽量なポリシーページです。

## この記事を読むべき理由
日本のサービスでも個人情報保護法対応や利用規約・クッキー表示は必須。手間を減らして確定的（同じ設定は常に同じ結果を返す）にポリシーを生成できる手法は、スタートアップや小規模チームに有益です。

## 詳細解説
背景：
- 旧来はAstroプラグインがビルド時にMarkdownファイルを生成してインポートしていたため、生成ファイルの管理や.gitignore、ファイルウォッチの手間が発生した。

新しい流れ：
- OpenPolicyのコアがポリシー設定をその場でコンパイル。ページのフロントマターから直接呼び出してHTML文字列を出力するため、生成ファイルもプラグイン設定も不要。
- 出力はビルド時に静的HTMLになり、クライアント側のJavaScriptは不要。SEOやパフォーマンスに有利。

基本手順（要点）：
1. 必要パッケージを追加（例：bunを使う場合）
```bash
# bash
bun add @openpolicy/sdk @openpolicy/core @openpolicy/renderers
```
2. ポリシー設定を定義（例：src/lib/openpolicy.ts）
```typescript
// typescript
import { defineConfig } from "@openpolicy/sdk";

export default defineConfig({
  company: { name: "Acme", legalName: "Acme, Inc." },
  privacy: {
    effectiveDate: "2026-04-01",
    dataCollected: { /* ... */ },
    jurisdictions: ["us","eu"]
  },
  cookie: { effectiveDate: "2026-04-01", cookies: [/* ... */] },
  terms: { effectiveDate: "2026-04-01", governingLaw: { jurisdiction: "Delaware, USA" } }
});
```
3. ページ内でコンパイルしてレンダー（例：src/pages/privacy.astro）
```astro
---
// astro
import { compile, expandOpenPolicyConfig } from "@openpolicy/core";
import { renderHTML } from "@openpolicy/renderers";
import openpolicy from "../lib/openpolicy";

const policies = expandOpenPolicyConfig(openpolicy);
const privacyPolicy = policies.find(p => p.type === "privacy");
if (!privacyPolicy) throw new Error("Privacy policy not found");
const policy = renderHTML(compile(privacyPolicy));
---
<html lang="ja">
  <head><meta charset="utf-8"/><title>プライバシーポリシー</title></head>
  <body><div set:html={policy} /></body>
</html>
```

技術的メリットまとめ：
- astro.config.mjsは空のまま（統合やプラグイン不要）
- 生成ファイルや専用ディレクトリが不要でGit管理が楽
- 同一のdefineConfigでprivacy/terms/cookieを一元管理
- determinisitc（同じ設定は同じ成果物）なのでレビューと追跡が簡単

## 実践ポイント
- まず既存のプライバシーページ文面を元に`defineConfig()`を作る。LLMで下書きを補助するのも早い（ただし法的チェックは必須）。
- src/libに設定ファイルを置き、各ポリシーページで`expandOpenPolicyConfig`→`compile`→`renderHTML`の流れを実行するだけで済む。
- 日本向けは「個人情報保護法」「利用者同意（クッキー）」の文言を必ず法務とすり合わせる。
- 将来的にPRでのポリシーチェックや同意トラッキングが欲しければOpenPolicy+を検討する（追加機能）。

著者メモ：小規模チームほど「設定ファイルで一元管理し、ビルド結果が確定的に出る」仕組みの恩恵が大きい。まずは単一ページで試して運用コストを比べてみることを推奨する。
