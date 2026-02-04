---
layout: post
title: "A programmer's guide to leaving GitHub - GitHubを離れるプログラマ向けガイド"
date: 2026-02-04T03:00:47.154Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://lord.io/leaving-github/"
source_title: "A Programmer&#x27;s Guide to Leaving GitHub &ndash; Lord.io"
source_id: 46880807
excerpt: "個人開発者向けにGitHub移行の実践手順、代替サービス比較とボイコット戦略を簡潔解説"
---

# A programmer's guide to leaving GitHub - GitHubを離れるプログラマ向けガイド
GitHubをやめるなら知っておきたい、本当に使える移行の考え方と最短ルート

## 要約
個人開発者がGitHubから離れる理由（倫理的・技術的・戦略的）を整理し、実際に移行する際の選択肢と手順、効果的なボイコット戦略を初心者向けにわかりやすく解説します。

## この記事を読むべき理由
MicrosoftやGitHubへの抗議運動が世界的に広がる中、個人でも「コードホスティングを変える」ことで参加できる。日本の個人開発者や小規模チームにとっては、影響が小さく実行可能なアクションだからです。

## 詳細解説
- 背景と主張の要点  
  海外では「Give Up GitHub（2022〜）」「Free Software Foundation」「BDS」など、契約やAI学習データ、軍事/移民機関との関係を問題視する動きが強まっています。著者は個人的な抗議と連動して、公開リポジトリを別ホストに移すことを選びました。

- GitHubをターゲットにする理由  
  1) 個人プロジェクトなら移行の摩擦が小さい（社内モノレポや巨大依存がなければ容易）。  
  2) 無料で公開することでGitHubに価値を提供している（視認性＝ブランド価値）。  
  3) 最近のUI/運用面の不満（遅延・Actions運用の不安定さなど）。  
  4) ハッカー文化や倫理的理由で移行の共感が得やすい。

- 代替プラットフォームの分類と特徴（要点）  
  - Centrally hosted（セルフホスト可）: Codeberg/Forgejo（GPL、FOSS寄り）、Gitea（軽量）、GitLab CE（機能豊富だが重い）  
  - Decentralized / Federated: Radicle（分散、自己ホスト推奨）、Tangled（パッチベース、ATProtocol系）  
  - Self-hosted only: Gerrit（レビュー重視）、Gogs（軽量）  
  - 著者の例: 小規模ならS3をGitリモートにする軽量ツール（j3のような自作ツール）も選択肢になる

- ブランチベース vs パッチベース  
  GitHubのPull Requestは「ブランチベース」。Gerrit系やpatch-basedツールは「commitを上書きして差分を積む」ワークフローで、積み重ね（stacking）や履歴管理の利点があります。好みとチームワークフローで選ぶべき。

- ボイコットの戦略的ヒント  
  ターゲットを絞る／代替を使いやすくする／複数ムーブメントと連携／具体的で達成可能な目標を掲げる／公に理由を示す（安全な範囲で）／完璧主義を捨て段階的に移行。

## 実践ポイント
- まずは小さな個人プロジェクトから試す。影響が少なく回復も簡単。  
- 代替サービス候補：Codeberg（Forgejo）、SourceHut、Gitea、GitLab CE、Radicle、Gerrit。用途（公開・私用・レビュー重視）で選ぶ。  
- 移行の流れ（例）: GitHub CLIで認証 → ローカルにクローン → 新ホストにpush → 公開リポジトリはREADMEで移行理由を説明。  
  ```bash
  # bash
  brew install gh
  gh auth login
  mkdir -p migrate archive private
  # 各リポジトリを手動/スクリプトでクローン → 新ホストへ push
  ```
- 公に理由を書いておく（README更新など）：単なる削除より影響が大きい。  
- 完璧を目指さない：必要なら引き続きGitHubで貢献を続けつつ段階的に移行する。  
- CI/CDや外部連携（Actions、Pages等）は代替で差異が出るので事前に確認・代替策（GitLab CI、SourceHutのCI、独自ランナー等）を用意する。

短期間でできるアクションは多く、個人レベルでも「声」としての意味があります。まずは一つ、小さなリポジトリを別ホストに移してみてください。
