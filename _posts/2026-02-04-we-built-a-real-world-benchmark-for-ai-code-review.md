---
layout: post
title: "We built a real-world benchmark for AI code review - 実運用に即したAIコードレビューベンチマークを構築した"
date: 2026-02-04T22:16:34.812Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.qodo.ai/blog/how-we-built-a-real-world-benchmark-for-ai-code-review/"
source_title: "How Qodo Built a Real-World Benchmark for AI Code Review"
source_id: 46891860
excerpt: "マージ済PRに故意の不具合を注入しAIレビューの見落としを暴く実運用ベンチマーク公開"
image: "https://www.qodo.ai/wp-content/uploads/2026/02/Qodo-Benchmark.png"
---

# We built a real-world benchmark for AI code review - 実運用に即したAIコードレビューベンチマークを構築した
AIが見落としがちな「現場の問題」をあぶり出す、侵入型ベンチマークの全貌

## 要約
Qodoは実際にマージ済みのPRに故意に不具合や規約違反を注入して、AIコードレビューの性能（正しさと品質の両面）を大規模に評価するベンチマークを公開した。100件のPR・合計580件の問題を使い、Qodoは他7ツールより高いF1（60.1%）を達成した。

## この記事を読むべき理由
日本のプロダクト開発でも、単一ファイルのバグ検出だけでなく「リポジトリ固有の規約」「跨る依存関係」「設計レベルの問題」を検出できるAIが求められている。今回の手法は現場に近い評価指標を提示し、ツール採用や導入評価に直接役立つ。

## 詳細解説
- アプローチの差分  
  既存ベンチマークは「修正コミットから逆算」して過去のバグを単発で検出するかに偏っていた。Qodoはまず実運用でマージ済みのPRを選び、そこに複数の「機能的バグ」と「ベストプラクティス違反（コンプライアンス）」を注入することで、レビュー現場で直面する複合的な課題を再現した。  
- ベンチマーク生成の流れ  
  1) リポジトリ解析でそのプロジェクト固有のコーディング規約・ルールを抽出（ドキュメント＋コードベース解析、Agent支援＋人検証）  
  2) フィルタ条件（3ファイル以上、行数制限、リバートなし等）を満たすマージ済PRを選定  
  3) コンプライアンス侵害を差分に注入→追加で1–3件の論理バグを注入  
  4) 最終検証でグラウンドトゥルースを確定  
- 評価設定と指標  
  PRをクリーンなフォークに適用し、各ツールをデフォルト設定で動作させた。生成されたインラインコメントを「当たり（Hit）」「偽陽性」「見落とし（False Negative）」で評価し、Precision／Recall／F1を算出。  
- 結果の要点  
  多くのツールは高PrecisionだがRecallが低く、明らかな問題のみを保守的に報告する傾向。一方Qodoは高いRecallを維持しつつ競合的なPrecisionを確保し、総合F1で上回った。Qodoは運用向けに「Precise」と「Exhaustive」の2モードを持つ。  
- 対象リポジトリと拡張性  
  TypeScript、Python、JavaScript、C、C#、Rust、Swiftなど多言語・フルスタック系の実プロジェクト（例：redis、tauri、aspnetcore等）を含み、手法自体はリポジトリ非依存でプライベートコードにも適用可能。

## 実践ポイント
- 自社採用時はまず「リポジトリ固有ルール」の抽出から始める（CIにAGENTS.mdを置く運用が有効）。  
- 評価はPrecisionだけでなくRecallを重視して比較する（見落としが致命的な領域では特に重要）。  
- ツールを「Precise／Exhaustive」モードや後処理フィルタで運用ニーズに合わせて切替える。  
- 小さく試す：まず10〜20件の代表PRで導入評価を行い、誤検知パターンを収集してチューニングする。  
- IDE・PRフロー両方で検出を確認し、レビュープロセス（人＋AI）の役割分担を明確化する。

--- 
元ベンチマークとツール群は公開されており、実運用に近い評価を自社で再現して導入判断できる点が最大の価値です。
