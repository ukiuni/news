---
layout: post
title: "More HTTP/3 focus, one backend less - HTTP/3に注力、バックエンドを一つ削減"
date: 2026-01-18T04:06:03.042Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://daniel.haxx.se/blog/2026/01/17/more-http-3-focus-one-backend-less/"
source_title: "More HTTP/3 focus, one backend less | daniel.haxx.se"
source_id: 1290841423
excerpt: "curlがOpenSSL-QUICを外した理由とHTTP/3移行で必須の検証ポイント"
image: "https://daniel.haxx.se/blog/wp-content/uploads/2017/06/QUIC-1200x1048.png"
---

# More HTTP/3 focus, one backend less - HTTP/3に注力、バックエンドを一つ削減
curlがOpenSSL-QUICのサポートを外した理由 — あなたのサービスは影響を受けるか？

## 要約
curlはOpenSSLの独自QUIC実装（OpenSSL-QUIC）のサポートを削除し、HTTP/3の選択肢を「nghttp2+nghttp3」と「quiche」の2つに絞ります（curl 8.19.0から反映）。主な理由はAPIの不足、性能の低さ、メモリ消費の多さです。

## この記事を読むべき理由
日本のサーバ運用者やOSS利用者にとって、curlのバックエンド変更はHTTP/3導入やCI、組み込みシステムのパフォーマンス・メモリ要件に直結します。使っているOpenSSLバージョンやビルド設定で挙動が変わるため、事前の確認とテストが必須です。

## 詳細解説
- 経緯（要点）
  - 2019年：BoringSSLがQUIC向けAPIを導入。実装が広まる。  
  - 2021年：OpenSSLは同じAPI採用のPRを拒否し、独自のQUIC実装を進める決定。  
  - 2023年：OpenSSL 3.2でQUIC機能を搭載するも初期は不安定。  
  - 2025年：OpenSSL 3.4.1で改善、3.5.0では独立QUIC実装用のAPIを追加。
- curlの状況
  - 以前から複数のHTTP/3（QUIC）バックエンドを試験的にサポートしていたが、徐々に整理中。msh3は既に除去済み。
  - 今回OpenSSL-QUICを外し、残るのは「nghttp2 + nghttp3（ngtcp2系）」と「quiche」。うちquicheはまだ実験的扱い。
- 削除理由（技術的）
  - API面：OpenSSL-QUICはcurlが必要とする細かな制御（ノブ）が不足している。メンテナと連携してきたが期待する改善が見られなかった。
  - 性能面：ngtcp2などの代替に比べてデータ転送速度が最大で数倍遅くなるベンチマークが報告されている。
  - メモリ面：同じ転送で必要とするメモリが大幅に多く（場合によって20倍）なるケースがあった。
- 影響
  - OpenSSLをメインにしてきた環境（特にディストリビューションや一部企業製品）は、HTTP/3利用時に意図しない性能低下やメモリ問題に直面する可能性がある。
  - curlをビルドしている環境ではバックエンド選択が明確化され、テスト負荷は減るが、既存のビルド設定確認が必要。

## 実践ポイント
- まず確認：現在のcurlでどのHTTP/3/QUICバックエンドが有効かは以下で確認できる。
```bash
# bash
curl --version
```
- 影響範囲の見積もり：自社サービスやCIでHTTP/3を使っている場合、curl 8.19.0以降でパフォーマンステストとメモリ使用量測定を実施する。
- 推奨対応：
  - 本番ではOpenSSL-QUICに頼らない。nghttp2/nghttp3（ngtcp2系）かquicheを選び、実働環境でベンチを取る。quicheはまだ実験的なので慎重に。
  - 組み込み／メモリ制約のある環境では特にngtcp2系を優先検討する（メモリ効率が優れる）。
  - 自前ビルドする場合はビルドオプションで明示的にバックエンドを指定し、CIで回帰テストを追加する。
- フィードバック：OpenSSL-QUICの改善を望むなら、OpenSSL側へ具体的な要望や実測データを投げると改善に繋がる可能性がある。

短くまとめると、curlの今回の整理は「より安定で高速・省メモリなHTTP/3体験を目指す選択」。日本の現場でも事前検証と適切なバックエンド選定が重要です。
