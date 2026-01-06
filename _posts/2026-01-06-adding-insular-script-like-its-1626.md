---
  layout: post
  title: "Adding insular script like it's 1626 - インスラル書体（Cló Gaelach）を1626年のように再現する"
  date: 2026-01-06T15:50:18.032Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://djmurphy.net/blog/clo-gaelach/"
  source_title: "Adding insular script like it&#39;s 1626"
  source_id: 1348465753
  excerpt: "古いアイルランド書体をWebで忠実に再現しつつ、コピーやスクリーンリーダー対応も両立する実装手法を解説"
  image: "https://djmurphy.net/blog-placeholder-1.jpg"
---

# Adding insular script like it's 1626 - インスラル書体（Cló Gaelach）を1626年のように再現する
古いアイルランドの美しい書体を、現代Webで「見た目そのまま」「アクセシブルに」復元する方法

## 要約
古いアイルランド書体「Cló Gaelach（インスラル書体）」の表示を、テキストの意味やアクセシビリティを損なわずに現代Web上で再現するために、OpenTypeの任意合字（discretionary ligatures）を使って視覚だけを置き換え、ruby要素とスクリーンリーダ向けの工夫で多言語表示を両立させる実例。

## この記事を読むべき理由
- 日本のフロントエンド／UXエンジニアにとって、歴史的書体の「見た目」を守りつつアクセシビリティとデータ互換性を壊さない手法は、多言語サイトやローカライズ（例：古文書体・旧仮名遣いの表現）で応用できる。  
- ruby要素の再利用やOTF機能の活用は、視覚表現と機械可読性のバランス問題に悩む現代Webに直結する実践知になる。

## 詳細解説
- 背景：Cló Gaelachは中世のラテン文字をアイルランド語の音に合わせて発展させた書体で、子音の「点（séimhiú）」で軟音化を示すのが特徴。機械化以前はタイプや写植の制約で「h」を使う置換が一般化したが、元の字形の美しさは失われた。
- 問題点：表示を古い書体風にすると見た目は良くなるが、生テキストが置き換わるとコピー／検索／スクリーンリーダでの処理が壊れる。特に音声読み上げや辞書連携は文字データが重要。
- 解決策：OpenTypeの「discretionary ligatures」を使い、表示上は「consonant + h」を古い点付き字へ置換する合字を定義する。これは視覚表現だけを変え、基底テキストはそのまま残るため、コピーやスクリーンリーダは元テキストを利用できる。
- 実装の流れ（要点）：
  1. Cló Gaelachフォント（例：Úrchló GC）をFontForge等で開く。  
  2. discretionary ligatureテーブルを追加し、該当する子音＋"h"の組を点付き子音へ置換するサブルールを作成。Tironian et（&）などの小技も同様に置換可能。  
  3. CSSで任意合字を有効化して表示に反映する（以下参照）。  
  4. 視覚用の置換はaria-hidden等でスクリーンリーダからは隠し、スクリーンリーダ向けには元テキスト＋翻訳をsr-onlyで提供する。Astroのコンポーネント例ではruby要素を併用して視覚的に読みやすく、音声的には「[アイルランド語テキスト] meaning: [翻訳]」という順で読ませている。

- ruby要素の再利用：日本語環境ではrubyでルビを振る習慣があるため理解しやすいが、通常のrubyはスクリーンリーダの振る舞いが標準化されていない点に注意。したがって、見た目用のrubyはaria-hiddenにして、別途スクリーンリーダ向けにlang属性付きのsr-onlyテキストを用意するのが安全。

短い実装例（要点のみ）：

```css
/* css */
.gaeilge-text {
  font-family: "urgc", sans-serif;
  font-variant-ligatures: discretionary-ligatures;
}
```

```html
<!-- html -->
<span class="sr-only">
  <span lang="ga">Fáilte romhat</span>
  <span lang="en"> (meaning: Welcome)</span>
</span>
<ruby aria-hidden="true">
  <span class="gaeilge-text" lang="ga">Fáilte romhat</span>
  <rp>(</rp><rt>Welcome</rt><rp>)</rp>
</ruby>
```

## 実践ポイント
- フォント準備：Cló Gaelach系フォントを入手し、FontForge等でdiscretionary ligaturesを追加する。合字は表示のみを変えるように設計すること（元のコードポイントはそのまま）。
- CSS設定：表示側で `font-variant-ligatures: discretionary-ligatures;` を有効にして視覚合字を適用する。
- アクセシビリティ：視覚用の合字は aria-hidden で隠し、スクリーンリーダ向けに lang="ga" と訳文 lang="en" を含む sr-only テキストを用意する。rubyは見た目改善に有効だが、スクリーンリーダ挙動は確認して障害者支援ソフトで必ずテストする。
- 応用例（日本の現場へ）：古文書体や歴史的仮名遣い、地域固有の書体を扱う際にも同様の「表示は装飾、意味は元テキストを保持する」アプローチが使える。ローカライズ時のUX／アクセシビリティ設計として有用。

上記は「見た目の再現」と「機械可読性／アクセシビリティ」を両立させる実践的な手法の紹介。歴史的書体を現代のWebで安全に“まぶす”ためのテンプレートとして活用できる。
