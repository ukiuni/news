---
layout: post
title: "Show HN: A custom font that displays Cistercian numerals using ligatures - リガチャで中世のシステムを再現するカスタムフォント"
date: 2026-02-09T04:38:47.201Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://bobbiec.github.io/cistercian-font.html"
source_title: "Cistercian Numeral Font"
source_id: 46939312
excerpt: "入力は数字のまま、表示だけ中世システルシアンに変えるフォントデモ"
image: "https://bobbiec.github.io/cistercian-font-preview.png"
---

# Show HN: A custom font that displays Cistercian numerals using ligatures - リガチャで中世のシステムを再現するカスタムフォント
驚きのタイポグラフィ体験：入力は通常の数字のまま、表示だけ中世の「システルシアン数字（Cistercian）」に変わるフォント

## 要約
通常のアラビア数字をそのまま入力すると、OpenTypeリガチャで自動的に中世のCistercian（システルシアン）数字に置き換えて表示するウェブ用カスタムフォントのデモと実装紹介です。表示は絵文字的ですが、テキスト自体は数字なのでコピーや検索が可能です。

## この記事を読むべき理由
フォントで表示を変えつつ、テキストの意味（検索・コピー・アクセシビリティ）を保てるテクニックは、デザイン性の高いUIや教育コンテンツ、ゲームのローカライズで役立ちます。日本でも和洋混植や独自表現を安全に実装したい開発者やデザイナーに参考になります。

## 詳細解説
- Cistercian数字とは：中世の修道院で使われた、1〜9、10〜90、100〜900、1000〜9000を四つの象限の線・点で組み合わせて1つの記号で表す体系。見た目は一つの複合図形になります。  
- フォントの仕組み：このプロジェクトはOpenTypeのリガチャ機能を利用。数字列（例えば "1984" や "42"）を特定のグリフ（部品）にマッピングして、合成された一字のCistercian記号として描画します。重要な点は「テキストは元の数字のまま」なので、コピー＆ペーストやブラウザの検索（Ctrl/Cmd-F）が効くこと。  
- 実装のメリット：表示だけ変えるため、HTMLやデータ層は通常の数値を保持。アクセシビリティ（スクリーンリーダー）や検索インデックスへの影響を最小化できます。  
- 技術的注意点：フォントはクライアント側で読み込む必要があり、フォールバックを用意すること。Cistercian記号は環境によってUnicodeで一貫してサポートされていないことがあるため、このアプローチは互換性と表現力のバランスを取る良い方法です。

## 実践ポイント
- まずはデモを開いて（https://bobbiec.github.io/cistercian-font.html）数字を入力して挙動を確認する。コピーや検索も試す。  
- ウェブに導入するには @font-face でフォントを読み込み、対象要素に font-family を指定するだけ（OpenTypeリガチャはフォント内で有効化済みの場合が多い）。簡単な例：
```css
/* css */
@font-face {
  font-family: "Cistercian";
  src: url("cistercian.woff2") format("woff2");
}
.cist {
  font-family: "Cistercian", system-ui, sans-serif;
}
```
- 実運用ではフォールバックフォント、フォント読み込みの遅延対策、ライセンス確認を忘れずに。  
- 日本向けの応用例：歴史系サイトのビジュアル化、教育コンテンツ、レトロ調UIやゲーム内の数字表現などで個性を出せます。
