---
layout: post
title: "Resurrecting _why's Dream - _whyの夢を復活させる"
date: 2026-02-19T22:13:25.351Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://schwadlabs.io/blog/resurrecting-whys-dream"
source_title: "SchwadLabs — Software That Just Works"
source_id: 1336283822
excerpt: "Rubyで一行でウィンドウを開くShoesの夢をWebViewで復活させるScarpeの進捗と配布法"
---

# Resurrecting _why's Dream - _whyの夢を復活させる
Rubyで「たった数行でウィンドウが開く」体験を取り戻す——Shoesの精神を受け継ぐScarpeの挑戦

## 要約
2008年のShoes（_why作）は“アイデア→動くプログラム”の摩擦を極限まで減らしたが、ネイティブGUIの維持コストで消えた。ScarpeはWebViewにレンダリングする戦略で再現を目指し、教材Hackety Hackの互換や単一バイナリ配布の実現に近づいている。

## この記事を読むべき理由
日本でも学校の授業、ハッカソン、プロトタイプ作成、アーティストのツール需要が高く、“簡単にウィンドウを立ち上げる”体験は依然有益。Ruby好き・教育関係者は今回のアプローチを知っておく価値がある。

## 詳細解説
- Shoesの強み：DSLでボイラープレートを排し、初心者がすぐにGUIを作れる設計（読みやすく教えやすい）。
- 失敗の原因：GTK/Cocoa/Win32などプラットフォーム固有のネイティブ実装を三度書く必要があり、メンテナンス負荷でプロジェクトが維持できなくなった。
- 過去の試み：Shoes3／Shoes4などの努力は学びを残したが、ネイティブ路線はボランティアチームにとって重すぎた。
- Scarpeの設計：ネイティブUIと戦わず、ShoesのDSLをDOM操作に変換してローカルWebView上で動かす。ブラウザエンジンの恩恵（CSSレイアウト、イベント処理の一貫性）を利用することでクロスプラットフォームの負担を大幅に削減する。
- マッピングの難しさ：多くは素直にDOMへ置き換えられるが、flowレイアウトや描画プリミティブ、一部のイベントチェーンは工夫が必要。技術的には解決可能な課題。
- 互換性目標：Hackety Hack（学習環境）を動かせれば合格ライン。サイドバー、レッスン、描画（star/oval/rect/line/arc）、タイマーなどの実装は進んでいるが一部問題あり。
- 配布（パッケージング）：Traveling Rubyを使いRubyランタイム／gemを同梱し、macOS用の単一.app（プロトタイプで約13MB）を生成可能に。コマンド例は下記。

```ruby
# Shoes風の例（入力）
stack do
  para "Hello"
  button("Click") { alert "Hi" }
end
```

```html
<!-- 生成される概念的なHTML -->
<div class="stack">
  <p>Hello</p>
  <button onclick="...">Click</button>
</div>
```

```bash
# パッケージ例
scarpe package myapp.rb
# → MyApp.app（約13MB）を出力
```

## 実践ポイント
- ScarpeのGitHubをチェックしてサンプルや進捗を追う（コントリビュート歓迎）。
- Hackety Hackを動かして互換性を確かめるのが第一歩。
- 教育用途やプロトタイピングではWebViewベースのGUIが実用的な選択肢になることを検討する。
- macOS向けパッケージは既に試せるので、小さな教材アプリを作って配布フローを試す（scarpe package）。
- Windows/Linuxサポートやイベント周りの細部はまだ発展途上なので、実運用前に十分なテストを行う。

（参考）Scarpeはオープンソースで開発中。開発への参加や実験的利用を通じて、Shoesの「一行でウィンドウが出る」体験を再現してみてください。
