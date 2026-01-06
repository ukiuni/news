---
  layout: post
  title: "Adding insular script like it's 1626 - インサラー書体を1626年のように追加する"
  date: 2026-01-06T00:04:40.847Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://www.djmurphy.net/blog/clo-gaelach/"
  source_title: "Adding insular script like it&#39;s 1626"
  source_id: 46488883
  excerpt: "テキスト性を損なわず古アイルランド書体をOpenType合字で再現する実践ガイド"
  image: "https://djmurphy.net/blog-placeholder-1.jpg"
---

# Adding insular script like it's 1626 - インサラー書体を1626年のように追加する
古いアイルランド文字（Cló Gaelach）を「見た目通り」にウェブで再現し、元テキストの可搬性やスクリーンリーダー対応を壊さずに見せる工夫。

## 要約
OTFの「discretionary ligatures」を使って、ラテン文字列（例：consonant + "h"）を視覚的にドット付きの古書体字へ置換する手法と、それをスクリーンリーダーやコピーで壊さないようにする実装（Astroコンポーネント＋ruby＋sr-only）を紹介する。

## この記事を読むべき理由
Cló Gaelachのような文化的・歴史的書体をただ画像で貼るのではなく、テキストの可搬性・アクセシビリティを保ちながら再現する手法は、国際化対応やレガシー文字表示の実務的な応用として日本のウェブ開発者にも参考になるから。

## 詳細解説
- 背景：中世の修道士がラテン文字を変形させて作ったCló Gaelachは、séimhiú（子音に点を置く表記）を特徴とする。印刷やタイプライタの制約で「h」を後置する表記に置き換えられた歴史がある。
- 問題点：視覚的再現だけを行うと、コピー／検索／スクリーンリーダーに不都合が生じる（文字が画像化される、意味情報が失われる）。
- 解法（キーアイデア）：
  1. フォント側で“discretionary ligatures”を定義し、内部的には元のラテン文字（例："bh", "mh"など）を保持しつつ表示上はドット付き文字に置換する。これによりコピーや読み上げは元のテキストを返す。
  2. FontForge等でフォントを編集：discretionary ligature tableを追加→該当のsubtableでconsonant + "h" → dotted-consonantを置換。装飾として&をTironian etに置換するのも可。
  3. 表示側ではCSSでligatureを有効化し、必要なら追加のfont-feature（例："ss01"）を指定する。
  4. 可読性とアクセシビリティの両立にはruby要素＋sr-onlyの組合せが有効。視覚的には古書体＋翻訳をルビで添え、スクリーンリーダーにはlang属性を付けた不可視テキストで「[アイルランド語] meaning: [英語訳]」のように読み上げさせる。

- 実装上の注意：
  - 元テキストはそのまま残す（検索や翻訳、スクリーンリーダー対策のため）。
  - discretionary ligaturesはオプションなので、フォールバックや設定でオフにできる設計が望ましい。
  - rubyのスクリーンリーダー挙動はブラウザや支援技術によって一貫性がないため、sr-onlyによる補助テキストを用いるのが現実的。

簡潔な実装例（CSS有効化）：

```css
.gaeilge-text {
  font-family: "urgc", sans-serif;
  font-variant-ligatures: discretionary-ligatures;
  /* 補助的にOpenTypeのfeatureを有効化することも可能 */
  font-feature-settings: "ss01" 1;
}
```

スクリーンリーダー向けの構造（要点）：

```html
<span class="sr-only">
  <span lang="ga">Fáilte romhat</span>
  <span lang="en"> (meaning: Welcome)</span>
</span>
<ruby aria-hidden="true">
  <span class="gaeilge-text" lang="ga">Fáilte romhat</span>
  <rp>(</rp><rt>Welcome</rt><rp>)</rp>
</ruby>
```

Astroコンポーネント化の利点：テンプレート内で簡単に再利用でき、表示と読み上げのロジックを集中管理できる。

## 実践ポイント
- まずフォントを用意し、FontForgeでdiscretionary ligaturesテーブルを作成して「consonant+h → dotted consonant」の置換を実装する。
- CSSでfont-variant-ligatures: discretionary-ligaturesを指定して有効化する（ユーザーがオフにできるUIも検討）。
- ruby＋sr-only＋lang属性で視覚表現とスクリーンリーダー出力を分離する。コピー／検索の互換性が維持されているか必ず確認する。
- テスト：コピー＆ペースト、スクリーンリーダー（NVDA/VoiceOver等）、機械翻訳や検索インデックスでの挙動を検証すること。
- 文化的表現を扱う際は、表示優先と可搬性のバランスを明示的に設計する。

短めのまとめ：見た目の再現はフォントの力を借りて行い、テキストの意味やアクセシビリティはHTML構造（langやsr-only、ruby）で担保する――この組合せが実用的かつ文化的に配慮されたアプローチです。
