---
layout: post
title: "Try text scaling support in Chrome Canary - Chrome Canaryでテキストスケーリングを試す"
date: 2026-01-27T21:42:15.957Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.joshtumath.uk/posts/2026-01-27-try-text-scaling-support-in-chrome-canary/"
source_title: "Try text scaling support in Chrome Canary - Josh Tumath"
source_id: 46784977
excerpt: "Canaryのtext-scaleメタでOS文字設定を尊重、早めの対応で読みやすく"
---

# Try text scaling support in Chrome Canary - Chrome Canaryでテキストスケーリングを試す
スマホで「文字だけ大きくする」時代が来る──Chrome Canaryの<meta name="text-scale">で変わるウェブの読みやすさ

## 要約
Chrome Canaryの実験機能で<meta name="text-scale">が試せるようになり、OSの文字サイズ設定をウェブページが尊重できるようになります。これによりアクセシビリティの改善とレイアウト設計の見直しが必要になります。

## この記事を読むべき理由
日本でも多くのユーザーが端末の文字サイズを変更しており（特に高齢ユーザーや視覚支援が必要な層）、ウェブがその設定を無視していると利用に支障が出ます。早めに対応法を押さえることで、ユーザビリティとアクセシビリティが向上します。

## 詳細解説
- 何が増えたか：HTMLの新しいメタタグ
  - <meta name="text-scale" content="scale"> をページに入れると、対応ブラウザ（現状はCanary上のフラグ有効時）がユーザーのOS文字スケールをページの既定フォントサイズとして扱います。
- ズームとテキストスケーリングの違い：
  - ズームは画像・レイアウト・余白など全てを拡大するのに対し、テキストスケーリングは「初期フォントサイズ」だけを変えます。目的は文字が読みやすくなること。
- なぜオプトインなのか：
  - 既存サイトのレイアウトが破綻する可能性があり、特にデスクトップでの文字サイズ変更で多くのサイトが崩れる事例があるため、サイト側が「対応します」と明示する必要があります（WCAG 1.4.4／1.4.10 関連）。
- 実装上の注意点（主要ポイント）：
  1. 初期フォントサイズを上書きしない（pxで固定しない）。
  2. コンテンツに使うサイズはrem/em等のフォント相対単位を使うが、余白やレイアウト要素には必ずしも相対単位を適用しない方が良いケースがある（縦長のモバイルで余白を確保するため）。
  3. テストは必須。320px幅・テキスト200%などで実機またはDevToolsの環境変数（env(preferred-text-scale)）を使い、表示崩れをチェックする。

コード例（metaタグ）:
```html
<meta name="text-scale" content="scale">
```

やってはいけない例（初期サイズをpxで上書き）:
```css
:root { font-size: 16px; } /* NG: ユーザーの既定サイズを無効化する */
```

推奨例（上書きしない／相対単位で調整）:
```css
/* 初期値は触らない、必要なら%で調整 */
html { font-size: 100%; }
body { font-size: 1rem; }
h1 { font-size: 2rem; } /* 見出しは相対で指定 */
```

## 実践ポイント
- まずページに<meta name="text-scale">を追加して挙動を観察（Canaryでフラグ有効にする）。
- px固定のフォント指定を探してrem/emに置換するか、重要箇所だけpxを残す判断をする。
- DevToolsで320px・200%のテストを実施し、ボタンや入力欄の折り返しやスクロール発生を確認する。
- 見出しの過剰な拡大をどう扱うかは検討課題：見出しは本文より緩やかに拡大する実装方針を検討する。

早めに試しておくと、アクセシビリティ対応の先手になります。
