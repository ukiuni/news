---
layout: post
title: "Bucketsquatting Is (Finally) Dead - バケットスクワッティングは（ついに）終焉"
date: 2026-03-13T09:01:52.411Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://onecloudplease.com/blog/bucketsquatting-is-finally-dead"
source_title: "Bucketsquatting is (Finally) Dead – One Cloud Please"
source_id: 47361913
excerpt: "S3の新命名規則でバケットスクワッティングを防ぎ、IaCと運用の即時見直しが必須に"
image: "https://onecloudplease.com/images/posts/bucket.jpg"
---

# Bucketsquatting Is (Finally) Dead - バケットスクワッティングは（ついに）終焉
S3バケット名の“当たり”を防ぐ新ルール。今すぐ命名ルールを見直すべき理由。

## 要約
AWSがS3の「バケットスクワッティング」対策として新しい名前空間（<prefix>-<accountid>-<region>-an）を推奨・強制できる仕組みを導入。これにより削除済みバケット名を奪われるリスクが大幅に低減する。

## この記事を読むべき理由
日本企業も予測可能なバケット名（例: app-region）を使いがちで、削除・再作成やIaCのテンプレート移行で思わぬ情報漏洩やサービス障害が起き得ます。新仕様は今後の運用・テンプレート設計に直結します。

## 詳細解説
- 問題の本質：S3バケット名はグローバル一意。所有者がバケットを削除すると同名が再登録可能になり、攻撃者が同名でバケットを作ると既存の依存先や公開設定によってデータ漏洩やサービス破綻を招ける（これが「バケットスクワッティング/バケツスナイピング」）。
- AWSの対策：新しい名前空間パターンを導入し、形式は  
  myprefix-123456789012-us-west-2-an のように `<prefix>-<accountid>-<region>-an` を推奨。  
  このパターンでは同一アカウント以外の作成を弾き、リージョン不一致での作成も InvalidBucketNamespace エラーを返す。
- 運用面：AWSはこのパターンをデフォルト推奨とし、組織全体で強制するための条件キー s3:x-amz-bucket-namespace を用意。SCPやポリシーで新規バケット作成時にこの命名を必須化できる。
- 範囲と限界：既存バケットには自動では適用されないため、保護するには名前空間付きの新バケットを作って移行が必要。テンプレート（CloudFormation/Terraform）や公開ドキュメントの命名規約も更新する必要がある。
- 他クラウドとの比較：GCPはドメイン所有確認ベースの名前空間で一部を保護、Azureはアカウントスコープ＋コンテナでリスクが小さい。

## 実践ポイント
- 命名規則を今すぐ変更：新規S3は `<prefix>-<accountid>-<region>-an` を採用。  
- IaCを更新：CloudFormation/Terraformテンプレートのバケット名生成ロジックを修正して自動化する。  
- 組織ポリシーで強制：SCP / IAMで s3:x-amz-bucket-namespace を使い、ルール違反を防止する。  
- 既存バケットの移行計画：影響評価→新バケット作成→データ移行→DNS/アプリの切替を段階的に実施。  
- 監査とアラート：バケット名のパターン違反や InvalidBucketNamespace エラーを検出する監視を追加。

参考（簡易ポリシー例）:
```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Deny",
    "Action": "s3:CreateBucket",
    "Resource": "*",
    "Condition": {
      "StringNotLike": {
        "s3:x-amz-bucket-namespace": ["*-123456789012-*-an"]
      }
    }
  }]
}
```

新ルールは「バケット名運用」の常識を変えます。まずはIaCと組織ポリシーのチェックから始めましょう。
