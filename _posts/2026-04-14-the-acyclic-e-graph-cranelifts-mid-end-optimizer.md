---
layout: post
title: "The acyclic e-graph: Cranelift's mid-end optimizer - 非巡回e-グラフ：Craneliftのミッドエンド最適化器"
date: 2026-04-14T16:00:10.047Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://cfallin.org/blog/2026/04/09/aegraph/"
source_title: "The acyclic e-graph: Cranelift&#x27;s mid-end optimizer"
source_id: 47717192
excerpt: "Craneliftのaegraphで純演算を海に浮かべ、パス順序問題を一発解決する実用的最適化設計"
---

# The acyclic e-graph: Cranelift's mid-end optimizer - 非巡回e-グラフ：Craneliftのミッドエンド最適化器
Cranelift流・実用的e-グラフ入門 — パス順序問題を一発で解く「浮遊ノード」の考え方

## 要約
Craneliftは純演算（副作用なし）をCFGの「骨格」から引き離して海のように浮かべ、浅い等価性（hash-consing）と局所的な書換で最適化を行うaegraph（acyclic e-graph）を導入した。これによりパス順序問題を抑えつつ実運用できる中間最適化器が実現された。

## この記事を読むべき理由
パス順序の問題（複数最適化が相互に作用して何度も繰り返す必要がある）を現実的に解く設計で、JITやWasmランタイムなどで実用的なコンパイラ性能改善を狙う日本のエンジニアにとってすぐに応用できる発想が詰まっているため。

## 詳細解説
- 問題意識：GVN（値の正規化）、LICM（ループ外移動）、定数伝播、冗長ロード除去など複数のパスが相互依存すると「何度も全関数を走らせないと収束しない」事態が発生する（pass-ordering problem）。
- 基本方針：副作用のない演算だけをCFGから切り離した「sea-of-nodes-with-CFG」を作る。副作用のある命令は従来通りの「骨格（side-effect skeleton）」に残す。
- canonicalization（hash-consing）：純演算ノードは内容でハッシュコンスして重複を消す。これにより同一計算は一度だけ最適化対象になり、重複した書換の繰り返しを防ぐ。
- 実装フロー（概念）：
  1. 純演算をCFGから「持ち上げ」て海に入れる（lift）。
  2. ドミネンス順などで深さ帰納的にハッシュコンスして同値化（canonicalize）。
  3. 海（aegraph）上で書換ルールを適用（rewrite／リライト群、リマテリアライズ等を含む）。
  4. 最後にノードをCFGへスケジュールして順序を決める（elaboration）。
- aegraphの工夫：従来のe-graph（完全な等価飽和）をそのまま持ち込むとコストが高いため、まずは「一つのenodeからなる自明なeclass」を出発点にして巡回（acyclic）性や運用効率を重視する設計にしている。多様なリライトルールを統一的に扱いつつ、実運用向けに効率化している点が肝。

## 実践ポイント
- 純演算と副作用命令を明確に分離する設計を検討する（Wasm/JITの中間表現に有効）。
- ハッシュコンス（内容ハッシュでの再利用）を導入すれば、同一式に対する書換を一回で済ませられる。
- HAC（dom-tree preorder）で定義を先に処理する順序を採ると深い式木の同値化が自然にできる。
- 小さなリライトルール群から始め、ノードのスケジューリング戦略（どこへ戻すか）で効果が大きく変わるため実測でチューニングする。
- リソース制約がある環境では「完全飽和」より「非巡回で局所的な収束」を優先すると実用性が高い。

元記事は設計意図、実装上のトレードオフ、評価まで詳述しているので、実装や最適化戦略を検討する際は原文を併せて参照すると良い。
