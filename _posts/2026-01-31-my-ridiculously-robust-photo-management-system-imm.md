---
layout: post
title: "My Ridiculously Robust Photo Management System (Immich Edition) - 私のとんでもなく堅牢な写真管理システム（Immich版）"
date: 2026-01-31T10:38:15.893Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://jaisenmathai.com/articles/my-ridiculously-robust-photo-management-system-immich-edition/"
source_title: "My Ridiculously Robust Photo Management System (Immich Edition) &#8211; Jaisen Mathai"
source_id: 46794971
excerpt: "EXIFを正典化しImmichとNASでGoogle依存を断つ堅牢な写真管理術"
image: "https://jaisenmathai.com/images/main-photo-workflow-immich.png?1"
---

# My Ridiculously Robust Photo Management System (Immich Edition) - 私のとんでもなく堅牢な写真管理システム（Immich版）
EXIFだけで未来保証する写真管理術 — ImmichでGoogle依存から脱却し、自前NASと共存させるリアルなワークフロー

## 要約
作者は「EXIFにすべてのメタデータを埋める」方針を保ったまま、Immichを単なるビューアから完全な整理ツールに拡張し、Synology NAS/Dropboxへ自動バックアップする堅牢な写真管理を作った。

## この記事を読むべき理由
日本でも家庭や小規模オフィスでNASを使う人は多く、プライバシーや将来性を考えると「クラウド依存を減らしつつ豊かな閲覧体験を得る」手法は実用的で魅力的だからです。

## 詳細解説
- 中心思想：写真メタデータ（説明、位置、日時、アルバム、お気に入り等）を外部DBではなく、写真ファイル内のEXIFに直接保存する。これにより将来の互換性と自己完結性を確保する。  
- 元ツール：作者は長年の整理ツール「Elodie」を使い、これがファイルシステム上にEXIFベースの“正準ライブラリ”を作る役割を担う。  
- Immich導入のポイント：Immichは外部ライブラリ（既存フォルダを読み込む機能）を「読み取り専用」でマウントできるため、既存のNASライブラリを参照しつつビューアとして使える。作者はこの機能を起点に、Immichを編集可能なワークフローへ拡張した。  
- 技術的障害と解決法：
  - ImmichはデフォルトでメタデータをPostgresに保存し、XMPサイドカーも扱えるが、オリジナルファイルを書き換えない設計。作者はEXIFを書き換えるプラグイン（immich-exif）を作り、写真ファイル自身に変更を埋め込む方式を採用した。
  - Elodieがアルバム追加でファイルを移動すると、Immich側では「削除＋新規作成」と解釈される問題が発生。作者は「最終的整合性（eventual consistency）」を前提に同期ロジックを組み、変更がやがて収束する仕組みで解決した。
- 補足：ImmichのAPIは柔軟で拡張しやすく、細かな同期戦略や差分検出を組めば安定運用が可能。詳細はGitHubの関連Issue（例：#496）や作者のコードを参照すると良い。

## 実践ポイント
- まずはバックアップを確保：変更前にNAS/Dropboxへフルバックアップを取る。  
- Elodieでファイル名／EXIF中心の整理を習慣化する（コマンドラインで自動化可）。  
- Immichは「外部ライブラリを読み取り専用でマウント」して動作確認。変更を反映させたい場合は immich-exif のようなEXIF書込プラグインを検討。  
- ファイル移動→同期の競合を避けるため「最終的整合性」を想定したリトライ／ログ監視を実装する。  
- 小規模ならSynology + Immich + ローカルバックアップの組合せでコスト低くプライベートな写真体験が作れる。  

興味がある方は immich-exif や該当GitHub issue（例：#496）を追うと、実装コードや最新議論が確認できます。
