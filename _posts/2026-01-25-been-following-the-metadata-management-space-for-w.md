---
layout: post
title: "Been following the metadata management space for work reasons and came across an interesting design problem that Apache Gravitino tried to solve in their 1.1 release. The problem: we have like 5+ different table formats now (Iceberg, Delta Lake, Hive, Hudi, now Lance for vectors) and each has its - メタデータ管理の混沌に挑むApache Gravitino 1.1: ランチ（Lance）対応と汎用カタログで湖屋を統合する"
date: 2026-01-25T15:40:13.951Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/apache/gravitino/releases/tag/v1.1.0"
source_title: "Release Apache Gravitino 1.1.0 · apache/gravitino · GitHub"
source_id: 417899162
excerpt: "Gravitino1.1がLance対応と汎用カタログで多様なテーブル形式と権限管理を統合"
image: "https://opengraph.githubassets.com/d1128afa4ee851e6df789bca56a951dcce7da0d16a213494edeebc762982683a/apache/gravitino/releases/tag/v1.1.0"
---

# Been following the metadata management space for work reasons and came across an interesting design problem that Apache Gravitino tried to solve in their 1.1 release. The problem: we have like 5+ different table formats now (Iceberg, Delta Lake, Hive, Hudi, now Lance for vectors) and each has its - メタデータ管理の混沌に挑むApache Gravitino 1.1: ランチ（Lance）対応と汎用カタログで湖屋を統合する

魅力的なタイトル: 「複数フォーマット時代を制す：Apache Gravitino 1.1で進化するデータ湖のガバナンスとベクトル対応」

## 要約
Apache Gravitino 1.1は、ベクトルデータ向けのLance RESTサービスや汎用レイクハウス・カタログ、Iceberg RESTの認可強化、Hive3・複数HDFSクラスタ対応などを追加し、多様化するテーブル形式と運用課題に対する統合的な解決を進めたリリースです。

## この記事を読むべき理由
日本の企業でもHiveや複数HDFS、オンプレ＋クラウド混在の環境が残る中、フォーマット多様化（Iceberg/Delta/Hudi/Lance等）に対応できる統一的なメタデータ管理とセキュリティ設計は移行・運用コスト削減に直結します。本稿は1.1の技術的要点と日本での導入・移行観点を短く整理します。

## 詳細解説
- Lance RESTサービス：ベクトル（検索・推論向け）データをHTTP経由で高性能に提供。推論サービスやノートブックから安全にアクセス可能で、AIワークロードを想定した設計。
- 汎用レイクハウス・カタログ：異なるテーブル形式やエンジンを抽象化するフレームワークを導入。新フォーマット対応のボイラープレートを減らし、拡張性と一貫した権限処理を実現。
- Iceberg RESTの認可強化：Iceberg経由のアクセスに対する認証・認可チェックを強化し、マルチテナントや公開API運用での安全性を高めた。
- Hive3カタログ対応：既存のHive3メタストアを移動なしで登録可能に。レガシー資産を壊さずガバナンス対象に組み込める。
- 複数HDFSクラスタ対応：複数HDFS間でのファイルセット管理を単一Gravitinoインスタンスで扱えるようにし、分離／DR構成に対応。
- メタデータの細粒度認可：タグ、統計、ジョブ、ポリシー等の補助リソースにも権限制御を適用し、最小権限原則をプラットフォーム全域に拡張。
- 互換性・運用改善：Icebergのアップグレード、メタデータキャッシュ、Pythonクライアントの改善、メトリクス強化、HelmやDockerベース改善、テスト安定化など運用面の改善多数。
- バグ修正と安定化：エンティティストア、キャッシュ、スキャン計画、コネクタの性能や観測性向上で運用摩擦を低減。

## 実践ポイント
- まずステージ環境で1.1のLance RESTを試し、自社の推論フロー（推論サーバ／ノート）からのレイテンシと互換性を評価する。
- 既存Hive3資産がある場合は、メタストアを直接登録して移行リスクを低減する手順を検討する。
- Icebergクライアント経由で公開するAPIは認可設定を必ず有効化して、マルチテナント運用の安全性を担保する。
- 複数HDFS運用やクロスリージョン移行を予定している場合は、ファイルセットのクラスタ設定とリソース分離ポリシーを定義してから導入する。
- Helmチャートやメトリクス設定で可観測性（エンティティ・キャッシュ・ジョブ指標）を整備し、運用時のトラブルシュートを容易にする。

以上。詳細はリリースノート（GitHubのv1.1.0）で興味ある変更番号やIssueを参照してください。
