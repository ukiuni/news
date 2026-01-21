---
layout: post
title: "Show HN: yolo-cage – AI coding agents that can't exfiltrate secrets or merge their own PRs - yolo-cage：秘匿情報を流出させず自分でPRをマージしないAIエージェント"
date: 2026-01-21T16:42:45.174Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/borenstein/yolo-cage"
source_title: "GitHub - borenstein/yolo-cage: AI coding agents that can&#39;t exfiltrate secrets or merge their own PRs."
source_id: 46706796
excerpt: "ローカルでブランチ毎に隔離しAIの秘匿漏洩と自己マージを技術的に防ぐツール"
image: "https://opengraph.githubassets.com/34193e2e10d2a2e5c742ec874ca2dfae1754515e32a830199505c41bdec6ceed/borenstein/yolo-cage"
---

# Show HN: yolo-cage – AI coding agents that can't exfiltrate secrets or merge their own PRs - yolo-cage：秘匿情報を流出させず自分でPRをマージしないAIエージェント

魅力的なタイトル: AIに「自由にさせつつ被害を最小化」する実験的サンドボックス—疲れたエンジニアの判断疲労を救うyolo-cage

## 要約
yolo-cageは、AIコード作成エージェント（例：Claude Code）にローカルで自由にコードを書かせつつ、シークレット流出や自己マージなど危険な操作を技術的にブロックする「ブランチ毎サンドボックス」ツールです。エグレスプロキシとdispatcherでHTTP/Git操作をフィルタリングします。

## この記事を読むべき理由
AIが開発作業に関わる場面が増える日本の現場で、ヒューマンエラー（判断疲労）を減らしつつ危険を制限する実践的な手法が学べます。社内リポジトリでAIを試すときの安全設計の参考になります。

## 詳細解説
- 基本コンセプト：エージェントに自由度（YOLOモード）を与える代わりに、影響範囲を「ブランチ単位のサンドボックス」に限定。最終的な変更はPRで人間がレビューしてマージする運用を想定。  
- アーキテクチャ：
  - Vagrant VM（MicroK8s）上に各ブランチ用のPodを作成。1ブランチ＝1サンドボックス。
  - Dispatcherがgit/ghコマンドを仲介し、許可されたブランチ以外へのpushや危険なghコマンドをブロック。
  - EgressプロキシがHTTP/Sを監視し、リクエスト本文・ヘッダ・URLをスキャンしてシークレットパターン（例：sk-ant-*, AKIA*, ghp_*, SSH鍵）や外部exfiltrationサイト（pastebin.com, file.io, transfer.sh等）をブロック。
  - TruffleHog等でpre-pushシークレット検査を行う。
- ブロック対象（例）：
  - Git操作：sandbox外へのpush、git credential操作の抑止
  - GitHub CLI/API：`gh pr merge`, `gh repo delete`, `gh api` や API のマージ・削除エンドポイントを遮断
  - HTTPエグレス：特定ドメイン・パターン・シークレット表現の遮断
- 前提要件：Vagrant＋libvirt（Linux）/QEMU（macOS）・8GB RAM・4CPU・GitHub PAT（repoスコープ）・Claudeアカウント 等
- 制限事項：DNSを使ったデータ化けこみ、タイミング副チャネル、画像ステガノ、巧妙な符号化などは防げない。生産用シークレットは使わない運用が必須。

## 実践ポイント
- まずローカルで試す（要件満たしていることを確認）：  
```bash
# bash
curl -fsSL https://github.com/borenstein/yolo-cage/releases/latest/download/yolo-cage -o yolo-cage
chmod +x yolo-cage && sudo mv yolo-cage /usr/local/bin/
yolo-cage build --interactive --up
yolo-cage create feature-branch
yolo-cage attach feature-branch
```
- 運用設計例：AIにはfeatureブランチで自由に作業させ、必ず人がPRレビューでマージするワークフローにする。  
- セキュリティ設定：エグレスのドメインブロックリストとシークレット検出ルールをプロジェクトごとに調整。スコープを限定したクレデンシャルを使用する。  
- テスト：Security Audit手順に沿ってescapeテスト（DNS漏洩やタイミング攻撃など想定パターン）を実施。  
- 日本の現場での活用案：オフライン環境や社外秘の多いプロジェクトではまずステージングで導入し、ポリシー成熟度に応じて範囲を拡大する。

以上。興味があれば公式READMEとSecurity Auditを参照して導入検討を。
