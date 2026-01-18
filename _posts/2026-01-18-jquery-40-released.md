---
layout: post
title: "jQuery 4.0 released - jQuery 4.0 リリース"
date: 2026-01-18T04:05:25.359Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://blog.jquery.com/2026/01/17/jquery-4-0-0/"
source_title: "jQuery 4.0 released"
source_id: 423983298
excerpt: "jQuery 4.0の破壊的変更とESM対応、移行チェック必須"
---

# jQuery 4.0 released - jQuery 4.0 リリース
20年目の大刷新：jQuery 4.0で何が変わるか、今すぐ押さえるべきポイント

## 要約
jQueryが約10年ぶりのメジャーアップデートである4.0.0を正式リリース。古いブラウザ対応の削減、ESモジュール化、Deprecated APIの削除、Trusted Types/CSP対応、そしてスリムビルドの見直しなど、モダン開発に向けた整理が行われた。

## この記事を読むべき理由
日本の企業サイトやレガシー案件では未だにjQueryが広く使われています。4.0は互換性に関わる破壊的変更を含むため、アップグレード方針や社内のブラウザサポート判断、ビルド・配布方法を検討する必要があるからです。

## 詳細解説
- ブラウザサポートの整理  
  - IE10以前やEdge Legacy、非常に古いiOS/Androidブラウザなどのサポートを削除。IE11はまだ残るが、将来的に段階的に外す予定（jQuery 5でさらに進む）。
- Trusted Types / CSP対応  
  - TrustedHTML入力を扱えるようにし、インラインスクリプトやCSPでのエラーを避けるために非同期スクリプトの多くを<script>タグで実行するよう変更。CSP厳格運用環境での互換性が向上。
- ソースのESモジュール化（AMD → ES modules）  
  - Rollupでパッケージングし、ESMとして扱えるようになったため、モダンなビルドツールやブラウザのモジュール機能と親和性が高まる。
- 削除されたDeprecated API（代表例）  
  - jQuery.isArray, jQuery.parseJSON, jQuery.trim, jQuery.type, jQuery.now, jQuery.isNumeric, jQuery.isFunction など。これらはネイティブの Array.isArray(), JSON.parse(), String.prototype.trim(), Date.now() などで代替可能。
- 内部専用メソッドの削除  
  - プロトタイプ上の push / sort / splice が削除。もし既存コードで直接使っているなら [].push.call($elems, elem) のように置換する必要がある。
- フォーカスイベント順の変更  
  - ブラウザのW3C準拠順に合わせ、以前のjQuery独自順序から変更（break）。フォーカス関連の挙動に依存するテストは要確認。
- スリムビルドの再設計  
  - Deferreds/Callbacksを除外したスリム版を提供（サイズはさらに小さく、約19.5k gzipped の目安）。多くはネイティブPromiseで代替可能。IE11サポートが必要ならポリフィル検討。
- サイズと配布  
  - 非推奨APIや古いIE対応の削除で圧縮サイズが削減。CDNとnpmで公開済み。移行用にjQuery Migrateプラグインとアップグレードガイドが用意されている。

## 日本市場との関連性
- 企業内レガシー環境ではIE11以前の端末や古い社内ブラウザが残存しているケースがあるため、即時移行は慎重に。特に社内ポータルや業務システムは影響が大きい。  
- 一方でスタートアップやモダン開発の現場ではESM対応や小さなビルドサイズは歓迎されるため、npm経由での移行やバンドル最適化が進めやすい。  
- CSPを厳格に運用する金融・大企業系サービスではTrusted Types対応はプラス材料。

## 実践ポイント
- 事前チェックリスト（優先順）  
  1. コードベースで削除されたAPIを検索（例: jQuery.trim → .trim()）  
  2. jQuery Migrateを使って問題点を検出し、順次修正する  
  3. DeferredをPromiseへ置換。IE11サポートが必要ならPromiseポリフィルを追加する  
  4. フォーカス/blur周りのテストを実行し、イベント順の違いを確認する  
  5. 内部配列メソッド利用箇所は [].push.call 等に差し替える  
  6. ビルドをESMに合わせて更新（import 'jquery'）、Rollup/Webpack等の設定確認  
  7. CDNリンクを差し替え：https://code.jquery.com/jquery-4.0.0(.min).js または npm install jquery@4.0.0  
- 短いコード例（Deprecated → 推奨）
```javascript
// deprecated
// var a = jQuery.isArray(obj);

// recommended
var a = Array.isArray(obj);

// deprecated
// var s = jQuery.trim(str);

// recommended
var s = String.prototype.trim.call(str);
```
- 移行タイミングの判断  
  - 顧客・社内ユーザーにIE10以下がいる場合は当面3.xを維持。モダン環境が主なら早めに4.xへ移行して恩恵を受ける。

まとめ：jQuery 4.0は「整理とモダン化」が中心のリリース。互換性に注意しつつ、ESM対応やCSP改善、軽量化といった利点を活かす計画を立てることが重要。まずはjQuery Migrateで現状評価を。
