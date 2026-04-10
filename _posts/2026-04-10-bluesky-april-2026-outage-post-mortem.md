---
layout: post
title: "Bluesky April 2026 Outage Post-Mortem - Bluesky 2026年4月の障害振り返り"
date: 2026-04-10T17:04:38.419Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://pckt.blog/b/jcalabro/april-2026-outage-post-mortem-219ebg2"
source_title: "pckt"
source_id: 47719975
excerpt: "8時間で半数が落ちた原因はバッチ処理の同時実行上限欠如と観測性不備"
image: "https://pckt-blog-media.s3.us-east-2.amazonaws.com/cover_image/ab3965c1-bb9f-49cd-9ec0-01e590a55f35/image.png"
---

# Bluesky April 2026 Outage Post-Mortem - Bluesky 2026年4月の障害振り返り
なぜ「小さなバグ」が8時間で半数のユーザーを落としたのか — 見落としが招く運用地雷

## 要約
Blueskyで発生した大規模障害は、1回のRPCが数万件のIDをバッチ処理したことで生じた接続枯渇と過剰ログ出力の連鎖が原因。根本は「バウンディング（同時実行制限）の欠如」と観測性の不足だった。

## この記事を読むべき理由
日本のプロダクトでも、マイクロサービスやキャッシュ層を組み合わせた構成は一般的。バッチ処理の想定外挙動や接続プール、ログ設計で同様の障害が起き得るため、具体的な教訓と対処法を学べます。

## 詳細解説
- 発端：内部サービスがほとんどリクエスト数は少ないが、まれに15k〜20kのURIをまとめて送るRPC（GetPostRecord）を導入。通常は1〜50件想定の処理が突発的に巨大化した。  
- 技術チェーン：GetPostRecordはまずmemcachedを参照し、キャッシュミスでScyllaへ問い合わせる実装。ここで各URIごとにゴルーチンを大量生成して接続を張りに行き、OSのエフェメラルポートを枯渇させた（TCP TIME_WAITの蓄積）。  
- コード欠陥：他のRPCはerrgroup.SetLimit等で同時実行数を制限していたが、このエンドポイントだけ制限が無かった（boundless goroutine spawn）。例：  
```go
// go
var group errgroup.Group
// group.SetLimit(50)  // ← これが抜けていた
for _, uri := range uris {
  group.Go(func() error { ... })
}
group.Wait()
```
- 負のフィードバックループ：memcachedエラーが大量ログを生み、blocking writeで多数のスレッドを消費。GoランタイムがOSスレッド（M）を増やしGC負荷→停止時間増大→OOM発生→プロセス再起動→TIME_WAITが残る→さらに接続不能、という「死のスパイラル」に陥った。  
- 応急策：クライアント側でローカルIPアドレスをランダムに選ぶカスタムダイラーを入れ、IP+ポート空間を“拡張”して一時的に回復させた（根本解決ではない）。例：  
```go
// go
memcachedClient.DialContext = func(ctx context.Context, network, address string) (net.Conn, error) {
  ip := net.IPv4(127, byte(1+rand.IntN(254)), byte(rand.IntN(256)), byte(1+rand.IntN(254)))
  d := net.Dialer{LocalAddr: &net.TCPAddr{IP: ip}}
  return d.DialContext(ctx, network, address)
}
```
- 観測性の問題：大量のログと複数キャッシュでエラーが散らばり、どのエンドポイントが原因か分かりにくかった。結果として根本特定までに時間を要した。

## 実践ポイント
- RPCごとに最大同時実行数を明示的に制限する（errgroup.SetLimitなど）。  
- クライアントでバッチサイズ上限を設け、サーバ側でも過大バッチを拒否・切り分けする。  
- 接続プールとMaxIdle設定、エフェメラルポートの監視（TIME_WAIT数、ソースIPポート枯渇）を運用指標に追加。  
- 大量エラーをそのままログ出力しない（非ブロッキングロガー or サンプリング）。PrometheusメトリクスやOTelトレースで高頻度情報を扱う設計に。  
- per-client（クライアントID単位）やエンドポイント単位の高粒度メトリクスを用意し、異常なバッチパターンを早期検出する。  
- 再現テスト：大量バッチを含む負荷試験を行い、接続枯渇やGC/OOMの挙動を確認する。

以上は日本のサービス運用にも直結する実践的な教訓です。小さな設計の見落としが大きな可用性リスクになる点を今一度確認してください。
