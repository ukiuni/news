---
layout: post
title: "I traced 3,177 API calls to see what 4 AI coding tools put in the context window - 3,177件のAPI呼び出しを追跡してわかった、4つのAIコーディングツールがコンテキストウィンドウに置いているもの"
date: 2026-02-19T14:07:12.982Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://theredbeard.io/blog/i-intercepted-3177-api-calls-across-4-ai-coding-tools"
source_title: "I Intercepted 3,177 API Calls Across 4 AI Coding Tools. Here&#39;s What&#39;s Actually Filling Your Context Window. | The Redbeard"
source_id: 437813095
excerpt: "3,177回の解析で判明、4ツールの文脈戦略がコストと信頼性を左右"
image: "https://theredbeard.io/blog/i-intercepted-3177-api-calls-across-4-ai-coding-tools/compare-all-four-v3-updated.png"
---

# I traced 3,177 API calls to see what 4 AI coding tools put in the context window - 3,177件のAPI呼び出しを追跡してわかった、4つのAIコーディングツールがコンテキストウィンドウに置いているもの
あなたのAIは何を「読んで」いる？3,177回の追跡で見えたコンテキストの無駄遣いと実務への影響

## 要約
同じバグ修正タスクを4種のAIコーディングツールに与え、3,177回のAPI呼び出しを解析したところ、ツールごとにコンテキスト（トークン）消費戦略が大きく異なり、コスト・安定性・予測可能性に直結することが分かった。

## この記事を読むべき理由
日本の開発現場でもLLMをCIやペアプログラミング代替に導入する流れが加速中。トークン課金と有限のコンテキストウィンドウを理解しないと、意図しないコスト増・遅延・不安定な自動修正が発生します。本記事は実データに基づく実務的示唆を短く示します。

## 詳細解説
- 実験概要：Express.jsリポジトリに故意のバグを差し込み、同一プロンプトでClaude(Opus/ Sonnet)、Codex(GPT-5.3)、Gemini 2.5 Proの4ツールを実行。各ツールがどの情報をAPIで取り込み、コンテキストに積むかを可視化するツール「Context Lens」で解析。
- トークンと文脈：トークンは課金と「短期記憶」に直結。モデルが多く読み込むほど文脈が膨らみ、費用と処理負荷が増える。
- 主な発見（簡潔に）:
  - Opus（Claude Opus 4.6）: ツール定義を毎回プロンプトに載せる「固定負荷」が大きい（約69%がツール定義）が、読み取りは最小限で一貫性高め。平均約27Kトークン。
  - Sonnet（Claude Sonnet 4.5）: テストファイルなどを広く読むバランス型。平均約50Kトークン。
  - Codex（GPT-5.3系）: grep/sed的に最小範囲を狙う「Unixハッカー」的戦略で予測可能、平均約35Kトークン。
  - Gemini 2.5 Pro: 文脈ウィンドウが大きいため大量に読み込む戦略（ファイル履歴やテスト出力を丸ごと取り込む）。平均約258Kトークン、最大350Kに達した実行もあり非常に不安定。
- 戦略の違いが効率差を生む：固定プロンプト負荷、読み込みの範囲、キャッシュ利用、手順（git-first、test-first、grep-first、全探索）によりトークン消費と実行時間が変化。多くのツールは「文脈予算」を能動的に管理していない。

## 実践ポイント
- トークンコスト管理：CIや自動修正では、モデル選定だけでなく「読み取り範囲」を制御するラッパー（行範囲指定、差分中心の探索）を設ける。
- プロンプト最適化：ツール定義を毎回送る方式は固定コストになる。サーバ側でツール定義保持できるモデルを検討するか、最小化する。
- リポジトリ設計：git履歴があると一部のモデルは効率的にバグを特定する。逆に全履歴を丸ごと返すコマンドはNG。APIレスポンスのトリミングを必須に。
- 監視・可視化：Context Lens や ContextIO のような監視ツールで実際のAPI呼び出しとトークン構成を継続的にログ化する（まずは可視化）。
- 現場ルール：テスト改変の自動リバートや一時テスト追加など、モデルの自律的な改変を許すか運用ポリシーで明確化する。

導入を試すなら（手早く動かすコマンド例）:
```bash
npm install -g context-lens
context-lens claude
```

短く言えば：同じ「できる」でも中身の戦略でコストと信頼性が全然違う。日本のプロジェクトではまず「何を読ませるか」を設計してからモデルを選ぶのが実務上の近道。
