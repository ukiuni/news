---
layout: post
title: "Faster, cheaper, messier: lessons from our switch to self-hosted GitHub Actions - 速く安く、だけど手間は増える：GitHub Actionsをセルフホストに切り替えた教訓"
date: 2026-02-04T15:59:09.331Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://theguardian.engineering/blog/faster-cheaper-messier-lessons-from-switch-to-self-hosted-github-actions?utm_source=insidestack&amp;utm_medium=social"
source_title: "The Guardian Engineering Blog - Faster, cheaper, messier: lessons from our switch to self-hosted GitHub Actions"
source_id: 409407782
excerpt: "余剰MacでActionsを自ホスト化し、月額削減とビルド高速化を実現も運用負荷が増"
---

# Faster, cheaper, messier: lessons from our switch to self-hosted GitHub Actions - 速く安く、だけど手間は増える：GitHub Actionsをセルフホストに切り替えた教訓

魅力的なタイトル: 「月額コストを削ってビルドを2倍速に？The Guardianが教える“社内MacでGitHub Actions”成功と落とし穴」

## 要約
The GuardianはmacOSビルドの高額＆遅延問題を解決するため、GitHubホストのランナーから社内の自前（自ホスト）ランナーに移行。速度とコストで大幅改善（ユニットテスト約50%速、アップロード約60%速、月額約£400削減）が得られた一方、メンテナンスや信頼性の運用負荷が増した。

## この記事を読むべき理由
日本でもiOSアプリ開発チームはmacOSランナーの時間課金で高コストに悩むことが多い。社内リソースでコスト・速度を改善できる実例と、移行時に避けるべき落とし穴が学べる。

## 詳細解説
- 背景：GitHubホストのmacOSランナーはLinuxより単価が高く（The Guardianは請求が突出）、さらにGitHub側のイメージ更新やアウトテージでビルドが遅延・タイムアウトするリスクがある。  
- なぜセルフホストか：余っていたMac Miniを利用して実験。自己管理でOSアップデートやデバッグが可能になり、外部依存の性能低下を回避できる。  
- セットアップ概要：GitHub公式のセルフホストランナー導入手順に従い、ランナーソフトをインストール→リポジトリ認証→ワークフローの実行先を変更。リモートアクセスも設定して物理的に触らずに運用。  
- 技術的トラブルと対策：  
  - 非エフェメラル環境（永続マシン）のためDerivedDataやビルドアーティファクトが残る→ジョブ毎に決まったDerivedData名／ポストジョブでのクリーンアップスクリプトを導入。  
  - キーチェーンや古いXcode・シミュレータの残存対策が必要。定期的な削除/整理を運用に組み込む。  
  - 同時実行数は物理CPUに依存（例：4並列設定でキューが発生）。より強力な1台を選ぶ方が管理効率が良いという教訓。  
- 成果と代償：ビルド時間が大幅改善、デバッグが容易、月額コスト削減（約£400）。ただしハードウェア保守、電源冗長性、物理再起動や監視など運用負荷が増加。

## 実践ポイント
- まずは小さなMac（余剰Mac Mini等）でPoCを行う。  
- GitHub公式手順でランナーを登録し、ワークフローのruns-onを切り替える。  
- ジョブ終了時にDerivedDataやキーチェーンを確実に消すポストジョブスクリプトを用意する。  
- ディスク容量／古いXcode・シミュレータを定期削除するジョブをスケジューリングする。  
- リモート管理（SSH、KVM、IPMI相当）と無停電電源を確保する。  
- コスト効果を見積もり、同時実行数とマシンスペックは「大きめ1台＞小分け複数台」を検討する。  

短く言うと：速さとコストは手に入るが、運用の「手間」を引き受ける覚悟が必要。iOS開発チームなら試す価値あり。
