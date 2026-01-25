---
layout: post
title: "Connection Exhaustion in High-Traffic Systems - 高トラフィックシステムにおけるコネクション枯渇"
date: 2026-01-25T02:01:50.430Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://open.substack.com/pub/systemdr/p/connection-exhaustion-in-high-traffic?utm_source=share&amp;utm_medium=android&amp;r=5bgzxg"
source_title: "Connection Exhaustion in High-Traffic Systems"
source_id: 419545259
excerpt: "遅いモバイル接続がサーバのソケットを枯渇させる問題と、L7プロキシで待ち時間を切り離す解決策を解説"
image: "https://substackcdn.com/image/fetch/$s_!gwsR!,w_1200,h_675,c_fill,f_jpg,q_auto:good,fl_progressive:steep,g_auto/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6302e411-379f-46bc-b6ca-8dfa62802df3_2800x1600.png"
---

# Connection Exhaustion in High-Traffic Systems - 高トラフィックシステムにおけるコネクション枯渇
スマホの遅いアップロードでサーバが詰まる？L7で“待ち時間”を切り離す現場の処方箋

## 要約
クライアント側の長い遅延（Long‑Tail）が原因でサーバのソケット／スレッドが埋まり、CPU/RAMは余っているのに新規接続が拒否される現象（コネクション枯渇）が発生する。L7プロキシでクライアントとバックエンドを切り離すことで解決できる。

## この記事を読むべき理由
モバイルや不安定なネットワークが増えた日本のサービス運用でも、見かけ上リソースに余裕があって突然「Connection refused」が出る問題は頻出。原因と対策（L4とL7の違い、設定例、監視指標）がすぐ実践できる形で得られます。

## 詳細解説
- 問題の本質  
  LinuxではTCPコネクションごとにファイルディスクリプタ（FD）とカーネル/アプリ側のリソースが消費される。スレッドやワーカープールを接続数分だけ消費する設計（thread‑per‑connection）だと、遅いクライアントが長時間スレッドやFDを保持してしまい、短時間で枯渇する。

- 長尾（Long‑Tail）遅延の影響（概算）  
  たとえば遅いクライアント割合$f=0.2$、到着率$r=500\ \mathrm{req/s}$、遅いセッション保持時間$T_s=30\ \mathrm{s}$、速いセッション$T_f=0.05\ \mathrm{s}$なら、同時占有コネクションは概ね次の式で見積もれます。  
  $$C \approx r \times (fT_s + (1-f)T_f)$$  
  この例だと短時間で数千〜万のコネクションに到達します。

- なぜL4（NAT型）ではダメか  
  NLBやハードウェアLBのようなL4はTCPを終端せずパケットを透過させるため、バックエンドはクライアントの遅さにそのまま引きずられる。RTTやパケットロスが大きいクライアントがいるとバックエンドのソケットが長時間 ESTABLISHED のままになる。

- L7バッファリングでの解決法  
  Nginx/Envoy/HAProxy等のL7はエッジでTCPを終端し、リクエストを自身のバッファに取り込んでからバックエンドへ高速な接続で転送する。これにより30秒のクライアント転送をバックエンド側では50msの短いトランザクションに変換でき、ワーカーの占有時間を劇的に減らせる。

- 実装上の注意  
  L7プロキシで「リクエストバッファリング」を有効にし、バックエンドごとの接続上限を設定、keepaliveで接続を温める。また client_body_timeout や最大リクエストサイズの制限を設けて悪影響を防ぐ。

Nginxの例（一部抜粋・要調整）:

```nginx
upstream backend_pool {
  server app1:8080 max_conns=1000;   # バックエンド保護
  keepalive 64;                      # Backend keepalive
}

server {
  listen 80;
  client_body_timeout 30s;
  client_max_body_size 10M;

  location / {
    proxy_pass http://backend_pool;
    proxy_http_version 1.1;
    proxy_set_header Connection "";   # keepalive用
    proxy_buffering on;               # レスポンスをバッファ
    proxy_request_buffering on;       # リクエストをバッファ
  }
}
```

## 実践ポイント
- エッジにL7プロキシ（Nginx/Envoy/HAProxy）を導入してクライアント遅延を吸収する。  
- バックエンドごとに max_conns や keepalive を設定し、ワーカー枯渇を防ぐ。  
- 監視項目を追加：ESTABLISHED/TIME_WAITソケット数、LBのバックエンド待ちキュー長、FD使用率（ulimit‑nの70%でアラート）。  
- client_body_timeout と client_max_body_size を設定して悪質/重い接続を早期切断。  
- 実験用コードやデモは参考に： https://github.com/sysdr/sdir/tree/main/connection-exhaustion

短時間の投資で「待ち時間に対する耐性」を作れば、無駄にアプリサーバを垂直／水平スケールするコストを大幅に減らせます。
