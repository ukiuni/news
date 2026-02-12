---
layout: post
title: "The Future for Tyr, a Rust GPU Driver for Arm Mali Hardware - Arm Mali向けRust GPUドライバ「Tyr」の将来"
date: 2026-02-12T15:18:45.358Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://lwn.net/Articles/1055590/"
source_title: "The future for Tyr [LWN.net]"
source_id: 46989117
excerpt: "Rust製MaliドライバTyr、ゲーム動作実証も電源・メモリ・復旧機能が未実装で実用前の課題"
---

# The Future for Tyr, a Rust GPU Driver for Arm Mali Hardware - Arm Mali向けRust GPUドライバ「Tyr」の将来

RustでMaliを動かす――モバイル向けGPUを安全に、低消費電力で動かす次世代ドライバの挑戦

## 要約
TyrはArm Mali向けのカーネル側GPUドライバをRustで書き直すプロジェクトで、プロトタイプはゲームが動くほどに到達したが、実用化には「メモリ管理・アドレス空間・電源管理・GPU復旧」など未実装の重要基盤の整備が必要。

## この記事を読むべき理由
Maliはスマホ／組込みで広く使われるため、日本のデバイスや組込み開発者に直接関係します。Rustを使った安全性向上と将来のカーネル方針（新規ドライバはRustへ）を知っておくことは重要です。

## 詳細解説
- 役割分担：GPUドライバは大きく「カーネル側（リソース共有・隔離・通知）」と「ユーザーモード（Vulkan/GL変換）」に分かれる。Tyrはカーネル側をRustで実装する試み。
- 現状：6.18に一部がマージされたが機能は限定的。LPC2025ではSuperTuxKartを動かせるプロトタイプが披露されたが、実運用で必須の機能が欠けている。
- 必要なRust抽象化：
  - GEM shmem（Lyude Paul）：統合メモリ割当（統合型GPU向け）。これが無いとファームウェアをブートできない。
  - GPUVM（Alice Ryhl 他）：ユーザードライバが持つGPUアドレス空間管理。
  - io-pgtable：IOMMUのページテーブル操作。
  - drm::Device初期化の循環依存解消（drm::DeviceCtxなど）。
- 運用面の必須機能：
  - 電力管理／周波数スケーリング：モバイルでのバッテリー・熱問題を解決するコードが未実装。
  - GPUハング時の復旧（GPU-recovery）：作業の消失防止のため必須。
  - 同期（fences）経路の安全性、DMAフェンスの有限時間でのシグナル、GFP_ATOMIC制約（メモリ圧迫時のデッドロック回避）などの厳密な実装。
- 互換性と性能：
  - Vulkan互換（PanVK上でVulkan CTS合格）が必要。Cドライバ並みのベンチマーク結果も目標。
- 今後の設計議論：
  - drm_gpu_schedulerの代替として「JobQueue」（依存解決のみ担当、ファームウェアがスケジューリング）をRustで作る議論が進行中。これをTyrで試験し、他ドライバへ波及させる狙い。
  - Cから使えるRustコンポーネントAPIの整備が重要なマイルストーン。

## 実践ポイント
- 日本の組込み／OS開発者はMali搭載機でのバッテリー・熱挙動に注目し、Tyrの電源管理実装動向をウォッチする。
- Vulkan互換性検証（Vulkan CTS）とベンチ結果は採用判断の鍵。PanVK＋Tyrでのテストを追うべき。
- カーネルへ貢献したい場合は、GEM shmem、GPUVM、io-pgtable、drm::Device初期化回りの議論とパッチが現状のブロッカー。Rustでのカーネル寄与を検討する良い機会。
- ドライバ設計の学びどころ：同期（fence）経路の安全やGFP_ATOMIC制約など、GPUドライバ固有の運用ルールを理解しておくと役立つ。

（元記事：The Future for Tyr, LWN.net）
