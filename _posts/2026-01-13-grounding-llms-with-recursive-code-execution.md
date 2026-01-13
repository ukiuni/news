---
layout: post
title: "Grounding LLMs with Recursive Code Execution - 再帰的コード実行でLLMを根付かせる"
date: 2026-01-13T07:56:04.904Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://yogthos.net/posts/2026-01-12-recursive-language-model.html"
source_title: "(iterate think thoughts): Grounding LLMs with Recursive Code Execution"
source_id: 1069469090
excerpt: "TypeScriptを生成しサンドボックスで実行、文書を正確に検証する"
---

# Grounding LLMs with Recursive Code Execution - 再帰的コード実行でLLMを根付かせる
魅せるタイトル: 「AIに『プログラムを書かせて調べさせる』――LLMのいい加減さをコード実行でつぶす新アプローチ」

## 要約
LLMが文書を「推測」して回答するのではなく、モデルにTypeScriptコードを書かせて安全なサンドボックス内で実行し、得られた事実をもとに答えを確定する手法（Recursive Language Model, RLM）を紹介する。

## この記事を読むべき理由
LLMの“でっち上げ（ハルシネーション）”は日本の企業での決算・契約書解析や法務調査でも重大な問題。RLMは「読む」のではなく「問いをプログラムとして実行して確かめる」ため、正確性が求められる現場に直結する実用性が高い。

## 詳細解説
- 問題点
  - 大きな文書でもトークン数が増えても、モデルは全体を正確に把握せず見積もりで答える傾向がある（例：売上合計を単に推測して誤答）。
  - RAG（埋め込み＋ベクタ検索）は概念的に近い箇所を取ってくるが、「数える」「正確に区別する」などの操作には弱い。

- RLMの核心アイデア
  - 文書そのものには直接働きかけず、読み取り専用としてサンドボックスに渡す。
  - モデルは「どう調べるか」をコード（TypeScript）で書き、そのコードをサンドボックス（isolated-vm等）で実行して結果を得る。
  - 実行結果は不変の事実（ex. regex が返した文字列や計算結果）として扱われ、モデルはそれを読み取り次のステップを決める。ループを回して十分に検証できたら最終回答を出す。

- 実装上の工夫
  - 安全性：isolated-vmで外部アクセスや危険なコマンドを遮断。ドキュメントは読み取り専用。
  - インターフェースを厳密に定義（UTCPパターン）してモデルに関数シグネチャを提示。例：
```typescript
// TypeScript
declare function fuzzy_search(query: string, limit?: number): Array<{
  line: string;
  lineNum: number;
  score: number; // 0 to 1 confidence
}>;
```
  - モデルが書いたコードの文法エラーや欠落インポートを自動補正する「セルフヒーリング」層を用意し、往復を減らす。
  - 典型的な探索ループ：
```typescript
// TypeScript (擬似)
while (!hasAnswer) {
  // モデルが生成したTSコードをサンドボックスで実行
  const output = sandbox.exec(modelCode);
  modelReads(output);
  modelWrites(nextModelCode);
}
FINAL("..."); // モデルが確証を得た段階で最終回答
```

- トレードオフ
  - イテレーションを重ねるため遅く・トークンを多く消費する可能性があるが、大きな文書を丸ごとコンテキストに読み込む必要が減るためトータルで有利になることもある。

- エコシステムとの親和性
  - ローカル環境（Ollama＋Qwen-Coder等）でも動くし、DeepSeekのような強力なホストモデルでも利用可能。
  - MCP（Model Context Protocol）サーバとして公開すればエージェント（例：Crush）からツールとして呼び出せる。Matryoshka実装は公開されている（https://github.com/yogthos/Matryoshka）。

## 実践ポイント
- 小さく試す：まずは「散らばった売上金額を合算する」など単純なタスクで、モデルに探索用TSコードを書かせるデモを作る。
- 厳格なツール契約を用意する：fuzzy_search / text_stats / slice 等、提供するAPIを型で明示しモデルに「できること」を限定する。
- セキュリティ第一：sandbox化は必須。読み取り専用のドキュメントと外部アクセス遮断を徹底する。
- エラー耐性を設ける：モデル生成コードの簡易修正（セミコロン不足や誤ったimport修正）で往復を減らすと実用性が上がる。
- エージェント連携：MCP経由でRLMをツール化すれば、高レベルの指示を出すだけでエージェントが精密な調査を任せられる。

短期的には「LLMに丸投げして誤答を受け取る」運用からの脱却、長期的には社内ドキュメントの自動精査・監査ワークフローへの適用が期待できる。興味がある場合はMatryoshkaのリポジトリを眺めつつ、小さなサンドボックス実験から始めると良い。
