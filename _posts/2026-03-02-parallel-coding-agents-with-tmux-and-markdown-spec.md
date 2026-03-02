---
layout: post
title: "Parallel coding agents with tmux and Markdown specs - tmuxとMarkdownスペックで並列コーディングエージェントを動かす"
date: 2026-03-02T17:38:37.778Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://schipper.ai/posts/parallel-coding-agents/"
source_title: "How I run 4–8 parallel coding agents with tmux and Markdown specs — Manuel Schipper"
source_id: 47218318
excerpt: "tmuxとMarkdownでFDを使いLLMエージェントを4〜8並列で設計・実装・検証する実践手法"
---

# Parallel coding agents with tmux and Markdown specs - tmuxとMarkdownスペックで並列コーディングエージェントを動かす
tmuxとMarkdownで「設計書を中心」に4〜8体のコーディングエージェントを同時運用する実戦ガイド

## 要約
tmuxとMarkdownベースの「Feature Design（FD）」仕様＋6つのスラッシュコマンドで、LLMエージェントをPlanner/Worker/PMに分担させ、4〜8並列で効率的に開発を回す手法の紹介。

## この記事を読むべき理由
日本の開発現場でも、LLMを使った並列開発は効率化の鍵。軽量で移植しやすいセットアップなので、既存リポジトリやチームにも短期間で導入できる点が有益です。

## 詳細解説
- 基本構成
  - tmuxでウィンドウごとに役割を固定（Planner / Worker / PM）。Ctrl-bでウィンドウ操作、色変化でエージェントのアイドル通知を受け取る。
  - すべての設計はMarkdownのFD（Feature Design）ファイルで管理：問題定義、検討した案（メリット/デメリット）、最終案と実装計画、検証手順を含む。
  - FDは docs/features/ に番号付きで保存（FD-001 …）し、FEATURE_INDEX.mdでライフサイクルを追跡。
- FDのライフサイクル（代表的なステージ）
  - Planned → Design → Open → In Progress → Pending Verification → Complete → Deferred → Closed
- 運用コマンド（スラッシュコマンド）
  - /fd-new：新規FD作成（アイデアダンプから）
  - /fd-status：インデックス表示（何が進行中か）
  - /fd-explore：プロジェクト文脈を読み込み（アーキ・ガイド・過去FDを供給）
  - /fd-deep：並列で複数エージェントを走らせて難問を多角的に探索
  - /fd-verify：コード校閲→検証計画→コミット
  - /fd-close：FDをアーカイブしてインデックス・CHANGELOGを更新
- 実装のコツ
  - ほとんどの実装は"完成したFD"から始める。WorkerはFDの行レベル実装計画に従ってコミットを積む（FD番号をコミットメッセージに紐付ける）。
  - 複雑案件は /fd-deep で4つ程度の視点（アルゴリズム・構造・インクリメンタル等）を同時に試す。
  - 検証は自動化。エージェントにライブデータで実行させ、結果をMarkdownで診断・記録させる。
- 運用の現実
  - 実用上の並列数は4〜8。8を超えると人間側の追跡が困難になり品質が落ちる。
  - CLAUDE.md的な「開発ガイド」を別ファイル化して要約を最初に読ませ、詳細は参照可能にする（無駄なコンテキスト消費を抑える）。
  - tmuxのベル監視やパス短縮エイリアスで快適性を上げる。

## 実践ポイント
- まず /fd-init をリポジトリで一回実行し、docs/features/とテンプレを自動生成する。
- 最初のFDを /fd-new で作り、/fd-explore → Plannerで設計 → Workerで実装 → /fd-verify → /fd-close の流れを1回完走させる。
- 並列は段階的に増やす：2→4→6で安定性を確認し、最大8を上限に運用する。
- FDは「意思決定の証跡」になるので必ず問題／検討案／最終案／検証手順を明記する。
- 日本の現場向け：CI/テスト基盤やコードレビュー規約、コンプライアンス要件（ログ、監査）をFDテンプレに必須項目として入れておく。

短時間で導入でき、設計の可視化と並列エージェントの効率的運用に役立つ手法です。興味があれば、あなたのプロジェクト用にFDテンプレやtmux設定の簡易チェックリストを作成しますか？
