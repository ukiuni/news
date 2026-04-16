---
layout: post
title: "Qwen3.6-35B-A3B on my laptop drew me a better pelican than Claude Opus 4.7 - Qwen3.6-35B-A3Bが私のノートでClaude Opus 4.7より良いペリカンを描いた"
date: 2026-04-16T20:20:22.322Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://simonwillison.net/2026/Apr/16/qwen-beats-opus/"
source_title: "Qwen3.6-35B-A3B on my laptop drew me a better pelican than Claude Opus 4.7"
source_id: 47796830
excerpt: "ローカル21GB量子化QwenがMacでClaude Opus 4.7を上回るペリカン自転車SVGを生成"
image: "https://static.simonwillison.net/static/2026/qwen-opus-card.jpg"
---

# Qwen3.6-35B-A3B on my laptop drew me a better pelican than Claude Opus 4.7 - Qwen3.6-35B-A3Bが私のノートでClaude Opus 4.7より良いペリカンを描いた
ローカルで動く21GBモデルが、意外にも「ペリカン自転車」イラスト勝負でAnthropicの最新Opusを上回った話

## 要約
Simon Willisonが、自分のMacBookで動かした量子化Qwen3.6-35B-A3B（約21GB）が、AnthropicのClaude Opus 4.7より「ペリカンが自転車に乗るSVG」などの生成タスクで良好な結果を出したと報告しています。ローカル量子化モデルの実用性が改めて示されました。

## この記事を読むべき理由
ローカルで動く大型モデルが手元のマシンで実用的になってきた今、プライバシー重視の日本企業や個人開発者が低コストで高度な生成を試せる可能性が高まっています。最新動向を押さえることで導入の判断や実験がスムーズになります。

## 詳細解説
- 何が行われたか：Willison氏はLM Studio＋llm-lmstudioプラグイン上で、Unslothが公開した量子化ggufモデル（Qwen3.6-35B-A3B-UD-Q4_K_S、約20.9GB）をMacBook Pro M5で動かし、同氏の“ペリカンが自転車に乗る”ベンチマークを実行。Anthropicのクラウド版Claude Opus 4.7とも同じタスクで比較しました。  
- 結果：Qwenが生成したSVGの完成度が高く、Opusはフレームなどを崩す失敗をしたケースがあり、Qwenに軍配が上がったと報告。別の「一輪車に乗るフラミンゴ」テストでもQwenが良い結果を出しています。  
- 意味合い：この比較はジョーク的ベンチマークにも見えますが、生成物の質とモデルの実用性には一定の相関があります。重要なのは「量子化＋ローカル実行で実用レンジに入りつつある」という点。ただしWillison氏自身も、汎用的な性能でOpusが劣るとは断言していません。  
- 技術的ポイント：量子化（gguf Q4系など）によりモデルサイズが劇的に落ち、MシリーズCPUでも扱えるように。LM StudioのようなローカルUIとプラグインで扱いやすくなっています。

## 実践ポイント
- LM Studio + llm-lmstudioでgguf量子化モデルを試す（Unsloth配布モデルが手軽）。  
- SVGなどの生成はプロンプト設計で差が出るので同一プロンプトで比較テストを行う。  
- 「thinking_level」などモデル固有の設定が結果に影響するためパラメータを調整して比較する。  
- ローカル実行はプライバシーとコスト面で有利。社内プロジェクトやプロトタイプ作成に有効。  
- モデルのライセンスと出自を確認し、商用利用やセキュリティ要件に注意する。
