---
layout: post
title: "Arm's Cortex X925: Reaching Desktop Performance - ArmのCortex X925：デスクトップ性能への到達"
date: 2026-03-03T08:47:44.799Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://chipsandcheese.com/p/arms-cortex-x925-reaching-desktop"
source_title: "Arm&#x27;s Cortex X925: Reaching Desktop Performance"
source_id: 47229344
excerpt: "GB10の4GHz実機でCortex X925がノートでデスクトップ級性能を証明"
image: "https://substackcdn.com/image/fetch/$s_!ZTUE!,w_1200,h_675,c_fill,f_jpg,q_auto:good,fl_progressive:steep,g_auto/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F223f5104-d87f-44cc-a80e-398a444bfd06_2010x1260.png"
---

# Arm's Cortex X925: Reaching Desktop Performance - ArmのCortex X925：デスクトップ性能への到達
ついにARMが“デスクトップ級”へ：Cortex X925は何を変えるのか？

## 要約
Armの新しい大幅強化コアCortex X925は、NVIDIAのGB10（Dell Pro Max搭載）で最大4GHz動作し、単コア性能でAMD Zen 5やIntel Lion Coveに迫る実力を示した。高い分岐予測精度、大容量BTB、広い実行窓、強力な実行ユニット群が特徴。

## この記事を読むべき理由
Windows-on-Armや高性能ノートPCが注目される日本市場で、ARMアーキテクチャが“デスクトップ用途”に本気で食い込む兆候は、OEMやソフトウェア開発者に直接影響します。省電力だけでなく「生の性能」を狙うARM製コアの実力と最適化ポイントを押さえておきましょう。

## 詳細解説
- コア設計概観：X925は「10-way」級の大きなコア設計で、L1命令・データともに64KB固定。L2は実装者が2MB/3MBを選択可能。クラスタ間はDSU-120（L3最大32MB）で接続。物理アドレスは40ビットで消費者向け想定。
- フロントエンド：MOPキャッシュを廃しつつ、L1Iの高いプリデコードや10命令/サイクルの取り回しを実現（2MBページ＋64KB L1Iでフルスループット）。分岐ターゲットキャッシュ（BTB）は階層化され最大で数万エントリに達し、分岐予測精度はZen 5に匹敵。
- リネーム／実行窓：実行中に約400〜525命令程度（テスト条件依存）の命令をインフライトで保持でき、Intel Lion Coveと同等クラス、Zen 5より大きめ。レネーム資源は広めで、ムーブ消去などの最適化あり。ただしPTRUEの特殊消去はX925では非対応。
- 実行パイプとスケジューラ：整数側は8つのALUポート＋分岐ユニット3、4つのスケジューラ配下で対称性を重視。FPは6パイプ、各FPスケジューラは大きなエントリ数を持つ。128-bitベクトル幅で、ベクタ性能は高いがAMD/Intelの広いベクトル幅に比べると設計トレードオフあり。
- メモリ系：AGU×4、L1 DTLBは96エントリ（全相関）、L2 TLBは2048エントリの統合型。ストア→ロードのフォワーディングは改善されているが、x86のゼロレイテンシ最適化ほどではない。L1Dは64KBで低レイテンシ。
- 実装例：NVIDIA GB10はX925を10コア構成で搭載、1コアが4.0GHzを記録。DellのPro Maxシリーズで実動製品化済み。

## 実践ポイント
- ホットコードサイズを64KBに納める（L1Iヒット）ことでフロントエンド性能を引き出す。
- 2MB巨大ページを試す：フロントエンドの10IPC持続に有利なケースあり。
- 分岐密度の高い処理はプロファイルして分岐予測に優しいコードへリライト（分岐整理・条件反転等）。
- ベクタ最適化は128-bit幅を前提に行う（SVE対応コンパイラで幅を意識して生成）。
- TLBミスを減らすためワーキングセットの局所性を高める／ソフトウェアプリフェッチを検討。
- 実機（GB10搭載機）でのベンチ＆プロファイルを優先し、コンパイラ最適化フラグでARM向け生成を確認する。

短期的には「高性能ARMノート／デスクトップ」が実務ワークロードで現実的になりつつあります。まずはGB10搭載機で自分の負荷を動かし、上記ポイントから最適化を始めてみてください。
