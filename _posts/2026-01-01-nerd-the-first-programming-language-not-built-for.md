---
layout: post
title: "Nerd: The First Programming Language Not Built for Humans - 人間向けに作られていない初のプログラミング言語「NERD」"
date: 2026-01-01T01:38:05.459Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.nerd-lang.org/about"
source_title: "Nerd: The First Programming Language Not Built for Humans"
source_id: 46450217
excerpt: "NERDはLLM生成を前提にトークン削減しLLVMへ直コンパイルする、人間非最適化の実験言語"
---

# Nerd: The First Programming Language Not Built for Humans - 人間向けに作られていない初のプログラミング言語「NERD」
LLMが「読むためのコード」を卒業させる？AI時代のソースコード再発明、NERD入門

## 要約
NERDは「人間が読むこと」を最優先しない言語設計を採り、LLM（大規模言語モデル）が効率的に生成・処理できることを前提にした実験的言語。英単語トークンを活かし、トークン数を削減してそのままLLVMでネイティブにコンパイルする。

## この記事を読むべき理由
日本でもAIがコード生成を担う割合が急増している中、NERDは「人が書かない前提」の開発ワークフローを具体化する最前線の試み。コスト、レビュー、監査、CI運用に与える影響は日本のプロダクション現場でも現実的な検討事項になる。

## 詳細解説
- 背景：LLMがソースコード生成の主要著者になりつつあり、従来の「人が読むこと」を最適化した言語設計（記号ベース、構文糖）はLLMにとって非効率的。例えば波括弧や===などは複数トークンに分解されやすいのに対し、"plus"や"if"は1トークンで済む傾向がある。
- 設計思想：NERD = No Effort Required, Done Not human-friendly。密で簡潔な英語キーワードを使い、同等のロジックで50–70%のトークン削減を狙う。ランタイム不要でLLVM IRへ直接コンパイルするため、追加依存がない。
- 例（原文抜粋）：
```text
fn add a b
  ret a plus b

fn calc a b op
  if op eq zero ret ok a plus b
  if op eq one  ret ok a minus b
  ret err "unknown"
```
- ワークフロー：人間は要件（例：「レート制限を追加」）を出し、LLMがNERDを生成・修正。生成物はネイティブ実行可能で、人間は読み取り・監査を行う。人は執筆者ではなくステークホルダーになるというパラダイムシフト。
- 反論への応答：デバッグや監査は高レベルの抽象（自然言語）や翻訳ビューで行うという主張。可監査性は「人が書くこと」と同義ではないとする。

## 実践ポイント
- 小規模で試す：まずは内部ユーティリティやバッチ処理でNERD→LLVMワークフローを試験運用、トークン利用とコスト差を測定する。
- 可視化レイヤーを用意：監査用にNERDから「自然言語／図／データフロー」への自動翻訳ビューを作る。規制対応が必要な分野（金融、医療）では必須。
- CI/テストを固定化：LLM生成物は頻繁に変わるためテスト・型・静的解析をパイプラインに組み込み、変更をLLMに指示する運用を確立する。
- ガバナンス設計：誰が要件を出し、誰が監査するのかを明確化。LLM出力の責任とトレーサビリティを定義する。
- 技術観察：LLVM連携、トークナイザ挙動、生成コストの変動、OSSの成熟度（NERDはApache 2.0で公開）を継続的にウォッチする。

## 引用元
- タイトル: Nerd: The First Programming Language Not Built for Humans  
- URL: https://www.nerd-lang.org/about
