---
layout: post
title: "You are not required to close your <p>, <li>, <img>, or <br> tags in HTML - HTMLで<p>や<li>、<img>、<br>を閉じる必要はありません"
date: 2026-01-11T10:07:24.986Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://blog.novalistic.com/archives/2017/08/optional-end-tags-in-html/"
source_title: "You are not required to close your &lt;p&gt;, &lt;li&gt;, &lt;img&gt;, or &lt;br&gt; tags in HTML &bull; blog.NOVALISTIC"
source_id: 46559065
excerpt: "HTMLではpやimg等の終了タグ省略は許容されるが、実務では可読性とツール互換のためルール化が重要"
image: "https://novalistic.com/images/logos/novalistic/tile_op_applist.png"
---

# You are not required to close your <p>, <li>, <img>, or <br> tags in HTML - HTMLで<p>や<li>、<img>、<br>を閉じる必要はありません
クリックせずにはいられないタイトル: 「HTMLの“閉じ忘れ”は本当に問題？ — 実は許容されるタグと今すぐ覚えるべき実務ルール」

## 要約
HTML（HTML5）では、<p>や<li>のように終端タグが「任意」の要素や、<img>や<br>のような「void（空）要素」は必ずしも閉じる必要がない。XHTML由来の慣習と混同されがちだが、実務では一貫性と用途に応じた運用が重要。

## この記事を読むべき理由
日本の現場ではレガシーコード、CMS、チームのコーディング規約、あるいは学習教材などで「全て閉じるべき」と教えられることが多い。だが仕様を正しく理解すると、可読性・生産性・互換性の観点でより適切な選択ができるようになる。

## 詳細解説
- 要点
  - HTML（特にWHATWGの生きた仕様＝HTML5）では一部要素の終了タグは「オプショナル」。
  - 代表例：任意の終了タグ → p, li（など複数）。void要素（中身を持たない） → img, br, hr, input, meta, link など。
  - XHTML（XMLベース）は厳格で全ての要素を閉じる／属性を引用する必要があったため、その習慣がHTML側にも誤って伝播した。
- self-closing (/>) について
  - /&gt; はXML由来で、HTML5では互換性のため許容されるが必須ではない。HTML側では意味が薄く（void要素は終端を持たないため）、書くか書かないかは移行時の利便性や好みに依る。
- 実装上の注意
  - 終端を省略すると、ブラウザは仕様に従い暗黙的に閉じる（エラー回復ではない）。ただし改行や空白の扱いが変わり、CSSのインライン配置などに影響することがある（隣接する要素のインター要素空白）。
  - JSX（React）や一部テンプレートエンジンではルールが異なり、void要素でも必ず self-close が必要だったりするので注意。

例（HTMLでどちらも有効）:
```html
<!-- 終了タグを省略 -->
<p>This paragraph.
<p>Another.

<!-- void要素（省略可） -->
<img src="icon.png" alt="">
<br>
```

## 実践ポイント
- 一貫性を最優先する：プロジェクト全体で「省略する派」か「明示的に閉じる派」かを決める。
- 初学者・チーム開発では明示的に閉じる：可読性とバグ防止の観点から推奨。
- 自動整形・リンターを利用：Prettier、HTMLHint、eslint-plugin-html 等でルールを決めてCIに組み込む。
- テンプレート／JSXの仕様を確認：React/Vue/SvelteなどはHTMLとは異なるルールを持つ。
- DOCTYPEは必須：<!DOCTYPE html> を忘れない。これはHTMLの動作を規定する重要事項。
- レガシー対応・移行時は /&gt; を活用：既存のXHTMLソースをHTML5に移行する際は /&gt; の有無は選択肢。

短くまとめると、HTMLでは「閉じ忘れ」が即エラーではないが、現場では可読性とツール互換のためにルールを定めて運用するのが賢い。
