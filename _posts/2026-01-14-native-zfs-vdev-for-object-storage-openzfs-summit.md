---
layout: post
title: "Native ZFS VDEV for Object Storage (OpenZFS Summit) - オブジェクトストレージ向けネイティブZFS VDEV"
date: 2026-01-14T22:26:09.910Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.zettalane.com/blog/openzfs-summit-2025-mayanas-objbacker.html"
source_title: "MayaNAS at OpenZFS Developer Summit 2025: Native Object Storage Integration - ZettaLane Blog"
source_id: 46620673
excerpt: "ZFSがS3へ直アクセスし3.7GB/sを実現、コスト大幅削減の新VDEV"
---

# Native ZFS VDEV for Object Storage (OpenZFS Summit) - オブジェクトストレージ向けネイティブZFS VDEV
魅力的タイトル: ZFSがS3を直ドライブ化する日──objbacker.ioでFUSEを越え、3.7GB/sを実現した仕組み

## 要約
Zettalaneのobjbacker.ioは、FUSEを経由せずにZFSの新しいVDEVとしてオブジェクトストレージ（S3/GCS/Azure Blob）へ直接アクセスする実装で、1MB単位のアラインメントとマルチバケット並列化により最大3.7GB/sの読み取りを実現した。

## この記事を読むべき理由
日本でもクラウドNASのコストと性能のバランスは重要課題。オンプレの代替やクラウド移行を検討する企業にとって、オブジェクトストレージを安価に高性能で使う現実的な選択肢が提示された点は見逃せない。

## 詳細解説
- 背景問題：クラウド上でのNAS運用は高コストになりがち（例：EBS/EFSの年間コスト差）。しかし全データが同じ性能を必要とするわけではない。ZFSなら「メタデータは低レイテンシNVMe」「大判のシーケンシャルデータは安価なオブジェクトストレージ」に分けられる。
- アーキテクチャの肝：objbacker.ioはZFSの新しいVDEVタイプ（VDEV_OBJBACKER）とユーザ空間デーモンで構成され、/dev/zfs_objbackerというキャラクタデバイス経由でZFSと会話する。従来のFUSEベース（s3fs等）ではカーネル<->ユーザ空間を何度も往復するためオーバーヘッドが大きいが、objbackerはその経路を最小化する。
- I/Oマッピング：
  - ZIO_TYPE_WRITE → PUTオブジェクト
  - ZIO_TYPE_READ → GETオブジェクト
  - ZIO_TYPE_TRIM → DELETEオブジェクト
  - ZIO_TYPE_IOCTL(sync) → flush（USYNC）
- 性能のポイント：
  - ZFSのrecordsizeを1MBに設定すると、1ブロック＝1オブジェクトの対応になり、PUT/GETが直行。大きくアラインされた転送がオブジェクトストレージには最適。
  - 並列化：複数（例では6）バケットに対してストライピングすることでネットワーク帯域を飽和させ、読み取りで3.7GB/s、書き込みで2.5GB/sを報告。
  - ベンチ構成例：recordsize=1MB、1MBブロック、10並列fioジョブ、各10GBファイル（合計100GB）、sync I/O。
- マルチクラウドとハイブリッド：MayaNAS（ファイル）とMayaScale（NVMe-oFブロック）を同一構成でAWS/Azure/GCPへ展開可能。NVMeローカルにメタデータと小ブロック、オブジェクトに大ブロックを配置する設計でコスト削減を狙う。
- 成果と主張：FUSEを介さないネイティブVDEV実装により、オブジェクトストレージ上で実用的なZFS運用が可能になったと報告。コスト面ではブロックストレージ比で大きな削減が見込める（記事では70%超の節約を例示）。

## 実践ポイント
- 小手先設定
  - ZFSでオブジェクトVDEVを使うなら recordsize を 1M に設定し、データのアラインメントを揃える。
  - メタデータ／小さいランダムI/OはローカルNVMe（Special Device）に割り当てる。
- 並列性の確保
  - 単一バケットに頼らず複数バケットでストライプ構成にすると帯域利用率が上がる（例：6バケット）。
- ベンチと検証
  - FIOでの検証は上記構成（1MB、10並列、sync）で実施してボトルネックを特定する。
  - ネットワーク（NIC、ENI、リージョン間）やクラウドの帯域制限を事前に確認する。
- 運用上の注意
  - オブジェクト命名規則と整合性（オフセットごとのオブジェクト名管理）を理解しておく。
  - S3等のAPI遅延や一時的なエラーに対するリトライ設計が必要。
- 日本企業向けの検討材料
  - 東京リージョンのS3/GCS/Blob環境で試し、コスト試算（EBS/EFSとの比較）を行う。
  - データ主権やコンプライアンス要件がある場合、オブジェクトの保存場所と暗号化運用を確認する。

最後に：OpenZFSコミュニティでの発表資料と録画（公開後）は実装詳細を理解するのに有益。クラウドNASのコスト構造を見直したいエンジニアは、まず小規模でobjbacker相当の検証を行ってみることを勧める。
