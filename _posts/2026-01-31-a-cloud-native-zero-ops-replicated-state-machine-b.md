---
layout: post
title: "A cloud native, zero-ops replicated state machine built atop S3. - S3上に構築されたクラウドネイティブなゼロオプス複製ステートマシン"
date: 2026-01-31T21:17:15.757Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/io-s2c/s2c"
source_title: "GitHub - io-s2c/s2c: A cloud native, zero-ops replicated state machine built atop S3."
source_id: 412625619
excerpt: "S3を合意基盤にし運用ゼロで線形化・exactly-onceなレプリケート状態マシン"
image: "https://opengraph.githubassets.com/9c889dcc151c407c67c55528955e91c03f23e309c09819c4ca6a58a33d9c6256/io-s2c/s2c"
---

# A cloud native, zero-ops replicated state machine built atop S3. - S3上に構築されたクラウドネイティブなゼロオプス複製ステートマシン
魅力タイトル: S3で合意を取る時代へ — 「クラウドにおけるゼロオペ」なレプリケート済み状態マシンS2Cとは？

## 要約
S2CはAWS S3（またはS3互換ストレージ）を合意基盤として使うことで、クォーラムや専用クラスタ運用を不要にする強整合なレプリケート状態マシンです。単一ノードでも線形化可能な読み書きと exactly-once 命令を提供します。

## この記事を読むべき理由
- クォーラム運用やRaft/Paxosの運用コストを下げたい開発者にとって現実的な選択肢だから。  
- 日本でもS3利用は一般的で、コストと運用負荷を抑えた分散設計の参考になるため。

## 詳細解説
- 基本アイデア：S3の強整合性と条件付き書き（Conditional Writes）／ETagを合意機構に見立て、Leader状態・ログ・コミットをS3上で管理する。  
- 置き換えるもの：
  - クォーラム → S3オブジェクト（単一ソース）  
  - 投票（voting） → ETagによるフェンシング  
  - リース（leader leases） → 条件付き書き（S3の原子的更新）  
- 主要保証：
  - 線形化（linearizable）な読み書き  
  - exactly-once コマンド処理（ただし一意で安定したノードIDが必要）  
  - 単一ノードでも可用（フルクラスタ停止後もコールドスタートで復旧可）  
  - シャーディングのためのマルチクラスタ対応、分割脳は設計上発生しない  
- 性能と制約：
  - S3レイテンシとコストのためバッチ処理やポーリング回避の設計を採用。低レイテンシ（マイクロ秒単位）用途には不向き。  
  - S3互換ストレージで同等の一貫性を満たす必要がある。  
- アーキテクチャ（高レベル）：
  - S3に保存された LeaderState が単一の権威ソース。  
  - フォロワーはRPCでステートをリアルタイム同期（オプション）し、必要時にリーダを引き継げる。  
  - スナップショット・ログ・コミットはS3で管理。ETagでフェンスして競合を防ぐ。  
- 活用例：コントロールプレーン、メタデータサービス、設定管理、分散ロック、永続カウンタなど。データベースとして使う場合はレイテンシ要件に注意。

## 実践ポイント
- 使いどころ：S3を既に使っており、運用を減らしたい管理系サービスに最適。  
- 注意点：超低遅延が必須のサービスやS3非対応環境では不適。ノードIDは一意かつ安定に管理すること（exactly-onceの前提）。  
- 簡単な始め方（Java／Gradle, JitPack経由）：  

```java
// build.gradle の依存例
repositories {
    mavenCentral()
    maven { url 'https://jitpack.io' }
}
dependencies {
    implementation 'com.github.io-s2c:s2c:0.1.2-alpha'
}
```

```java
// 初期化の骨子（概念的）
S3Client s3Client = S3Client.builder().region(Region.AP_NORTHEAST_1).build();
S3Facade s3Facade = S3Facade.createNew(s3Client);
NodeIdentity id = NodeIdentity.newBuilder().setAddress("127.0.0.1").setPort(8080).build();
S2CNode node = S2CNode.builder().bucket("my-s2c-bucket").nodeIdentity(id).s2cGroupId("my-cluster").build();
S2CServer server = new S2CServer(id, new S2COptions());
server.start(); node.start();
```

- 日本向けの実務TIPS：
  - 東京リージョン（ap-northeast-1）を使うことでレイテンシを最小化。  
  - S3のAPIコストを踏まえ、バッチやスナップショット閾値を調整する。  
  - 監視はMicrometer等で統合（S2CはMeterRegistryを受け取れる）。

S2Cは現時点でアルファ版。運用前に十分な検証（Jepsen系の耐障害テスト、ベンチマーク）を推奨するが、運用負荷を下げたい日本のチームには魅力的な選択肢となり得る。
