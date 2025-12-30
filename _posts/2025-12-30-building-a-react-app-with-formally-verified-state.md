---
layout: post
title: "Building a React App with Formally Verified State - 形式手法で検証された状態を持つReactアプリを構築する"
date: 2025-12-30T16:38:45.119Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://midspiral.com/blog/building-a-react-app-with-formally-verified-state/"
source_title: "Building a React App with Formally Verified State"
source_id: 1595851593
excerpt: "状態が壊れないReactをDafnyで実現する実践ガイドと導入チェックリスト"
---

# Building a React App with Formally Verified State - 形式手法で検証された状態を持つReactアプリを構築する
React×Dafnyで「状態が壊れない」UIを作る方法 — 実践レポートと導入チェックリスト

## 要約
Dafnyで状態遷移を形式検証し、検証済みの状態管理をJavaScriptへコンパイルしてReactアプリに組み込んだ実践レポート。設計→UI確認→証明の順で進めることで、仕様と実装のズレを早期に潰した点が要旨。

## この記事を読むべき理由
日本のプロダクトで求められる信頼性（金融、医療、組込み、規制対応）に直結する手法。LLMを補助にして形式仕様を書き、実用的なUIと検証済みロジックを両立させるワークフローは、品質向上と開発効率の両立に有効です。

## 詳細解説
- 概要  
  - 作例はColorWheel（5色パレット生成）。ユーザー操作（生成、微調整、undo/redoなど）はすべてDafnyで定義された「検証済みカーネル」を通る。結果的に状態破損が理論上不可能になる。

- 仕様設計とLLMの役割  
  - 著者はClaude Codeとの対話で仕様を詰めた。LLMからの詳細質問（例えば「softとは何か」「パレットサイズ固定か」）が、仕様の曖昧さを露呈させ、より厳密な設計につながった。結果的にDafnyの仕様ファイル（ColorWheelSpec.dfy）と自然言語のDESIGN.mdが整備された。

- Dafnyでの検証サイクル  
  - 初回のverifyで型や前提（requires）の不備、添字範囲などが検出される。TypeScriptの厳格モードと似た利点はあるが、Dafnyは「遷移不変量を全遷移で保つ」ことを証明できる点が強み。量化子（forall）の扱いでSMTが分断する問題に対しては、共通の述語に切り出す（predicate AllColorsSatisfyMood(...)）ことで解決した。

- UIとの統合と発見の価値  
  - 先にReactで動かしてから証明に入る戦略を採用。これにより「意図とUI挙動のズレ」を早期に発見（ボタン名と実挙動が逆になっていた等）。UIを動かしてから証明すれば、無駄な証明工数を避けられる。

- 実装的な落とし穴と対処  
  - Dafny→JS変換で出る差分例：Dafny Seq<int>がJS配列でない、整数がBigNumberラッパーになる等。ロギングで検体を確認し、変換ルールに合わせてラップ/アンラップを行うことで解決した。

- 証明の分離設計  
  - Proofファイル（ColorWheelProof.dfy）を仕様ファイルとドメインファイルから分離することで可読性を確保。ドメインは薄く、実証はProof側へ集中させる構成が推奨される。

## 実践ポイント
- 仕様は「UI設計より先」に厳密化するが、UIは先に動かしてユーザー体験を検証する。
- LLMは「質問を引き出す設計アシスタント」として有効。曖昧な点を突かせると仕様品質が上がる。
- Dafnyでは前提（requires）や不変条件を明示すること。TypeScriptのstrictに相当する恩恵がある。
- 証明はドメインコードから分離して保守性を確保する（spec → proof → domainの依存）。
- インタープロップ問題（Seq vs Array, BigNumber等）はログで実態を確認して明示的変換を挟む。
- 量化子によるSMTの扱いに注意。共通の述語へ切り出すと証明が通りやすくなる。
- チェックリスト（導入時）
  - 仕様の自然言語版(DESIGN.md)を自動生成してレビューする
  - UIのプロトタイプを先に用意して仕様と照合する
  - Dafnyでverify→見つかったrequires/範囲エラーを潰す
  - 変換結果をロギングしてJS側の形状を確認する
  - 証明は別ファイルにしてCIで再検証可能にする

## 引用元
- タイトル: Building a React App with Formally Verified State  
- URL: https://midspiral.com/blog/building-a-react-app-with-formally-verified-state/
