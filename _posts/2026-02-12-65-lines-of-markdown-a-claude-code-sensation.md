---
layout: post
title: "65 Lines of Markdown, a Claude Code sensation - 65行のMarkdown、Claude Codeのセンセーション"
date: 2026-02-12T09:16:34.105Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://tildeweb.nl/~michiel/65-lines-of-markdown-a-claude-code-sensation.html"
source_title: "65 Lines of Markdown, a Claude Code Sensation"
source_id: 46986001
excerpt: "65行MarkdownでAI支援コーディングを安定化する実践ガイドと公開課題"
---

# 65 Lines of Markdown, a Claude Code sensation - 65行のMarkdown、Claude Codeのセンセーション
たった65行でAI支援コーディングが変わる？“Think Before Coding”が話題の拡張の正体

## 要約
たった65行のMarkdownルールがClaude系の拡張として注目を集め、作者はそれをVS Code／Codex向けにパッケージ化して公開した。小さなルールセットがAIツールの振る舞いに影響を与える可能性を示している。

## この記事を読むべき理由
日本でもAI支援コーディングが広がる中で、少ない工数でモデル出力の質を上げる「ルール化」の実例と、拡張公開に伴う現実的なハードル（マーケットプレースの検証や公開手続き）を知ることは実務で役立ちます。

## 詳細解説
- 発端：GitHubで人気の「Karpathy風のClaude向けガイドライン」が実は65行のMarkdownファイルだった。先頭の原則が "Think Before Coding"（コーディングの前に考える）で、他に合計4つの原則が並ぶ。
- パッケージ化：記事の著者はClaude Codeを使わないため、同ファイルを元にCodex/VS Code用の拡張を作成して公開。拡張自体はルールをツールに読み込ませるだけの軽いものだが、配布周りに手間があった。
- 公開の現実：VS Code Marketplaceでは「Verified Publisher」になっていないと警告が出る（申請には一定期間の公開実績が必要）。CursorやOpen VSX向け公開ではEclipseアカウント連携や合意書の締結、ネームスペースのクレームなど複雑な手続きが必要だった。
- ユーザ体験：ルール適用後のモデル出力は非決定的で評価が難しい。著者は「変更に慎重になる」傾向を感じたが、明確な改善が常に出るとは限らない。しかしルールはチーム固有の制約（コーディング規約／アーキテクチャ条件）を明示するのに有効で、実務での安定化に寄与する可能性がある。

## 実践ポイント
- まずは自分のプロジェクト向けに「簡単なルールファイル」を作ってみる（例：Think Before Coding、命名規則、不要変更の回避）。
- LLM系ツールは非決定的なので、A/Bで複数プロンプト／ルールを比較して安定性を評価する。
- チーム配布ならMarkdownベースでルール化→拡張化を検討。公開時の信頼性（Verified Publisher等）を事前に確認する。
- 日本語ドキュメントや社内規約と合わせてルールを整備すれば、外部ツール導入時の品質ばらつきを減らせる。

元記事: https://tildeweb.nl/~michiel/65-lines-of-markdown-a-claude-code-sensation.html
