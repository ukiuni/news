---
layout: post
title: "Compressed Agents.md > Agent Skills - 圧縮した AGENTS.md がスキルを上回る"
date: 2026-01-29T22:42:48.750Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals"
source_title: "AGENTS.md outperforms skills in our agent evals - Vercel"
source_id: 46809708
excerpt: "圧縮AGENTS.mdでNext.js未学習API対応が成功率100%に—即導入できる索引運用法"
image: "https://assets.vercel.com/image/upload/contentful/image/e5382hct74si/NrCaFKRo4wJnZm4hhbuJ0/752791d02cda6e1f367dbfefed3ed963/agentsmd_outperforms_skills_in_our_agent_evals_og_card.png"
---

# Compressed Agents.md > Agent Skills - 圧縮した AGENTS.md がスキルを上回る
Next.jsでAIエージェントを確実に正しく動かす最短ルート：8KBのAGENTS.mdがスキル依存を超えた理由

## 要約
Vercelの評価で、ドキュメント索引を圧縮してAGENTS.mdに埋めた方式が、スキル（on‑demandツール）より高い成功率（100% vs 最大79%）を示した。

## この記事を読むべき理由
日本のプロダクトやレガシーNext.jsプロジェクトでは、モデルの学習データに入っていないAPI（Next.js 16の新APIなど）を使う場面が増え、AIでのコード生成の正確性が課題になっているため、手元のドキュメントをどうエージェントに与えるかは即効性のある改善策です。

## 詳細解説
- 問題点：AIコーディングエージェントは学習データが古いと新API（例: use cache、connection()、forbidden()、cacheLife()/cacheTag()、proxy.ts、async cookies()/headers()、after()/updateTag()/refresh() など）を知らず誤ったコードを生成する。逆に最新APIを提案して動かないこともある。
- 比較対象：
  - Skills：ドメイン知識をパッケージ化し、必要時にエージェントが呼び出す仕組み。理論上は効率的だが、評価で56%のケースでエージェントがスキルを呼ばなかった。
  - AGENTS.md：プロジェクトルートに置くマークダウンで、内容が常にコンテキストとして与えられるためエージェントが参照を「決定」する必要がない。
- 評価結果（強化したハード化済みevalで再試行）：
  - ベースライン（ドキュメントなし）: 53% 合格
  - Skill（デフォルト）: 53%
  - Skill + 明示的指示: 79%（ただし指示文のワーディングに脆弱性あり）
  - AGENTS.md（圧縮索引）: 100%
- なぜAGENTS.mdが効いたか：
  1. エージェントに「調べるかどうか」の判断をさせない（No decision point）  
  2. 常にコンテキストとして利用可能（consistent availability）  
  3. 「先に読むか／先にプロジェクトを把握するか」の順序問題を回避（ordering issues）
- コンテキスト肥大化対策：全文投入ではなく索引を圧縮（初期40KB→8KB）し、pipe区切りの最小形式でAGENTS.mdに埋め、実ファイルは .next-docs/ に保存して必要時に参照させる方式を採用。

## 実践ポイント
- 手早く試すコマンド（Next.js公式codemodが自動化）：
```bash
npx @next/codemod@canary agents-md
```
- 推奨運用
  - AGENTS.mdに「検索主導の推論を優先する（Prefer retrieval-led reasoning）」のような一行指示を入れる。  
  - ドキュメントは索引化して小さく圧縮し、詳細ファイルはプロジェクト内に置く（agentsが参照できる構造にする）。  
  - スキルは垂直タスク（アップグレードやマイグレーション等、明示的トリガがあるワークフロー）に残し、一般知識はAGENTS.mdでカバーする。  
  - 自前の評価スイートを作り、モデル訓練データに含まれないAPIを対象にテストする（実際の振る舞いを検証）。

短く言えば、今すぐ試せる実践は「圧縮した索引をAGENTS.mdに入れること」。特に日本のエンタープライズや長寿プロジェクトでは、バージョン整合したドキュメントをエージェントに常時渡す運用が有効です。
