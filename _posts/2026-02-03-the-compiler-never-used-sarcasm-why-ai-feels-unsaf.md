---
layout: post
title: "The Compiler Never Used Sarcasm: Why AI Feels Unsafe to the Neurodivergent Coder - コンパイラは皮肉を言わない：AIが神経発達差異のあるコーダーにとって不安に感じられる理由"
date: 2026-02-03T20:52:32.726Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://dev.to/btarbox/the-compiler-never-used-sarcasm-why-ai-feels-unsafe-to-the-neurodivergent-coder-30i3"
source_title: "The Compiler Never Used Sarcasm: Why AI Feels Unsafe to the Neurodivergent Coder - DEV Community"
source_id: 3210948
excerpt: "確実性が消えたAI時代、神経発達差のあるコーダーが安心して書ける聖域をどう取り戻すか"
image: "https://media2.dev.to/dynamic/image/width=1000,height=500,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Fyhk4fwqqg1o429wr1ze7.png"
---

# The Compiler Never Used Sarcasm: Why AI Feels Unsafe to the Neurodivergent Coder - コンパイラは皮肉を言わない：AIが神経発達差異のあるコーダーにとって不安に感じられる理由
クリックせずにはいられないタイトル: コンパイラの「確かさ」が消えた日 — AI時代に安心してコードを書ける場所はどこへ行ったのか？

## 要約
従来のコンパイラが与えてくれた「明確さ（正誤の二値性）」が、生成AI／LLMによる確率的な応答に置き換わり、特に神経発達差異（neurodivergent）を持つ開発者には心理的負担と不安を生んでいる、という問題提起。

## この記事を読むべき理由
AIツールは便利だが、根底にある設計思想（決定論 vs 確率論）が変わると、これまで「安全」と感じていたワークフローが崩れる。日本の開発現場でも英語でのあいまいさや説明責任、検証コストが増すため、広く知っておくべき話題です。

## 詳細解説
- コンパイラの安心感：従来のプログラミングは命令→実行が文字通りで、エラーは明確なフィードバックだった。これは特に明確なルールやパターンを好む人にとって「聖域」だった。  
- LLMの本質：大規模言語モデルは言語の統計的な「次単語予測」を基礎にしており、出力は確率的。つまり「予測（token）」であって「確証（bit）」ではない。  
- ブラックボックスとTheory of Mind：NNは解答に至る過程が不透明で、人間同士のあいまいな会話に似た振る舞いをする。神経発達差異のある人にとって、人間の意図を推測する負担が再び発生する。  
- 実際の危険性：言語のあいまいさは現実の事故にも繋がる（パイロットの「takeoff power」誤解など）。AIへの曖昧な指示も、機能誤動やバグの温床になりうる。  
- 情報理論的視点：シャノンの「ビット（確実性）」から「エントロピー（言語の不確実性）」へのパラダイムシフトが進行中で、開発プロセスの検証負荷が上がる。

## 実践ポイント
- 出力を鵜呑みにしない：生成物は必ずユニットテストや静的解析で検証する。  
- プロンプトは「交渉」であると意識する：期待する出力の形式（入力例／出力例、制約）を明示して曖昧さを減らす。  
- 小さな決定論的ツールと組み合わせる：パーサ、型チェック、CI を使って「確実に検証できる層」を残す。  
- アクセシビリティ配慮：日本語・英語のあいまいさが影響する場面では、文言の標準化・テンプレート化を進める。  
- Explainabilityとログ：LLMの出力生成に対して理由（根拠）を求めるプロンプトや出力差分のログを必ず保存する。  
- チーム文化の再設計：言語的な交渉力に偏らない評価基準と、神経発達差異のあるメンバーへの配慮（明確な仕様、書面での指示）を導入する。

短く言えば、AIは強力だが「確かさ」を自動で保証しない。ツールの性能を引き出すには検証と設計の習慣を変え、あいまいさをシステムで吸収する仕組みが必要です。
