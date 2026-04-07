---
layout: post
title: "Dropping Cloudflare for Bunny.net - Cloudflareからbunny.netへ乗り換え"
date: 2026-04-07T14:24:11.945Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://jola.dev/posts/dropping-cloudflare"
source_title: "Dropping Cloudflare for bunny.net | jola.dev"
source_id: 47675013
excerpt: "Cloudflare依存を脱し、低コストで高速なbunny.netへ移行する設定手順と運用ポイント"
image: "https://jola.dev/images/og-image-2b7872671fc7c11e464dac899d8d3068.png?vsn=d"
---

# Dropping Cloudflare for Bunny.net - Cloudflareからbunny.netへ乗り換え
魅力的なタイトル: 「Cloudflare離脱で自由を取り戻す――低コストで速いbunny.netに移行した理由と実践ガイド」

## 要約
筆者はCloudflare依存のリスクと中央集権化への懸念から、EU系CDNのbunny.netへブログを移行。設定手順、キャッシュ戦略、運用上の注意点を具体的に紹介します。

## この記事を読むべき理由
Cloudflareは強力ですが単一障害点になり得ます。日本の個人開発者や中小サイト運営者が、低コストで高性能な代替を評価・導入するために実用的な手順と考慮点が得られます。

## 詳細解説
- なぜbunny.netか：スロベニア発のEU企業で、世界的に高いパフォーマンスを示しつつCloudflareよりPoP数は少ないものの競争力あり。欧州事業者を支援したい、あるいは米国集中に抵抗がある場合の選択肢になる。
- 料金と試用：初期クレジット（$20、条件で追加$30）あり。従量課金で月最低$1。コスト可視化がしやすく小規模運用に向く。
- 基本構成（Pull Zone）：bunny.netの「Pull Zone」を作り、Origin URL（サーバのIPやホスト）を設定。複数アプリ運用時はHostヘッダを透過する設定が重要。
- DNS連携：カスタムホスト名を追加し、ドメイン側にCNAMEを登録（例: yoursite.b-cdn.net を指す）。登録後「Verify & Activate SSL」で証明書を有効化。
- キャッシュの基本：bunny.netはデフォルトでオリジンのCache-Controlを尊重。Cache-Controlを適切に返すことで静的ファイルだけでなくHTMLまで高速に配れる。
  - オプションとしてSmart Cacheを有効化すれば典型的な静的リソースを自動でキャッシュ。
- 実運用の高速化：著者はHTMLにもs-maxageを付与してエッジでキャッシュする構成を採用。公開後はPull Zoneのパージが必要。
  - 例：Phoenixで応答ヘッダを付けるミドルウェア（抜粋）。

elixir
```elixir
defp put_cdn_cache_header(conn, _opts) do
  put_resp_header(conn, "cache-control", "public, s-maxage=86400, max-age=0")
end
```

- 付帯設定：Force SSL、Origin Shield（オリジンに近いシールドPoPでキャッシュを集約してオリジン負荷を低減）、Stale Cacheオプション（オリジン不在時や更新中に古いコンテンツを返す）などを活用。
- Edge Rules：b-cdn.net の自動ドメインから本来のドメインへ301リダイレクトするルールを作るとクロールやSEOで混乱しない。
- その他：ダッシュボードのログ/メトリクスが充実。将来的にS3互換ストレージなど機能追加予定。

## 実践ポイント
- まず試用クレジットでPull Zoneを作成し、CNAME→SSLの流れを確認する。
- 重要：オリジンが返すCache-Controlを設計する（静的は長め、HTMLはs-maxageでエッジキャッシュを制御）。
- 公開フローに「Pull Zoneパージ」を組み込む（CIやデプロイ後のAPI呼び出しで自動化すると楽）。
- Origin Shieldを有効にしてオリジン負荷を減らす。リージョンはオリジンに近い場所を選択。
- Edge RuleでCDN自動ドメインから本来ドメインへのリダイレクトを設定。
- レジストラはPorkbunなどの選択肢を検討（WHOISプライバシーやサポートも確認）。

参考に、まずは非本番サイトで数日運用してログやキャッシュ状況を確認すると安全です。
