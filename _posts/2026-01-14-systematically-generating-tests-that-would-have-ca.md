---
layout: post
title: "Systematically generating tests that would have caught Anthropic's top‑K bug - Anthropicのtop‑Kバグを検出したであろうテストを系統的に生成する"
date: 2026-01-14T11:58:51.904Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://theorem.dev/blog/anthropic-bug-test/"
source_title: "Theorem"
source_id: 46579387
excerpt: "定理分解＋PBTでTPUの稀なtop‑Kバグを少ない計算で高速に発見"
---

# Systematically generating tests that would have caught Anthropic's top‑K bug - Anthropicのtop‑Kバグを検出したであろうテストを系統的に生成する

もし「最もらしいトークン」がトップKから消えるような致命的なバグを、顧客に見つけられる前に自動で見つけられたら——Theoremの手法はそれを現実にします。

## 要約
Theoremは、「証明的な分解」とプロパティベーステスト（PBT）を組み合わせた手法（fractional proofs）で、AnthropicのTPU上のapproximate top‑Kバグのような稀な不具合を自動で発見できると示しました。

## この記事を読むべき理由
日本でもLLM運用や独自推論インフラの導入が進み、稀なハードウェア依存バグは大きなコストと信頼失墜を招きます。本手法は「少ない計算でレアケースを効率よく検出」する実務的なアプローチを提供します。

## 詳細解説
要点
- 問題：TPU上のapproximate top‑K実装で、最も確率の高いトークン（top‑1）が稀にtop‑K集合から漏れるバグが発生。再現には手作業でのバグ最小化が必要だった。
- 標準手法の課題：エンドツーエンドのPBTは網羅的だが稀なケースを検出するのに膨大な計算が要る。形式証明は網羅性が高いが実用的ではない。
- 解法（fractional proofs）：大きな性質（定理）をPBTとして定義し、推論に基づき再帰的に小さな部分性質に分解する。分解した小さなPBTを高速に多数回実行して稀なエッジケースを効率的に探す。

代表的な“全体定理”は次のように表せます：
$$
\forall\ \text{prompt},\ k,\quad LLM_{\text{top-1}}(\text{prompt}) \in LLM_{\text{top-}k}(\text{prompt})
$$

分解例（トップレベル→中間→ユニット）
- end-to-end: 最頻トークンがtop‑kに含まれることを確認するPBT
- 中間定理: approx_max_kの出力の最大値が元配列の最大値と一致すること、ロジットが有限であること、トークンIDとロジット辞書の整合性 等
- ユニットPBT: 配列を小さな入力空間に制限してapprox_max_kの性質を高速で検証

実際には、bin分割（L個のビン）に基づく近似top‑KアルゴリズムやXLA/TPUの余剰精度問題といった実装依存の欠陥を、分解して検出しています。分解の停止基準は「各サブテストが十分速い」「入力分布の十分な割合をカバーする」「サブ性質が合成可能で全体性質を保証する」ことです。

簡単なPBTスニペット例（概念）：
```python
@given(k=st.integers(min_value=0, max_value=TOP_K_RANGE), arr=arr_strategy)
def test_approx_max_k(k, arr):
    N = len(arr)
    k = int(k % min(N - MIN_TOP_K, TOP_K_RANGE)) + MIN_TOP_K
    approx_values, _ = lax.approx_max_k(arr, k=k)
    assert jnp.max(approx_values) == jnp.max(arr)
```

## 日本市場との関連
- 日本企業もクラウドGPU/TPUやオンプレ推論を増強しており、ハードウェア依存の稀バグはサービス停止や品質問題に直結します。
- 少ない検証コストで高い信頼性を確保する手法は、スタートアップから大手製造業のAI導入まで幅広く有用です。
- 規制や品質保証の観点でも「説明可能で再現可能なテスト」が評価されやすく、fractional proofsは監査対応にも寄与します。

## 実践ポイント
- まず「守るべき全体性質（定理）」を明確化してPBT化する。例：top‑1はtop‑kに含まれる。
- 定理を推論で再帰的に分解し、ユニットレベルまで落とす。小さな入力空間で高速に回せるPBTを作る。
- Hypothesisなど既存のPBTフレームワークをCIに組み込み、分解後のユニットPBTを並列で大規模に走らせる。
- 実装依存（精度や並列実行の挙動）を意識した中間定理を用意し、ハードウェア差異を局所化する。
- 再現できたテストは必ず最小化してユニットテスト化し、デプロイ前に回すルールを整備する。

短くまとめると、fractional proofsは「推論による分解」と「高速PBTの大量実行」を組み合わせ、稀な実装バグを実用的なコストで捕まえる手法です。日本のAI開発現場でも即効性のある投資対効果が期待できます。
