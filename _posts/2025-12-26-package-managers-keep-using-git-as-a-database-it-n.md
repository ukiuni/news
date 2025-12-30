---
layout: post
title: Package managers keep using git as a database, it never works out - パッケージマネージャーがgitをデータベースとして使い続けているが、決してうまくいかない
date: 2025-12-26 03:58:16.567000+00:00
categories:
- tech
- world-news
tags:
- tech-news
- japan
source_url: https://nesbitt.io/2025/12/24/package-managers-keep-using-git-as-a-database.html
source_title: Package managers keep using git as a database, it never works out |
  Andrew Nesbitt
source_id: 1374378779
---
# Package managers keep using git as a database, it never works out - パッケージマネージャーがgitをデータベースとして使い続けているが、決してうまくいかない

## 要約
多くのパッケージマネージャがメタデータをgitリポジトリで配布し続けるが、履歴肥大やCIでの毎回クローンといった現実的コストで必ず問題化する。各プロジェクトが採った回避策と、そのトレードオフを整理する。

## この記事を読むべき理由
国内の開発現場でもCIの遅延、ディスク肥大、ネットワークコストは無視できない。どのような対策が現実的か（設定変更、CDN/HTTP切替、キャッシュ戦略、リポジトリ運用）を短く具体的に示す。

## 詳細解説
- 問題の本質  
  gitは履歴管理に優れるが「完全複製（clone + delta resolution）」を前提とするため、履歴が増えるとクローンやフェッチが重くなり、特にCIやステートレス環境で毎回フル取得する運用は致命的になる。さらに“shallow clone”はサーバ側の計算負荷を増やし、レート制限やCPU負荷を招く。

- Cargo（crates.io）  
  旧来のgitインデックスは履歴が増大してlibgit2のdelta解決が長時間化。RFC 2789の「sparse HTTP」へ移行し、必要なメタデータだけHTTPSで取得する方式へ。結果として多数のユーザーがインデックス全体を触らなくなった。

- Homebrew  
  homebrew-core の.gitが巨大化し、shallow/unshallow操作が極めて重い。JSONベースのtap更新に切り替えてHTTPで差分を配信、更新頻度も下げることでユーザー体験を改善。

- CocoaPods  
  Specsリポジトリの深いツリーと多数のpodspecでクローン/更新が長時間化。GitHub側の負荷も問題となり、最終的にCDN経由のHTTP配信をデフォルトにして高速化・ディスク節約を実現。

- Nixpkgs  
  リポジトリ自体がパッケージ定義（コード）でありCDN化が難しいため、巨大なgitリポジトリがそのまま問題に。GitHub上のfork/PR処理やCIのマージコミット生成がインフラに負荷をかけるケースが発生。

- vcpkg  
  ポートをgitツリーのハッシュで参照する設計のため完全な履歴が必要。GitHub ActionsやDevContainersのデフォルトで入るshallow cloneが原因で「shallow repo」で失敗する。対応はフルクローンを要求するか、ローカルに完全履歴を保持する運用しかないケースが多い。

- 共通するトレードオフ  
  gitをやめてHTTP/CDNやJSONインデックスに移すと配信コストは下がるが、PRや分散コラボレーションといったgit由来のワークフローを失ったり、署名・信頼性の保証（誰がいつ何を変えたか）を別実装する必要がある。

## 実践ポイント
- まず自分のプロジェクト/CIで使うパッケージマネージャがインデックスをgitで配っているか確認する。  
- Cargoを使うならクライアントを最新にし、sparse HTTP（オンデマンド取得）が有効になっているか確認する。  
- vcpkg等でツリーハッシュを参照する設計なら、CIでフルクローンを行うか、ポートをベンダリングして履歴依存を無くす。  
- HomebrewやCocoaPodsのようにHTTP/CDN配信が可能なら切替を検討する（社内ミラー／CDN導入）。  
- CIのワークフローを見直し、インデックスの毎回フル取得を避ける。キャッシュ（ワークスペース、artifact）、長期的なエージェント（stateful runner）導入を検討する。  
- Nixのようにgitリポジトリ自体がソースである場合はバイナリキャッシュの活用と、リポジトリ運用（PR/CI頻度の見直し）を検討する。  
- 企業内での対策：プライベートレジストリ／プロキシ（Verdaccio, Artifactory等）やミラーを立て、帯域とGitHub API制限を回避する。

