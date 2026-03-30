---
layout: post
title: "Formally verifying digital circuits with category theory in Lean - カテゴリ理論とLeanで回路を形式検証する"
date: 2026-03-30T22:16:17.798Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://matt.hunzinger.me/2026/03/28/circuits.html"
source_title: "Formally verifying digital circuits with category theory in Lean | Matt Hunzinger"
source_id: 410160191
excerpt: "カテゴリ理論×Leanで四値論理の加算器を形式証明する実践ガイド。"
---

# Formally verifying digital circuits with category theory in Lean - カテゴリ理論とLeanで回路を形式検証する
カテゴリ理論×Leanで「証明済み」の加算器を作る：数本のワイヤから始めて回路の振る舞いを定理として証明する手法を紹介

## 要約
カテゴリ理論を使って組合せ回路を対等・結合性・交差の法則でモデル化し、Lean（Lean4）上で四値論理と基本ゲートを定義して加算器の振る舞いを形式的に証明しています。

## この記事を読むべき理由
ソフトウェアだけでなくハードウェアの信頼性・安全性が問われる日本の組込み／半導体開発現場で、回路を「実装して測定する」だけでなく「数学的に正しい」と保証する技術は即戦力になります。Leanとカテゴリ理論はその入り口を実用的に示します。

## 詳細解説
- モデル化の核：この記事は「組合せ回路」を対象に、オブジェクトをワイヤの数、射（morphism）をワイヤ間の回路とする対称モノイダル圏（symmetric monoidal category）で回路を表現します。並列接続はテンソル $⊗$、直列接続は合成 $≫$（関数合成に同型）で扱います。  
- 四値論理：実世界の断線や短絡を表現するためにBelnap由来の四値論理を採用し、回路の意味論（denotational semantics）を定義して射が実際にどう振る舞うかを数学的に記述します。  
- 圏の法則で配線の安全性を保証：結合子（associator）$α$ による再結合が結果を変えないこと（パンタグン則）、単位元との相互作用（トライアングル則）、ワイヤ交差が結合と整合すること（ヘキサゴン則）、および交差の自己反転性（対称性）などを満たすことで配線操作が意味論的に安全だと保証します。例えば再結合の直感は
  $$((A\otimes B)\otimes C)\otimes D \simeq A\otimes (B\otimes (C\otimes D))$$
  と表現されます。
- Leanでの実装例：Lean上でオブジェクトを自然数（OfNat）として扱い、基本ゲート（and/or/not）や分岐（fork）を射として定義。さらにコピー回路を作り、xor／halfAdder／adderを構成して、それぞれについて入力の全場合（Boolの場合分け）で期待する出力になることを簡潔に証明しています。証明は反射や単純な場合分け（`by cases x; rfl`）で済む箇所が多く、定義から意味論までをLeanに書かせる流れが示されています。例（notの意味論）：
```lean
-- Lean
theorem not_def (x : Bool) : not.val #v[↑x] = #v[↑(!x)] := by cases x; rfl
```

## 実践ポイント
- まずLean4と関連ライブラリ（mathlib相当や circuitlib）をセットアップして、記事にあるnot→xor→halfAdder→adderの流れを手で追ってみる。  
- 四値論理やモノイダル圏の直感（並列＝横に並べる、直列＝つなぐ）をツールに落とし込み、実装と定理の対応関係を体感する。  
- 日本の用途：ASIC/FPGAの小ブロック（加算器、論理ユニット、シリアル変換回路等）を形式検証してから合成ツールに渡すワークフローに適用可能。安全クリティカルや車載・医療機器分野での信頼性向上に直結します。  
- 次の挑戦：順序回路（状態を持つ回路）のモデル化や非同期回路の扱いはまだ研究分野。記事の手法を学んだら、順序回路の表現（ストリーム関数や因果性）に拡張してみましょう。

興味があれば、元記事の circuitlib 実装をローカルで動かし、加算器の定理を実際にLeanでチェックしてみてください。
