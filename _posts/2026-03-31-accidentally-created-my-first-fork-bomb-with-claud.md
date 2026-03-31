---
layout: post
title: "Accidentally created my first fork bomb with Claude Code - Claude Codeで初めてフォークボムを作ってしまった"
date: 2026-03-31T18:25:30.589Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.droppedasbaby.com/posts/2602-01/"
source_title: "February 2026 P1: $3800 Claude API Bill and a Fork Bomb | droppedasbaby - engineering blog | home of swe word vomit"
source_id: 47583959
excerpt: "Claude Codeのフック誤設定でプロセス爆発、夜間に$3,800請求とシステム停止。"
---

# Accidentally created my first fork bomb with Claude Code - Claude Codeで初めてフォークボムを作ってしまった
API請求が$3,800に膨らんだ夜：AIローカルツールが“フォークボム”を生んだ話

## 要約
ローカルで動かしていたClaude Code（CC）のフックがプロセスを指数的に増やす設定になっており、夜間に大量インスタンスが立ち上がってマシンを事実上ブリック化。高負荷とAPI利用の爆発で請求が膨らんだが、その過程で実用的なツール群も生まれたという体験記。

## この記事を読むべき理由
AIエージェントやローカルでのLLM運用を始める日本のエンジニアにとって、設定ミスがシステム／コスト両面で致命的になる実例と、そこから得られた実践的対策が参考になるため。

## 詳細解説
- 問題の発端  
  セッション開始用のHook（SessionStart）が、バックグラウンドでclaudeコマンドを2つ生成するよう設定されていた。各インスタンスがさらに同じHookを起動する設計ミスにより、プロセス数が指数関数的に増加（1→2→4→8…）してメモリ圧迫、熱暴走、最終的にシステムが応答不能に。

- 実機影響とコスト  
  単一マシン上での大量インスタンスによるメモリ使用とTUIチェーン（Bun→React→TUIなど）の重さでロック。API利用は社内課金で計測され、短期間に数百〜数千ドル相当の請求増を確認。

- 背景技術  
  - Claude Code（CC）はCLIベースでフックやスキルを登録できる。スキルは外部ツール呼び出しやスクリーンショットOCRなどを自動化するため、誤設定で外部プロセスを多重に起動しやすい。  
  - 「agentic」ワークフロー（自律的にツールや外部APIを呼ぶ仕組み）は便利だが、ループや自己複製的動作の危険をはらむ。

- 著者が作った主なツール（要旨）  
  - /yadumb: 問題発生時の動作ログを残す。  
  - /memento: 会話やコンテキストのスナップショット保存。  
  - /yablind: 画像やPDFから必要情報だけ抽出してコンテキストを節約。  
  - /adhd: 各種サービスから今日のタスクを集約・優先化。  
  - /money: プロジェクトごとの状態保存と復元。  
  - PreToolUse/PostToolUseフック: ツール呼び出しの記録をappend-onlyで保存。

## 実践ポイント
- フック・自動化を有効にする前に「ドライラン」と「最大同時実行数」を確認する。  
- 開発環境はホスト直上ではなくVM／コンテナで実行してサンドボックス化する。  
- ulimit / cgroups / systemd Slice 等でプロセス数・メモリ上限を設定する。  
- APIキーの請求上限（quota）とアラートを設定し、使用量のデイリー監視を有効化する。  
- フックやスキルは最小権限で、明示的なKillスイッチ（緊急停止フラグ）を用意する。  
- ログは軽量なappend-only形式でローカル保存し、必要なメタだけを収集して解析コストを抑える。  
- 組織の課金ルールを事前に確認し、実験的な大量トークン使用は許可を得るか個人負担で行う。

短いまとめ：自律型AIの便利さは大きいが、ループや並列起動の危険を常に疑い、サンドボックス化・上限設定・請求監視を徹底すること。
