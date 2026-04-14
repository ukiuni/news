---
layout: post
title: "Debloat your async Rust - 非同期Rustの肥大化を解消する"
date: 2026-04-14T01:50:56.078Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://tweedegolf.nl/en/blog/235/debloat-your-async-rust"
source_title: "Tweede golf"
source_id: 1736122658
excerpt: "不要なasync/awaitを減らしFutureサイズを削減、組み込みやサーバのメモリを即効節約"
image: "https://media.tweedegolf.nl/images/logo-1024.png"
---

# Debloat your async Rust - 非同期Rustの肥大化を解消する
本当に必要？Asyncで増えるコード・メモリを即効で減らす5つのテクニック

## 要約
async/awaitは便利だが、コンパイラが生成する「ステートマシン」がコードサイズ・メモリ・CPUを増やす原因になる。不要なステートを減らす実践的なテクニックを紹介する。

## この記事を読むべき理由
クラウドのランニングコスト、サーバ性能、組み込み機器のフラッシュ/RAM制約――日本のプロダクト開発でも無視できない問題。少ないリソースで速く・小さく動かすための実務的知見が得られる。

## 詳細解説
- なぜ肥大化するか  
  async fn は await ごとに内部でステートを持つ未来 (future) を生成する。ステート数やステート中に保持する変数が増えると、生成コードとメモリが増える。

- 無駄な async を避ける  
  await を持たない async fn でもステートマシンが作られる。即値を返す実装は std::future::ready を返すことで小さい future にできる。
  ```rust
  // 悪い（ステートマシンが生成される）
  async fn load_default() -> Config { Config::new() }

  // 良い（Ready を返す）
  fn load_default() -> impl Future<Output = Config> {
      std::future::ready(Config::new())
  }
  ```

- 単純な委譲は await を使わず未来をそのまま返す  
  trait 実装で内部ドライバの future をそのまま返せば、余分なラッパーステートマシンが増えない。
  ```rust
  // 余分なステートマシンを作る（async）
  async fn transaction(&mut self, ...) -> Result<(), E> {
      self.transaction(address, ops).await
  }

  // ステートを増やさない（そのまま返す）
  fn transaction(&mut self, ...) -> impl Future<Output = Result<(), E>> {
      self.transaction(address, ops)
  }
  ```

- preamble/postamble がある場合は futures::FutureExt 等で出力を map する  
  map や and_then で出力変換すれば中間の await を削れる。ただし前処理を遅延実行するか即時実行するかの振る舞い差に注意。

- await をまとめる（共通の await ポイントにする）  
  同じ非同期呼び出しで結果だけ使い分けるように書き換えるとステート数を減らせる（例：match の中でそれぞれ await する代わりに先に await して値を選ぶ）。

- 大きな値は参照で渡す  
  async 内で所有を移すと future に大きなデータが丸ごと入る。配列や大きな構造体は &mut / & を使い、future のサイズ増加を抑える。

## 実践ポイント
- await を持たない関数は async にしない。std::future::ready を使う。
- 単純に他の future を返す（"pass-through"）場合は -> impl Future で返す。
- futures クレートの拡張メソッド（map 等）で postamble を実装し、余計な await を減らす。
- 同じ await を分散させず、できるだけまとめて一度だけ await する設計にする。
- 大きなバッファや構造体は所有ではなく参照で渡す。std::mem::size_of_val で future サイズを確認する習慣をつける。

上記を意識するだけで、組み込みや高負荷サーバでのメモリ・バイナリサイズ・実行効率が改善する。
