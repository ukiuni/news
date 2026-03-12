---
layout: post
title: "Kotlin creator's new language: a formal way to talk to LLMs instead of English - Kotlin創設者の新言語：英語の代わりにLLMと正式に対話する方法"
date: 2026-03-12T15:47:33.913Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://codespeak.dev/"
source_title: "CodeSpeak: Software Engineering with AI"
source_id: 47350931
excerpt: "CodeSpeak：仕様からLLMが実装を生成、コードを5〜10倍削減"
image: "https://codespeak.dev/opengraph-image?85ad0ffb0f3838a8"
---

# Kotlin creator's new language: a formal way to talk to LLMs instead of English - Kotlin創設者の新言語：英語の代わりにLLMと正式に対話する方法
CodeSpeakで「仕様を書く」開発へ――コードを5〜10倍小さくし、LLMで実装を生成する新しいプログラミング言語

## 要約
CodeSpeakはKotlinの創設者が関わる、LLMを核にした新しい言語／ワークフローで、プレーンな「仕様(spec)」から実働コードを生成し、コードベースを5〜10倍縮小できると主張します（アルファ版）。

## この記事を読むべき理由
仕様中心の開発は保守性・チーム開発・ドキュメント性を高め、日本の企業で問題になりやすいレガシー肥大化や人手不足を解決する可能性があります。実プロジェクトの事例でテストが維持・追加されている点も注目です。

## 詳細解説
- アプローチ：人間が読み書きしやすい「plain-text spec」を一級要素として扱い、LLMで実行可能なコードを生成する。手書きコードと生成コードの混在プロジェクトに対応。  
- 逆変換（Coming Soon）：既存コードから仕様を生成して置き換え、保守対象を「コード」から「仕様」にシフトする機能を目指す。  
- 効果のエビデンス：オープンソースの実ケースでLOC縮小とテスト維持を報告。例：  
  - WebVTTサポート: コード255行 → 仕様38行（6.7x短縮）、テストは増加。  
  - Italian SSN generator: 165 → 21（7.9x）など。  
- ツール状態：Alphaプレビュー／codespeak-cliなどの導入手段が用意されており、長期プロジェクトやチーム利用を念頭にしている。  
- 意味合い：仕様を中心にするとレビューや意思統一がやりやすくなり、LLMの再生成で実装差分を管理できればリファクタや移植が容易になる。

## 実践ポイント
- 危険度低めのモジュール（フォーマッタ、コンバータ、テストヘルパ等）でアルファ版を試す。  
- 既存のテストスイートを保持し、生成コードがテストを通すことを必須にする。  
- 仕様は人が読める短い単位で書き、CIで再生成→テストの流れを自動化する。  
- チームで責任範囲（誰が仕様を書くか）を明確化し、ドキュメント化と法令順守（特に日本の規制が絡む領域）を検討する。  

出典: CodeSpeak (codespeak.dev) — Alphaプレビュー、事例あり。
