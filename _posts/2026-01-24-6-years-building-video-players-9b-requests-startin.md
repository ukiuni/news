---
layout: post
title: "6 Years Building Video Players. 9B Requests. Starting Over - 6年間のプレイヤー開発、90億リクエスト、再出発"
date: 2026-01-24T16:39:16.394Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.mux.com/blog/6-years-building-video-players-9-billion-requests-starting-over"
source_title: "6 Years Building Video Players. 9 Billion Requests. Starting Over. | Mux"
source_id: 46689342
excerpt: "Vidstackの知見を活かしたVideo.js v10が再設計でカスタム性と保守性を大幅向上"
image: "https://cdn.sanity.io/images/2ejqxsnu/production/2478dba052821b4a949e3ed8b7151fa63130247c-1200x760.png"
---

# 6 Years Building Video Players. 9B Requests. Starting Over - 6年間のプレイヤー開発、90億リクエスト、再出発
90億リクエストで学んだ“動画プレイヤー再設計”──Video.js v10が日本の開発現場にもたらす実利

## 要約
Vidstackの6年の試行錯誤と実運用から得た教訓を取り込み、MuxがVideo.js v10として「フレームワークに自然に馴染む」「本質的にモジュール化された」動画プレイヤー基盤を再構築する話。

## この記事を読むべき理由
動画配信は日本でもニュース、Eコマース、教育、エンタメで必須。既存プレイヤーのカスタマイズ困難やビルド維持コストに悩む現場にとって、v10の設計は実務的な解決策を示すからです。

## 詳細解説
- 問題の所在：従来の「ウィジェット型」プレイヤーはブラックボックス化し、イベントに依存したUI連携やブラウザ差異で壊れやすい。Web Componentsは「一度書けばどこでも」の利点がある一方で、Shadow DOMやライフサイクル、SSR、TypeScript対応などの摩擦が大きかった。
- Vidstackの貢献：signalsと「state-down / events-up」設計、リクエスト追跡（ユーザーアクション→メディア応答を紐づける）やRadix風のコンポーネント群、アクセシビリティやマルチプロバイダ対応（HLS/DASH/YouTube等）を実装。だが「モノリス化した状態管理」「スキンの自由度不足」「フレームワーク間の保守コスト」が限界に達した。
- Video.js v10のアプローチ：
  - フレームワークネイティブなコンポーネントAPI（Web Componentsを無理に押し付けない）。
  - 非同期ストアやガードを備えた新コアで「スライス（slices）／プリセット」で必要な機能だけ導入できる設計。
  - React + Tailwindを共通言語にするコンパイラで、多フレームワーク＆スタイリングに出力（例：6フレームワーク×3CSS×36コンポーネント→自動生成で維持可能に）。
  - shadcn風の「ソースをコピーして自由にカスタムできる」スキン提供、React Nativeを最初から想定したコア分離。
- 小さなコード例（概念）：

```javascript
// javascript
const { Provider, usePlayer } = createPlayer({ slices: [playback] });
// usePlayer() に play(), pause() などが型付きで現れる
```

## 実践ポイント
- 現行のVidstack利用者は急ぎで移行する必要はないが、スキンや深いカスタムを考えるならv10の設計は移行メリット大。
- 日本の現場では「バンドルサイズ」「アクセシビリティ」「ネイティブアプリ連携（React Native）」を優先順位に入れて評価する。
- 開発ワークフロー：まずReact＋Tailwindでプロトタイプを作り、コンパイラ出力で他フレームワーク対応を検証するのが効率的。
- 貢献や採用を検討する際は、必要機能をスライス単位で選べる設計か、スキンのソースが実際に触れるかを確認する。

短く言えば、Video.js v10は「現場でカスタムしやすく、維持しやすい」ことを目指した再設計。日本のサービスでも採用メリットが見込めます。
