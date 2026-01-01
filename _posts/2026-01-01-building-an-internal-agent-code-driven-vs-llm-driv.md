---
  layout: post
  title: "Building an internal agent: Code-driven vs. LLM-driven workflows - 内部エージェント設計：コード主導 vs LLM主導ワークフロー"
  date: 2026-01-01T20:57:50.702Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://lethain.com/agents-coordinators/"
  source_title: "Building an internal agent: Code-driven vs LLM-driven workflows | Irrational Exuberance"
  source_id: 46456682
  excerpt: "LLMで高速プロトタイプ→信頼性はコード化するハイブリッド運用法を具体事例で解説"
  image: "https://lethain.com/static/author.png"
---

# Building an internal agent: Code-driven vs. LLM-driven workflows - 内部エージェント設計：コード主導 vs LLM主導ワークフロー
LLM任せで便利だが「決定性」を失う――現場で使えるのはどちらか？

## 要約
LLM＋ツールで多くのワークフローを自動化できる一方、誤動作や非決定性が問題になる事例があり、実運用では「最初はLLMで試し、信頼性が必要な部分はコード化して運用する」ハイブリッドが有効だと著者は示す。

## この記事を読むべき理由
日本のプロダクト開発現場では、コンプライアンス、安定性、コストの観点から「結果が明確で再現できる仕組み」が求められる。社内自動化を導入する際、LLMの実験性とコードの決定性をどのように共存させるかは現場レベルで直面する実務課題だ。

## 詳細解説
- 問題提起：Slack内のプルリク通知に「:merged:」リアクションを自動で付けるLLMワークフローを導入したが、誤ってマージされていないPRにも付与してしまい、運用上の信頼を損なった。
- 決定性の重要性：自動化は「人手を減らす」だけでなく「情報の信頼性」を維持することが目的。誤検知があれば利用者は自動マークを信用しなくなる。
- 実装アーキテクチャ（要点）：
  - トリガー → ハンドラが設定に応じて処理を選択。
  - LLMモード：プロンプトと許可されたツールを渡し、LLMの推奨に従ってツール呼び出しをコーディネート。過剰な呼び出しを防ぐ終了条件を持つ。
  - スクリプト（コード）モード：設定で coordinator: script を指定すると、カスタムPythonスクリプトが同じツール・データにアクセスして処理を決定。必要ならサブエージェントとしてLLMを呼ぶことも可能。
- 運用メリット：コードはコードレビュー、CI、依存管理の下で変更されるため決定性・監査性が高い。LLMは探索的・曖昧対応に強い。両者を「目的に応じて使い分ける」ことが最適解。
- 実務知見：多くの場合は「まずLLMでプロトタイプ→安定化が必要な箇所をコード化（progressive enhancement）」の流れが効く。モデルが進化しても、狭い知的判断だけLLMに頼る方針は残る。

簡単な設定例（要点）
```yaml
# yaml
coordinator: llm        # デフォルトはLLM駆動
# or
coordinator: script
coordinator_script: scripts/pr_merged.py
```

## 実践ポイント
- まずはLLMで高速にプロトタイプを作る。判断が不安定ならそこだけコード化する。
- コード化する部分は必ずコードレビューとCIで管理し、権限・依存の導入を慎重に行う。
- LLMのツールアクセスは最小権限にして誤操作を減らす。終了条件や呼び出し制限を必須化する。
- ロギングとエバリュエーション（evals）を用意し、誤判定の頻度を定量化する。閾値越えでコード化を検討。
- サブエージェント設計で「必要時のみLLMを呼ぶ」パターンを採用するとコストと信頼性のバランスが取れる。

## 引用元
- タイトル: Building an internal agent: Code-driven vs. LLM-driven workflows
- URL: https://lethain.com/agents-coordinators/
