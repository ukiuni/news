---
layout: post
title: "When All You Can Do Is All or Nothing, Do Nothing - 全か無かしかできないなら、何もしない"
date: 2026-03-29T01:29:17.774Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://csswizardry.com/2026/03/when-all-you-can-do-is-all-or-nothing-do-nothing/"
source_title: "When All You Can Do Is All or Nothing, Do Nothing – CSS Wizardry"
source_id: 1030035333
excerpt: "不確かな優先付けはやめて、ブラウザに任せる安全策—実例と判断基準でLCP改善へ"
---

# When All You Can Do Is All or Nothing, Do Nothing - 全か無かしかできないなら、何もしない

優先度ヒントで失敗するより「何もしない」を選べ — デザインシステムでの安全なパフォーマンス戦略

## 要約
デザインシステムやCMSがコンポーネントの表示コンテキストを正確に知らないと、loading=lazy や fetchpriority=high といった「ヒント」は逆効果になる。確信が持てないなら属性を付けず、ブラウザの既定動作に委ねる方が安全だ。

## この記事を読むべき理由
日本のECやメディア運営ではエディタに自由度を与えるCMSが多く、誤った優先付けでLCPやUXを悪化させるリスクが高い。現場で即使える判断基準が分かる。

## 詳細解説
- ヒントは「魔法の高速化属性」ではなく「確かな情報がある場合の補助」。loading=lazy はユーザーがまだ必要としない資源に有効だが、LCP候補を遅延するとパフォーマンスは悪化する。fetchpriority=high は「一つの」重要リソースを特定するためのヒントであり、複数に付けると効果が失われる。
- デザインシステムが使われる文脈が多様なら、システム側で勝手に優先度を推測すべきではない。安全なベースラインは「何もしない」で、ブラウザに発見・優先付けを任せること。
- ただし、明確に判定できるケース（例：常にヒーローで最初に来る画像、カルーセルの2枚目以降、メニュー内のアイコンなど）はヒントを付けて良い。判断ロジックがあるなら限定的に使う。

短いコード例（安全なデフォルトと、確信がある時の例）:

```html
<!-- 安全なデフォルト：ヒントを付けない -->
<img src="/img/promo.jpg" alt="Promotional image" width="640" height="360">

<!-- 明確なLCP候補なら優先度を明示 -->
<img src="/img/hero.jpg" alt="Hero" width="1200" height="675" fetchpriority="high">

<!-- 明確に遅延可能なケース（カルーセル2枚目以降など） -->
<img src="/img/thumb-2.jpg" alt="Thumb" width="200" height="112" loading="lazy">
```

## 実践ポイント
- デザインシステムは「わからないことはしない」を原則に。汎用コンポーネントに一律の loading/fetchpriority を付けない。  
- CMSに「コンテキスト情報」を持たせる：位置（heroか？）、出現回数、初期表示かどうかなどをフロントエンドに伝えられると限定的な最適化が可能。  
- 優先度ヒントは狭く具体的に使う：LCP候補が一意に特定できる場合のみ fetchpriority=high、明らかに非即時な要素のみ loading=lazy。  
- 計測で効果を確認する：変更前後のLCPやネットワーク優先度を計測し、誤った最適化を防ぐ。  

当面は「全部高優先／全部遅延」の誘惑を振り切り、シンプルで安全な基準を採るのが現場の負担を最小にする最良策です。
