---
layout: post
title: "nvidia-smi hangs indefinitely after ~66 days - nvidia-smiが約66日でハングする問題"
date: 2026-01-25T04:11:10.999Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/NVIDIA/open-gpu-kernel-modules/issues/971"
source_title: "nvidia-smi hangs indefinitely after ~66 days 12 hours uptime with driver 570.133.20 OpenRM on B200 and kernel 6.6.0 · Issue #971 · NVIDIA/open-gpu-kernel-modules · GitHub"
source_id: 46750425
excerpt: "約66日でnvidia-smiが無限ハングする原因とログ解析、即効回避策を詳述"
image: "https://opengraph.githubassets.com/2bf389c09f317b2250afda6031af786b88553cbb96ba308e7ab01e948b9791f5/NVIDIA/open-gpu-kernel-modules/issues/971"
---

# nvidia-smi hangs indefinitely after ~66 days - nvidia-smiが約66日でハングする問題
66日ほどの長時間稼働で突然止まるnvidia-smi――データセンター運用者が震える「長期稼働バグ」の正体とは？

## 要約
NVIDIAのオープンGPUカーネルモジュールで、B200（GH100派生）搭載環境の長時間稼働（約66日）後にnvidia-smiが無限ハングする現象が報告され、ログにはNVLink周りの「knvlinkUpdatePostRxDetectLinkMask」等の失敗メッセージが残されています。専有（proprietary）ドライバでは再現しないとのこと。NVBugが作成され調査中です。

## この記事を読むべき理由
日本のクラウド／AI推論基盤やオンプレGPUサーバは長時間安定稼働が必須です。オープンカーネルモジュールを採用する現場では、今回のような「長期稼働で顕在化する不具合」が運用リスクになり得ます。本件は運用設計やドライバ選定に直結するため把握しておくべきです。

## 詳細解説
- 再現環境（抜粋）
  - ドライバ: Open GPU Kernel Modules 570.133.20 (OpenRM)
  - GPU: B200（GH100系）
  - カーネル: 6.6.0（安定リリース）
  - OS: openEuler 2.0 LTS-SP2
  - 発生条件: 約66日〜67日経過後にnvidia-smiが応答しなくなる
- ログのポイント
  - dmesgに繰り返し出るメッセージ:
    - NVRM: knvlinkUpdatePostRxDetectLinkMask_IMPL: Failed to update Rx Detect Link mask!
    - NVRM: knvlinkDiscoverPostRxDetLinks_GH100: Getting peerX's postRxDetLinkMask failed!
  - これらはNVLink（GPU間の高帯域接続）周りでピアのポスト検出マスクを取得／更新できない、つまりNVLinkのピア検出／通信に失敗していることを示唆します。
- 考えられる影響
  - NVLinkの状態取得/更新ルーチンで例外や待ちが発生してユーザー空間コマンド（nvidia-smi）がブロックされる可能性。
  - 長時間稼働で累積する状態（タイマー/カウンタ/リソース枯渇や競合）がトリガーになっている可能性が高く、専有ドライバでは回避される点から実装差に起因する不具合と推定。
- 対応状況
  - 該当IssueはNV-Triaged扱いでNVBugが作成され、開発側で調査中。

## 実践ポイント
- 今すぐできる対策
  - 一時回避: 影響を避けるため「専有（proprietary）ドライバ」を使えるなら切り替える（報告者は専有ドライバでは再現しないと確認）。
  - 再起動スケジュール: 66日を超えない定期再起動（cronでの再起動/ドライバ再読み込み）を検討。
  - 監視: dmesgでNVRM関連エラーを監視し、エラー発生時に自動でログ取得・アラートを上げる。
- 調査・報告時に添えるべきログ（Issue作成時）
  - /proc/driver/nvidia/params の内容
  - dmesg -T | grep -i nvrm の該当区間
  - uptime と last reboot
  - nvidia-bug-report.log.gz（可能な限り）
  - カーネル、ドライバ、GPUモデル、ファームウェアバージョン
  - 再現手順と発生までの稼働時間
- 長期運用設計への示唆
  - オープン実装採用時は長期稼働試験（数週間スケール）を事前に行うこと。
  - 自動回復（プロセスリスタート、ノード再起動）やフェイルオーバーを必ず組み込むこと。

参考コマンド（ログ取得例）:
```bash
# dmesgのNV関連ログ
dmesg -T | grep -i nvrm | tail -n 200

# ドライバ設定確認
cat /proc/driver/nvidia/params

# システム稼働時間
uptime
```

短期的には「専有ドライバ使用」か「定期再起動・監視」で被害を抑えつつ、NVBugの対応を待つのが現実的です。
