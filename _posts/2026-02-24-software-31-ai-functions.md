---
layout: post
title: "Software 3.1? – AI Functions - Software 3.1? — AI関数"
date: 2026-02-24T16:22:40.082Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://blog.mikegchambers.com/posts/software-31-ai-functions/"
source_title: "Software 3.1? - AI Functions | Mike G Chambers"
source_id: 47138718
excerpt: "仕様だけでLLMが実行・Pydantic検証しネイティブ結果を返す新ランタイム"
image: "https://blog.mikegchambers.com/assets/images/ai-functions-2.png"
---

# Software 3.1? – AI Functions - Software 3.1? — AI関数

ランタイムで「生成→実行→検証」を自動化する──AIがコードを書くだけでなく実行し、ネイティブオブジェクトを返すSoftware 3.1の衝撃

## 要約
AI Functionsは、自然言語で仕様を書くだけでLLMがその場でコードを生成・実行し、Pydanticなどの型付きネイティブPythonオブジェクトを返し、毎回ポストコンディションで自動検証・再試行する仕組みです。開発時だけでなくランタイムでAIを活用する新しいパラダイムを提案します。

## この記事を読むべき理由
日本でもデータ処理、自動化、プロトタイピングの需要は高く、AI Functionsは「人がコードを書く負担」を下げつつ実行時の柔軟性を提供します。一方でローカル実行や再試行ループの運用・セキュリティ設計が必須になるため、導入判断に必要なポイントを短く整理します。

## 詳細解説
- パラダイムの変化  
  - Software 3.0：プロンプトでコード（文字列）を生成し、人が統合・検証する。  
  - Software 3.1（提案）：仕様→（LLMが）生成→実行→ポストコンディションで検証、失敗なら自動でフィードバック→再試行。ランタイムでAIが動く点が本質的な違い。

- コア概念  
  - @ai_functionデコレータ：関数の実装を空にしてドキュメンテーション（自然言語）で仕様を書くと、呼び出し時にLLMが実装を生成して実行する。  
  - ネイティブオブジェクト返却：JSONではなくDataFrameやDBコネクションなど実行中のPythonオブジェクトを直接返せる（ローカル実行を許可した場合）。  
  - Pydantic等の型連携：戻り値に型を指定すればスキーマ検証が入り、不正なら自動で再試行。  
  - ポストコンディション：通常のPython関数で書くアサーション（決定論的検査）や、AI関数自身を使った品質チェック（非決定論的）を組み合わせられる。失敗メッセージが生成側LLMへのフィードバックになる。  
  - 実行モデルと信頼：code_execution_mode="local"は明示的有効化、許可インポート列挙、AST検査やタイムアウトなどの緩和策があるが完全なサンドボックスではない。運用ではコンテナ分離や監視が重要。

- ワークフロー適用例  
  - フォーマット不明なログを一つのAI関数でDataFrame化→別のAI関数で分析→経営向け要約作成、という普通の関数合成で複雑ワークフローが実現可能。

## 実践ポイント
- 小さく始める：非機密なCSV解析や要約などから試す。  
- スキーマを明確化：Pydanticで戻り値を定義し、期待形を厳密にする。  
- 決定的なポストコンディションを増やす：まずはPythonのアサーションで検証可能な条件を作る。  
- ローカル実行は最小化：必要な関数だけcode_execution_mode="local"を有効にし、許可インポートを限定する。  
- 分離と監視：本番はコンテナやプロセス分離、リソース監視（ループやメモリ膨張対策）を必須にする。  
- 運用観点：自動再試行の回数やレート制限、可観測性（ログ、メトリクス）を設計する。  
- 適用領域の検討：ETL、レポート自動生成、フォーマット不定データ取り込み、プロトタイピングに向く。機密処理や厳格なセキュリティ環境では慎重に。

簡単なイメージ例（Pydantic返却＋ポストコンディション）:
```python
python
from ai_functions import ai_function
from pydantic import BaseModel

class Summary(BaseModel):
    key_points: list[str]
    action_items: list[str]

def check_nonempty(summary: Summary):
    assert summary.key_points, "key_points must not be empty"

@ai_function(post_conditions=[check_nonempty])
def summarize_transcript(transcript: str) -> Summary:
    """Summarize the transcript into key points and action items."""
```

日本の現場では「実行時に扱えるオブジェクト」で手早く価値を出せる一方、運用・セキュリティ設計を怠るとリスクになる点を忘れずに。導入は段階的に、まずは観測性と最小権限から。
