---
layout: post
title: "Floci – A free, open-source local AWS emulator - Floci — 無料のオープンソース ローカルAWSエミュレータ"
date: 2026-03-22T04:03:17.951Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/hectorvent/floci"
source_title: "GitHub - hectorvent/floci: Light, fluffy, and always free - AWS Local Emulator · GitHub"
source_id: 47471801
excerpt: "MITライセンスで超軽量、ローカルで本物に近いAWS環境を即起動できるFloci"
image: "https://repository-images.githubusercontent.com/1160497244/575740e3-dd0e-487b-993f-315bb7850275"
---

# Floci – A free, open-source local AWS emulator - Floci — 無料のオープンソース ローカルAWSエミュレータ
ローカルで「本物に近いAWS」を超軽量かつ無料で再現する、新しい選択肢 — 今すぐ試したくなる小さなクラウド

## 要約
FlociはMITライセンスの軽量なローカルAWSエミュレータで、LocalStackのコミュニティ版が制限を強めた後の「無償でCIでも使える」代替となるツールです。複数サービスに対応し、非常に高速・低メモリで動作します。

## この記事を読むべき理由
LocalStackコミュニティ版の仕様変更でローカル開発／CI環境に影響が出る日本の開発チームにとって、Flociはコストゼロで既存のAWS SDK互換ワークフローに差し替えられる現実的な選択肢です。スタートアップや教育現場、オフラインでの検証にも最適です。

## 詳細解説
- ライセンスと方針：MITで永続的に無料。認証トークンやCI制限なし。セキュリティ更新を継続提供。
- パフォーマンス：Nativeイメージで起動時間約24ms、アイドル時メモリ約13MiB、イメージサイズ約90MB（LocalStackと比べ格段に軽量）。
- 対応状況：20以上のサービスをサポートし、408/408のSDKテストを通過。API Gateway v2、Cognito、ElastiCache、RDS、S3オブジェクトロックやDynamoDB Streams、IAM/ST Sの主要操作など、多くがネイティブ対応。
- 設定：Docker Composeで簡単に立ち上がり、エンドポイントは http://localhost:4566 。認証情報は任意でOK（例：accessKey=test）。
- カスタマイズ：FLOCI_プレフィックスの環境変数でポート、リージョン、ストレージモード（memory/persistent/hybrid/wal）などを調整可能。

簡単な起動例：
```yaml
# yaml
services:
  floci:
    image: hectorvent/floci:latest
    ports:
      - "4566:4566"
    volumes:
      - ./data:/app/data
```

SDK接続例：
```java
// java
DynamoDbClient client = DynamoDbClient.builder()
  .endpointOverride(URI.create("http://localhost:4566"))
  .region(Region.US_EAST_1)
  .credentialsProvider(StaticCredentialsProvider.create(AwsBasicCredentials.create("test","test")))
  .build();
```

```python
# python
import boto3
client = boto3.client("s3", endpoint_url="http://localhost:4566", region_name="us-east-1",
                      aws_access_key_id="test", aws_secret_access_key="test")
```

```javascript
// javascript
import { S3Client } from "@aws-sdk/client-s3";
const client = new S3Client({
  endpoint: "http://localhost:4566",
  region: "us-east-1",
  credentials: { accessKeyId: "test", secretAccessKey: "test" },
  forcePathStyle: true,
});
```

## 実践ポイント
- まずは docker compose up で立ち上げ、既存のテストを endpoint を変えるだけで流す（CIも同様）。  
- S3は forcePathStyle が必要な場合があるのでSDK設定を確認。  
- 永続化が必要なら FLOCI_STORAGE_MODE=persistent とデータディレクトリをマウント。  
- 本番挙動との差分（特にIAM・KMSの詳細挙動）は簡易に確認しておく。  
- 軽量ネイティブイメージ（latest）を使えば起動が非常に速くローカル開発が快適になる。
