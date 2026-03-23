---
layout: post
title: "I Reverse-Engineered the TiinyAI Pocket Lab from Marketing Photos - TiinyAI Pocket Labをマーケティング写真から逆解析した話"
date: 2026-03-23T02:15:46.630Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://bay41.com/posts/tiiny-ai-pocket-lab-review/"
source_title: "I Reverse-Engineered the TiinyAI Pocket Lab From Marketing Photos. Here's Why Your $1,400 Is Probably Gone. — bay41"
source_id: 47435127
excerpt: "写真解析で判明：TiinyAIは80GB分割と外付NPUで性能表示が誇張の可能性"
image: "https://bay41.com/images/logo.ca48f6e7668ee9e8279e795154a62954cd552c8914b052146c59f531f31bca34.png"
---

# I Reverse-Engineered the TiinyAI Pocket Lab from Marketing Photos - TiinyAI Pocket Labをマーケティング写真から逆解析した話
「ポケットAI」は本当に“120Bで20 tok/s”？写真から暴く“見えない”真実

## 要約
海外ライターがTiinyAIのマーケティング写真と公開スペックだけを手がかりに逆解析した結果、同社が掲げる「120Bモデルをローカルで動かすポケットAI」には、設計上の制約（分割メモリ、外付けNPU、プロプライエタリなモデル形式）による実用上の限界と、誇張やミスリードが混在している可能性が高いと結論付けています。

## この記事を読むべき理由
日本でも「オフラインで大規模モデルを動かしたい」「データをクラウドに出したくない」といったニーズが高まる中で、広告やKOL動画だけで判断すると高額な投資を失敗するリスクがあります。本記事はハード／ソフト両面の“見えないポイント”を短くまとめます。

## 詳細解説
- 主要推定コンポーネント（筆者の逆解析による推定）
  - SoC：12コア Armv9.2（筆者はCIX P1/CD8180を最有力候補と推定）。SoC内蔵NPU ≒ 30 TOPS。
  - 外付けdNPU：M.2モジュール上のデュアルダイ構成で合計約160 TOPS（筆者はVeriSiliconのVIP9400系を指摘）。
  - メモリ：合計80GB LPDDR5Xと表記されるが、写真のレンダではSoC側とdNPU側でメモリが分割されている（例：SoC側32GB、dNPU側48GBのような配置が示唆される）。
  - ストレージ／セキュリティ：1TB NVMe（AES-256はSSDの標準機能）。
  - ソフトウェア：PowerInfer／Tiiny独自の変換・モデルストア（NBG/Tiiny形式で事前コンパイルが必要な可能性）。

- 技術的要点と影響
  - 分割メモリ（「80GB」との表記は誤解を招く） → 大規模モデル推論では“統一メモリ＋高帯域”が必要。M.2経由での転送は帯域・レイテンシのボトルネックになりやすい。
  - 外付けNPUは専用コンパイラで事前コンパイルが必要なことが多く、モデルの互換性・更新性が制限される（モデルロックイン）。
  - マーケティング数値（「120B」「20 tok/s」）はベンチ条件やモデルアーキテクチャ次第で大きく変わるため、実測条件の開示が不可欠。
  - 露出情報から得られるチーム／サプライチェーンの透明性の低さは、量産・サポート・保証のリスクになりうる。

## 実践ポイント
- 購入前に必ず確認すべき項目
  1. SoCとNPUの型番（写真・仕様で明示できるか）。  
  2. 「80GB」が単一のアドレス空間か、複数プールか（統一バスの帯域[GB/s]を要求する）。  
  3. 提供ベンチの条件：モデル名、トークン長、バッチ、TTFT（time-to-first-token）。  
  4. モデルの実行に事前コンパイルが必要か、オープンフォーマットでの動作可否。  
  5. 実機レビュー／分解レポートの有無、公式の生産写真や大量出荷の証拠。  
- 代替案
  - 同等スペックを公開しているSBC/ミニPC（Radxa/Orange Pi等）や、まずはクラウドで実測してからローカル投資を判断する。  
  - 日本での利用を想定するなら、サポート体制・保証・修理オプションの有無を重視する。

短く言えば：見た目の数字だけで飛びつかず、メモリの「形」とソフトの「運用制約」を確かめることが失敗を防ぐ鍵です。
