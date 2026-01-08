---
  layout: post
  title: "Insert HTML from another file with 1 line of raw JS (works on github pages) - 1行の生JSで別ファイルのHTMLを挿入（GitHub Pagesで動く）"
  date: 2026-01-06T02:55:59.723Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://codeberg.org/UltimaN3rd/Static_HTML_include"
  source_title: "Insert HTML from another file with 1 line of raw JS (works on github pages)"
  source_id: 471220372
  excerpt: "1行の生JavaScriptでGitHub Pagesに外部HTMLを簡単挿入"
---

# Insert HTML from another file with 1 line of raw JS (works on github pages) - 1行の生JSで別ファイルのHTMLを挿入（GitHub Pagesで動く）

魅せる静的サイトの小ワザ：1行のネイティブJSでHTMLを差し込んでパーツ化を実現する方法

## 要約
Codebergのリポジトリは、最小限の生JavaScriptで静的サイトにHTMLを差し込む手法を示します。紹介されているのは、`document.currentScript.insertAdjacentHTML` を使った非常にシンプルな実装で、GitHub Pages／Codeberg Pagesのような静的ホスティング上でも動作します。

## この記事を読むべき理由
- 静的サイト（ドキュメント、個人ブログ、プロダクトページ）でヘッダーやフッターを簡単に共通化したい日本の開発者にすぐ使えるテクニックだから。
- ビルドツールを増やさずに軽量にパーツ化を実現でき、CI／ホスティングのコストや工数を抑えられるため実務で価値が高い。

## 詳細解説
リポジトリのコアはごく短いスクリプトで、実行箇所（スクリプト直前）にHTMLを挿入します。サンプルは次の通りで、テンプレートリテラルを使うため複数行のHTMLをそのまま書けます。注意点は、スクリプトがbodyの中で実行される必要があること（空のHTMLだとheadで動くため想定どおりにならない）です。

```html
<!DOCTYPE HTML>
<html>
<body>
<script src="included.js"></script>
</body>
</html>
```

```javascript
document.currentScript.insertAdjacentHTML('beforebegin',`
  <h3>You can write HTML code inside these back-ticks.</h3>
  <p>The back-ticks allow you to write out the HTML within a multiline string ...</p>
`);
```

元記事タイトルでは「別ファイルのHTMLを挿入」とありますが、上記は同一スクリプト内にHTMLを埋める方式です。外部HTMLを読み込みたい場合は、同じ考え方でfetchを使って相対パスのHTMLを取得して挿入する拡張も簡単です（静的ホスティングではCORSや相対パスの制約に注意）。

簡単なfetch版の例：

```javascript
(async()=>{
  const resp = await fetch('snippet.html');
  const html = await resp.text();
  document.currentScript.insertAdjacentHTML('beforebegin', html);
})();
```

## 実践ポイント
- スクリプトは必ずbody内、挿入したい直前に置く。headに置くと期待通りに動かない。
- テンプレートリテラル（バックティック）で複数行HTMLをそのまま扱える。バックティック自体を含める場合はエスケープを検討。
- 外部ファイルを使う場合は相対パスとホスティングの挙動（GitHub Pages / Codeberg Pages は静的ファイルをそのまま返す）を確認。必要ならfetch版を採用。
- 小規模サイトやドキュメントに最適。大規模なアプリではテンプレート管理やセキュリティ（XSS対策）を検討すること。

短いJSで済ませてメンテを楽にしたいときの即効ワザとして有効。静的ホスティングで軽量に共通パーツを導入したい開発者は試してみてほしい。
