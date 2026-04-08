---
layout: post
title: "Under the hood of MDN's new frontend - MDNの新フロントエンドの内部構造"
date: 2026-04-08T11:15:51.469Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://developer.mozilla.org/en-US/blog/mdn-front-end-deep-dive/"
source_title: "Under the hood of MDN&#39;s new frontend"
source_id: 1117256551
excerpt: "MDNがLitで部分的インタラクティブを差し込み、軽量で高速なドキュメント運用を実現"
---

# Under the hood of MDN's new frontend - MDNの新フロントエンドの内部構造
MDNが教える「軽く、速く、保守しやすい」フロント実装のリアル

## 要約
MDNは従来の巨大なReactアプリを見直し、サーバー生成コンテンツに対して必要な箇所だけを効率的に差し込むために、LitベースのWeb Componentsへ部分移行しました。結果として保守性・パフォーマンス・執筆体験が改善しています。

## この記事を読むべき理由
ドキュメントやコンテンツ中心のサイトを運用する日本のチーム（企業ドキュメント、OSS、教育サイト等）にとって、MDNの設計選択は実務的な指針になります。特に「静的コンテンツ＋部分的なインタラクティブ」をどう扱うかは多くの現場で直面する課題です。

## 詳細解説
- アーキテクチャ概要  
  - MDNのコンテンツはMarkdownで管理され、ビルドでHTML化＋メタデータを含むJSONに変換される。フロントエンドはそのJSONをもとにサーバー側でページを組み立てて配信する（いわゆるSSR的な工程）。
- 旧フロントの問題点  
  - 既存のReact（yari）はCRAから派生して複雑なWebpackやビルドスクリプト、SassとモダンCSSの混在、スコープのない大きなレンダーブロッキングCSSといった技術的負債を抱えていた。さらに、サーバー生成済みのHTMLをReactで再解釈するには膨大なクライアント処理が必要になり、実際は dangerouslySetInnerHTML で生HTMLを埋め込む運用になっていた。結果、コンテンツ内の小さなインタラクションはDOM APIで別実装するなど二重管理が発生。
- 採用したアプローチ：Web Components（Lit）  
  - Litでカスタム要素を作り、コンテンツ内にそのまま挿入する設計に移行。ビルド済みのHTMLを再解析せず、必要なインタラクションをコンポーネント単位で差し込めるため、重複実装や大規模なクライアントコードの送信を避けられる。  
  - 例：Scrimbaの埋め込み（Scrim）を <scrim-inline> のようなカスタム要素で実装。iframeはユーザー操作まで遅延ロードし、dialog要素でフルスクリーン表示を実現。Litのプロパティ／ライフサイクルで状態管理とテンプレート再描画を簡潔に書ける。
- インタラクティブ例（Playground）の再設計  
  - これまで分散していたプレイグラウンドを、小さなカスタム要素群に分割（例：<play-editor>, <play-console>, <play-runner>, <play-controller>）。要素同士を組み合わせて <interactive-example> を構成することで、著者がページ内で簡単にインタラクティブを埋められるようにした。  
  - Reactアプリに段階的に組み込めるため一気に全移行する必要はなく、既存のコードと共存しながら移行が可能。
- 効果  
  - クライアントに送る不要なJS/CSS削減、コンポーネント単位のスコープ化による副作用低減、技術的負債の抑制、コンテンツ作者の負担軽減。

## 実践ポイント
- 「静的にレンダリングされたHTMLをそのまま配る」設計にして、必要な箇所だけWeb Componentで差し込むと総体の負荷が下がる。  
- インタラクションは可能な限り遅延ロード（ユーザー操作トリガ）する。iframeやdialogを活用すると実装がシンプル。  
- 大規模なReactモノリスを一度に書き換えず、再利用可能なカスタム要素へ段階的に分割する。  
- CSSはコンポーネントスコープ（Shadow DOMやCSSカスタムプロパティ）で分離して、レンダーブロッキングを減らす。  
- 日本語ドキュメントや翻訳管理を残しつつ、著者が直接埋め込めるマクロ／要素を提供すると運用コストが下がる。

参考として、コンテンツ内に差し込むカスタム要素のイメージ：
```html
<!-- html -->
<scrim-inline url="https://v2.scrimba.com/〜" scrimtitle="Request-Response Cycle"></scrim-inline>
```

MDNのケースは「大規模ドキュメント＋多数の寄稿者・翻訳者」を抱えるプロダクトにとって実践的な設計例です。導入検討時はまず小さなインタラクションからLit/Web Componentsで試すことをおすすめします。
