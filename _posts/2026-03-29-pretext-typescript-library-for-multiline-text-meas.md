---
layout: post
title: "Pretext: TypeScript library for multiline text measurement and layout - Pretext：複数行テキストの測定とレイアウト用TypeScriptライブラリ"
date: 2026-03-29T18:49:02.380Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/chenglou/pretext"
source_title: "GitHub - chenglou/pretext · GitHub"
source_id: 47556290
excerpt: "DOM測定不要で日本語・絵文字混在の行高を高速かつ高精度に算出するTypeScriptライブラリ"
image: "https://opengraph.githubassets.com/c1bf92218e505db80de21f46bda175c0ea8cf1b7dd8c3c68b71d7c835addb0cb/chenglou/pretext"
---

# Pretext: TypeScript library for multiline text measurement and layout - Pretext：複数行テキストの測定とレイアウト用TypeScriptライブラリ
DOM測定を不要にして「行高さ」を正確かつ高速に計算する—UIのパフォーマンスと見た目を一段上げるツール

## 要約
PretextはCanvasベースの計測とテキスト分割ロジックで、getBoundingClientRectなどの高コストなDOM再レイアウトを避けつつ、複数行テキストの高さや行分割を正確に算出するTypeScriptライブラリです。

## この記事を読むべき理由
日本でも多言語対応（日本語＋絵文字＋RTL混在）や仮想化リスト、動的コンテンツでのレイアウト崩れ（CLS）対策は重要です。PretextはそれらをDOM依存なしに高速・正確に解決でき、パフォーマンスとUXの改善に直結します。

## 詳細解説
- 基本思想：ブラウザのフォントエンジンを「計測の基準」として、CanvasのmeasureText等を使い一度だけ分析（prepare）→以降は算術的に行分割と高さを算出（layout）する。これによりレイアウトの再フローを防ぎ高速化する。
- 主なAPI
  - prepare(text, font, options?) → 段落を正規化・分割・計測してキャッシュ化するハンドルを返す。
  - layout(prepared, maxWidth, lineHeight) → 指定幅と行高で高さと行数を返す（DOM不要）。
  - prepareWithSegments / layoutWithLines → 行ごとの文字列や幅、カーソル情報を取得してCanvas/SVG/WebGLなどへ自前で描画可能。
  - walkLineRanges → 行幅だけを効率的に列挙し、二分探索などで最適幅を探す用途に便利。
  - layoutNextLine → 行ごとに異なる幅で流し込める（フロート画像などに対応）。
- 対応面：日本語・絵文字・混在の双方向テキスト（bidi）などを考慮。tabsはブラウザ標準のtab-size=8。white-space:'pre-wrap'オプションで改行・タブを保持可。
- 性能目安：ベンチマークスナップショットでは prepare が共有500テキストバッチで約19ms、layout が同バッチで約0.09ms と報告（環境依存）。
- 注意点：フォント指定はCSSと同期させる必要あり（例: "16px Inter"）。system-uiはmacOSで不安定。完全なフォントレンダラーではないため特定ケースの差異はあり得る。

使用例（TypeScript）:
```ts
import { prepare, layout } from '@chenglou/pretext'

const prepared = prepare('こんにちは 世界 🚀', '16px "Noto Sans JP"')
const { height, lineCount } = layout(prepared, 320, 24)
```

行毎に取り出してCanvasへ描画する例:
```ts
import { prepareWithSegments, layoutWithLines } from '@chenglou/pretext'

const prepared = prepareWithSegments('長い日本語テキスト…', '18px "Noto Sans JP"')
const { lines } = layoutWithLines(prepared, 300, 26)
lines.forEach((l, i) => ctx.fillText(l.text, 0, i * 26))
```

## 実践ポイント
- まず1回prepareしてキャッシュを再利用する（prepareは高コストだが一度で済む）。
- フォント指定（サイズ・ファミリ・ウェイト）とCSSを必ず同期させる。
- 仮想化リストや動的高さが必要なコンポーネントでlayoutを使い、DOM測定を削減してスクロール性能を改善する。
- テキストの「縮み包み（shrinkwrap）」やナイスな幅探索にはwalkLineRangesで二分探索を組み合わせる。
- フォントやロケールを切り替える場合は clearCache() を呼ぶ。サーバーサイドレンダリング対応は今後の展望。

導入は npm install @chenglou/pretext 。まずは公式デモを動かして自分のケースで精度とパフォーマンスを確かめることを推奨。
