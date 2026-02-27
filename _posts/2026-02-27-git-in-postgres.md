---
layout: post
title: "Git in Postgres - Postgres上のGit"
date: 2026-02-27T12:55:01.122Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://nesbitt.io/2026/02/26/git-in-postgres.html"
source_title: "Git in Postgres | Andrew Nesbitt"
source_id: 1195116852
excerpt: "PostgresでGitを管理し、フォージ統合・検索・バックアップをDB一元化"
image: "https://nesbitt.io/images/boxes.png"
---

# Git in Postgres - Postgres上のGit
Gitをデータベースに載せると、フォージ運用と統合が一変する――Postgresで動く「gitgres」の可能性

## 要約
libgit2のストレージをPostgresのテーブルに差し替えた実験（gitgres）で、gitオブジェクトと参照をSQLとして扱えるようにし、フォージの統合・バックアップ・検索が劇的にシンプルになる可能性を示した話です。

## この記事を読むべき理由
Forgejo/Giteaなどを自前で運用する日本のチームや、gitデータをアプリ側DBと強く連携させたい開発者にとって、運用負荷の低減と新しい検索・連携の道が開きます。

## 詳細解説
- アプローチ概要  
  gitのデータモデル（コンテンツアドレス可能なオブジェクトストアと参照）はプロトコルとフォーマットが分離可能で、保存先をファイルからPostgresに差し替えられます。作者はlibgit2のbackend（git_odb_backend, git_refdb_backend）をCで実装し、gitクライアントは通常通りpush/cloneできます。クライアント側のリモートヘルパーは git-remote-gitgres。

- スキーマ（要点）  
  オブジェクトと参照は2テーブルに収まります。例えば：
  ```sql
  -- sql
  CREATE TABLE objects (
    repo_id integer NOT NULL,
    oid bytea NOT NULL,
    type smallint NOT NULL,
    size integer NOT NULL,
    content bytea NOT NULL,
    PRIMARY KEY (repo_id, oid)
  );

  CREATE TABLE refs (
    repo_id integer NOT NULL,
    name text NOT NULL,
    oid bytea,
    symbolic text,
    PRIMARY KEY (repo_id, name)
  );
  ```
  オブジェクトのOIDは従来通り
  $ \mathrm{SHA1}(\text{"<type> <size>\0<content>"}) $
  で計算され、pgcryptoのdigest()で得られます。

- Postgres側の利点  
  - SQLでコミット・ツリー・メタデータを参照できるため、コミットとIssueの結び付けなどが単一クエリで可能（アプリ側でgit logを呼ぶ必要が消える）。  
  - NOTIFYでプッシュ通知、行レベルセキュリティでマルチテナント隔離、論理レプリケーションで部分的ミラーが実現可能。  
  - 検索はpg_trgm等でDB内完結。コミットグラフ探索は再帰CTEで表現できる。

- そのままでは残る課題  
  - diff/merge/blame等のコンテンツ比較やグラフアルゴリズムはlibgit2に任せる想定（SQLで再実装する必要はない）。  
  - ストレージ効率：packfileのデルタ圧縮を使わずオブジェクトをフル保存するので、履歴が深い大きなバイナリは肥大化する。対策は定期的なDB内の再パック処理や大きなBLOBの外部オフロード（S3やLFS相当）。

## 実践ポイント
- 小規模フォージ運用なら試す価値あり：dockerでgitgresを試し、バックアップ/復元がどう簡単になるか確認する。  
- Forgejo連携は「modules/git を libgit2+Postgres に置換」する方針が現実的。まずは参照や簡易クエリに置き換えて段階的移行を。  
- ストレージ戦略を早めに決める：大きなバイナリはLFS/外部ストレージ、定期再パックで運用コストを抑える。  
- DB機能を活用：NOTIFYで即時反映、RLSでリポジトリ隔離、論理レプリケーションで部分的ミラーを検討する。

短所（ストレージ効率／サーバ側のupload/receive-pack実装）がある一方で、運用の単純化とアプリ連携の利便性は魅力的。小さなセルフホスト群を増やしたい日本のコミュニティ運用には特に刺さる提案です。
