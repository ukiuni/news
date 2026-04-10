---
layout: post
title: "Clojure on Fennel Part One: Persistent Data Structures - Fennel上のClojure（第1回）：永続データ構造"
date: 2026-04-10T17:03:45.248Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://andreyor.st/posts/2026-04-07-clojure-on-fennel-part-one-persistent-data-structures/"
source_title: "Clojure on Fennel part one: Persistent Data Structures · Andrey Listopadov"
source_id: 47669923
excerpt: "Neovim開発者必読：Fennel上でClojureの永続構造を再現、性能と落とし穴を解説"
image: "https://andreyor.st/me.jpg"
---

# Clojure on Fennel Part One: Persistent Data Structures - Fennel上のClojure（第1回）：永続データ構造
クリックしたくなる見出し: FennelでClojureの不変データ構造を再現する挑戦 — Lua/Neovim開発者が知るべき実装と落とし穴

## 要約
Clojureの永続データ構造（HAMTベースのハッシュマップ、ビット分割トライのベクター、永続赤黒木など）をFennel/Lua上で再実装したimmutable.fnlの解説。設計選択、性能トレードオフ、実運用で注意すべきポイントをまとめる。

## この記事を読むべき理由
- LuaやFennelで不変データ構造を使いたい人（Neovimプラグイン、ゲーム、組み込みスクリプト）に実装知識と実践的な注意点を教える。
- ClojureのコレクションをFennel上で再現する際の妥協（分岐率、ハッシュ、トランジェント）の理由が分かる。

## 詳細解説
- 背景: 著者は既存の実験的ライブラリ（fennel-cljlib）を土台に、Clojure互換のコンパイラ（ClojureFnl）を作る過程で性能問題に直面。copy-on-writeの単純実装は配列で致命的に遅く、置き換えが必要になった。
- 主要実装:
  - Persistent HAMT（ハッシュ配列マップトライ）を実装。分岐率は16（Clojureは32）を採用し、Luaの環境差やビット操作コストを考慮した設計。
  - Persistent Vectorはビット分割トライ（分岐率32）で、インデックスで直接辿る方式。appendは実質的にO(1)、lookup/updateはO(log N)。
  - 永続的赤黒木（ソート済みマップ/セット）にはOkasakiやGermane & Mightのアルゴリズムを使用。
  - トランジェント（一時的にミュータブルにしてまとめて処理する最適化）をサポートし、性能改善に寄与。
- ハッシュと衝突回避:
  - 文字列等のハッシュにdjb2を採用（ビット演算が無いLua互換性のため）。衝突対策としてロード時ランダム化を行い、さらに永続コレクションにはプロトタイプ（オブジェクトの実体）アドレスでソルトを付加して、同じ内容の“可変テーブル”と“永続マップ”が同じバケットに入り不整合を起こすのを防いでいる。
- API（代表）:
  - マップ: new, assoc, dissoc, conj, contains, count, get, keys, vals, transient, from, to-table, iterator。トランジェント側は assoc!, dissoc!, persistent。
  - ベクター: new, conj, assoc, count, get, pop, transient, subvec。トランジェント側は assoc!, conj!, pop!。
- 性能トレードオフ:
  - ネイティブのLuaテーブルと比べると多くの操作が数十〜数百倍遅い。ただし単位操作のコストはマイクロ秒オーダーで、用途によっては許容できる場合もある（特に読み中心や変更が少ないケース）。
  - LuaJIT環境では相対差は改善されるが、ネイティブテーブルの速さが際立つため依然差は大きい。
- 実装上の判断:
  - 配列（ベクター）では高い分岐率、マップではビット幅/分岐率の妥協が必要。Luaの実行系特性を踏まえた調整が重要。

## 実践ポイント
- 小規模の不変マップならネイティブテーブルで十分だが、構造共有や構文的な不変性を明示したい場合はimmutable.fnlを検討する。
- 変更操作を多く行うバッチ処理にはトランジェントを使ってから最終的に永続化すると性能改善が大きい。
- Neovimプラグインやゲームで使う場合は、必ず自環境（PUC Lua / LuaJIT）でベンチマークを取り、分岐率やハッシュ関数のチューニングを検討する。
- 不変コレクションをキーにする場合は「可変テーブルと永続マップのハッシュ差」を意識する（作者はプロトタイプのアドレスでソルトして回避）。
- まずはimmutable.fnlを試し、hot path（頻繁に更新される箇所）はネイティブ構造やトランジェントで補う運用を推奨。

オリジナル記事（英語）: https://andreyor.st/posts/2026-04-07-clojure-on-fennel-part-one-persistent-data-structures/
