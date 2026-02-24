---
layout: post
title: "Goodbye InnerHTML, Hello SetHTML: Stronger XSS Protection in Firefox 148 - innerHTMLよ、さようなら。setHTMLこんにちは：Firefox 148で強化されたXSS防御"
date: 2026-02-24T14:22:39.881Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://hacks.mozilla.org/2026/02/goodbye-innerhtml-hello-sethtml-stronger-xss-protection-in-firefox-148/"
source_title: "Goodbye innerHTML, Hello setHTML: Stronger XSS Protection in Firefox 148 - Mozilla Hacks - the Web developer blog"
source_id: 47136611
excerpt: "Firefox 148のsetHTMLでinnerHTMLを置換しXSSを簡単に防止"
image: "https://hacks.mozilla.org/wp-content/themes/Hax/img/hacks-meta-image.jpg"
---

# Goodbye InnerHTML, Hello SetHTML: Stronger XSS Protection in Firefox 148 - innerHTMLよ、さようなら。setHTMLこんにちは：Firefox 148で強化されたXSS防御

魅力的なタイトル: 「もうinnerHTMLで悩まない——Firefox 148が導入したsetHTMLで簡単にXSS対策」

## 要約
Firefox 148で標準化されたSanitizer API（setHTML）が導入され、ユーザー生成コンテンツを安全にDOM挿入できるようになりました。これによりinnerHTML依存のリスクを低減し、より簡単にXSS対策を行えます。

## この記事を読むべき理由
日本の多くのサービス（CMS、掲示板、ECレビュー等）はユーザー入力を扱います。既存コードの小さな変更でXSSリスクを大幅に下げられるため、実務で即役立つ知識です。

## 詳細解説
- XSS問題：悪意あるHTML/スクリプトが注入されるとセッション乗っ取りや情報漏洩につながる。CSPなどの対策はあるが導入のハードルが高いケースが多い。  
- Sanitizer API：悪意ある要素・属性を除去して「安全なHTML」に変換する標準API。Firefox 148が初採用で、他ブラウザも追随予定。  
- setHTML(): HTML挿入と同時にサニタイズが行われる安全な代替手段。デフォルト設定で危険な属性（onclick等）やタグを削除する。カスタム設定で許可タグ・属性を制御可能。  
- Trusted Typesとの併用：Trusted Typesと組み合わせればHTML注入経路を中央管理でき、より厳格な運用が可能。setHTMLを許可しつつ、他の危険な挿入方法をブロックするポリシーも作りやすくなる。

例（簡単な使い方）:
```javascript
document.body.setHTML('<h1>Hello <img src="x" onclick="alert(1)"></h1>');
// 結果: <h1>Hello </h1> など、安全化されたHTMLが挿入される
```

## 実践ポイント
- まずinnerHTMLの代わりにsetHTML()を試す（影響範囲が小さければ置換で即効果）。  
- デフォルトが厳しすぎる場合はサニタイズ設定で許可ルールを調整する。  
- Trusted Typesと組み合わせて、許可された挿入経路を限定する。  
- 導入前にSanitizer API playgroundで挙動を検証する。  
- 日本語コンテンツや既存CMSのテンプレートでタグ・属性の扱いを確認して移行計画を立てる。
