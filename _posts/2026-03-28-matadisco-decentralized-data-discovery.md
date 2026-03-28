---
layout: post
title: "Matadisco – Decentralized Data Discovery - Matadisco — 分散型データ発見"
date: 2026-03-28T09:49:59.096Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://matadisco.org/"
source_title: "Matadisco — Decentralized Data Discovery"
source_id: 47519845
excerpt: "マタディスコはATプロトコルで分散メタデータを共有し、見えないデータを発掘"
---

# Matadisco – Decentralized Data Discovery - Matadisco — 分散型データ発見
見えないデータを一発で発掘する仕組み — Matadiscoが切り拓く分散型データ検索

## 要約
Matadiscoは、データ本体をそのまま移すのではなく「発見用メタデータ」を分散ネットワーク上で公開・共有する仕組み。AT Protocolを土台にして、誰でもデータの発見性を高められるオープンなネットワークを目指すプロジェクトです。

## この記事を読むべき理由
日本でも衛星データ、気候モデル、ゲノム、文化資産など大量の公開データがある一方、検索はポータルごとに分断されています。Matadiscoは「派生データやコミュニティ貢献が埋もれない仕組み」を提供し、日本の研究機関や自治体、データ利活用コミュニティに直結する可能性があります。

## 詳細解説
- アーキテクチャ
  - 発見（discovery）と保存（storage）を切り分ける。実データは既存のリポジトリに残し、軽量なメタデータ（レコード）だけをAT Protocol上で流通させる。
  - 基盤はAT Protocol（オープンなソーシャルプロトコル）。各レコードは署名され、中央管理者が不要で自己ホスト可能。
- 役割
  - Producer：既存カタログやデータソースを監視して、メタデータへのポインタ（レコード）をPDS（Personal Data Server）へ書き込む。
  - Consumer：PDSやJetstream（Blueskyの配信）からレコードを読み取り、フィルタしてウェブポータルとして表示する。数十〜100行程度のコードでポータルを作れることを目標にしている。
- スキーマ（要点）
  - MatadiscoのレコードはATProtoのLexiconで定義。必須は公開日時とメタデータへのURI。プレビュー（サムネ、音声スニペット等）は任意。
  - 例（MLF表記）:
```mlf
cx.vmx.matadisco
record matadisco {
  publishedAt!: Datetime,
  resource!: Uri,
  preview: {
    mimeType!: string,
    url: Uri,
  },
}
```
- 対応可能なメタデータ規格
  - STAC（衛星／地理空間）、DataCite（研究データ）、IIIF（画像コレクション）、RSSなど。つまり既存標準を壊さず接続できる。
- 既存コンポーネント（プロトタイプ）
  - sentinel-to-atproto（Sentinel-2のSTACを監視して公開）
  - gdi-de-csw-to-atproto（ドイツ地理データカタログから取り込み）
  - matadisco-viewer / matadisco-geo-viewer（Jetstream/PDSから表示）
- 背景と影響
  - 中央集権的なアグリゲータや政府ポータルの制限を回避し、コミュニティや研究者が独自に発見性を高められる。IPFS Foundation発、OSSとして開発中。

## 実践ポイント
- まずデモで動きを確認：ライブデモで衛星画像レコードの流れを観察する。
- GitHubをクローンして触る：PublisherやViewerのソースが公開されている。簡単なポータルは数十〜100行の実装から。
- 自組織での活用案：
  - 衛星/STAC系データ：自動でSTACカタログを監視してMatadiscoへ公開。
  - 文化財/美術館：IIIFメタデータをレコード化して発見性を強化。
  - 研究データ：DataCiteメタデータへのリンクを公開して引用・二次利用を促進。
- 運用面：PDSを立てて自ドメインで公開、または既存のJetstreamリレーと連携して消費側ポータルを構築する。
- 貢献：スキーマ改善や日本語ドメタデータ事例の追加でプロジェクトに参加可能。

興味があれば、まずライブデモ→GitHub→自組織の小さなデータカタログを公開、の順で試すと早いです。
