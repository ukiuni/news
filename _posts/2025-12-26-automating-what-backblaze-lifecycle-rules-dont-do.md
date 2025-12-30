---
layout: "post"
title: "Automating What Backblaze Lifecycle Rules Don't Do Instantly - Backblazeのライフサイクルルールが即座に行わないことの自動化"
date: "2025-12-26 09:17:11.660000+00:00"
categories:
- tech
- world-news
tags:
- tech-news
- japan
source_url: "https://blog.tymscar.com/posts/backblazeb2cleanup/"
source_title: "Automating What Backblaze Lifecycle Rules Don't Do Instantly :: The Tymscar Blog"
source_id: "1424259147"
excerpt: "B2の遅延で溜まる隠れバージョンをrcloneで即削除、請求を激減"
---
# Automating What Backblaze Lifecycle Rules Don't Do Instantly - Backblazeのライフサイクルルールが即座に行わないことの自動化

## 要約
Backblaze B2のライフサイクルは即時ではなく最大48時間待機＋24時間ごとのクリーンアップで、大容量ファイルを頻繁に上書きすると「日毎請求」で不要な重複ストレージ費用が発生する。rcloneの cleanup を定期実行すれば即座に古いバージョンを削除できる。

## この記事を読むべき理由
TrueNASやSynology等で大きいqcow2イメージやVMバックアップをB2に置いていると、知らぬ間に数百GB〜TB規模の“隠れたバージョン”が蓄積し、毎日の使用量で課金される。日本のホビー／中小環境でも無視できない出費になるため、対策は必須。

## 詳細解説
- 問題点：Backblazeのライフサイクルルールは「バージョンを1つだけ残す」設定でも即時反映されない。サポート説明によれば適用開始まで最大48時間、さらにクリーンアップは24時間に1回走るため、短間隔で上書きすると古いバージョンが最大24時間（かそれ以上）残る。
- 課金影響：Backblazeは「日単位の使用量」を集計して課金するため、1日に複数バージョンが存在するとその全てが課金対象になる。例：100GBファイルを6時間毎に上書きすると1日で4〜5バージョン、最大で500GB相当が課金対象に。
- 実例：著者はサービス用バケットで2万件超の隠れバージョンが溜まり、手動での削除は現実的でない状況に陥った。
- 解決策：rclone cleanup コマンドはB2の古いバージョンを一括削除できる。定期実行（例：15分間隔）すればライフサイクルの遅延に依存せず、重複蓄積を短時間で解消できる。

## 実践ポイント
1. まずトライ：小さなテストバケットで rclone cleanup を試す。
   - 使い方（シンプル）:
```bash
# bash
rclone cleanup b2:your-bucket-name
```
2. 定期実行：ライフサイクル遅延を補うために短い間隔で実行（例：15分）。
   - NixOSでのsystemdタイマー例（参考）:
```nix
# nix
{ pkgs, ... }:
{
  systemd.services.b2-cleanup = {
    description = "Clean up old B2 file versions";
    serviceConfig = {
      Type = "oneshot";
      ExecStart = "${pkgs.bash}/bin/bash -c '${pkgs.rclone}/bin/rclone cleanup b2:tymscar-truenas-services && ${pkgs.rclone}/bin/rclone cleanup b2:tymscar-truenas-important'";
      User = "tymscar";
    };
  };
  systemd.timers.b2-cleanup = {
    wantedBy = [ "timers.target" ];
    timerConfig = {
      OnBootSec = "5min";
      OnUnitActiveSec = "15min";
      Persistent = true;
    };
  };
}
```
3. 認証管理：rcloneのB2認証は環境変数やシークレットマネージャ（agenix、Vault等）で安全に管理する。
4. 監視：定期的に rclone lsjson や Backblazeコンソールで「バージョン数」を確認して運用効果を検証する。
5. 運用設計：頻繁に上書きする大容量ファイルは差分やスナップショット方式に変える、あるいはバックアップ間隔を見直すことで根本的に課金を抑えられる。
6. サポート活用：Backblazeサポートは有用。ポリシーや挙動確認で疑問があれば問い合わせる。

