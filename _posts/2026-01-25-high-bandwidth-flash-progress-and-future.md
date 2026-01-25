---
layout: post
title: "High-bandwidth flash progress and future - 高帯域フラッシュの進展と未来"
date: 2026-01-25T00:49:08.847Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://blocksandfiles.com/2026/01/19/a-window-into-hbf-progress/"
source_title: "A window into HBF progress: Engineering prof talks of decade ahead"
source_id: 46700384
excerpt: "AI向けキャッシュでGPU帯域を補うHBFが2027年頃実用化、Kioxiaが試作"
image: "https://blocksandfiles.com/wp-content/uploads/2026/01/Screenshot-2026-01-19-at-12.04.40.png"
---

# High-bandwidth flash progress and future - 高帯域フラッシュの進展と未来
魅せる記憶装置の新レイヤー：AI時代に「HBMとSSDの間」を埋めるHBFの衝撃

## 要約
KAISTの金正浩教授らによれば、High-Bandwidth Flash（HBF）はAI向けメモリ階層を再定義し、2038年までにHBMを超える市場規模になる可能性がある。製品化は2027年頃から始まり、SK hynix、SanDisk、Samsung、Kioxiaらがプロトタイプやコンソーシアムで動いている。

## この記事を読むべき理由
日本のクラウド事業者、AIインフラ設計者、ストレージベンダーは、GPUアクセラレータ周りの遅延・帯域要件に対する新しい解決策が来ることを知る必要がある。特にKioxia（日本企業）のプロトタイプ事例は国内事業者にとって即時の関心事です。

## 詳細解説
- HBFとは：HBM（High-Bandwidth Memory）より容量は大きく、従来のSSDよりは帯域が高い「中間レイヤー」のフラッシュメモリ。AI推論や大規模モデルのトークンキャッシュに向く。
- 階層イメージ：教授はHBM（非常に高速）→ HBF（高速・大容量のフラッシュ）→ ネットワーク接続SSD（さらに大容量）という3層構成を提示。これによりGPUとストレージ間でホストCPU/DRAMを経由しない経路が可能になる（DPU経由など）。
- 性能・構造のポイント：示されたターゲットとして$512\ \mathrm{GB}$／$1.638\ \mathrm{TB/s}$級のHBFユニットが議論されている。実装は多数積層した3D NANDと、下層を貫通するTSV（Through-Silicon Via）やプラグによる接続を要するため、従来の3D NANDとは製造設計が異なる。例えば既存の2Tb（約250GB）・321層3D NANDを2枚積むと一例の$512\ \mathrm{GB}$構成になるが、積層やTSVでの歪み対策が課題。
- エコシステム動向：SK hynix、SanDisk、Samsungが標準化やMOUで動き、SK hynixはまもなくプロトタイプを出す見込み。KioxiaはPCIe Gen6 x8（記事では64Gbps表記）接続の5TB HBFモジュールを試作済み。Micronや主要GPUメーカーはまだ公表を抑えているが、NVIDIAのICMSPのようなソフトウェア層はHBMとSSDを跨いだ管理を想定しており、HBFは自然にそのミドル層に適合する。

## 実践ポイント
- 製品計画担当者：2027年以降のHBF製品化を想定して、AI推論向けキャッシュ戦略やDPU/SmartNIC（例：BlueField系）を使ったストレージ経路の設計検討を始める。
- システム設計者：HBM⇄HBF⇄ネットワークSSDの3層を想定したデータ配置・キャッシュ階層をベンチマークで評価する。現行NVMe SSD/PCIe Gen6機器での試作検証を行うと有利。
- 日本市場向け視点：Kioxiaの動きは国内調達と共同開発のチャンス。国内クラウド／エッジ事業者は早期にベンダーと連携し、導入ロードマップを策定する。

（注）仕様やタイムラインは各社発表・プロトタイプ情報に基づく予測であり、製品化時の最終仕様は変わる可能性があります。
