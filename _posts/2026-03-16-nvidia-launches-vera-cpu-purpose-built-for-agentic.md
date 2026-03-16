---
layout: post
title: "Nvidia Launches Vera CPU, Purpose-Built for Agentic AI - NVIDIA、エージェント型AI向けCPU「Vera」を発表"
date: 2026-03-16T20:58:03.355Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://nvidianews.nvidia.com/news/nvidia-launches-vera-cpu-purpose-built-for-agentic-ai"
source_title: "NVIDIA Launches Vera CPU, Purpose-Built for Agentic AI | NVIDIA Newsroom"
source_id: 47404074
excerpt: "NVIDIAのVera、エージェントAI向けにNVLink結合で処理効率2倍のCPU"
image: "https://iprsoftwaremedia.com/219/files/202603/69b83bf73d6332289074debc_vera-cpu-rack/vera-cpu-rack_dd1864d1-171f-410c-956d-0a24da3c4906-prv.png"
---

# Nvidia Launches Vera CPU, Purpose-Built for Agentic AI - NVIDIA、エージェント型AI向けCPU「Vera」を発表
Veraで「AIが考え・動く」インフラが変わる — CPUがモデルの実行効率を引き上げる新世代プラットフォーム

## 要約
NVIDIAがエージェント型AI／強化学習向けに設計した「Vera」CPUを発表。従来のラック向けCPUと比べて同等の処理で約2倍の効率、50%高速化をうたう新アーキテクチャで、GPUと密結合した大規模AIファクトリー向けのサーバー設計が特徴。

## この記事を読むべき理由
エージェント型AI（ツール呼び出し・計画・実行を行うAI）が普及する中、単にGPUを足すだけではなくCPU側の性能・帯域・効率がボトルネックになる場面が増えています。日本のクラウド事業者やSIer、AIサービス開発者は導入動向とコスト/電力の影響を早めに評価する必要があります。

## 詳細解説
- 目的：Veraは「モデルを支えるだけのCPU」から「モデルを駆動するCPU」へという設計哲学。エージェントが多数の独立プロセスを並行で動かす運用でのスループットとレスポンス改善を狙う。
- コアとスレッド：NVIDIA独自設計のOlympusコアを88コア搭載（世代や構成により変動）。各コアはNVIDIAのSpatial Multithreadingで同時に2つのタスクを効率的に処理でき、多数のマルチテナント環境で安定した性能を狙う。
- メモリ／帯域：LPDDR5Xベースの低電力メモリサブシステムで最大約1.2 TB/sの帯域を実現し、従来CPUより帯域当たりの消費電力を低く抑える。
- CPU–GPU結合：NVLink–C2CでCPUとGPU間に最大1.8 TB/sのコヒーレント帯域を提供。PCIeより大幅に高速なデータ共有でGPUアクセラレーションとの協調が強化される。
- システム形態：256個を液冷で詰めたVeraラック（NVL72参照）で数万インスタンスの同時稼働を想定。ConnectX SuperNICやBlueField-4 DPUでネットワーク/ストレージ/セキュリティ支援。
- エコシステム：主要ハイパースケール事業者やクラウド、OEMが採用を表明（例：Alibaba、Meta、Oracle、Dell、HPE、Lenovo、Supermicro等）。国内クラウド・ベンダーの対応が鍵。

## 実践ポイント
- 導入検討：まずクラウドでのVera搭載インスタンス提供を監視し、実ワークロード（エージェント推論・リアルタイムストリーミング・強化学習）でベンチを回す。
- アプリ改修：多タスク・マルチテナント設計やメモリボトルネックを見直し、NVLinkやDPUを活かすデータパス設計を検討する。
- コスト最適化：消費電力あたりのスループットが改善される想定のため、TCO試算に電力削減効果を反映する。
- 互換性と運用：既存のGPUアクセラレーションスタック（ドライバ、ランタイム、Orchestration）との整合性を事前確認する。

（Veraは2026年後半にパートナー経由で出荷予定。初期採用動向を追い、実際のベンチマークで評価することを推奨します。）
