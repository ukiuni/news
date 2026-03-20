---
layout: post
title: "Attention Residuals - アテンション残差"
date: 2026-03-20T19:23:58.334Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/MoonshotAI/Attention-Residuals"
source_title: "GitHub - MoonshotAI/Attention-Residuals · GitHub"
source_id: 47458595
excerpt: "層ごとに過去出力を選択的に集約し、学習安定化と下流性能を同時に改善するAttnRes"
image: "https://opengraph.githubassets.com/171f3e2127f0e757913e934d5d5ea9dd470306a79ed65b8707f42bbdf5712fd7/MoonshotAI/Attention-Residuals"
---

# Attention Residuals - アテンション残差

魅力的な日本語タイトル: 層ごとに「振り分ける」残差――Transformerの深さを賢く使う新手法、AttnResの全貌

## 要約
AttnResはTransformerの固定残差合算を、各層が過去の出力に対して入力依存のアテンションで選択的に集約する仕組みで、学習安定化と性能向上を同時に実現します。

## この記事を読むべき理由
PreNormで深さが増えると貢献が希薄化する問題は日本の大規模モデル開発・ファインチューニングでも現実的な障壁です。AttnResはその根本対策になり得るため、研究・実装の両面で即チェックに値します。

## 詳細解説
従来の残差は層出力を単純に足し合わせるため、深くなるほど各層の寄与が希薄化し、隠れ状態の大きさが発散しやすい（PreNorm問題）。AttnResはこれを次の式で置き換えます：

$$\mathbf{h}_l = \sum_{i=0}^{l-1} \alpha_{i \to l} \cdot \mathbf{v}_i$$

ここで重み $\alpha_{i \to l}$ は各層ごとの学習された擬似クエリ $\mathbf{w}_l \in \mathbb{R}^d$ に基づくsoftmax注意で計算され、各層が「どの過去表現を重視するか」を入力依存に決定します。  
完全版（Full AttnRes）は全過去層に出席するためメモリが $O(Ld)$ となりますが、実用的な解としてブロック化（Block AttnRes）を導入。層をNブロックに分け、ブロック単位で集約することでメモリを $O(Nd)$ に削減し、約8ブロック程度でFullに近い利得を得られると報告されています。

主な効果：
- 学習挙動：出力の大きさが深さで発散しにくく、勾配が層に均等に分配される傾向
- スケーリング：同じ計算予算で常にベースラインより良い損失を示し、Block版はベースラインを1.25×の学習に相当する性能に近づける
- 下流タスク改善：推論力・推論ステップが要求される問題やコード生成で顕著（例：GPQA-Diamond +7.5、HumanEval +3.1など）

## 実践ポイント
- 小さく始める：大規模化前にBlock AttnResを試す（目安：N≈8）。メモリ増は最小限でほとんどの利得を得られる。  
- モニタリング：隠れ状態ノルムや各層の注意分布を可視化して、どの深さが実際に参照されているか確認する。  
- 適用先の選定：マルチステップ推論やコード生成を重視する日本語モデルやファインチューニングで特に効果が出やすい。  
- 実装：GitHubリポジトリはAttnResのPyTorch風擬似実装とPDFを提供。既存Transformerの残差を置き換える「drop-in」感覚で試せる。  
- 計算資源：フル版はメモリ負荷が高いので、実運用ではBlock版を推奨。

この記事で紹介した手法は、深さを「賢く参照」させることで学習効率と下流性能を同時に改善する実用的なテクニックです。まずはBlock AttnResで手元のモデルに差分導入して挙動を確認してください。
