---
layout: post
title: "I'm spending 3 months coding the old way - AI全盛期にあえて「手で書く」3ヶ月"
date: 2026-04-17T21:21:58.063Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://miguelconner.substack.com/p/im-coding-by-hand"
source_title: "I&#x27;m Coding by Hand - Miguel Conner"
source_id: 47807583
excerpt: "AIを封印して3ヶ月手書きコーディングし、基礎理解と実機最適化の力を取り戻した体験記"
image: "https://substackcdn.com/image/fetch/$s_!K739!,w_1200,h_675,c_fill,f_jpg,q_auto:good,fl_progressive:steep,g_auto/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F619758e3-8a22-4eff-aa30-e86effa991cd_1536x1024.png"
---

# I'm spending 3 months coding the old way - AI全盛期にあえて「手で書く」3ヶ月
AIに頼らずコードを書くと、見える世界が変わる — ブルックリンのレトリートで著者が再発見した“職人としての力”

## 要約
著者はRecurse Centerで3ヶ月のコーディングリトリートを行い、LLMやコーディングエージェントに依存せず「手で書く」ことで得た技術的理解と実践的スキルの重要性を再確認した。

## この記事を読むべき理由
AIがコード生成を当たり前にする今、短期的な生産性と長期的な理解のトレードオフをどう扱うかは日本の開発現場にも直結する。育成や採用、プロダクト品質に関心のある人は知っておくべき話題です。

## 詳細解説
- 目的と背景：著者は「LLMを一から学ぶ」「手で書くPython力を高める」「コンピュータの理解を深める」を目標にRC（自己主導のプログラミング合宿）へ参加。AIが便利な今だからこそ基礎力を鍛える意図がある。
- LLMを“スクラッチ”で扱う：Stanfordの課題を通じ、トークナイザーやGPT-2風アーキテクチャをPyTorchで自前実装。Tiny StoriesやOpenWebTextでの学習・ハイパーパラメータ調整、A100での短時間トレーニング、FlashAttention2をTritonで実装するなど、実機寄りの最適化にも踏み込んでいる。
- コーディングエージェントとの関係：エージェントは迅速な反復と“チューター”として有効だが、設計要件が曖昧だとエージェントは勝手に仮定を埋めてしまい、結果としてコードベースを深く理解できない危険がある。深い知識がある人ほどAIを有効活用できるという逆説も示された。
- ハンズオンでの学び：ペアプロでの短い試行（端末で即実験する習慣）、古いマシンでのBASIC体験、Vimでの手作業、CTFでのUnixスキル向上、Clojureのモブプログラミングなど、多様な実践が理解を加速させた。
- 文化的要素：短時間のテクニカルトークや共同作業の場が学習を促進。成果は“全部を終わらせること”よりも“集中してコードを書く時間”そのものに価値があるという認識。

## 実践ポイント
- 1週間だけでも「LLMを補助にしない」期間を作って小さなプロジェクトを一から実装する（例：簡単なトークナイザー＋小型Transformer）。
- ペアプログラミングを定期化し、分からない構文は端末で即試す癖をつける（Google検索より手を動かす）。
- Advent of CodeやCTFでターミナル・Unixスキルを鍛える。
- GPUプロファイリングやFlashAttentionなど、実機最適化の基本を1つ学ぶ（TritonやPyTorchのプロファイラを触る）。
- AIは「チューター／コーチ」として使い、設計や基礎理解は自分の手で掘り下げるバランスを保つ。

（元記事：I'm spending 3 months coding the old way — Miguel Conner）
