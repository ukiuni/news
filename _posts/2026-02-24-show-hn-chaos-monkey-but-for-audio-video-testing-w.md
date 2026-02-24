---
layout: post
title: "Show HN: Chaos Monkey but for Audio Video Testing (WebRTC and UDP) - オーディオ/ビデオ向けChaos Monkey（WebRTCとUDP）"
date: 2026-02-24T20:37:40.168Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/MdSadiqMd/AV-Chaos-Monkey"
source_title: "GitHub - MdSadiqMd/AV-Chaos-Monkey: Chaos Monkey but for Audio Video Testing (webRTC and UDP)"
source_id: 47119767
excerpt: "1500人規模の会議で現実的なネットワーク障害を自動注入して耐久性を検証するツール"
image: "https://opengraph.githubassets.com/3834d7ad893f55aeb61a918af988eee54b7d7c1724e169b8e73add17b8e95d7f/MdSadiqMd/AV-Chaos-Monkey"
---

# Show HN: Chaos Monkey but for Audio Video Testing (WebRTC and UDP) - オーディオ/ビデオ向けChaos Monkey（WebRTCとUDP）

1500人規模のビデオ会議を“壊して”耐久性を検証する――AV Chaos Monkeyで本番に近い障害テストを回してみよう

## 要約
AV Chaos Monkeyは、H.264/Opusの実ストリームを大量にシミュレートし、パケットロス・ジッタ・帯域制限・フレーム落ち等の“スパイク”を注入して会議システム（SFU/MCU/mesh）の耐障害性を検証する分散テスト基盤です。ローカル〜Kubernetesで最大1500+参加者を再現できます。

## この記事を読むべき理由
日本でもリモート会議、遠隔授業、テレヘルス、低遅延配信の需要が高まる中、本番に近いネットワーク劣化条件での品質保証は必須です。AV Chaos Monkeyは実データに基づく負荷と障害を自動化でき、SRE／QA／プロダクト開発に直結する有用なツールです。

## 詳細解説
- 基本設計  
  - メディア処理：起動時にFFmpegで入力動画をH.264（Annex‑B）とOgg/Opusに変換。NALリーダーとOpusフレームリーダーでフレームをメモリ共有（ゼロコピー）し、参加者ごとの再エンコードを避けCPU負荷を大幅削減。  
  - コントロールプレーン：HTTPサーバ（:8080）でテストライフサイクルを管理。Spike Schedulerがスパイク（障害イベント）を時間分布戦略に沿って割り当て、Network Degraderが実際にパケット損失・ジッタ・ビットレート低下・フレームドロップ等を適用する。  
  - 参加者プール：参加者はRTP（PT=96動画、PT=111音声）で送信し、RTP拡張に参加者IDを埋め込む。パーティションは participant_id % total_partitions = partition_id で分散。局所テストからKubernetesスケールまで対応（ローカル1–100、Docker100–500、K8s500–1500）。  
- スパイク（注入）タイプと配布戦略  
  - スパイク：rtp_packet_loss、network_jitter、bitrate_reduce、frame_drop、bandwidth_limit。パラメータで損失率やジッタ分布、目標ビットレートを指定可能。  
  - 配布：even / random / front-loaded / back-loaded / legacy。テスト目的（回復力評価、ピーク耐性など）に合わせて選べる。  
- UDPリレーとKubernetesの工夫  
  - kubectl port-forwardはTCPのみのため、クラスタ内でUDPを集約→長さプレフィックス付きTCPで転送→ローカルでTCP→UDP変換する“UDP relay chain”を採用。これにより1500ストリームを単一経路で受け取れる。  
- インフラと観測  
  - WebRTC向けにはcoturn StatefulSetやwebrtc-connectorを用意。Prometheus/Grafanaで参加者数、パケットロス、ジッタ、MOSスコアなどを可視化できる。  
- 実行モードとスケール感  
  - ローカル（Go実行）: 開発・デバッグ向け（数〜100参加者）  
  - Docker Compose: CI/中規模検証（100–500参加者）  
  - Kubernetes＋Nix: 本番規模検証（500–1500参加者）。StatefulSetでパーティションを分散、各Podは概ね1–4CPU、2–4Giメモリを目安。

## 実践ポイント
- まずはローカルで10人程度から始める：config/config.jsonでnum_participantsを10にし、go run cmd/main.go と UDPレシーバ（examples/go/udp_receiver.go）で動作確認。  
- 目的に応じたスパイク設計：回復力テストならfront-loaded、ランダム障害による平均性能評価ならrandomを選ぶ。  
- リソース目安を確認：Dockerモードでの参加上限は割当メモリに依存するため、docker-compose.yamlのlimitsを調整して負荷を再現する。  
- CIへの組み込み：Docker Composeで軽量な破壊テストを定期実行し、重要なリリースの前にKubernetesでスケールテストを行う。  
- 可観測性を活用：Prometheus＋GrafanaでスパイクごとのMOSやパケット統計を比較し、再現可能な劣化シナリオを作成する。  

短時間で“本番に近い”ネットワーク劣化を再現できるため、SREやQAが手元で現実的な耐障害性を検証するのに非常に有用です。興味があれば、まずはリポジトリのREADMEに従ってローカル実行から試してみてください。
