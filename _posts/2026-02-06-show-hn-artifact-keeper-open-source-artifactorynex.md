---
layout: post
title: "Show HN: Artifact Keeper – Open-Source Artifactory/Nexus Alternative in Rust - Show HN: Artifact Keeper — Rust製のオープンソースなArtifactory/Nexus代替"
date: 2026-02-06T07:12:25.453Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/artifact-keeper"
source_title: "artifact-keeper · GitHub"
source_id: 46909037
excerpt: "Rust製OSSのArtifactory代替、45種対応と脆弱性スキャン搭載"
image: "https://avatars.githubusercontent.com/u/258666557?s=280&amp;v=4"
---

# Show HN: Artifact Keeper – Open-Source Artifactory/Nexus Alternative in Rust - Show HN: Artifact Keeper — Rust製のオープンソースなArtifactory/Nexus代替

企業レジストリを“丸ごと”自前で持てる時代へ — Artifact Keeperで始める社内パッケージ管理革命

## 要約
Artifact KeeperはRust製のセルフホスト型アーティファクトレジストリで、JFrog ArtifactoryやSonatype Nexusのドロップイン代替を目指す。45以上のネイティブプロトコル、脆弱性スキャン、WASMプラグイン、エッジ複製など企業向け機能をOSS（MIT）で提供する。

## この記事を読むべき理由
日本企業でもオンプレ／閉域ネットワークでのパッケージ配布やセキュリティ・コンプライアンスが重視される中、コストのかかる商用ソリューションに代わる選択肢として有望。既存のビルドパイプライン（npm/maven/docker/cargo等）をほぼそのまま置き換えできる点は実務的メリットが大きい。

## 詳細解説
- コア設計
  - バックエンド：Rust + Axum。PostgreSQLでメタデータ管理、Meilisearchで全文検索。
  - フロントエンド：Next.js（TypeScript）、モバイルはSwift/Kotlinのネイティブアプリ。
- 主要機能
  - 45+パッケージ形式をネイティブプロトコルでサポート（単なるバイナリラベルではない）。
  - セキュリティスキャン統合：Trivy（イメージ/FS）とGrype（依存関係）を利用し、ポリシーによる閾値・隔離・ダウンロード前スキャンが可能。
  - WASMプラグイン：独自フォーマット対応を外部プラグイン（Wasmtime）で実装でき、バックエンドをフォークする必要がない。
  - エッジ複製：メッシュベースでノード間の同期・P2P転送が可能。ビルドエージェント近傍にキャッシュを置ける。
  - SSO/認証：OIDC、LDAP、SAML、JWT、APIトークン、RBAC対応。
  - Artifactoryからの移行ツールを備え、リポジトリ・ユーザー・権限の一括移行を想定。
- 運用面
  - Docker ComposeやKubernetesでデプロイ可能。MITライセンスで全機能がOSSに含まれる（オープンコアなし）。

クイックスタート（ローカル検証用）
```bash
# clone と docker-compose 起動
git clone https://github.com/artifact-keeper/artifact-keeper.git
cd artifact-keeper
docker compose up -d

# ブラウザでアクセス
# http://localhost:9080
```

## 実践ポイント
- まずローカルでDocker Composeを起動して、既存のCIでnpm/pytest/docker pull等を向けて動作検証する。
- セキュリティスキャンの閾値を設定し、既存の脆弱性ワークフローと統合する（Trivy/Grype連携）。
- Artifactory/Nexusからの移行を試す際は、テストリポジトリで移行ツールを試運転してメタデータ整合性を確認する。
- 独自フォーマットがある場合はWASMプラグインでプロトタイプを作り、運用負荷を評価する。
- 複数拠点でビルドがあるならエッジ複製を検証してネットワーク負荷とビルドキャッシュヒット率を比較する。

参考：リポジトリ（README）とドキュメントで詳細手順、デプロイガイド、API仕様が公開されているため、まずは公式リポジトリをチェックして実際に触ってみてください。
