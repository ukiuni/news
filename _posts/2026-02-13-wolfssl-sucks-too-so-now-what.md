---
layout: post
title: "WolfSSL Sucks Too, So Now What? - WolfSSLもダメだった、さてどうする？"
date: 2026-02-13T11:35:23.204Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://blog.feld.me/posts/2026/02/wolfssl-sucks-too/"
source_title: "WolfSSL Sucks Too, So Now What? &ndash; Makefile.feld"
source_id: 47001095
excerpt: "WolfSSLのTLS1.3 middlebox互換でElixir/OTP接続が失敗、回避策あり"
image: "https://blog.feld.me/static/site_logo_512.png"
---

# WolfSSL Sucks Too, So Now What? - WolfSSLもダメだった、さてどうする？
WolfSSLがTLS 1.3でつまずく理由と、Elixir/Erlang環境で今すぐできる対処法

## 要約
WolfSSLのTLS 1.3実装がRFC準拠の「middlebox互換モード」を柔軟に扱えず、Elixir/Erlang（OTP）のデフォルト設定と組み合わさると接続失敗を引き起こす問題が報告されています。

## この記事を読むべき理由
日本でも組み込み系や軽量SSL実装を採用する場面が増えており、WolfSSLを使う/接続先にする場合の互換性問題は実運用で直面する可能性が高いため。

## 詳細解説
- RFC 8446（TLS 1.3）は、古い中継機（middlebox）互換性のために「セッションIDを利用した互換モード」とダミーの ChangeCipherSpec（CCS）交換を規定しています。これは本質的にはTLS1.3動作をTLS1.2風に“偽装”するための折衷策です。  
- WolfSSLはその互換機能をコンパイル時フラグ（-DWOLFSSL_TLS13_MIDDLEBOX_COMPAT）で固定しており、実行時にクライアント／サーバ間で部分交渉する仕様になっていないため、RFCの期待する挙動と合致しないケースが発生します。  
- Erlang/OTPのssl実装は安全策として middlebox_comp_mode をデフォルト有効にしているため、WolfSSLをサーバにした場合にTLS1.3でハンドシェイクが失敗し、Elixir/Erlang系のHTTPクライアントが接続できなくなる事象が確認されています（ログに「Failed to assert middlebox server message」などが出る）。  
- 結果として、WolfSSLが常にRFC互換であるとは限らず、相手方ライブラリや設定次第で相互運用性の問題が生じます。

## 実践ポイント
- 接続トラブルの切り分け
  - サーバ側がWolfSSLか確認する（サーバ管理者へ問い合わせ / TLS fingerprint）。  
  - クライアントで middlebox_comp_mode を明示的に無効化して試す（Elixir/OTPの場合は ssl オプションで middlebox_comp_mode: false）。  
- 一時回避策
  - TLSバージョンをtlsv1.2限定にする（短期的に互換性確保）。  
  - Elixir用PoC（Elixir 1.17.3 + OTP 26）例：
```elixir
#!/usr/bin/env elixir
url = "https://some-wolfssl-endpoint" |> String.to_charlist()
{:ok, _} = Application.ensure_all_started(:inets)
{:ok, _} = Application.ensure_all_started(:ssl)
:logger.set_application_level(:ssl, :debug)

http_options = [
  ssl: [
    verify: :verify_peer,
    cacerts: :public_key.cacerts_get(),
    depth: 2,
    customize_hostname_check: [match_fun: :public_key.pkix_verify_hostname_match_fun(:https)],
    versions: [:"tlsv1.2", :"tlsv1.3"],
    middlebox_comp_mode: false
  ]
]
options = [body_format: :binary]
:httpc.request(:get, {url, []}, http_options, options)
```
- 長期的対策
  - WolfSSLを使うなら、ビルドオプションとTLS1.3中継互換モードの実装方針を確認する（必要ならパッチ/ビルド変更を依頼）。  
  - 公開サービスでは互換性実績のあるライブラリ（LibreSSLや広く使われるOpenSSL系）を検討する。  
  - 問題を見つけたらWolfSSL側にバグ報告し、相互運用性の改善を促す。

（出典: feld.me の記事「WolfSSL Sucks Too, So Now What?」を基に要約・翻案）
