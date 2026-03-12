---
layout: post
title: "Show HN: We analyzed 1,573 Claude Code sessions to see how AI agents work - Show HN: 1,573件のClaude Codeセッションを分析してAIエージェントの動きを調べた"
date: 2026-03-12T14:36:25.953Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/obsessiondb/rudel"
source_title: "GitHub - obsessiondb/rudel: Claude Code Session Analytics · GitHub"
source_id: 47350416
excerpt: "1,573件のセッション解析でAIエージェントの挙動と漏洩リスクをダッシュボードで可視化"
image: "https://opengraph.githubassets.com/029af8d06439f5b51995d4f7cf1e6163ef35a774d49cd33d7ab2a697a344af16/obsessiondb/rudel"
---

# Show HN: We analyzed 1,573 Claude Code sessions to see how AI agents work - Show HN: 1,573件のClaude Codeセッションを分析してAIエージェントの動きを調べた
実データで見えてきた「AIコード補助」の使われ方と落とし穴 — Rudelで可視化する開発現場の本当

## 要約
RudelはClaude Codeのセッションを自動収集して、トークン利用・セッション時間・モデル/サブエージェントの利用傾向などを可視化するツールです。1,573件の実セッション解析を通じ、AIエージェントの実務での振る舞いやリスクが明らかになります。

## この記事を読むべき理由
日本の開発現場でもAIペアプログラミングが普及しつつある今、利用実態の可視化はコスト管理・品質向上・情報流出防止に直結します。Rudelはその第一歩を手軽に提供します。

## 詳細解説
- 何をするか：RudelはClaude Codeのセッション終了時にトランスクリプトやメタデータをアップロードし、ClickHouseに保存して解析ダッシュボードを生成します。ダッシュボードはトークン使用量、セッション長、モデルやサブエージェントの利用頻度、リポジトリ／ブランチなどのコンテキストを表示します。
- 収集データ：セッションID・タイムスタンプ・ユーザ/組織ID・プロジェクトパス・Gitコンテキスト（リポジトリ/ブランチ/コミットSHA）・完全なプロンプトと応答（トランスクリプト）・サブエージェント利用情報 等。
- 導入方法：bunランタイムが前提。CLIは npm install -g rudel。rudel login → rudel enable（セッション終了時に自動アップロード）で即運用可能。過去セッションは rudel upload で一括登録。
- 開発・運用：OSS（MIT）で自己ホスティング可能。docs/self-hosting.md に手順あり。セキュリティ報告や貢献ガイドもリポジトリに用意されています。
- リスク：トランスクリプトにはソースコード、コマンド出力、URL、場合によってはシークレットが含まれる可能性があり、アップロード対象を厳選する必要があります。ホスト型（app.rudel.ai）／セルフホストの選択は社内ポリシー次第。

## 実践ポイント
- まず試す：rudel.aiのホスト版でダッシュボードを確認し、開発チームの利用傾向を把握する。  
- 導入コマンド（手早く試す）：
  - npm install -g rudel
  - rudel login
  - rudel enable
  - rudel upload（過去ログ）
- プライバシー対策：機密プロジェクトではアップロードを無効化、または自己ホスティングを検討する。  
- 運用ルール：AI利用のスコープ、シークレット管理、トークン使用上限をポリシー化してコストと漏洩リスクを抑える。  
- 日本企業向け：社内規定や個人情報保護法を踏まえ、SaaS利用前に法務・情報セキュリティと調整すること。

Rudelは「何が起きているか」を見える化してくれるツールです。まずは非機密プロジェクトで試用し、運用方針を整えてから拡大するのがおすすめです。
