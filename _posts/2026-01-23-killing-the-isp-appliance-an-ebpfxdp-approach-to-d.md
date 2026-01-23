---
layout: post
title: "Killing the ISP Appliance: An eBPF/XDP Approach to Distributed BNG - ISP用アプライアンスを捨てる：eBPF/XDPで分散BNGへ"
date: 2026-01-23T19:11:25.463Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://markgascoyne.co.uk/posts/ebpf-bng/"
source_title: "Killing the ISP Appliance: An eBPF/XDP Approach to Distributed BNG"
source_id: 46735179
excerpt: "eBPF/XDPでOLT上に分散BNGを実装し低コスト・低遅延を実現"
---

# Killing the ISP Appliance: An eBPF/XDP Approach to Distributed BNG - ISP用アプライアンスを捨てる：eBPF/XDPで分散BNGへ

物理アプライアンスに頼らないISPの未来—OLT上で動くeBPFベースの分散BNGが実現する低コスト・低遅延・高可用性

## 要約
中央集約型の高価なBNGアプライアンスを廃し、eBPF/XDPでBNG機能を各OLT（エッジ）に分散させる設計とプロトタイプ実装を紹介。DHCPの高速パスをカーネルで処理し、IP割当てはRADIUS時に決定することでスケーラブルかつオフライン耐性のある構成を実現する。

## この記事を読むべき理由
日本のFTTH/ALTN事業者やネットワークエンジニアにとって、数百万〜数千万の顧客を相手にする従来モデルはコスト・冗長性の壁に直面している。本稿のアプローチは白箱OLTと標準LinuxでBNGを分散化し、運用コストと単一障害点を劇的に削減する現実的な代替案を示す。

## 詳細解説
- 問題点（従来モデル）
  - すべての加入者トラフィックが中央BNGを経由 → 単一障害点、数十万〜数百万ドルの専用装置、運用負荷。
- アイデア（分散BNG）
  - OLT上でBNG機能を動作させ、トラフィックをローカルで処理。各サイトは独立運用可能。
  - 中央は制御面（設定配布、IP調整、監視）だけを担当。
- なぜeBPF/XDPか（VPPとの比較）
  - VPP: コア集約向け、100+Gbps級で強力だが導入複雑。  
  - eBPF/XDP: 標準Linuxで簡単にデプロイでき、OLTクラス（10–40Gbps）には十分。デバッグはtcpdump/bpftoolで親和性が高い。
- アーキテクチャ（要点）
  - 中央（Kubernetes上のNexus）: CRDTベースの状態同期、hashringでIP割当て。制御平面のみ。
  - エッジ（OLT-BNG）: eBPF/XDPでパケット処理、各OLTが1,500–2,000加入者を処理。加入者トラフィックは中央を経由しない。
- DHCPの二層設計（Fast Path / Slow Path）
  - Fast Path（XDP・カーネル）: 既知MACはeBPFマップで即ACK。典型的に ~10μs、数万req/s。
  - Slow Path（ユーザ空間）: キャッシュミス時に中央キャッシュやRADIUSを参照してIPを返し、eBPFキャッシュを更新。数msオーダー。
  - 効果: ウォームアップ後のキャッシュヒット率が高ければ大部分の処理がカーネル内で完了。
- IP割当ての決定タイミング
  - RADIUS認証時にhashringでIPを決定してサブスクライバーレコードに保存 → DHCPは単なるREAD。これでノード間のIP競合を回避。
- オフライン初期化（edge-first設計）
  - 中央断線時でも既存セッション、DHCP更新、NAT、QoSは継続。新規認証やIP割当てはローカルプールにフォールバック。
- 実装概要
  - 単一のGoバイナリにeBPFプログラムを組み込み（bpf/ に dhcp_fastpath.c 等）。
  - モジュール: ebpf loader, dhcp slowpath, nexus client, radius client, nat, qos, pppoe, routing, metrics など。
  - 実行例:
```bash
# Standalone (ローカルプール)
sudo ./bng run --interface eth1 --pool-network 10.0.1.0/24 --pool-gateway 10.0.1.1

# Nexus連携（本番）
sudo ./bng run --interface eth1 --nexus-url http://nexus.internal:9000 --radius-enabled --radius-servers radius.isp.com:1812
```
- 対象ハードウェア
  - Linuxカーネル5.10+が動く白箱OLT（例: Radisys RLT-1600G）。従来BNGに比べコストを大幅削減可能。
- 未解決項目
  - デバイス認証（TPM等）、IPv6（DHCPv6/SLAAC）、完全なRADIUS会計、管理GUIなど。

## 実践ポイント
- プロトタイプの始め方
  - カーネル5.10+の白箱サーバでXDPサンプルを動かし、簡単なDHCP Fast Pathを実装してレイテンシ/スループットを計測する。
- 設計上の重要決定
  - IP割当てをRADIUS時に固定することで分散運用の整合性が得られる（hashring等で実装）。
- 運用上の注意
  - 中央は制御面に限定し、エッジはオフラインで安全に動けることを前提にする（ローカルプールの用意、監査ログの同期設計）。
- 次に投資すべき技術
  - eBPFマップ設計、bpftoolでのデバッグ習熟、TPMベースのデバイス認証、IPv6対応の計画。

以上が、eBPF/XDPでOLTにBNGを分散させる実践的なアプローチの要点です。興味があれば実験用のXDP DHCPパッチやNexus風の制御プレーン設計をさらに共有できます。
