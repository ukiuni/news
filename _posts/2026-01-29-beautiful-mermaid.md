---
layout: post
title: "Beautiful Mermaid - 美しい Mermaid"
date: 2026-01-29T03:14:53.610Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/lukilabs/beautiful-mermaid"
source_title: "GitHub - lukilabs/beautiful-mermaid"
source_id: 46804828
excerpt: "ターミナルでも美麗な図を即生成、VS Codeテーマ連携の高速Mermaidレンダラー"
image: "https://opengraph.githubassets.com/6cbfd9111c3e84cba1c96c8bec47548ea04333a57d79882ff057674b1d6451aa/lukilabs/beautiful-mermaid"
---

# Beautiful Mermaid - 美しい Mermaid
ターミナルでも「見やすく・美しい」図を即座に作る——AI時代のMermaidレンダラー

## 要約
Beautiful Mermaidは、Mermaidソースから高速かつテーマ可能なSVGとASCII/Unicode出力を生成するTypeScriptライブラリ。ゼロDOM依存でCLIやチャット、リッチUIまで幅広く使える。

## この記事を読むべき理由
ドキュメントやAIアシスタントとの対話で図が必須になっている日本の開発現場で、見栄え・速度・端末互換性を同時に満たす実用的な選択肢だから。VS Codeテーマとの親和性も高く、日本の開発ワークフローに容易に組み込める。

## 詳細解説
- 出力形式：SVG（リッチUI向け）とASCII/Unicode（ターミナル/チャット向け）を両方サポート。ASCIIエンジンは mermaid-ascii をTypeScriptに移植・拡張。
- 対応図種：Flowchart、State、Sequence、Class、ERの5種類。
- テーマ設計：最小は bg（背景）と fg（前景）の2色で自動派生（color-mix()）する「Mono Mode」。必要に応じて accent, line, muted, surface, border 等を上書きする「Enriched Mode」も可能。
- ライブ切替：SVG内のCSSカスタムプロパティでテーマを切り替えれば再レンダリング不要で即時反映。
- Shiki互換：Shikiを通して任意のVS Codeテーマから色を抽出して使える（fromShikiTheme）。日本で流行しているテーマ（例：tokyo-night相当）もそのまま利用可能。
- パフォーマンス＆依存：Pure TypeScriptでDOM不要。非常に高速（例：100以上の図を500ms未満でレンダリング可）。
- ライセンス：MIT。

主要API（抜粋）
- renderMermaid(text, options?): Promise<string> — SVGを返す
- renderMermaidAscii(text, options?): string — ASCII/Unicodeを返す
- fromShikiTheme(theme) — Shikiテーマから図用色を抽出
- THEMES — 15の組み込みテーマ

## 実践ポイント
- まず導入：npm / pnpm / bun でインストールして試す。
  ```typescript
  // typescript
  npm install beautiful-mermaid
  ```
- SVG出力（VS CodeやWeb UI向け）：
  ```typescript
  // typescript
  import { renderMermaid } from 'beautiful-mermaid'
  const svg = await renderMermaid(
    `graph TD; A[Start] --> B{Decision} B -->|Yes| C[Action]`,
    { bg: '#1a1b26', fg: '#a9b1d6' } // MonoまたはEnriched指定
  )
  ```
- ターミナル表示（CLIやチャットボット向け）：
  ```typescript
  // typescript
  import { renderMermaidAscii } from 'beautiful-mermaid'
  const ascii = renderMermaidAscii('graph LR; A --> B --> C', { useAscii: false })
  console.log(ascii)
  ```
- VS Codeテーマ連携：Shikiで高亮テーマを読み込み、fromShikiThemeで図色を自動抽出して統一感のあるドキュメントに。
- 実運用案：CIのREADME生成、チャットOpsの図解レスポンス、ターミナルベースのデバッグ出力などに組み込むと即効で見栄え向上。
- 注意点：複雑なカスタムテーマはEnriched色を指定すると見やすくなるが、コントラストや可読性を確認する。

元リポジトリ：Beautiful Mermaid (GitHub: lukilabs/beautiful-mermaid) — MITライセンス。
