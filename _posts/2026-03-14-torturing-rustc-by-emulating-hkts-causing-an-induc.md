---
layout: post
title: "Torturing rustc by Emulating HKTs, Causing an Inductive Cycle and Borking the Compiler - HKTsをエミュレートしてrustcを苦しめ、帰納的サイクルでコンパイラを壊す"
date: 2026-03-14T12:12:02.443Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.harudagondi.space/blog/torturing-rustc-by-emulating-hkts/"
source_title: "Torturing rustc by Emulating HKTs, Causing an Inductive Cycle and Borking the Compiler — ramblings of @harudagondi"
source_id: 1310266920
excerpt: "RustでHKTsを真似したら型の帰納的サイクルでrustcがE0275を出す原因と回避法"
image: "https://www.harudagondi.space/uploads/torturing-rustc/dynamic-wang.jpg"
---

# Torturing rustc by Emulating HKTs, Causing an Inductive Cycle and Borking the Compiler - HKTsをエミュレートしてrustcを苦しめ、帰納的サイクルでコンパイラを壊す
魅力的タイトル: Rustで「型の型（HKT）」を真似したらコンパイラがパニックに — 新米でも分かる原因と対処法

## 要約
記事は、RustでHigher-Kinded Types（HKTs）をエミュレートしようとした結果、Trait評価の帰納的サイクルが発生してrustcが「overflow evaluating requirement（E0275）」で止まる事例を解説します。根本は「型の再帰的展開」がトレイト境界評価を無限に誘発する点です。

## この記事を読むべき理由
Rustを使ってライブラリ設計や汎用的データ構造を作る際、GAT（Generic Associated Types）や「型コンストラクタの真似」による落とし穴は現実に遭遇します。日本の開発現場でもコンパイル不具合やデバッグで時間を浪費しがちなので、原因の把握と回避パターンは役立ちます。

## 詳細解説
要点をかみくだいて説明します。

- HKTsとは？
  - 普通のジェネリクスは「型」を受け取るが、HKTsは「型コンストラクタ」（例: Vec）自体を抽象化して、さらに型引数を与えて使える概念です。Rustは直接のHKTsを持たないため、GATやトリックで近似します。

- 著者がやったこと（概念）
  - trait Wrap { type Wrapper<T>; } のようなGAT的トレイトを用意し、Wrapper を通して Spanned<T> / Simple<T> のような包みを一般化。
  - しかし enum Ast<W: Wrap> の各フィールド型に W::Wrapper<Ast<W>> のように書くと、型展開が自己参照的に深くなります。

- なぜコンパイラがバグるのか
  - #[derive(PartialEq)] 等がトレイト境界（例えば Wrapper<Ast<W>, Range>: PartialEq）を評価しようとすると、Wrapper の中身が再び Ast<W> を含み、同じ境界を再要求する……という具合に評価が帰納的にループします。
  - rustc はこの再帰を無限に評価しようとして「overflow evaluating the requirement（E0275）」や「inductive cycle」のようなエラー/内部処理限界に達します。これは言語仕様というより、評価アルゴリズムと設計の相互作用で生じる実用的な落とし穴です。

## 実践ポイント
すぐ使える対処法と回避策を示します。

1. 包む位置を変える（簡単で有効）
   - 各フィールドを個別に W::Wrapper<Ast<W>> するのではなく、Ast<W> 全体を一度包む（SpannedAst { inner: Ast<W>, span }）ことで自己参照の深さを減らし、境界の再帰を断ち切れることが多いです。

   ```rust
   // 悪い例（再帰的に展開してしまう）
   enum Ast<W: Wrap> {
       Binary { left: Box<W::Wrapper<Ast<W>>>, /* ... */ },
       /* ... */
   }
   ```

   ```rust
   // 良い例（Ast全体を一度だけ包む）
   struct SpannedAst<W: Wrap> { inner: Ast<W>, span: Range<usize> }
   enum Ast<W: Wrap> {
       Binary { left: Box<Ast<W>>, /* ... */ },
       /* ... */
   }
   ```

2. deriveを盲目的に使わない
   - 深い再帰を含む型では #[derive(PartialEq/Debug/…)] が無限境界を生成することがあるので、必要なら手動実装で境界を明示的に制御する。

3. 抽象レベルを落とす
   - 本当にHKTsが必要か見直し、Concreteな型（マーカー型や明示的Wrapper）を使う設計に落とすと安全です。

4. 代替手段の検討
   - GATを適切に使う、もしくは標準的な新型（newtype）ラッパーを使って型の展開を明確にする。場合によってはBox/Rcで再帰構造を外側に置く。

5. バグ報告とツール運用
   - 再現最小ケースを作ってrustcのissueに報告すると、コンパイラ改善につながります。VSCode内でテストを最小化して試すと再現が早いです（integrated terminal / output paneを活用）。

以上を押さえれば、HKTsを真似する際の落とし穴を避け、設計上のトレードオフを明確にできます。
