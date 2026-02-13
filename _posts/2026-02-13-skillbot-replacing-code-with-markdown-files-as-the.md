---
layout: post
title: "skillbot: Replacing code with Markdown files as the only abstraction for AI agent capabilities — 815 lines of TypeScript vs OpenClaw's 300K - skillbot：AIエージェントの機能をすべてMarkdownで置き換える（815行のTypeScriptで実現）"
date: 2026-02-13T08:35:57.664Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/batechworks/skillbot"
source_title: "GitHub - batechworks/skillbot: OpenClaw in 815 lines: a personal AI assistant where every capability is a Markdown file."
source_id: 442860316
excerpt: "Markdownファイルを追加するだけでLLM統合の自動化エージェントを815行で実現する実践ガイド"
image: "https://opengraph.githubassets.com/3734935217c859049fe4e798464edb66162787e0b2d386ddb85bfa34df9a6de2/batechworks/skillbot"
---

# skillbot: Replacing code with Markdown files as the only abstraction for AI agent capabilities — 815 lines of TypeScript vs OpenClaw's 300K - skillbot：AIエージェントの機能をすべてMarkdownで置き換える（815行のTypeScriptで実現）
「コードを書かずに“.md”を足すだけでAIが新機能を覚える――815行のスモールエージェントが示す、現場で使える自動化の最短ルート」

## 要約
skillbotは“スキルをコードではなくMarkdownで定義する”という思想で、コアはわずか815行のTypeScript。CLIを武器にLLMを統合層として使い、個別ツール実装をほぼ不要にしている。

## この記事を読むべき理由
日本のエンジニアや現場オートメーション担当者にとって、既存のCLI資産（gh, docker, curl など）を活かしつつ、短期間で安全にAIエージェントを導入できる実践的アプローチだから。企業内ツールやオンプレ資産との統合コストを下げたいチームに価値がある。

## 詳細解説
- コア設計：コアは9ファイルで815行。複雑なプラグインを大量に書く代わりに「スキル＝Markdownファイル」で機能を定義する。
- 実行フロー：User → LLM → bash（shell）→ CLIツール → LLM → User。LLMに手順を読ませ、必要なshellコマンドを実行することで統合を実現。
- 最小ツールセット：実装は2つのツールだけ（bash：任意のシェルコマンド実行、spawn：背景サブエージェント起動）。それ以外は既存CLIに任せる。
- スキルの例と拡張性：33個のMarkdownスキルが同梱。新しいスキルは単に skills/*.md を追加するだけで即時利用可能（例：docker.md を作るだけでDocker操作が可能に）。
- メモリとプロンプト管理：
  - Dual-layer Markdownメモリ（MEMORY.md と daily logs）でLLM自身に履歴管理を任せる。
  - 必須スキルのみ常時プロンプト注入、他はカタログ参照でオンデマンド読み込み→プロンプト肥大化を回避。
- 人格・ユーザ設定：SOUL.md / USER.md でボットのトーンやユーザプロファイルを定義。ファイル編集で性格変更可。
- 安全性：危険コマンドのブロッキングやワークスペース制限（RESTRICT_WORKSPACE）で実行範囲を限定可能。
- 対応プロバイダ・チャネル：OpenAIやAnthropic、Gemini等複数プロバイダ対応。CLIのほかTelegram/Discord/Slack/iMessage等に接続可能。
- テストと導入：単体テストは決定論的で高速。モックや統合テストも用意され、CI組み込みが比較的容易。

## 実践ポイント
- まず試す：リポジトリをクローンして.envにAPIキーを書くだけでCLIチャットが起動できます。
```bash
git clone <repo-url> skillbot && cd skillbot
npm install
echo 'SKILLBOT_PROVIDER=openai' >> .env
echo 'OPENAI_API_KEY=sk-...' >> .env
npm start
```
- スキル追加は簡単：skills/new-skill.md を作り、Markdown内に実行するコマンド列を書くだけで即戦力化。
- 社内適用：社内CLIツールやwrapperを活かしてスキルを作れば、低コストで自動化エージェントを展開できる。まずはREADMEのRESTRICT_WORKSPACEやサンドボックス設定で安全に試すこと。
- 運用の勘所：MEMORY.mdの運用ルールと定期的なオートコンパクション設定を決め、個人情報や機密データが不要に保存されないようにする。

短時間でプロトタイプを回せて、既存シェル資産を最大限活用できる点がskillbotの肝。小さく始めて、社内ワークフローに合わせてMarkdownスキルを積み増す運用が現実的です。
