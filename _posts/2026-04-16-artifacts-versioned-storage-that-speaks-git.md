---
layout: post
title: "Artifacts: Versioned storage that speaks Git - Artifacts：Gitに対応するバージョン付きストレージ"
date: 2026-04-16T19:17:48.973Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://blog.cloudflare.com/artifacts-git-for-agents-beta/"
source_title: "Artifacts: versioned storage that speaks Git"
source_id: 47792374
excerpt: "Cloudflare Artifactsで即席Gitリポジトリを作り、AIセッションを秒で復元"
image: "https://cf-assets.www.cloudflare.com/zkvhlag99gkb/3agnY3anQtjeSkoITT532S/4ff57c61bfaf9ecc4eaa53c13d229726/BLOG-3269_OG.png"
---

# Artifacts: Versioned storage that speaks Git - Artifacts：Gitに対応するバージョン付きストレージ
AIエージェント時代の「即席リポジトリ」――CloudflareのArtifactsは、Git互換の分散版ファイルシステムでエージェント・サンドボックス・サーバーレスに最適化されています。

## 要約
Cloudflare Artifactsは「Gitとして振る舞う」バージョン付きストレージで、プログラムからリポジトリを即座に作成・フォーク・インポートでき、WorkersやREST API経由でサーバーレス環境からも操作できます。

## この記事を読むべき理由
エージェント／AIが大量のコードとセッション状態を生成する今、従来のソース管理はスケール不足。日本の開発チームやSaaSプロダクトでも、サンドボックス起動時間短縮やセッション共有、顧客別設定のロールバックなど即効性ある改善が期待できるからです。

## 詳細解説
- 基本コンセプト：Gitプロトコル互換のリモートを提供し、エージェントがそのままgit操作できるようにした「エージェント優先」のバージョン付きファイルシステム。非Gitクライアント向けにREST/Workers APIやSDKも用意。
- 主な機能：プログラムによるリポジトリ作成・トークン発行・インポート（既存Gitからのブートストラップ）・リポジトリのフォークや読み取り専用コピー生成。
- スケールと実装：Durable Objects上に各リポジトリを配置。軽量なZigで書かれたGit実装をWasm化してWorkersで動かし、R2（スナップショット）とKV（トークン追跡）を利用。大オブジェクトはチャンク化してSQLite-backed storageへ格納、ストリーミングで効率的に配信。
- Gitの利点：エージェントはGitを学習済みで互換性が高く、履歴・差分・フォークといったGitのセマンティクスはファイル以外の状態管理（セッション、プロンプト履歴、顧客設定等）にも有効。
- ArtifactFS：大規模リポジトリ向けのドライバで「ブロブレスクローン」を実現。ツリーとrefだけ先に取得し、ファイル内容は背景で優先度を付けて逐次ハイドレートすることで起動時間を大幅短縮（数分→十数秒を目標）。
- 互換性：Gitプロトコルv1/v2、浅いクローン、ls-refs、have/want交渉、git-notes対応。ArtifactFSは任意のGitリモート（GitHub/GitLab等）でも動く。

## 実践ポイント
- まず試す：Workers有料プランのプライベートベータに登録して、env.AGENT_REPOS.createで即席リポジトリを作ってみる。  
  ```javascript
  // javascript
  const repo = await env.AGENT_REPOS.create(name)
  return { repo.remote, repo.token }
  ```
  ```bash
  # bash
  git clone https://x:${TOKEN}@123def456abc.artifacts.cloudflare.net/git/repo-13194.git
  ```
- サーバーレスから運用：WorkerやLambdaからREST APIでリポジトリをインポート／生成し、エージェントごとに隔離されたセッションストレージを実装。
- 大規模リポジトリ改善：開発コンテナ／CIの起動時間が課題ならArtifactFSで「ツリー先行・コンテンツ後入れ」を導入して体感速度を改善。
- コスト設計：数百万リポジトリを想定するなら、操作回数とGB単位のストレージ課金を試算して運用ポリシー（コールドリポジトリの扱い等）を決定。
- ドキュメント確認：公式のGetting Started／APIドキュメントとBetaの利用条件を事前にチェックして段階的に導入。

Cloudflareはβから順次公開予定。AIエージェントや大量のサンドボックス運用をしているチームは早めに試しておくと恩恵が大きいでしょう。
