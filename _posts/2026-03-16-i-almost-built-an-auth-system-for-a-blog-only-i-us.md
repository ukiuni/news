---
layout: post
title: "I almost built an auth system for a blog only I use - ブログを自分だけが使うための認証システムをほぼ作った話"
date: 2026-03-16T11:25:33.917Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://thobiasn.dev/posts/a-pragmatic-blog"
source_title: "A Pragmatic Blog - thobiasn.dev"
source_id: 382552861
excerpt: "公開リポを活かしgit＋git-crypt＋SQLite＋Goで認証ゼロの個人ブログ運用術"
---

# I almost built an auth system for a blog only I use - ブログを自分だけが使うための認証システムをほぼ作った話
認証ゼロでOKなブログ運営術：シンプルさを貫いたら全部うまくいった話

## 要約
著者は個人ブログを最小限の複雑さで実装し、認証やPostgresを廃してMarkdown＋git＋git-crypt＋SQLite＋Go単一バイナリで必要機能を満たした。

## この記事を読むべき理由
日本でも「将来に備えて最初からスケール設計」をやりがちだが、小規模用途では逆に手間と技術負傈を招く。個人開発や起業初期のプロダクト設計で「いま必要な最小構成」を学べる。

## 詳細解説
- 基本方針：公開リポジトリを基盤に、コンテンツはMarkdownファイルで管理（gitで自動バックアップ）。データベースや重たい認証は避ける。  
- プライベート投稿：リポジトリは公開のまま、content/private/ 配下を git-crypt で自動暗号化。git の clean/smudge フィルタでコミット時に暗号化され、ホスティング側には平文が残らない。新しいマシンでは鍵を設定して git-crypt unlock するだけで復号される。  
  例：
  ```bash
  git-crypt unlock
  ```
- 管理周り：購読者・コメント等の管理は SQLite（ファイル）でシンプルに保持。フルウェブの管理画面やセッション周りは作らず、CLIツールで管理。APIキーを.envで渡して認証を最小化する。  
  .env例：
  ```env
  BLOG_URL=https://thobiasn.dev
  ADMIN_API_KEY=thats_pretty_neat
  ```
- 実装技術：Goで単一バイナリ（小メモリ、Docker化しやすい）。サーバーサイドでHTMLを出力し、ページは軽量（<50KB）。コード量も小さく保たれている（記事時点で <2000行のGo）。
- メリット：運用コスト低、バックアップ自動、寄稿やレビューがしやすい（公開リポジトリの利点を維持）、認証攻撃面の縮小、ローカル編集はGitHubエディタで可能。

## 実践ポイント
- まずはMarkdownで書く：投稿数が少ないならDB不要。gitに全て委ねる。  
- プライベートな下書きは git-crypt で暗号化して公開リポジトリを活かす。  
- 管理用は軽量DB（SQLite）＋CLIで済ませる：認証やセッション実装を避けられる。  
- Goの単一バイナリで配布・デプロイを簡素化（Docker化も容易）。  
- .env に ADMIN_API_KEY を置き、簡易APIキー認証で管理操作を制限する。  
- 日本の開発現場でも「将来のための複雑さを先に入れない」判断は有効。まずは動くシンプルな仕組みで価値を出すことを優先する。
