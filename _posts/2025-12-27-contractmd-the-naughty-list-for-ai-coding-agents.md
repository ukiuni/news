---
layout: "post"
title: "CONTRACT.md: The Naughty List for AI Coding Agents - CONTRACT.md：AIコーディングエージェントのための「いたずらっ子リスト」"
date: "2025-12-27 02:08:29.316000+00:00"
categories:
- tech
- world-news
tags:
- tech-news
- japan
source_url: "https://www.discussdontcode.com/zettels/contract.md-the-naughty-list-for-ai-coding-agents/"
source_title: "Discuss, don't code. | CONTRACT.md: The Naughty List for AI Coding Agents"
source_id: "1736512109"
excerpt: "CONTRACT.mdでAIの過剰設計を封じ、MVPと依存制限で品質と納期を守る"
---
# CONTRACT.md: The Naughty List for AI Coding Agents - CONTRACT.md：AIコーディングエージェントのための「いたずらっ子リスト」

## 要約
AIコーディングエージェントは「未来を見越して複雑化」しがちだ。CONTRACT.mdはその暴走を止める短く厳しいルールブックで、許容する複雑さの上限を明確にする実務的な対策だ。

## この記事を読むべき理由
日本のプロダクト開発では保守性・安定性・ガバナンスが重視される。AIを導入するほど「要件が不確実→AIが過剰設計」という罠に陥りやすく、早期にCONTRACT.mdを定めることが品質と納期を守る最短経路になる。

## 詳細解説
- AGENTS.md（または.github/copilot-instructions.md）は「やり方のガイド」。CONTRACT.mdは対極にあり、「これ以上はやらない」という禁止リスト／上限値を示す。
- 背景：LLM系エージェントは未来-proofingや過度な抽象化を好み、最初のグリーンフィールド実装で無駄に多層化・複雑化する傾向がある。人がまだ「馬に乗れていない」段階で馬車を作るような順序ミスをする。
- CONTRACT.mdの目的：設計の肥大化を防ぎ、最小限で反復可能な成果物を得ること。要は「複雑さ予算」の明文化と、違反時の自動停止ルール。
- 含めるべき項目の例（概念）：
  - 機能スコープの上限（最小実装でOKな範囲）
  - 許可するライブラリ／バージョンのホワイトリスト
  - 最大依存関係数や外部APIコールの上限
  - PRあたりの最大行数／ファイル削除・大幅リファクタの禁止
  - パフォーマンス／レイテンシ予算（必要な場合）
  - テストカバレッジ最低ラインと必須の統合テスト
  - 必須ヒューマンゲート（アーキテクチャ変更やDBスキーマ変更は人の承認）
  - 逸脱時の処置（エージェント停止、ロールバック、担当者への通知）
- なぜこれが効くか：AIは指示に従うので「やっていいこと」と「やってはいけないこと」を短く明確に示すだけで、無駄な先回り設計を抑止できる。

## 実践ポイント
- まずは1ページに収まる短いCONTRACT.mdを作る。長文化はNG。  
- CIに簡易ルールチェックを入れる（PRサイズ、依存追加の検出、スキーマ変更フラグなど）。  
- PRテンプレートで必須チェック項目として組み込む（「このPRはCONTRACT.mdを破っていませんか？」）。  
- チームで定期レビューし、守れなかったケースを短くログ化してルールを改善する（OODAループ）。  
- 日本企業向け追加注意点：セキュリティ/コンプライアンス（個人情報取り扱い、外部API利用規約）やオンプレ制約などを明文化する。  
- 小さく始め、成功パターンをCONTRACT.mdに蓄積する。AIに「自由に作らせてから直す」は避ける。

例（CONTRACT.mdの骨子）：
```text
# CONTRACT.md（例）
- Scope: MVP endpoints only. No schema changes without human approval.
- Dependencies: Only approved list (axios@0.27, express@4.x). Max +2 new deps per PR.
- PR size: <= 300 LOC touched. No cross-cutting global refactors.
- Tests: Unit tests for new logic + 1 integration scenario required.
- Human gates: DB schema, infra changes, authentication flows.
- Violation: CI fail and agent shutdown; notify owner.
```

