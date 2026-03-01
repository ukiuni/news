---
layout: post
title: "AWS Middle East Central Down, apparently struck in war - AWS中東リージョン（ME-CENTRAL）ダウン、被弾による停電の可能性"
date: 2026-03-01T20:08:37.362Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://health.aws.amazon.com/health/status"
source_title: "AWS Middle East Central Down, apparently struck in war"
source_id: 47209781
excerpt: "AWS中東リージョンの単一AZ被弾で長時間停止、復旧と設計見直しの急所を解説"
---

# AWS Middle East Central Down, apparently struck in war - AWS中東リージョン（ME-CENTRAL）ダウン、被弾による停電の可能性

AWS中東リージョンの単一AZ（mec1-az2）が「飛来物で被弾 → 火災 → 消防による停電」で長時間停止。ほかAZは稼働中だが、EC2/EBS/RDSなどに影響が出ており、復旧は数時間単位。

## 要約
単一のAvailability Zone（mec1-az2）が外的要因で火災・停電し、同AZ内のEC2/EBS/RDS等が利用不可に。AWSはトラフィックを他AZへ回避中だが、プロビジョニング遅延やエラー増加が発生している。

## この記事を読むべき理由
地政学的リスクや物理的障害がクラウド運用に直結する事例は、日本のAWS利用者にも他人事ではありません。設計や運用の見直し、BCP（事業継続計画）の実践点を学べます。

## 詳細解説
- 事象概要: 3/1 朝、mec1-az2に「外部からの物体衝突で発火」。消防が消火のため施設と発電機の電源を遮断。電源復旧は許可待ちで、復旧まで数時間。
- 影響範囲: EC2インスタンス起動障害、既存EC2/EBS/RDSの接続不可。多数のAWSサービスでエラー率・レイテンシ増。AWSは影響AZを「weighted away」（トラフィック回避）して対応。
- 運用上の観測: 他AZへの負荷集中により、プロビジョニング遅延や特定インスタンスタイプの枯渇が発生。APIリトライを推奨、即時回復が必要な場合はスナップショットからの復元や別AZ/別リージョンでの再作成を案内。
- 復旧見込み: 数時間単位。AWSは定期的にステータス更新を提供。

## 実践ポイント
- まず確認: AWS Health DashboardとEventBridgeの通知を即時購読する（自動通知設定）。
- 設計:
  - 重要リソースはマルチAZまたはマルチリージョン配置にする（RDSはMulti‑AZ/リードレプリカ）。
  - 単一AZ依存の設計は避ける／早急に移行計画を作成。
- バックアップと復旧:
  - EBSスナップショット、AMI、RDSスナップショットの定期取得と復元手順をドキュメント化・自動化。
  - IaC（Terraform/CloudFormation）で別AZ/別リージョンへ迅速に再作成できるようにする。
- 耐障害運用:
  - Auto ScalingとRoute53ヘルスチェック／フェイルオーバーを活用。
  - プロビジョニング失敗に備え、代替インスタンスタイプのリストを用意。
  - API呼び出しは指数バックオフ付きリトライを実装。
- 定期検証: DR訓練を定期実施し、復元時間とデータ整合性を検証する。

短く言えば、クラウドでも「物理的リスク」は現実。単一AZ依存のリスクを見直し、バックアップ・自動化・検証を強化することが今回の教訓です。
