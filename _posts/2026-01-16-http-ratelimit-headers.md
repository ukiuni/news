---
layout: post
title: "HTTP RateLimit headers - HTTP RateLimit ヘッダ"
date: 2026-01-16T01:44:49.898Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://dotat.at/@/2026-01-13-http-ratelimit.html"
source_title: "HTTP RateLimit headers &ndash; Tony Finch"
source_id: 1293853842
excerpt: "GCRAを用いたRateLimitヘッダで429を減らし、次に送れる量と待ち時間を明確に伝える"
---

# HTTP RateLimit headers - HTTP RateLimit ヘッダ
429を減らす：クライアントに優しいRateLimitヘッダ設計ガイド

## 要約
HTTPの標準ドラフトは、サーバーがクライアントに現在の許容量を伝える `RateLimit` 系ヘッダを定義します。線形レートリミッタ（GCRA系）を使えば、クライアントを「バースト→待機」の非効率な挙動に誘わず、滑らかなリクエスト間隔を促せます。

## この記事を読むべき理由
APIやモバイル向けサービスでの「429 Too Many Requests」はユーザー体験とコストに直結します。日本の帯域やモバイル環境で多い短いバースト通信にも強い、実用的なレート通知設計を学べます。

## 詳細解説
ドラフトは主に2つのヘッダを想定します：
- RateLimit-Policy: サーバーが適用するポリシーの入力パラメータ（名前、partition key(pk)、quota(q)、window(w)、quota units(qu)など）
- RateLimit: 実際にそのリクエストに適用された結果（名前、pk、available quota(r)、effective window(t)）

最大持続レートは
$$
\text{rate} = \frac{\text{quota}}{\text{window}}
$$
最大レート時のリクエスト間隔は
$$
\text{interval} = \frac{1}{\text{rate}} = \frac{\text{window}}{\text{quota}}
$$

線形レートリミッタ（GCRAの亜種）はクライアントごとに「not-before」時刻だけを保持します。処理の要点は以下の通りです：
- state[pk] に not-before を保持（新規は十分過去の値）
- not-before をスライディングウィンドウ内に clamp（バースト上限と悪意への保険）
- リクエストの「時間コスト」を not-before に加算（cost × interval）
- 現在時刻 now が not-before より後なら許可。差分からヘッダの r（残り許容量）と t（有効ウィンドウ）を算出し、r は切り捨て、t は切り上げで整数にする
- not-before ≥ now なら拒否。r=0、t=ceil(not-before-now)

擬似コード（核心部分）:
```python
# python
time = state.get(pk, 0)                   # not-before
time = clamp(now - window, time, now)
time += interval * cost                   # spend nominal time
if now > time:
    state[pk] = time
    d = now - time
    r = floor(d * rate)
    t = ceil(d)
    return ALLOW(r, t)
else:
    r = 0
    t = ceil(time - now)
    return DENY(r, t)
```

この方式の利点：
- 追加状態が少なくスケールしやすい（タイムスタンプのみ）
- 許可したバーストはその後の有効ウィンドウを縮め、自動的にリクエスト間隔を平滑化する
- クライアントに「次にいつどれだけ送れるか」を明確に伝えられる

対照として「固定リセット」型（窓終了でquotaリセット）は、バースト→待機→バーストの周期的行動を促してしまいます。スライディングログ方式は正確だがコスト高です。

## 実践ポイント
- API側で RateLimit-Policy と RateLimit ヘッダをセットしてクライアントに現在の r/t を返す（r は floor、t は ceil）
- 実装は GCRA（not-beforeタイムスタンプ）を推奨：状態は timestamp 1つ／クライアントのみ
- 内部計算はサブ秒精度で行い、ヘッダのr,tは整数で返す
- 過剰な試行へのペナルティやタイムアウトは clamp の上限を未来に広げる形で実装可能
- 使い分け：短いバーストを許容するAPIは window/q を調整し、モバイル回線のばらつきを考慮する（日本のキャリア環境では小さな window と滑らかな interval が有効な場合が多い）
- 長期アイドルクライアントの state は定期クリーンアップで削除する
- API Gateway（Nginx / Cloudflare / AWS）での導入時はヘッダの付与・ログ化と、クライアント向けのドキュメント（どのヘッダを見てどう振る舞えばよいか）を用意する

短くまとめると：単に「429を返す」より、GCRA系の線形リミッタと RateLimit ヘッダで「次に何ができるか」を伝えれば、クライアント側がスマートにリトライできて全体のユーザー体験が改善します。
