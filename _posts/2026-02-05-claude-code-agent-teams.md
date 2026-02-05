---
layout: post
title: "Claude Code Agent Teams - Claude Codeのエージェントチーム"
date: 2026-02-05T19:14:14.587Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://code.claude.com/docs/en/agent-teams"
source_title: "Orchestrate teams of Claude Code sessions - Claude Code Docs"
source_id: 46902368
excerpt: "複数のClaudeCodeエージェントで並列検証し、レビューや大規模リファクタを高速化する実験機能"
image: "https://claude-code.mintlify.app/_next/image?url=%2F_mintlify%2Fapi%2Fog%3Fdivision%3DBuild%2Bwith%2BClaude%2BCode%26appearance%3Dsystem%26title%3DOrchestrate%2Bteams%2Bof%2BClaude%2BCode%2Bsessions%26description%3DCoordinate%2Bmultiple%2BClaude%2BCode%2Binstances%2Bworking%2Btogether%2Bas%2Ba%2Bteam%252C%2Bwith%2Bshared%2Btasks%252C%2Binter-agent%2Bmessaging%252C%2Band%2Bcentralized%2Bmanagement.%26logoLight%3Dhttps%253A%252F%252Fmintcdn.com%252Fclaude-code%252Fo69F7a6qoW9vboof%252Flogo%252Flight.svg%253Ffit%253Dmax%2526auto%253Dformat%2526n%253Do69F7a6qoW9vboof%2526q%253D85%2526s%253D536eade682636e84231afce2577f9509%26logoDark%3Dhttps%253A%252F%252Fmintcdn.com%252Fclaude-code%252Fo69F7a6qoW9vboof%252Flogo%252Fdark.svg%253Ffit%253Dmax%2526auto%253Dformat%2526n%253Do69F7a6qoW9vboof%2526q%253D85%2526s%253D0766b3221061e80143e9f300733e640b%26primaryColor%3D%25230E0E0E%26lightColor%3D%2523D4A27F%26darkColor%3D%25230E0E0E%26backgroundLight%3D%2523FDFDF7%26backgroundDark%3D%252309090B&amp;w=1200&amp;q=100"
---

# Claude Code Agent Teams - Claude Codeのエージェントチーム
複数のClaude Codeセッションが分担して動く――「エージェントチーム」で開発・レビューを爆速化する方法

## 要約
複数の独立したClaude Codeセッション（チームリード＋複数の teammate）を並列に動かし、タスク共有・直接通信・集中管理で複雑なコード作業を効率化する実験機能です。

## この記事を読むべき理由
日本の開発現場でも、レビュー・調査・大規模リファクタで「並列で異なる仮説を試す」ニーズが高まっています。Claudeのエージェントチームは、役割分担と相互通信でこうした作業を高速化できるため、特に大規模プロジェクトやクロスレイヤ変更に有効です。

## 詳細解説
- 概要：チームは「リード（調整）」と複数の「teammate（独立セッション）」で構成。リードがタスクを作り、共有タスクリストでteammateが自律的に取り組み、必要なら直接相互メッセージをやり取りします。
- いつ使うか：研究・レビュー、機能分割リファクタ、仮説対立によるデバッグ、フロント/バック/テスト横断の調整など、並列探索に価値がある場面が適切。単純連続作業や同一ファイルの競合が多い場合はサブエージェントか単一セッションが向きます。
- サブエージェントとの違い：サブエージェントはメインに結果を返す「フォーカス型」。エージェントチームは各メンバーが独立して対話・協調できる「議論型」。トークンコストはチームの方が高い。
- 有効化：実験機能で無効がデフォルト。環境変数で有効化します（例：settings.jsonに設定）。
```json
{
  "env": { "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1" }
}
```
- 表示モード：in-process（単一端末内で切替）とsplit panes（tmux/iTerm2で各メンバーを同時表示）。tmuxはOS依存の注意あり。
- 制御機能：人数・モデル指定、プラン承認モード（実装前にリードが設計を承認）、delegateモード（リードは調整のみ）、個別メッセージ、タスクの割当・自己取得、ファイルロックによる競合防止、優雅なシャットダウンとチームのクリーンアップ。
- 内部動作：各メンバーは個別コンテキスト（CLAUDE.md等を読み込む）。タスク・チーム設定はローカルに保存。通信は自動配信と共有タスクリストで管理。トークン消費はメンバー数に比例して増加。
- 注意点と制限：セッション再開やシャットダウンの挙動、タスク同期に制限あり。短い・依存の強い連続作業ではコストとオーバーヘッドが無駄になる可能性。

## 実践ポイント
- まずは小さな並列化から：レビューや調査で2〜3人チームを試す。  
- 役割を明確に：セキュリティ／性能／テストなど「視点」を分けると効果大。  
- プラン承認を使う：データベースや設計変更はプラン承認で安全に。  
- displayモードは環境で選択：macであればtmux/iTerm2で可視化、他はin-processで試す。  
- コスト管理：トークン増を意識して、ルーチン作業は単一セッションに留める。  
- クリーンアップ手順を守る：先にteammateをシャットダウンしてからリードにcleanupを実行する。

短時間で実験的に並列化を導入し、成果とコストのバランスを見ながら適用範囲を拡大すると現場効果が得られます。
