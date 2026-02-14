---
layout: post
title: "Show HN: Sameshi – a ~1200 Elo chess engine that fits within 2KB - 約1200 Elo・2KBに収まるチェスエンジン"
date: 2026-02-14T15:06:22.763Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/datavorous/sameshi"
source_title: "GitHub - datavorous/sameshi: a ~1200 Elo chess engine that fits within 2KB"
source_id: 47014500
excerpt: "2KBのC実装で約1170Elo、αβ探索と完全な合法手検査を備えた最小チェスエンジン"
image: "https://opengraph.githubassets.com/a447b9595db6abfd10afa3f4fedec3077c493d1685da707b26b5ab0c84bc7bab/datavorous/sameshi"
---

# Show HN: Sameshi – a ~1200 Elo chess engine that fits within 2KB - 約1200 Elo・2KBに収まるチェスエンジン
2KBの奇跡：ミニマルなC実装で学ぶチェスAIの基本

## 要約
Sameshiは約2KBに収まるC製のミニマルチェスエンジンで、Negamax＋αβ枝刈り、素材評価、完全な合法手検査を持ち、実戦強度は約1170 Elo（95% CI:1110–1225）です。

## この記事を読むべき理由
小さなコードベースでチェスAIの核となるアルゴリズム（ボード表現、探索、評価、手生成）を学べるため、アルゴリズム学習、組み込み/省メモリ開発、コンテスト向けのアイデア源として最適です。日本の教育現場や趣味のハードウェアプロジェクトでも応用しやすい設計です。

## 詳細解説
- 実装と言語: リポジトリは主にC（main.c, sameshi.h）。ヘッダは約1.95KBで非常にコンパクト。
- ボード表現: 120セルの「mailbox 120」方式を採用（境界ガードが容易で手生成が単純）。
- 探索: Negamaxアルゴリズムにαβ枝刈りを適用。固定深さ探索（深さ5）で動作。
- 評価: 素材評価のみ（駒価値合算）を基本にし、シンプルな評価関数。
- 手順の工夫: 捕獲優先の手並べ（capture-first move ordering）を採用し枝刈り効率を向上。
- 合法手検査: チェック/チェックメイト/ステイルメイトの判定を含む「完全な合法手検証」を実装。
- 制約・未実装: キャスリング、アンパッサン、昇格、繰り返し規則、50手ルールは未実装。
- 強さと評価方法: Stockfish（レベル1320–1600）との240局の対局で評価。固定深度5、ルールを制約、最大60半手（plies）で約1170 Eloを得たとのこと。
- 用途的観点: デモシーン的なサイズ勝負、アルゴリズム学習教材、組み込み機器での簡易AIとして適合。

## 実践ポイント
- まず動かす（Makefileあり）:
```bash
# Clone and build
git clone https://github.com/datavorous/sameshi.git
cd sameshi
make
./sameshi
```
- 学習用途: sameshi.h を読んで、ボード表現・手生成・αβの流れを追うのが効率的。
- 拡張課題（練習案）: 昇格・キャスリング・アンパッサンを追加して強化、評価関数に位置評価（テーブル）を導入して比較してみる。
- 小型環境応用: IoTデバイスや組み込みコンテストでの「サイズ対性能」トレードオフ研究に活用可能。
- ベンチ方法: Stockfish等との固定深度対戦や自己対局でEloを再計測し、変更ごとの影響を定量化する。

オリジナルリポジトリ: https://github.com/datavorous/sameshi
