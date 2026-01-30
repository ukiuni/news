---
layout: post
title: "Richard Feynman Side Hustles - リチャード・ファインマンのサイドハッスル"
date: 2026-01-30T16:18:54.202Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://twitter.com/carl_feynman/status/2016979540099420428"
source_title: "Richard Feynman Side Hustles"
source_id: 46824867
excerpt: "JavaScript依存で情報が消える危険と具体的対策を実例で学ぶ"
---

# Richard Feynman Side Hustles - リチャード・ファインマンのサイドハッスル
「ファインマンがもしWeb開発者だったら？」——JavaScript無効で表示不能になったツイートから学ぶ、実践的なウェブ設計

## 要約
元ツイートのページが「JavaScriptが無効です」と表示され閲覧できない事例をきっかけに、JavaScript依存の落とし穴と回避策（プログレッシブ・エンハンスメント、SSR、フォールバック設計）を分かりやすく解説します。

## この記事を読むべき理由
日本の企業内ブラウザやプライバシー重視の設定、LINEなどのWebViewではスクリプトが制限されることが多く、重要な情報が読めない／サービスが壊れるリスクがあります。ユーザー体験とアクセシビリティを守る実践知が得られます。

## 詳細解説
- 問題の本質：JavaScript必須設計は、スクリプト無効化や広告・追跡防止拡張によってページが機能不全になる。結果として情報が見えない、検索エンジン評価が下がる、障害者支援技術との非互換が起きる。  
- 対策の考え方：まず「重要コンテンツはサーバ側で提供できるか」を検討する（プログレッシブ・エンハンスメント）。次に必要ならクライアント側で機能強化（ハイドレーション等）する。  
- 実装パターン：  
  - サーバサイドレンダリング（SSR）や静的生成（SSG）で初期HTMLを確保する（Next.js、Nuxt、Astroなど）。  
  - <noscript>で最低限の案内を出す。  
  - 重要機能はJavaScriptの存在に依存させず、フォームやリンクでフォールバック可能にする。  
  - プライバシー拡張で外部スクリプトがブロックされる想定で、外部依存を最小化する。  
- 運用面：ブラウザ互換性情報や「JavaScriptが必要な理由」を明示し、企業のセキュリティ担当向けにホワイトリスト案内を用意すると導入障壁が下がる。

## 実践ポイント
- まずHTMLだけで主要コンテンツが読めるか確認する。  
- 最低限の案内を出す例（HTML）:
```html
<noscript>
  このページはJavaScriptが無効なため正しく表示されない可能性があります。JavaScriptを有効にするか、こちらのテキスト版をご覧ください。
</noscript>
```
- JavaScript存在チェックで軽い強化表示（JavaScript）:
```javascript
document.documentElement.classList.remove('no-js');
document.documentElement.classList.add('js');
```
- 技術選定の優先順：SSR/SSG → プログレッシブ・エンハンスメント → クライアント側ハイドレーション。  
- 日本向け配慮：企業のプロキシやモバイルキャリア環境、LINE内ブラウザを想定した確認を行う（社内検証端末・QAリストに追加）。

短く言えば、JavaScript依存に頼り切るのは情報を失うリスクを招く。まず「HTMLで読めること」を担保し、必要な場面で安全にJSで強化する設計を習慣にしましょう。
