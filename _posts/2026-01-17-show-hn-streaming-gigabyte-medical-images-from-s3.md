---
layout: post
title: "Show HN: Streaming gigabyte medical images from S3 without downloading them - S3上の数ギガ医療画像をダウンロードせずにストリーミングする"
date: 2026-01-17T10:41:42.878Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/PABannier/WSIStreamer"
source_title: "GitHub - PABannier/WSIStreamer: WSI Streamer is a tile server for Whole Slide Images (WSI) stored in S3-compatible object storage. It serves tiles on-demand using HTTP range requests, so you never have to download or mount multi-gigabyte slides on local disk."
source_id: 46656358
excerpt: "S3上の数GB級病理スライドを部分取得で瞬時表示、ローカル保存不要で運用コストとセキュリティを改善"
image: "https://opengraph.githubassets.com/1df69ba63f4be8365005a2251d646e6228f580582f291b630eed5208ede43604/PABannier/WSIStreamer"
---

# Show HN: Streaming gigabyte medical images from S3 without downloading them - S3上の数ギガ医療画像をダウンロードせずにストリーミングする
もう巨大WSIを丸ごと落とさない。S3上の病理スライドをその場で切り出して表示する「WSI Streamer」の使い方と意義

## 要約
WSI StreamerはS3互換オブジェクトストレージ上のWhole Slide Image（WSI）を、HTTPのRangeリクエストで必要なバイトだけ取り出してタイル（JPEG）で返すタイルサーバ。ローカルに数GBのファイルを置かずに、即座にビュー/配信できる点が特徴。

## この記事を読むべき理由
医用画像や病理スライドは巨大で、ダウンロードやマウントがボトルネックになりがち。日本の病院・研究機関やクラウド運用の現場では、ストレージコスト・運用負荷・セキュリティ要件を抑えつつ高速に画像を閲覧できる仕組みが求められており、WSI Streamerは現実的な解決策を提示するから。

## 詳細解説
- 背景と狙い  
  - Whole Slide Image（WSI）は1〜10GBを超えることが多い。従来のビューアはファイル丸ごとを読み込むため、ネットワークやディスクI/Oがネックになる。  
  - WSI Streamerはフォーマット（Aperio SVS、ピラミッドTIFF）をネイティブに理解し、必要なブロックだけHTTP Rangeで取得してタイルを返す。これにより「スライド全体をダウンロードしない」運用が可能になる。

- 技術的要点（簡潔に）  
  - HTTP Rangeリクエストを活用：オブジェクトストレージの部分取得で必要バイトだけ取得。  
  - ネイティブフォーマットパーサ：Rust実装でSVS/TIFFのピラミッド構造を解析してタイル座標に対応。  
  - 出力はJPEGタイル（クライアントはOpenSeadragonベースの組込みビューアでパン・ズーム）。  
  - 認証はHMAC-SHA256による署名付きURLに対応。CORSやキャッシュ設定で運用性を確保。  
  - マルチレベルキャッシュ（スライド・ブロック・エンコード済タイル）により繰り返しアクセスを効率化。  
  - デプロイ方法：Rustバイナリ（cargo install）、Dockerイメージ、Docker Compose（MinIOと組み合わせたローカル検証）をサポート。

- 限界と注意点  
  - 対応フォーマットはタイル化されたピラミッド形式が前提（ストリップ形式や非ピラミッドは不可）。  
  - 医療データの取り扱い（匿名化、アクセス制御、ログ管理、国内法／病院ルール）に注意が必要。  

## 実践ポイント
すぐ試せる最短コマンド例（ローカルでMinIOを使う場合やDocker利用）：

```bash
# ローカルで試す（Rustがある場合）
cargo install wsi-streamer
wsi-streamer s3://my-slides-bucket --s3-region ap-northeast-1

# Dockerで立ち上げ（環境変数でバケット指定）
docker run -p 3000:3000 -e WSI_S3_BUCKET=my-bucket ghcr.io/pabannier/wsistreamer:latest

# タイル取得例
curl http://localhost:3000/tiles/sample.svs/0/0/0.jpg -o tile.jpg
```

運用時のチェックリスト（日本の現場向け）：
- ストレージ：S3互換（AWS S3 / MinIO / オンプレのS3ゲートウェイ）でRangeが使えるか確認。  
- セキュリティ：HMAC署名を有効化し、HTTPSのリバースプロキシ＋IP制限や認証を併用する。  
- データ保護：個人情報に該当する場合は匿名化・アクセスログ保存・APPI準拠の運用を設計。  
- パフォーマンス：キャッシュ（タイルキャッシュ/ブロックキャッシュ）サイズを環境に合わせて調整し、監視を入れる。  
- フォーマット互換性：既存WSIがピラミッド・タイル化されているか確認。必要なら変換ツールを用意する。

短くまとめると、WSI Streamerは「巨大スライドを丸ごと置かずに、クラウド上から必要箇所だけ取り出して高速に表示する」現実的で導入しやすいアプローチ。日本の病理画像運用や研究データ共有の現場で試す価値が高い。
