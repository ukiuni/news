---
layout: post
title: "Zero-Code Instrumentation of an Envoy TCP Proxy Using eBPF - Envoy TCP プロキシをコード変更ゼロで eBPF による自動計測"
date: 2025-12-31T15:38:04.403Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://sergiocipriano.com/beyla-envoy.html"
source_title: "Zero-Code Instrumentation of an Envoy TCP Proxy Using eBPF"
source_id: 46444481
excerpt: "Envoyをコード変更ゼロでeBPF(OBI)がホップ毎の遅延を即可視化し原因特定も可能"
---

# Zero-Code Instrumentation of an Envoy TCP Proxy Using eBPF - Envoy TCP プロキシをコード変更ゼロで eBPF による自動計測

魅力的タイトル: 「コードを書かずにレイテンシの“どこ”を突き止めるか — Envoy + eBPF（OBI）でたった数分の可観測化」

## 要約
Envoy（TCP プロキシ）経由のリクエストをアプリ側のコード変更なしに eBPF ベースの OBI（OpenTelemetry eBPF Instrumentation）で自動計測し、ホップごとのスパン／レイテンシやリクエスト属性を取得して問題箇所を迅速に特定できる手法を紹介します。

## この記事を読むべき理由
- 日本のクラウド／SRE チームでも、NLB や Envoy を使ったサービスで「稀発だが致命的なレイテンシ問題」が発生します。従来のアクセスログや tcpdump だけでは原因追跡が困難な場面で、OBI はコード変更ゼロで有力な観測手段を提供します。
- Privileged な eBPF アプローチにより、マイクロサービス間の往復やプロキシの内部動作を可視化でき、インシデント対応時間を短縮できます。

## 詳細解説
ポイントは「ゼロコードでの自動計測」と「eBPF によるカーネルレベルのトレース」です。

- 仕組み
  - OBI（以前の Grafana Beyla）は Linux の eBPF を使い、プロセス／ソケット層にフックして TCP/HTTP の送受信イベントを拾い、OpenTelemetry 準拠のスパンやメトリクスを生成します。
  - 生成されるログ例（抜粋）は、各スパンに対してタイムスタンプ、ホップごとの遅延（total / internal）、HTTP ステータス、メソッド、経路、送受信バイト量、traceparent（トレース ID）を表示します。これにより「どのホップで時間がかかっているか」を簡単に辿れます。

- 再現環境（簡易）
  - Envoy を TCP プロキシで設定（listener 8000 → backend:8080）。
  - backend は単純な Go HTTP サーバ（コード例は後述）。
  - Docker Compose で otel/ebpf-instrument（autoinstrumenter）を privileged / host PID Namespace で実行し、Envoy の開いたポートを監視させる。

- マルチホップの可視化
  - もう一台 Envoy を追加して 9000→8000→backend の経路を作ると、OBI は各 Envoy の「server」（HTTP）スパンと「client」（HTTPClient）スパンを生成し、traceparent により全体のトレースを紐付けます。結果としてリクエストチェーン全体のどこで時間を食っているかが一目で分かる。

- 本番に近いセットアップ
  - OBI は OpenTelemetry Collector にトレース／メトリクスを出し、Collector が Jaeger（トレース可視化）と Prometheus（メトリクス）に流す構成が有効。
  - 問題: OBI 側で「特定 PID のみ」を直接フィルタできない（記事時点）。対策として Otel Collector 側でプロセッサ（filter）を用い、service.instance.id（OBI が付与する instance=host:pid）で望むプロセスのトレースだけを通す手法を紹介しています。

- 実運用上の注意
  - autoinstrumenter は privileged 権限とホスト PID 名前空間を必要とするためセキュリティ要件を満たす必要があります（実稼働では慎重な承認プロセスを）。
  - eBPF を利用するため Linux カーネルのサポートが必要（比較的新しいカーネル）。コンテナランタイム／ホスト設定も影響します。
  - 大量のサービスがある環境ではフィルタリング設計が重要（不要なテレメトリを流さない）。

以下は抜粋で使える設定・コード例（簡潔版）。

envoy.yaml（TCP proxy 最小構成）:
```yaml
# yaml
static_resources:
  listeners:
    - name: go_server_listener
      address:
        socket_address: { address: 0.0.0.0, port_value: 8000 }
      filter_chains:
        - filters:
            - name: envoy.filters.network.tcp_proxy
              typed_config:
                "@type": type.googleapis.com/envoy.extensions.filters.network.tcp_proxy.v3.TcpProxy
                stat_prefix: go_server_tcp
                cluster: go_server_cluster
  clusters:
    - name: go_server_cluster
      connect_timeout: 1s
      type: LOGICAL_DNS
      load_assignment:
        cluster_name: go_server_cluster
        endpoints:
          - lb_endpoints:
              - endpoint:
                  address:
                    socket_address: { address: target-backend, port_value: 8080 }
```

Go の簡易バックエンド:
```go
// go
package main
import ("fmt"; "net/http")
func main() {
  http.Handle("/", http.FileServer(http.Dir(".")))
  server := http.Server{ Addr: ":8080" }
  fmt.Println("Starting server on :8080")
  panic(server.ListenAndServe())
}
```

docker-compose 抜粋（autoinstrumenter の重要点）:
```yaml
# yaml
services:
  autoinstrumenter:
    image: otel/ebpf-instrument:main
    pid: "host"
    privileged: true
    environment:
      OTEL_EBPF_TRACE_PRINTER: text
      OTEL_EBPF_OPEN_PORT: "8000-9000"
  envoy:
    image: envoyproxy/envoy:v1.33-latest
    ports: ["8000:8000"]
    volumes: ["./envoy.yaml:/etc/envoy/envoy.yaml"]
  target-backend:
    image: golang:1.22-alpine
    command: go run /app/backend.go
    volumes: ["./backend.go:/app/backend.go:ro"]
    expose: ["8080"]
```

Otel Collector 側での PID フィルタ（概念）:
- autoinstrumenter のログや /metrics から instrumented プロセスの service.instance.id（例: host:297514）を得る。
- Collector の processors に filter を追加し、traces の pipeline に挿入して当該 instance のみを通す。

## 実践ポイント
- まずは「ローカルの再現環境」で試す：Docker Compose + Envoy（単一路由）+ autoinstrumenter。動作確認が取れたら範囲を広げる。
- autoinstrumenter は privileged かつ pid: host が必要。実環境導入時はセキュリティチームと調整を。
- OBI が生成する traceparent と span ごとの latency を見れば、「プロキシ内部の待ち時間」か「バックエンドの処理時間」かを素早く切り分け可能。
- 多数コンテナ環境では Otel Collector 側で service.instance_id を使ってフィルタ処理するのが現実的。OBI の PID フィルタが未成熟な場合の回避策として有効。
- 監視体制に組み込む際は Prometheus/Grafana/Jaeger を組み合わせてダッシュボード化し、アラート閾値を設定しておく。

