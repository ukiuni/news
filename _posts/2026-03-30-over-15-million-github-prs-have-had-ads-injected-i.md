---
layout: post
title: "Over 1.5 million GitHub PRs have had ads injected into them by Copilot - 150万件以上のGitHubプルリクにCopilotが広告を挿入"
date: 2026-03-30T15:31:39.815Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.neowin.net/news/microsoft-copilot-is-now-injecting-ads-into-pull-requests-on-github-gitlab/"
source_title: "\"Over 1.5 million GitHub PRs have had ads injected into them by Copilot\""
source_id: 47575212
excerpt: "Copilotが150万件超のPRに隠しHTMLで広告を挿入、要点検"
---

# Over 1.5 million GitHub PRs have had ads injected into them by Copilot - 150万件以上のGitHubプルリクにCopilotが広告を挿入
あなたのプルリクにも広告が混入？CopilotがPR説明を自動編集して“プロモーション”を差し込んでいる問題

## 要約
MicrosoftのCopilotがPull Requestの説明欄に広告的な「チップ」を自動挿入しており、調査では150万件以上のPRで確認されている。隠しHTMLコメント（"START COPILOT CODING AGENT TIPS"）を使って挿入している痕跡がある。

## この記事を読むべき理由
GitHub/GitLabを使う日本の開発チームにとって、PRの信頼性・ドキュメント整合性・社内コンプライアンスに直接関係します。自動化されたAIツールが開発フローの可視性に介入する現実を知っておく必要があります。

## 詳細解説
- 何が起きているか：Copilot（および関連拡張）がPRの説明を修正する過程で、Raycastなどのパートナー機能や「Copilot coding agent」を紹介する文言を差し込んでいる事例が多数報告されています。  
- 技術的な痕跡：挿入箇所の直前に隠しHTMLコメント "START COPILOT CODING AGENT TIPS" があり、プログラム的にヒントを差し込んでいることが示唆されます。Markdownの生データを確認すると発見しやすいです。  
- 範囲：GitHubだけでなくGitLabのマージリクエストでも類似の挙動が観測され、影響は幅広く見積もられています。  
- 背景：大規模AI運用のコストを広告などで補填する流れの一端で、既に他社（例：OpenAI）の広告展開成功例が参考にされています。  
- リスク：誤情報や無関係な宣伝がPRに入ると、コードレビューの信頼低下、コンプライアンス違反（社外プロモーションの無断掲載）、自動化フローの破壊などを招く可能性があります。

## 実践ポイント
- PRの生データ（Raw/Markdown）を確認し、隠しコメントが無いかチェックする。検索例：
```bash
# リポジトリ直下で隠しコメントを検索
grep -R "<!-- START COPILOT CODING AGENT TIPS" .
```
- チームでルール化：PRテンプレートやCIで説明欄の検査（不審なHTMLコメントや外部リンクの自動検出）を組み込む。  
- エディタ/拡張の設定確認：CopilotやRaycast等の拡張が自動でPRを編集する設定を無効化する。  
- 自動修正を受け入れないワークフロー：重要リポジトリはPR本文を手動レビューのみ許可するなどポリシーを適用。  
- 組織的対応：企業利用ならベンダーに問い合わせ、影響範囲と対策（契約・設定の見直し）を確認する。

短時間でできるチェックと、組織的なルール整備が当面の対処として有効です。
