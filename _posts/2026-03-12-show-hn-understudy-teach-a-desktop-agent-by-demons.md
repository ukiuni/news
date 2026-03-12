---
layout: post
title: "Show HN: Understudy – Teach a desktop agent by demonstrating a task once - デスクトップエージェントに一度のデモで教える Understudy"
date: 2026-03-12T18:57:48.458Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/understudy-ai/understudy"
source_title: "GitHub - understudy-ai/understudy: An understudy watches. Then performs. · GitHub"
source_id: 47353957
excerpt: "一度の画面デモでルーチン作業を自動化するmacOS向けAIエージェント"
image: "https://opengraph.githubassets.com/54489075d38232f69a04865b6ad26d6a1e5a5c977f93874568142c0f18f24083/understudy-ai/understudy"
---

# Show HN: Understudy – Teach a desktop agent by demonstrating a task once - デスクトップエージェントに一度のデモで教える Understudy
魅力的なタイトル: 「一度見せるだけで仕事を覚えるAI同僚—Understudyが“デスクトップを代行”する日」

## 要約
Understudyは画面操作・ブラウザ・シェル・メッセージングを横断して“人のやり方を見て学ぶ”デスクトップエージェントです。一度デモを見せるだけで意図を抽出し、繰り返しタスクを自動化します（現状は macOS とレイヤー1〜2が実用化済み）。

## この記事を読むべき理由
日本の職場では複数のツール（ブラウザ、Slack/LINE、業務アプリ、スクリプト）が散在し、単純作業が残りやすいです。UnderstudyはAPI連携や複雑なワークフロー作成なしに“画面で教えるだけ”でルーチンを自動化できるため、現場の生産性改善に直結します。

## 詳細解説
- 基本コンセプト：演劇の「代役（understudy）」のように、観察→模倣→記憶→最適化→自律、という5段階の成長モデルを採用。
- 5つのレイヤー（実装状況）
  - Layer 1（Operate Software Natively）: GUI操作／スクリーン認識／ネイティブ入力、ブラウザはPlaywright+拡張、シェル/CLI連携などを統合したローカル実行基盤（macOSで動作）。
  - Layer 2（Learn from Demonstrations）: /teachで画面と意味的イベントを録画→意図抽出→対話で確認→SKILL.mdとして公開。座標ではなく「意図」を覚える点が肝。
  - Layer 3（Crystallized Memory）: 使用実績から繰り返しパターンを自動で抽出・結晶化する仕組みが部分実装。閾値が満たされれば自動でスキル化する。
  - Layer 4（Route Optimization）: GUI→ブラウザ→CLI→APIの優先順位づけで、より高速なルートを優先する方針は実装中。完全自動プロモーションは未完成。
  - Layer 5（Proactive Autonomy）: 長期観察に基づく提案・自律実行は将来の目標。
- 技術ポイント
  - デュアルモデルのGUIグラウンディング（何をするか決めるモデルと、画面上の位置を決めるグラウンディングモデルを分離）。
  - SKILL.mdは3層（意図手順／ルート候補／GUIヒント）で再現性と堅牢性を両立。
  - ルート選択は失敗率や環境権限を考慮し動的に切り替え（例：Chrome拡張→Playwright→GUI）。
- 現実的な制約
  - 現状はmacOS中心、Layer1-2が主に実用的。完全自律化や大規模な自動ルート探索はこれから。
  - セキュリティ・プライバシー（画面録画やシェル実行）は運用ポリシーの整備が必要。

## 実践ポイント
- まずは非機密で単純な繰り返し作業（定型レポートのファイル整理、スクリーンショット処理、メッセージ送信）で /teach を試す。
- /teach start → 実演 → /teach stop → 対話で意図を確認 → /teach publish でSKILL.mdを生成して挙動を読む。
- 権限（アクセシビリティ、ブラウザ拡張、ファイルアクセス）を事前に確認してから運用。
- チーム導入時は監査ログと承認フローを整え、最初は“読み取り専用”やサンドボックスで検証する。
- 日本で有利な点：LINEやSlack等のメッセージング連携、カスタム業務アプリのGUI中心運用に向く点。

短くまとめると、Understudyは「教えるだけで覚えるローカルのAIアシスタント」を目指すプロジェクトで、今すぐ試せる部分（デモ学習・GUI統合）があり、ルーチンタスクの自動化で現場の負荷軽減につながる可能性が高いです。興味があれば examples にある SKILL.md を覗いて実際の出力を確認してください。
