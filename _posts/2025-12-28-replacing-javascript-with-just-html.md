---
layout: "post"
title: "Replacing JavaScript with Just HTML - JavaScriptをHTMLだけで置き換える"
date: "2025-12-28 02:15:28.408000+00:00"
categories:
- tech
- world-news
tags:
- tech-news
- japan
source_url: "https://www.htmhell.dev/adventcalendar/2025/27/"
source_title: "Replacing JS with just HTML - HTMHell"
source_id: "46407337"
excerpt: "ネイティブHTMLでJSを減らし表示速度とアクセシビリティを劇的改善。"
---
# Replacing JavaScript with Just HTML - JavaScriptをHTMLだけで置き換える

## 要約
HTMLのネイティブ機能（例：<details>、<datalist>、<dialog>など）を活用することで、よくあるUIパターンを余計なJavaScriptなしで実現し、読み込み性能・メンテナンス性・アクセシビリティを改善できる。

## この記事を読むべき理由
日本のサービスでも「ページ表示速度」「モバイル回線での体験」「運用負荷低減」がますます重要になっています。軽量化と意味のあるJavaScript分離は、ユーザ体験の底上げに直結します。

## 詳細解説
なぜHTMLで置き換えるのか
- JavaScriptは強力だがダウンロード・パース・実行・メモリ監視などコストが高い。
- ネイティブ要素はブラウザ実装で高速かつアクセシブルに振る舞う（フォーカス管理やキーボード操作を標準提供することが多い）。
- HTML/CSSでできる部分はまずそちらで実装し、複雑な状態管理や非同期処理だけJSに任せるのが近年の潮流。

代表的な置き換え例（技術ポイント）
- アコーディオン（折りたたみ）
  - <details>/<summary> を使えば、開閉状態はブラウザが管理。open属性やCSSの::marker、[open]疑似クラスで見た目を制御できる。
  - ラジオ的な排他開閉は name 属性のサポートがある実装では可能（ブラウザ依存の挙動に注意）。
```html
```html
<details>
  <summary>見出し（クリックで開閉）</summary>
  <p>中身のコンテンツ</p>
</details>
```
```

- 入力のオートフィルター（候補）
  - <input list="..."> と <datalist> の組み合わせで、タイプ時に候補を表示し絞り込み可能。軽量な検索候補やフォームの補助に最適。
```html
```html
<label for="browser">Browser</label>
<input id="browser" name="browser" list="browsers" autocomplete="off">
<datalist id="browsers">
  <option value="Chrome">
  <option value="Firefox">
  <option value="Safari">
</datalist>
```
```

- モーダル / ポップオーバー
  - <dialog> はモーダルをネイティブに提供（showModal() と close()）。モダールのフォーカス管理をブラウザが担う。
  - 互換性がない場合は :target やチェックボックスハック＋ARIAで代替。どちらもキーボード操作とスクリーンリーダー確認が必須。
```html
```html
<dialog id="info">
  <p>モーダルの内容</p>
  <button onclick="document.getElementById('info').close()">閉じる</button>
</dialog>
<!-- 開く（JSを使う場合） -->
<!-- document.getElementById('info').showModal() -->
```
```

互換性とアクセシビリティの注意点
- <details> と <datalist> は現代ブラウザで広くサポートされているが、表示スタイルや挙動に差がある。ユーザーエージェント差分は確認すること。
- <dialog> はまだ一部でポリフィルが必要な場合がある。フォールバック実装を用意する。
- 画面リーダー挙動やキーボード操作（Tab順、Escで閉じる等）は必ず確認し、必要ならARIA属性を補う。

いつJSを使うべきか
- 状態が複雑、サーバーと頻繁にやりとり、あるいはアニメーションやパフォーマンスでブラウザAPIが必要な場合はJSを使う。
- ただしUIの初期レンダリングと基本的な相互作用はまずHTML/CSSで実装しておき、JSは強化（progressive enhancement）として追加するのがベストプラクティス。

## 実践ポイント
- まずHTMLの意味論的要素を探索：<details>, <summary>, <datalist>, <dialog> を試す。
- ブラウザ互換性を確認して、ポリフィルやフォールバックを用意する。
- アクセシビリティを自動で期待せず、スクリーンリーダー・キーボード操作で実装を検証する。
- 測定（LCP、TBT、JavaScriptバンドルサイズ）で効果を数値化し、どこをHTMLに移すか判断する。
- 小さなウィジェットから移行を開始し、運用コストとパフォーマンス改善を確認する。

