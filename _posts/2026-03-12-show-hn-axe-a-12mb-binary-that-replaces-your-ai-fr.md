---
layout: post
title: "Show HN: Axe A 12MB binary that replaces your AI framework - Show HN: Axe — AIフレームワークを置き換える12MBバイナリ"
date: 2026-03-12T14:39:07.068Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/jrswab/axe"
source_title: "GitHub - jrswab/axe: A ligthweight cli for running single-purpose AI agents. Define focused agents in TOML, trigger them from anywhere; pipes, git hooks, cron, or the terminal. · GitHub"
source_id: 47350516
excerpt: "12MBバイナリAxeでフレームワーク不要の高速AI自動化をローカルCIへ簡単導入"
image: "https://opengraph.githubassets.com/5affd76161847173f55b25f7d6859dbf7f1a10437391fbb05bc1c68518d52d1b/jrswab/axe"
---

# Show HN: Axe A 12MB binary that replaces your AI framework - Show HN: Axe — AIフレームワークを置き換える12MBバイナリ
12MBで「フレームワーク不要」のAIエージェント運用へ──コマンドラインで小さく素早く組み合わせるAxeの使いどころ

## 要約
AxeはTOMLで定義する単機能LLMエージェントをコマンドラインから実行する軽量バイナリ（Go製）。チャットUIや常駐サービスを持たず、Unix哲学でパイプやgitフック、cronと簡単に組み合わせられる。

## この記事を読むべき理由
日本の開発現場でも「クラウド依存を減らしつつ自動化を手早く導入したい」ケースが増えています。Axeは小さな構成でCIやローカル環境へ安全に組み込めるため、データ保護や運用コストを重視する企業／個人に有益です。

## 詳細解説
- アーキテクチャ: 各エージェントはTOMLで定義（name, model, system_prompt, skill, files, workdir, tools, sub_agents, memory 等）。Axeは実行者でありスケジューラではないため、cron/git-hooks/パイプ等と組み合わせて運用する想定。
- モデル & プロバイダ: Anthropic、OpenAI、ローカルのOllamaに対応。環境変数でAPIキーを渡すか、ローカルOllamaを併用してオンプレ運用可能。
- スキル＆再利用: SKILL.md形式でドメイン知識／ワークフローを定義し再利用可能。複数エージェントを連鎖（sub_agents）させることもできる。
- ツールとサンドボックス: read_file, write_file, list_directory, run_command 等の組み込みツールで作業ディレクトリ外へのアクセスは禁止。ツール呼び出しはLLMと対話しながら最大50ターンまで続けられる。
- 永続メモリ: 実行ログをタイムスタンプ付きmarkdownで保持し、次回実行時にコンテキストとして読み込める。GC機能でメモリ肥大を抑制。
- 出力と自動化向け機能: JSON出力、dry-run（コンテキスト確認）やstdinパイプ連携があり、スクリプトやCIに組み込みやすい。
- 実行環境: Go 1.24+でビルド可能。Dockerイメージ／docker-composeが用意され、非root・ReadOnlyルートなどのハードニング設定がある。

## 実践ポイント
- まず試す（ローカル）:
  ```bash
  # Goによるインストール
  # bash
  go install github.com/jrswab/axe@latest

  # 設定初期化
  # bash
  axe config init

  # 例をコピーして実行（AnthropicやOpenAIのAPIキーを環境変数で）
  # bash
  cp -r examples/code-reviewer "$(axe config path)/agents/"
  export ANTHROPIC_API_KEY=your-key
  git diff | axe run code-reviewer
  ```
- CI/フック連携: git hooksやpre-commitと組み合わせ、差分を自動レビュー→PRテンプレート生成などを実装すると早期フィードバックが得られる。
- セキュリティ/オンプレ運用: 機密データを扱う場合はOllama等のローカルモデルとDockerで隔離し、ネットワークやボリュームを最小化する。
- 再利用性の確保: SKILL.mdでレビュー基準やテンプレートを定義してチーム共有すると効果的。
- メモリ運用: memory.enabledを使う場合はgcコマンドで定期的に整理し、不要な履歴でトークンを浪費しない。

短くまとめると、Axeは「小さく分離されたAIエージェント」をUnixツール群にシームレスに組み込める実践向けツールで、日本の現場でもローカル運用やCI統合による速い価値提供に向いています。
