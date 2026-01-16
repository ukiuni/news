---
layout: post
title: "Show HN: Gambit, an open-source agent harness for building reliable AI agents - Gambit：信頼できるAIエージェントを構築するためのオープンソースハーネス"
date: 2026-01-16T04:49:35.176Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/bolt-foundry/gambit"
source_title: "GitHub - bolt-foundry/gambit: Agent harness framework for building, running, and verifying LLM workflows"
source_id: 46641362
excerpt: "Gambitで型付きデッキを組みローカルで可視化・デバッグして信頼性あるLLMワークフローを実現"
image: "https://opengraph.githubassets.com/8fdd13254d8138993509d2749c25774cd9b27f59ec4f80d1d92d2f602a0d4ab5/bolt-foundry/gambit"
---

# Show HN: Gambit, an open-source agent harness for building reliable AI agents - Gambit：信頼できるAIエージェントを構築するためのオープンソースハーネス
魅力的な日本語タイトル: 小さな「デッキ」でLLMワークフローを確実に──GambitでデバッグしやすいAIパイプラインを作る

## 要約
Gambitは「小さな型付きデッキ（deck）」を組み合わせてLLMワークフローを作るフレームワークで、ローカルで実行・トレース・デバッグできるツール群（CLI、デバッグUI、ライブラリ）を提供する。入出力を明確化し、モデル呼び出しをアクションの一種として扱うことで再現性とテスト性を高める設計が特徴。

## この記事を読むべき理由
日本の開発チームがAIを組み込む際、モデル呼び出しのコスト増大やハルシネーション、運用時のデバッグ難易度に悩む事が多い。Gambitは「型付きI/O」「局所オーケストレーション」「ローカルでのトレース可視化」を強みに、検証可能で企業向け要件に適合しやすいワークフロー設計を支援するため、日本の現場にも即効性がある。

## 詳細解説
- 基本コンセプト
  - 「デッキ（deck）」：小さく分割されたステップ単位。各デッキに明確な inputSchema / outputSchema を定義し、Zodで型検証できるため入出力の不整合によるバグを未然に防げる。
  - モデル呼び出しは「アクション」の一種。LLMと純粋な計算（compute）処理を同じデッキツリー内で混在させられる。
  - ガードレール：各ステップで必要な情報だけをモデルに渡し、不要な文書の丸投げを避ける設計。

- ツール群
  - CLI（npx / Deno対応）：デッキの実行、REPL、serve（デバッグUI起動）、test-bot、grade（セッション採点）など。
  - Debug UI（Simulator）：ブラウザでストリーム表示・トレース確認・フォームからの入力が可能。ローカル-firstで .gambit/ にセッションを保存。
  - ライブラリ：TypeScriptデッキを作成可能。APIは defineDeck/defineCard、ctx.spawnAndWait、ctx.log といった形でプログラムから親子デッキ呼び出しやトレース出力が行える。

- 実行例・開発フロー（抜粋）
  - 必要条件：Node.js 18+, 環境変数 OPENROUTER_API_KEY（プロキシするなら OPENROUTER_BASE_URL）
  - CLIで初期ファイルを取得：
    ```bash
    export OPENROUTER_API_KEY=...
    npx @bolt-foundry/gambit init
    ```
  - Markdownデッキの例（モデル呼び出し）：
    ```bash
    npx @bolt-foundry/gambit run ./hello_world.deck.md --init '"Gambit"' --stream
    ```
  - TypeScriptで計算デッキを書く例（Zodでスキーマ）：
    ```typescript
    import { defineDeck } from "jsr:@bolt-foundry/gambit";
    import { z } from "zod";

    export default defineDeck({
      label: "echo",
      inputSchema: z.object({ text: z.string() }),
      outputSchema: z.object({ text: z.string(), length: z.number() }),
      run(ctx) {
        return { text: ctx.input.text, length: ctx.input.text.length };
      },
    });
    ```

- デバッグと検証
  - 実行トレースはJSONLで保存でき、--trace、--stateオプションでセッション再現や採点が可能。
  - test-bot 機能で「ペルソナ」デッキを使った振る舞いテストができるため、回帰テストや振る舞い保証に活用可能。

- ライセンス・エコシステム
  - Apache-2.0ライセンスで公開。TypeScript主体（ほぼ98%）で、Denoサポートも用意されている。

## 日本市場との関連性
- コスト管理：ステップ単位で必要な情報だけを渡す設計はトークンコスト削減につながる。日本の予算厳しいプロジェクトにもメリットが大きい。
- セキュリティとガバナンス：オンプレやプロキシ経由（OpenRouter互換）での利用が想定でき、社内データ流出リスクを抑えやすい。
- ローカルでの再現性：現場でのデバッグ・監査・QAがやりやすく、金融・医療などコンプライアンスが厳しい領域への適用可能性が高い。
- エンタープライズ統合：TypedなI/Oやテストフローは既存CI/CDやSRE運用に馴染みやすい。

## 実践ポイント
- まず触る
  - 環境変数を用意して npx で init → serve して Debug UI を起動し、既存の hello デッキを動かしてみる。
    ```bash
    export OPENROUTER_API_KEY=...
    npx @bolt-foundry/gambit serve gambit/hello.deck.md --port 8000
    # ブラウザで http://localhost:8000 を開く
    ```
- 型から始める：Zodで inputSchema/outputSchema を定義するとデバッグが劇的に楽になる。
- 局所化してコスト抑制：大きなRAGブロブを渡す代わりに、参照カードや必要最小限の文脈だけを渡す設計に切り替える。
- テスト自動化：test-bot と grade 機能で振る舞いテストをCIに組み込み、回帰チェックを自動化する。
- 企業則対応：OpenRouter互換設定やローカル保存を活用して社内ポリシーに合う形に整備する。

参考：GitHubリポジトリ（bolt-foundry/gambit）。試すときはリポジトリのREADMEとLICENSEを確認すること。
