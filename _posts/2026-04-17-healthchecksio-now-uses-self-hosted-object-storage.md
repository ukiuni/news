---
layout: post
title: "Healthchecks.io Now Uses Self-Hosted Object Storage - Healthchecks.io がセルフホスト型オブジェクトストレージを採用"
date: 2026-04-17T15:00:01.236Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://blog.healthchecks.io/2026/04/healthchecks-io-now-uses-self-hosted-object-storage/"
source_title: "Healthchecks.io Now Uses Self-hosted Object Storage &#x2013; Healthchecks.io Blog"
source_id: 47806348
excerpt: "監視サービスがVersity＋Btrfsで自前S3化、遅延改善と費用削減"
image: "https://blog.healthchecks.io/wp-content/uploads/2026/04/s3-api-timing-1024x668.png"
---

# Healthchecks.io Now Uses Self-Hosted Object Storage - Healthchecks.io がセルフホスト型オブジェクトストレージを採用
監視サービスが選んだ「自前S3」──性能低下と費用に疲れたら取れる実践的な道

## 要約
Healthchecks.io は頻繁な小〜中サイズのペイロード保存で課題が増えたため、OVH/UpCloudなどのマネージドS3から Versity S3 Gateway＋Btrfs を用いたセルフホストへ移行し、レイテンシと信頼性を改善した。

## この記事を読むべき理由
日本でもSaaSや自社サービスで「大量の小さなオブジェクト」を扱うケースは増えており、マネージドS3のコスト／パフォーマンス制約や運用負担に悩むチームにとって現実的な代替案とその設計トレードオフが学べるため。

## 詳細解説
- 利用状況（2026年4月時点）: 1,400万オブジェクト、合計119GB、平均8KB、通常30PUT/s、ピーク150PUT/s。オブジェクトは100B〜100kB。
- 問題点: AWSはリクエスト単位課金とCLOUD Actの懸念、OVH/UpCloudでは時間経過でS3操作（特にDeleteObjects）が遅くなりタイムアウトやキュー増大を招いた。遅いS3操作がWebリクエストを阻害したため、ロードシェディングを導入する必要が出た。
- 検討した自前候補: Minio / SeaweedFS / Garage。いずれも基本構築は容易だが、運用（ノード展開・アップグレード・故障対応・監視）が複雑で、単独運用者の負担が大きい。
- 採用した構成: Versity S3 Gateway（ローカルFSをS3 APIで提供）。特徴はメタデータDB不要でPut/Get/Deleteが通常のファイル操作になること。バックエンドはBtrfs（小ファイル大量に強い、inode枯渇問題なし）。物理構成は専用サーバ（NVMe×2 RAID1）、アプリはWireGuardで接続。バックアップは2時間毎にrsyncで差分同期、バックアップ側で日次フルを暗号化してオフサイト保管、30日分保持。
- リスクとトレードオフ: 単一システム故の可用性・耐久性リスク（最悪で2時間分のデータ損失想定）。費用は専用サーバで増えるが、レイテンシ改善と信頼性向上を確認。Versityは小さなバグ修正が早く、運用がシンプルなのが利点。

## 実践ポイント
- 自前検討の前に規模を数値化する（オブジェクト数・平均サイズ・PUT/sピーク）して単一サーバで収まるか確認する。
- 小ファイル大量運用ならBtrfsを検討（inode問題回避）。
- S3ゲートウェイを使う場合、WireGuard等でプライベート接続を確保し、バックアップ頻度（例: 2時間）とオフサイト暗号化を決める。
- 運用コストと可用性のトレードオフを明確に：専用サーバ×RAID1＋定期バックアップなら運用はシンプルだが「ゾーン冗長性」はない。
- 本番導入前にS3操作のレイテンシ監視・障害時の復元手順を必ず実働でテストする。
