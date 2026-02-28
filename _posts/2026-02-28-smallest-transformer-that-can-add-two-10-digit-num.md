---
layout: post
title: "Smallest transformer that can add two 10-digit numbers - 2つの10桁の数を足せる最小トランスフォーマー"
date: 2026-02-28T01:11:17.203Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/anadim/AdderBoard"
source_title: "GitHub - anadim/AdderBoard: Smallest transformer that can add two 10-digit numbers"
source_id: 47170030
excerpt: "数百パラメータで10桁加算を99%達成、手作36・学習311の最小モデル"
image: "https://opengraph.githubassets.com/1af82512e445710edfaa88872f3216002aa9ec874e56c35c6a2fe16ea992c1fa/anadim/AdderBoard"
---

# Smallest transformer that can add two 10-digit numbers - 2つの10桁の数を足せる最小トランスフォーマー
たった数百パラメータで10桁の足し算を解く──「最小モデル」争いの舞台裏を覗く

## 要約
GitHubのAdderBoardチャレンジは、自己注意を備えた自己回帰トランスフォーマーで「二つの$10$桁の整数の和」を$ \ge 99\% $精度で解くための最小構成を競うもの。手動設定（構成的証明）と学習済み（SGD 等で学習）の両方の最小化が進み、手作りで36パラメータ、学習済みで311パラメータという驚くべき成果が出ています。

## この記事を読むべき理由
小さく効率的なモデル設計は、組み込み・エッジ推論やコスト最適化、モデル理解の教材として直結します。日本のスタートアップ／組込み系開発者やAI教育にとって「何が本当に必要か」を示す良い実例です。

## 詳細解説
- ルールの核：モデルは「自己注意を持つ自己回帰トランスフォーマー」であること。forward()は標準のテンソル入力→ロジット出力で、桁ごとの繰り上がり（carry）はモデルの出力で生じなければならない。推論ループに問題固有のロジックを埋め込むのは不可。
- 参加カテゴリ：手動設定（hand‑coded）＝アーキテクチャが加算を表現できることの構成的証明、学習済み（trained）＝汎用最適化で発見可能であることの実証。
- 主要テクニック
  - ペアトークン（digit pairs）やトークン化工夫で入力圧縮
  - 低ランク／rank-3因子分解でパラメータ削減
  - ALiBi（対数スロープ＝log(10)など）やRoPEなどの位置エンコーディングを桁位置に最適化
  - curriculum learning や grokking（学習ダイナミクスの利用）
  - 手作り解では浮動小数点精度（float64）や特殊ゲートでさらに圧縮
- コミュニティの知見：パラメータ数約800付近で精度が急落する「パラメータクリフ」が観察され、単層（1L）が同予算では二層より有利という傾向。手作りは学習可能性を考慮しないためさらに小さくできる。

## 実践ポイント
- リポジトリをクローンして README と verify.py を読む。検証は `verify.py submissions/your_submission.py --seed 2025` で10,000対の固定テストを使う（必須条件は $ \ge 99\% $）。
- 小型化を試すなら：トークン化（ペア化）、rank-3 因子化、ALiBi の斜率調整（base-10を意識）を順に導入して効果を評価する。
- 学習派はカリキュラム学習と学習率スケジュール、初期化の工夫で「grokking」を活用する余地あり。
- 教育用途には最小モデルのソースを分解して、注意機構・桁合わせ・繰り上がりの発生を可視化すると理解が深まる。

参考：GitHub リポジトリ（AdderBoard）にはリーダーボード、提出テンプレート、検証スクリプトが揃っています。興味があればまずフォークして手を動かしてみてください。
