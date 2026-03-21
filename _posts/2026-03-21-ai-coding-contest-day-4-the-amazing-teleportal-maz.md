---
layout: post
title: "AI coding contest day 4: The Amazing Teleportal Maze. Three bots eliminated. Two survived. Claude won. - Day 4: 驚異のテレポータ迷路。3体脱落、2体生存、勝者はClaude"
date: 2026-03-21T22:56:08.518Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://boreal.social/post/ai-coding-contest-day-4-the-amazing-teleportal-maze-three"
source_title: "AI coding contest day 4: The Amazing Teleportal Maze. Three bots eliminated. Two survived. Claude won. — boreal.social"
source_id: 418618139
excerpt: "視界5×5のテレポータ迷路でClaudeが示した即時ワープ活用術とI/O落とし穴を覗く"
image: "https://boreal.social/static/og_images/516357ff54884132aa3dc2ac2d4f6de4.png"
---

# AI coding contest day 4: The Amazing Teleportal Maze. Three bots eliminated. Two survived. Claude won. - Day 4: 驚異のテレポータ迷路。3体脱落、2体生存、勝者はClaude
驚愕の「見えない迷路」でAIが勝負 — Claudeが示した“近道を知る”戦略とは？

## 要約
5×5の視界しかない迷路にテレポータ（ワープ）が混在する対戦で、Claudeが80%のラウンドを制覇。鍵は「ポータル情報の即時解決」と「出口方向への探索バイアス」だった。

## この記事を読むべき理由
不完全情報下での探索・経路計画はロボット工学やゲームAIだけでなく、実運用システムの設計にも通じる。日本のエンジニアが学べる実践的な設計原則が詰まっている。

## 詳細解説
- ルール概観：各ボットは自分位置を中心とした5×5の“霧”のみを観測し、マップ全体は不明。テレポータは文字で表示され、出口は左上とは限らず遠方にある。500ステップ超で失格。
- 実行環境：同一マシン（localhost:7474）で各ボットが接続し、100ラウンド実行。
- 成績概略：Claudeが圧倒（約80%勝利）、Grokが残存して性能は良いが大迷路で非効率。他ボットは接続切れやタイムアウトで早期脱落。
- 主な失敗原因
  - I/Oの扱いミス：受信テキストの末尾や行の空白を.strip()などで削ると、5×5ビュー中の空白（通路情報）が消え、パーサが壊れて接続断になる（MiMo／Gemini類似トラブル）。
  - プロトコル誤解釈：ビュー行がコマンドと誤認されると状態が同期不能になり脱落。
  - 計算時間切れ：毎手で全グラフに対して完全なBFSや重い処理を行うと、盤面が大きくなると1秒制限に抵触（ChatGPTの例）。
- 戦略差の核心
  - Grok：近接の「未知セル」へBFSで探索→出口発見後は出口へBFS。ポータルは視認した文字の一致でリンクするため、両端を直接見ないと使えない→遠隔ワープの活用が遅れる。
  - Claude：優先順位（1.出口が見えるなら直行、2.出口方向へバイアスしたフロンティア探索、3.未解決のポータルへ踏む）を持つ。重要なのは、テレポートで到達先をサーバ応答（TELEPORT r c）から即座にマップに双方向で記録し、以降の経路探索でワープを即活用できる点。
  - これによりClaudeは「探索と活用（explore vs exploit）」を切り替え、遠隔ショートカットを素早く利用してステップ数を大幅に削減した。

## 実践ポイント
- I/O設計：観測データの空白や行末を安易にtrimしない。プロトコルは明示的にパーシングして同期を保つ。
- ポータル／ショートカットは即時記録：一度得たショートカット情報は双方向に反映して経路探索で使えるようにする。
- 探索方針に方向性を持たせる：単純な最短未知経路だけでなく、目的地方向へのバイアス（例：スコア = 路長 - α*(r+c)）を導入すると無駄探索を減らせる。
- 計算コストを管理：毎手で全体BFSをやるとスケールしない。増分探索（D* Lite等）や局所更新を検討する。
- 再現性：複数クライアントが同一環境で動く場合、ログとプロトコル仕様を厳密に残す。参考実装やデータは github.com/rrezel/llmcomp に公開されている。

この記事を読むことで、「不完全情報＋ショートカット」の設計で何を優先すべきかが明確になる。実装上の落とし穴（I/O、プロトコル、計算時間）もそのまま実務に応用可能。
