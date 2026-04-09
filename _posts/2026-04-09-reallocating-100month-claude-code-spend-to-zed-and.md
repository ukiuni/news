---
layout: post
title: "Reallocating $100/Month Claude Code Spend to Zed and OpenRouter - 月100ドルのClaude Code支出をZedとOpenRouterへ再配分"
date: 2026-04-09T11:09:47.259Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://braw.dev/blog/2026-04-06-reallocating-100-month-claude-spend/"
source_title: "Reallocating $100/Month Claude Code spend to Zed and OpenRouter – Braw.dev"
source_id: 47700972
excerpt: "月100ドルをZed($10)とOpenRouterへ回し、Claudeを安価かつ柔軟に使う具体策"
image: "https://braw.dev/images/braw-dev-og-background_hu_960e5912b59745f.png"
---

# Reallocating $100/Month Claude Code Spend to Zed and OpenRouter - 月100ドルのClaude Code支出をZedとOpenRouterへ再配分
Claudeの課金を賢く切り替える：月100ドルをZed($10)＋OpenRouterへ回して柔軟性と貯蓄を両立する方法

## 要約
月100ドルのAnthropic/Claudeサブスクを、Zedエディタの$10とOpenRouterへの残額トップアップに振り分けることで、使わない月のクレジットを無駄にせず、複数モデルや大きなコンテキストを安価に試せる提案です。

## この記事を読むべき理由
Claudeの利用制限やコスト上限に悩む開発者が増えています。日本でもコスト管理と柔軟なモデル利用は重要で、代替エディタ＋OpenRouterで実務コストを抑えつつ生産性を維持できます。

## 詳細解説
- エージェントハーネスとは：LLMへの入出力やツール呼び出し、再試行などワークフローを管理する仕組み。Claude Codeはその一例で、ファイルI/Oやツール連携を自動化します。
- Zed（$10/月）：軽快なエディタでネイティブのエージェント機能を備える。VSCodeより応答が速く感じることが多く、ACPでClaudeや他モデルと統合可能。ネイティブ統合だとGeminiの文脈上限を200kに制限する場合があるが、OpenRouter経由なら1Mまで使えるケースがある。
- OpenRouter：多数プロバイダ／モデルを仲介するプラットフォーム。クレジットは365日で有効期限があり、使わない月は残高が残るため「使った分だけ消える」Anthropicの定期枠より柔軟。手数料（記事では5.5%指摘）や提供モデルの差異には注意。
- Cursor（$20〜）：VSCode互換の利点＋細かいルール適用やデバッグモードが強み。拡張互換があるため一部ユーザーは併用を継続。
- Claude CodeをOpenRouter経由で使う設定例：Claude Codeを今まで通りハーネスとして使いつつAPI先をOpenRouterに向けることができる。環境変数でOpenRouterのAPIキーとエンドポイントを設定するだけで切り替え可能。

例：環境変数設定（bash）
```bash
export OPENROUTER_API_KEY="<your-openrouter-api-key>"
export ANTHROPIC_BASE_URL="https://openrouter.ai/api"
export ANTHROPIC_AUTH_TOKEN="$OPENROUTER_API_KEY"
export ANTHROPIC_API_KEY=""
export ANTHROPIC_DEFAULT_OPUS_MODEL="anthropic/claude-opus-4.6"
export ANTHROPIC_DEFAULT_SONNET_MODEL="anthropic/claude-sonnet-4.6"
export ANTHROPIC_DEFAULT_HAIKU_MODEL="anthropic/claude-haiku-4.5"
export CLAUDE_CODE_SUBAGENT_MODEL="anthropic/claude-opus-4.6"
# claude CLI を再起動して設定確認
claude > /logout
claude > /status
```

## 実践ポイント
- まずZedを無料で試す（$10プランはコスパ良）。反応速度とエージェント挙動を確認する。  
- OpenRouterに少額（例:$20〜$70/月相当）をプリチャージして運用。クレジットは365日有効で繰越せる点を活用。  
- Claude Codeを使い続けたい場合は上記のようにOpenRouterに向けて設定を変更し、必要なモデルだけ使う。  
- プライバシーはOpenRouterのZDR（Zero Data Retention）やデータ利用同意の設定を活用してリスクを下げる。  
- Cursorや他のハーネスは必要に応じて併用。まずは少額で試して、月次の消費パターンに合わせて配分を調整する。
