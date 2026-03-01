---
layout: post
title: "Show HN: Vertex.js – A 1kloc SPA Framework - Vertex.js — 1KB台で完結するSPAフレームワーク"
date: 2026-03-01T14:13:55.638Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://lukeb42.github.io/vertex-manual.html"
source_title: "Float64 Vertex"
source_id: 47205659
excerpt: "約1KBの単一ファイルでフック・ルーター付きReact風SPAをビルド不要で即構築"
---

# Show HN: Vertex.js – A 1kloc SPA Framework - Vertex.js — 1KB台で完結するSPAフレームワーク
たった1KBで「Reactっぽい」開発体験を提供する超軽量フレームワーク、Vertex.jsの全体像と実践的な使いどころ

## 要約
Vertex.jsはUMD形式の単一ファイル（約1k行）で、React風のFiber reconciler、フック群、テンプレートエンジン、jQuery互換のDOMラッパー、AJAX、ハッシュルーティングまで揃えた軽量SPAフレームワークです。ビルド不要でそのまま静的配信できるのが特徴です。

## この記事を読むべき理由
ローカルの静的サイトや社内ツール、プロトタイプを素早くSPA化したい日本の開発者にとって、最小限の依存でReactライクな開発体験を得られる実用的な選択肢だからです。ビルドチェーンを避けつつフックやコンポーネント設計を試したい場面で特に役立ちます。

## 詳細解説
- 配布と導入  
  - 単一ファイルのUMDモジュールなので、staticフォルダに置くだけで <script> から読み込めます（jQueryと共存可能）。読み込み後はグローバルに Vertex と V$（DOMラッパー）が使えます。

  - 例（HTML読み込み）:
  ```html
  <script src="/static/vertex.js"></script>
  <div id="root"></div>
  ```

- DOMラッパー（V$）  
  - jQuery風のチェーン可能API。要素選択、作成、イベント（.on/.off/.trigger）、属性・スタイル操作、挿入・削除・走査など基本操作が揃っています。jQueryが既にいる場合は干渉せず併用できます。

- AJAX  
  - Fetchをラップした Vertex.ajax があり、jQueryライクな success/error や .done/.fail をサポート。簡単なGET/POSTラッパーも用意。

- テンプレートエンジン（Vertex.template）  
  - Mustacheライクなテンプレートをサポート。外部テンプレートを baseUri にまとめて読み込み、テンプレート内の input に data-bind を付けると双方向バインディングが働きます。テンプレートはローカル断片（<template>）かレスポンス全体を利用可能。

- FiberベースのUI（createElement / render）  
  - APIはReact互換を目指しており、createElement（h）/render/Fragment を使ってコンポーネントを定義・マウントできます。Vertex.lazy による遅延ロードも対応。

  - 例（マウント）:
  ```javascript
  const { createElement: h, render } = Vertex;
  function App(){ return h("div", null, "Hello Vertex"); }
  Vertex.render(h(App), document.getElementById("root"));
  ```

- フック（useState 等）  
  - Reactと同じルールで useState, useReducer, useEffect, useRef, useMemo, useCallback, createContext/useContext が利用可能。useHash フックはハッシュ変更で自動的に再レンダリングするためシンプルなルーティングに便利。

- ルーター  
  - ハッシュベースの Router（Backbone風）を内蔵。named params や splat（*path）対応、RouterClass でクラスベース定義も可能。useHash と併用してURL駆動の画面切替が簡単にできます。

- jQuery互換性  
  - jQueryを先に読み込めば Vertex は $ を上書きしません。V$ または Vertex.$v() を使えば衝突なく共存できます。

## 実践ポイント
- すぐ試す手順（最短）  
  1. vertex.js を static に置く（curl で取得可）。  
  2. HTMLで読み込み、root要素を用意。  
  3. 簡単なコンポーネントを h + render でマウントして動作確認。

- 使いどころの目安  
  - プロトタイプ、ドキュメントサイト、CMSテンプレート、社内ツールや管理画面など「ビルド不要で軽くSPA化したい」ケースに最適。Reactの学習コストなしにフックやコンポーネント設計を試せます。

- 注意点  
  - 大規模アプリや豊富なエコシステムが必要な場合は従来のフレームワークの方が有利。ライブラリサイズは小さいが機能はミニマムなので、要件に応じて使い分けてください。

以上を踏まえ、まずは既存の静的プロジェクトに数行足してVertexの感触を掴むことをおすすめします。
