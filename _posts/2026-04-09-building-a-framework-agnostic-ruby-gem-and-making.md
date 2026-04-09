---
layout: post
title: "Building a framework-agnostic Ruby gem (and making sure it doesn't break) - フレームワーク非依存のRuby gemを作る（壊れないようにする工夫）"
date: 2026-04-09T15:10:44.202Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://newsletter.masilotti.com/p/on-building-a-framework-agnostic"
source_title: "On building a framework-agnostic Ruby gem (and making sure it doesn’t break)"
source_id: 47680061
excerpt: "data-native-*でERB/React/Vue共通のネイティブUIを作り、E2Eで回帰を防ぐ"
image: "https://substackcdn.com/image/fetch/$s_!iykL!,w_1200,h_675,c_fill,f_jpg,q_auto:good,fl_progressive:steep,g_auto/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F55d3362c-4568-4b33-baba-4fff3ef408c3_1999x1306.jpeg"
---

# Building a framework-agnostic Ruby gem (and making sure it doesn't break) - フレームワーク非依存のRuby gemを作る（壊れないようにする工夫）

RailsでもReactでもVueでも同じUIを動かす――「data-*属性」で作る壊れにくいRubyライブラリ

## 要約
単一のRuby gemでERB/React/Vue向けに同じネイティブUIを提供するため、HTMLのdata-native-*属性を出力するアプローチと、それを壊さないための自動化テスト戦略を紹介する。

## この記事を読むべき理由
日本でもRails＋フロント複合（React/Vue/Inertia）は増えており、異なるフレームワーク間で同一のネイティブ連携を保つ設計とテスト手法は現場で役立つから。

## 詳細解説
- アーキテクチャの核：ネイティブ連携は「隠しHTML要素に data-native-* を埋める」だけ。ネイティブ側はDOMを読み取り、MutationObserverで変化を検知してネイティブUIを作る。生成元（ERB/React/Vue）は問わない。
- フレームワーク別のAPI設計：各フレームワークで「らしさ」を保つ薄いラッパーを作る。ERBはブロック＆ビルダー、React/Vueはコンポーネント＆propsで出力を揃えるだけにするのがポイント。
  - ERB風（概念）:
```erb
<%= native_navbar_tag "Account" do |navbar| %>
  <% navbar.button icon: "ellipsis.circle" do |menu| %>
    <% menu.item "Edit profile", href: "/account/edit" %>
  <% end %>
<% end %>
```
  - React風（薄いコンポーネントの例）:
```javascript
export function NativeButton({ icon, href, children }) {
  const props = { "data-native-button": true };
  if (icon) props["data-native-icon"] = icon;
  if (href) props["data-native-href"] = href;
  return createElement("div", props, children);
}
```
- テスト戦略：HTML/JSの内部実装ではなく「実際のネイティブUI」を検証する。XCUITestでERB(Hotwire)、React(Inertia)、Vue(Inertia)のデモアプリを立ち上げ、実際のRailsサーバを動かしてネイティブ表示をアサートすることで、フレームワーク横断の回帰を防ぐ。
  - 例：メニューが表示される/タブ遷移でナビゲーションが更新される等をUIレベルで確認する。
- 拡張性の利点：data属性に依存するため、SinatraなどRails以外のテンプレートでも動作可能。ライブラリ側のヘルパーはRails特化でも、React/Vueコンポーネントや生HTML出力で対応できる点が拡張性を生む。

## 実践ポイント
- UI連携はまず「data-native-*」の設計で始める（DOMが共通契約になる）。
- フレームワーク別ラッパーは「薄く」：出力を揃え、ロジックはネイティブ側に寄せる。
- 各フレームワークを普段使う開発者のフィードバックを得る（「使い心地」を重視）。
- E2EでネイティブUIを検証するテストを用意する（XCUITest等）。HTML単体テストだけに頼らない。
- Rails以外の環境（Sinatraなど）での生HTML出力も想定しておくと採用の幅が広がる。
