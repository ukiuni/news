---
layout: post
title: "AyaFlow: A high-performance, eBPF-based network traffic analyzer written in Rust - AyaFlow：高性能eBPFベースのネットワーク解析器（Rust製）"
date: 2026-03-29T17:43:09.039Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/DavidHavoc/ayaFlow"
source_title: "GitHub - DavidHavoc/ayaFlow: A high-performance, eBPF-based network traffic analyzer written in Rust. · GitHub"
source_id: 47563978
excerpt: "Rust＋eBPFでサイドカー不要にノード全通信を低負荷可視化"
image: "https://opengraph.githubassets.com/cd55961ade2e0042280afd281ce3ccce8147179b7cab2fa77dae802c5a844eea/DavidHavoc/ayaFlow"
---

# AyaFlow: A high-performance, eBPF-based network traffic analyzer written in Rust - AyaFlow：高性能eBPFベースのネットワーク解析器（Rust製）
K8sノードを「サイドカー不要」で丸ごと可視化する、軽量eBPFソリューション

## 要約
AyaFlowはRust+Ayaで書かれたeBPFベースのネットワークトラフィックアナライザ。KubernetesでサイドカーレスなDaemonSetとして動き、カーネル内でパケットをフックして低オーバーヘッドでノード全体の通信を可視化する。

## この記事を読むべき理由
クラウドネイティブで増えるノード間／ポッド間通信を、サイドカーを増やさずに可視化・監査・メトリクス化したい日本のSRE／開発チームに即戦力となる設計と導入手順がまとまっているため。

## 詳細解説
- アーキテクチャ（概略）  
  カーネル側：NIC → TCフック（ingress/egress）でEthernet/IPv4/TCP/UDPをパースし、方向タグ付きの軽量PacketEventをリングバッファへ。  
  ユーザ空間：Tokioイベントループがリングバッファをポーリングし、DashMapでライブ接続状態を保持、SQLiteへ永続化。AxumでREST API／WebSocketを公開しPrometheusメトリクスを出力する。

- 主要特徴  
  - eBPFネイティブ：libpcap不要でカーネルのTraffic Controlに直接フック。  
  - サイドカーレスDaemonSet：ノード単位で一Pod、アプリごとにサイドカーを置かない。  
  - リアルタイムと履歴：API/WebSocketでライブ表示、SQLiteで履歴検索。  
  - 深いL7情報（オプション）：TLS SNIやDNSクエリ抽出で暗号化トラフィックのドメイン可視化。  
  - Prometheusメトリクス：ayaflow_packets_total / ayaflow_bytes_total / ayaflow_active_connections など。  
  - セキュリティ：APIアクセスのIP許可リスト対応。

- 導入要件・制約  
  - Rust（stable + nightly）、bpf-linker（cargo +nightly）、Linuxカーネル >= 5.8 でBTF必須。CAP_BPF/CAP_NET_ADMIN/CAP_PERFMONが必要。  
  - DaemonSetは hostNetwork: true、/sys/fs/bpf マウントを使う。  
  - eBPFプログラムサイズは小さく、ユーザ空間RSSは約33MB（計測例）。データ保持や集約設定でSQLiteの肥大化を抑える必要あり。

## 実践ポイント
- 最低限のビルド／実行手順（ローカル確認）：
```bash
# bpf-linker をインストール
cargo +nightly install bpf-linker
# ビルド（eBPF + userspace）
cargo xtask build
# rootで実行（例: eth0）
sudo ./target/debug/ayaflow --interface eth0
# 動作確認
curl http://localhost:3000/api/health
curl http://localhost:3000/metrics
```

- Kubernetesでの導入  
  k8s/daemonset.yaml を適用（hostNetwork: true、/sys/fs/bpf マウント、Prometheus scrape 注釈あり）:
```bash
kubectl apply -f k8s/daemonset.yaml
```

- 運用Tips  
  - deep-inspect はTLS/DNS情報を得られるがリングバッファ・メモリを増やすため必要時のみ有効化。  
  - --data-retention／--aggregation-window でSQLite肥大化対策を設定。  
  - Prometheusへ /metrics をスクレイプしてGrafanaで可視化。リソースは推奨値（requests: 32Mi/50m、limits: 128Mi/500m）を参考に。  
  - APIアクセスは --allowed-ips で制限する。  
  - カーネルのBTF可否やCAP権限、クラスタポリシー（Pod Security）を事前確認すること。

短時間でノード全体のネットワーク可視化を始められ、特にリソース制約のある環境やサイドカー運用を避けたいプロジェクトに向くツール。興味があればリポジトリ（README、k8sマニフェスト、Grafanaダッシュボード）を参照してPOCを始めると良い。
