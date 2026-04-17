---
layout: post
title: "288,493 Requests – How I Spotted an XML-RPC Brute Force from a Weird Cache Ratio - 24時間で288,493件のリクエスト：異常なキャッシュ率で見つけたXML-RPCブルートフォース"
date: 2026-04-17T03:36:49.714Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://marcindudek.dev/blog/xmlrpc-brute-force-cache-rate/"
source_title: "288,493 Requests in 24 Hours — How I Spotted an XML-RPC Brute Force via Cache Rate — Marcin Dudek"
source_id: 47751608
excerpt: "キャッシュ率急落で発見：/xmlrpc.phpに24時間288,493回の多重ログイン攻撃"
image: "https://marcindudek.dev/images/headshot.png"
---

# 288,493 Requests – How I Spotted an XML-RPC Brute Force from a Weird Cache Ratio - 24時間で288,493件のリクエスト：異常なキャッシュ率で見つけたXML-RPCブルートフォース
そのキャッシュ率、放っておくとサーバー燃えます — Cloudflareの「異常な低キャッシュ率」で発見した静かな攻撃の話

## 要約
Cloudflareのキャッシュヒット率が0.8%に急落して発見。単一のIPが24時間で288,493回のPOSTを/xmlrpc.phpに送り、system.multicallで1リクエストあたり数百の認証試行を行っていた。対策はエッジでのWAFブロック＋WordPress側でxmlrpcを無効化する多層防御。

## この記事を読むべき理由
キャッシュ率の急落は、見た目の稼働（ページが表示される）では気づきにくい攻撃を示す重要なシグナルであり、日本のWordPress運用者にもすぐ実行できる対処法があるため。

## 詳細解説
- なぜキャッシュ率がシグナルになるか：xmlrpc.phpはPOSTのみで動的扱いになるため、攻撃リクエストはすべて「アンキャッシュ（dynamic）」に入り分母を増やす。静的寄りのサイトでヒット率が70–90%のところが1%以下になると異常。
- system.multicallの仕組み：単一のXML-RPC POSTに複数（数百）の認証試行を詰め込めるため、リクエスト数ベースのレート制限や単純なWAFを回避しやすい。効率的で静かな増強（アンプリフィケーション）。
- どうやって検出するか（Cloudflare）：
  - DashboardのAnalytics → Traffic → Top Pathsで/xmlrpc.phpが上位に入り、cacheStatusがdynamicで大量リクエストなら要注意。
  - APIで確認する例：
```graphql
query($zone:String!, $since:Time!, $until:Time!) {
  viewer {
    zones(filter:{zoneTag:$zone}) {
      httpRequestsAdaptiveGroups(
        limit:20,
        filter:{datetime_geq:$since, datetime_leq:$until},
        orderBy:[count_DESC]
      ) {
        count
        dimensions { clientIP clientCountryName clientRequestPath cacheStatus }
      }
    }
  }
}
```
- 具体的な攻撃例（簡易イメージ）：
```xml
<?xml version="1.0"?>
<methodCall>
  <methodName>system.multicall</methodName>
  <params>...多数のlogin試行を含む...</params>
</methodCall>
```

## 実践ポイント
- まず確認：CloudflareのTop Pathsを週次でチェック。/xmlrpc.phpが上位なら既に攻撃されている可能性大。
- 速攻対策（エッジでブロック）：Cloudflare WAFカスタムルールを追加。
```text
(http.request.uri.path eq "/xmlrpc.php")
```
- WordPress側でも無効化（防御の重ね掛け）：
```php
add_filter('xmlrpc_enabled', '__return_false');
add_filter('xmlrpc_methods', function($methods) { return []; });
```
- Jetpackを使う場合は全ブロックではなく、JetpackのIPレンジだけ許可するWAFルールを検討。
- 習慣化：キャッシュヒット率の監視を主要KPIに追加、WAFルールは新規サイトに事前適用、CDN/WAFを導入してないならまずそこから。

以上。
