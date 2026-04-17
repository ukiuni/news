---
layout: post
title: "The Claude Coding Vibes Are Getting Worse - Claude Codeの雰囲気が悪化している"
date: 2026-04-17T03:37:14.211Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://blog.matthewbrunelle.com/the-claude-coding-vibes-are-getting-worse/"
source_title: "The Claude Coding Vibes Are Getting Worse"
source_id: 766660762
excerpt: "Claude CodeのOpus 4.7更新で“長い思考”廃止、開発効率が大混乱"
image: "https://blog.matthewbrunelle.com/content/images/2026/04/pelican_riding_bicycle_opus_4.7.svg"
---

# The Claude Coding Vibes Are Getting Worse - Claude Codeの雰囲気が悪化している
魅惑のツールが変わった？Claude Codeの“使い勝手悪化”を読み解く — 今すぐ知っておくべき影響と対処

## 要約
AnthropicのClaude Codeは急成長に伴う負荷対策で最近のアップデートにより使い勝手が悪化しており、Opus 4.7で「extended thinking（長めの思考予算）」廃止など開発向けワークフローに影響を与えている。

## この記事を読むべき理由
日本の開発現場でもLLMツールを組み込む動きが進んでおり、Anthropicの仕様変更は開発効率・コスト・運用ポリシーに直結します。事前に変化を把握し対策を取ることで生産性低下を防げます。

## 詳細解説
- 背景：Opus 4.5→4.6で評判が上がり利用が急増。需要増に対しAnthropicはキャパシティ制御や最適化でサービスを縮小する選択を取っている。  
- 具体的な変更点と問題例：
  - Planモードの「clear context / execute」表示が非表示化（showClearContextOnPlanAccept が false デフォルトに）。後に戻されたが、UXが断続的に悪化。  
  - API利用のトークン運用変更：Pro/Maxのサブスクトークンをサードパーティが使えなくなり、APIクレジットのみ許可に。告知は薄く、利用者混乱を招いた。  
  - キャッシュTTLの短縮（1時間→5分）を「バグ」として修正したが、最適化の名目でコスト・レスポンス挙動が変わった。  
  - Opus 4.7で extended thinking（{"type":"enabled","budget_tokens":N}）が廃止。設定すると400エラー。Anthropic側は adaptive thinking の方が良いとするが、複雑なエンジニアリングタスクでの再現性・安定性が下がったという報告多数。  
- 結果：機能の不可逆的な削減や突発的な挙動変更で「有料でも品質が落ちる」事態が発生。コミュニティの不満がGitHubやSNSで散見される。

## 実践ポイント
- 依存分散：重要なワークフローは1プロバイダに依存しない（複数モデル／オンプレ候補を検証）。  
- 設定のバックアップ：UI/オプションが消される前提でローカルに設定やプロンプトを保存。  
- 事前テスト：大型アップデート前にレグレッションテストを行い、特に「長めの思考」を要求する処理を重点チェック。  
- コスト／認証設計見直し：サブスクトークン運用の変更を踏まえ、課金・認証フローを検証。  
- オープンモデル検討：Qwenなどの公開モデルやセルフホスティングを評価し、代替プランを準備する。  

短期的にはログとチェンジログをこまめに監視し、影響の大きい変更は社内で早めに周知・撤退基準を定めてください。
