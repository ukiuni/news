---
layout: post
title: "Facebook's Fascination with My Robots.txt - Facebookの私のrobots.txtへの執着"
date: 2026-02-23T13:52:21.798Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://blog.nytsoi.net/2026/02/23/facebook-robots-txt"
source_title: "Facebook's Fascination with My Robots.txt"
source_id: 47121210
excerpt: "Metaのクローラーが自宅Forgejoの/robots.txtを何千回も叩く謎と簡単対策"
---

# Facebook's Fascination with My Robots.txt - Facebookの私のrobots.txtへの執着
Metaが/robots.txtを何千回も叩く理由？Forgejo自宅サーバーに現れた「謎の外部ヒット」を追う

## 要約
自宅で動かすForgejoインスタンスの/robots.txtに、過去数日間にわたりMeta（Facebook）のクローラーが秒間複数回、しかも同じパスだけを大量にリクエストしている。影響は限定的だが原因と対処は把握しておくべきだ。

## この記事を読むべき理由
個人や小規模で自己ホスティングする日本のエンジニアにとって、巨大サービスの「異常な」アクセスは帯域やサーバー負荷の思わぬ原因になり得る。こうした現象の見分け方と簡単な対策を知っておくと安心です。

## 詳細解説
- 観測内容：ユーザーエージェントは facebookexternalhit/1.1（Metaの外部ヒットクローラー）で、送信元IPはMetaのレンジ。問題は「アクセス先が/robots.txtだけ」で、数千〜数万リクエスト／時に達している点。
- Metaのクローラー目的：基本的にリンク共有時のプレビュー（タイトル／説明／サムネ）を取得・キャッシュするためにサイトをクロールする。ただし通常はページ単位で巡回するので、特定のパスだけを延々と叩くのは異常挙動（ループやバグ、内部の一括調査処理などが考えられる）。
- なぜ/robots.txtだけ？推測例：キャッシュ準備やスキャンのトリガー誤判定、内部ループ、あるいは「まずrobots.txtを確認してから本格クロール」の処理が何らかの理由で繰り返されている可能性。
- 自己ホスティングへの影響：小さなVPSだと数千req/時でも帯域やIOに影響する。ログ肥大化や監視の誤アラートにもつながる。

## 実践ポイント
- まずログを確認：IPのASN（Metaか確認）、UA、時間帯、頻度を把握。
- UAだけを信用しない：逆引きやwhoisでIPレンジ（Metaのもの）を確認する。
- 速攻対処（サーバー側）
  - 軽い対応：robots.txtにキャッシュ指示を追加（Cache-Control）してレスポンス負荷を下げる。
  - レート制限：Webサーバーやプロキシで同一IP/レンジのリクエスト頻度を制限。
  - ファイアウォールで制限：nftables/iptables/ufwで過剰アクセスの遮断または制限。
  - キャッシュ/CDN導入：Cloudflare等でフロントキャッシュすればオリジン負荷を軽減。
- 参考設定（nginxの簡易レートリミット例）:
```nginx
limit_req_zone $binary_remote_addr zone=rl:10m rate=5r/s;

server {
  location = /robots.txt {
    limit_req zone=rl burst=20 nodelay;
    try_files /robots.txt =404;
  }
}
```
- 長期対策：ログローテーション・監視ルール（閾値超過で通知）、必要ならMeta側へ問い合わせ（企業規模ならIPの誤動作報告）。
- 日本の自己ホスト環境への応用：低帯域のホーム回線や共有レンタルサーバでは早めにレート制限／CDNで防御するのが実用的。

これらを順に試せば、原因究明しつつサーバーへの影響を最小化できます。
