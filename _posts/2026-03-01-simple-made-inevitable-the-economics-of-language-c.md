---
layout: post
title: "Simple Made Inevitable: The Economics of Language Choice in the LLM Era - LLM時代の言語選択の経済学：単純さは不可避"
date: 2026-03-01T04:41:49.502Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://felixbarbalet.com/simple-made-inevitable-the-economics-of-language-choice-in-the-llm-era/"
source_title: "Simple Made Inevitable: The Economics of Language Choice in the LLM Era"
source_id: 393823770
excerpt: "LLM時代、Clojure的な不変性と小さな抽象で保守コストとLLMトークン消費を劇的に抑える方法"
image: "https://felixbarbalet.com/content/images/size/w1200/2026/02/Gemini_Generated_Image_mlqylgmlqylgmlqy.png"
---

# Simple Made Inevitable: The Economics of Language Choice in the LLM Era - LLM時代の言語選択の経済学：単純さは不可避
AIがコードを書く時代、言語選びが“資本配分”を左右する — Clojureが示す「単純さ」の経済性

## 要約
LLM（大規模言語モデル）の登場で「習熟のハードル」はほぼ消え、言語選択の本質は「単純さ（accidental complexityを減らす抽象）」に移った。Clojureのようなデータ志向・不変性・小さな抽象は、LLMと組むと技術的負債の雪だるま化を抑えられる。

## この記事を読むべき理由
- 日本の開発現場でもLLM活用が加速中。選ぶ言語で将来の維持コストが大きく変わるため、今の判断が長期的な生産性とコストに直結します。

## 詳細解説
- 基本概念：Fred Brooksの「本質的複雑さ vs 偶発的複雑さ」およびRich Hickeyの「simple（単純）とeasy（容易）」の区別。業界は長らく「慣れやすさ」を優先してきたが、LLMはその優位性を奪う。
- 学習コストの消失：LLMは構文の馴染みや学習曲線を気にしないため、「人にとってeasy」だった理由が価値を失い、抽象の質（単純さ）が重要になる。
- ブラウンフィールド障壁：小さなコード量では差が見えにくいが、10万行規模になると偶発的複雑さの累積でLLMも処理できなくなる（McKinneyの指摘）。言語の選択は長期的な「利回り」になる。
- Clojureの優位点
  - トークン効率：Rosetta Code等の分析でClojureはPythonより約19%少ないトークンで同等のロジックを表現できる。LLMのコンテキスト窓は有限なため有利。
  - 不変性：ミュータブルな状態に起因する防御的ボイラープレート（nullチェックや同期処理）が減る。LLMが生成する「余計な複雑さ」を物理的に防げる。
  - データ志向（マップ等）：汎用操作（assoc, mergeなど）で扱えるため、クラスごとのAPI学習が不要になり、スケール時の認知負荷が線形に済む。
  - REPLフィードバック：即時評価で小さな単位の検証ができ、コンパイルループ中心のワークフローより短い検証サイクルを実現。ただし、REPLは不変性と組み合わせた場合に効果を発揮する点が重要。
- 対照例としてGo：人間にとって読みやすい「易しい」設計は冗長なトークンを生み、LLMのコンテキスト資源を浪費する可能性がある。

## 実践ポイント
- 新規プロジェクトや大規模リファクタでは「単純さ」を重視する（データ第一、不変性、小さな抽象）。
- LLM活用時はトークン消費を定量化する（重要ファイルで実際のトークン量を測る）。
- 小さな関数と共通のデータ操作APIを設計して、エージェントが一貫したツールセットで作業できるようにする。
- REPLや即時検証ループを取り入れ、LLM→実行→検証の短いフィードバックを回す（不変データと組み合わせること）。
- 既存の大規模コードベースは「言語を替えれば万事解決」という期待を捨てず、段階的に偶発的複雑さを削る戦術を採る。

（原著者：Felix Barbalet の論考を日本語向けに要約・再構成）
