---
layout: post
title: "Switching higher-order streams to first-order streams - 高階ストリームを一次ストリームに切り替える"
date: 2026-04-16T08:37:09.604Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://mnt.io/articles/switching-higher-order-streams-to-first-order-streams/"
source_title: "Switching higher-order streams to first-order streams"
source_id: 1236266651
excerpt: "Rust非同期でflattenとswitchの違いを実例で解説、最新優先か全処理かを直感で理解"
image: "https://mnt.io/image/site-poster.jpg"
---

# Switching higher-order streams to first-order streams - 高階ストリームを一次ストリームに切り替える
「最新だけを追うか、それとも全部処理するか？flatten と switch で学ぶ Rust 非同期ストリームの直感」

## 要約
高階ストリーム（ストリームがストリームを生む）を一次ストリーム（要素を直接出す）に変換する代表的な2つの操作、flatten と switch の違いを、Rust の実装例を交えて分かりやすく解説します。

## この記事を読むべき理由
非同期処理が増える日本の現場（Web サービス、IoT、GUI、ストリーミング処理）では、ストリームの合成や切り替えの意味を正しく理解することがバグ防止と性能改善に直結します。flatten と switch の挙動を知らないと、意図しない順序やキャンセルが発生します。

## 詳細解説
- 基本概念  
  - Iterator と Stream の対応関係：Iterator が同期的に値を返すのに対し、Stream は非同期に値を返す（Rust の簡易定義）。  
  - Poll::Pending / Poll::Ready(Some) / Poll::Ready(None) が意味するところ：準備中・値あり・終了。

- flatten の振る舞い（「全部消費してから次へ」）  
  flatten は外側ストリームが生成した inner stream を受け取り、各 inner を「完全に消費してから」次の inner を取りに行きます。外側が新しい inner を用意していても、現在の inner が閉じるまでは切り替えません。用途：各タスクを順に確実に処理したい場合（ログの逐次処理など）。

  簡略化したイメージ実装：
  ```rust
  // rust
  pub struct Flatten<Outer, Inner> {
      outer_stream: Outer,
      inner_stream: Option<Inner>,
  }
  impl<Outer> Stream for Flatten<Outer, Outer::Item>
  where Outer: Stream, Outer::Item: Stream {
      type Item = <Outer::Item as Stream>::Item;
      fn poll_next(...) -> Poll<Option<Self::Item>> {
          loop {
              if let Some(inner) = &mut self.inner_stream {
                  match inner.poll_next(...) {
                      Ready(Some(item)) => return Ready(Some(item)),
                      Ready(None) => self.inner_stream = None,
                      Pending => return Pending,
                  }
              } else {
                  match self.outer_stream.poll_next(...) {
                      Ready(Some(new_inner)) => self.inner_stream = Some(new_inner),
                      Ready(None) => return Ready(None),
                      Pending => return Pending,
                  }
              }
          }
      }
  }
  ```

- switch の振る舞い（「常に最新を反映」）  
  switch は常に外側を積極的にポーリングし、外側が新しい inner を出したら即座に現在の inner を破棄して新しい inner に切り替えます。現在の inner は外側が Pending のときにだけ進められるイメージ。用途：ユーザーの最新入力だけを反映したいライブ検索やキャンセル可能なタスク。

  簡略化したイメージ実装：
  ```rust
  // rust
  pub struct Switch<Outer> { outer_stream: Outer, inner_state: Option<Outer::Item> }
  impl<Outer> Stream for Switch<Outer>
  where Outer: Stream, Outer::Item: Stream {
      type Item = <Outer::Item as Stream>::Item;
      fn poll_next(...) -> Poll<Option<Self::Item>> {
          // まず外側をできるだけ取り出す（最新を保持）
          while let Ready(opt) = self.outer_stream.poll_next(...) {
              match opt {
                  Some(new_inner) => self.inner_state = Some(new_inner),
                  None => { outer_closed = true; break; }
              }
          }
          match &mut self.inner_state {
              None => if outer_closed { Ready(None) } else { Pending },
              Some(inner) => match inner.poll_next(...) {
                  Ready(Some(it)) => Ready(Some(it)),
                  Ready(None) if outer_closed => Ready(None),
                  _ => Pending,
              }
          }
      }
  }
  ```

- 比較まとめ  
  - flatten: 各 inner を完全に消費 → 順次処理、外側の更新は待たされる  
  - switch: 外側の最新 inner を優先 → 最新優先、古い inner は中断／破棄される

## 実践ポイント
- 使い分け例
  - flatten：ログを順番に確実に処理、バッチ的ワークフロー
  - switch：検索候補・ユーザー操作のキャンセル可能処理・ライブフィード（最新のみ）
- 実装で注意する点
  - switch は「中断・破棄」を行うため、途中状態の巻き戻しやクリーンアップを設計する（リソースリーク防止）。  
  - Pin / Context / 世代管理（どの inner が最新か）に注意する。  
- すぐ試せるサンプル（futures の stream::iter と flatten）
  ```rust
  // rust
  use futures::{executor, stream::{self, StreamExt}};
  fn main() {
      executor::block_on(async {
          let stream = stream::iter(vec![
              stream::iter(vec![1,2,3]),
              stream::iter(vec![4,5]),
              stream::iter(vec![6,7,8,9]),
          ]).flatten();
          let v = stream.collect::<Vec<_>>().await;
          dbg!(v); // [1,2,3,4,5,6,7,8,9]
      });
  }
  ```
- 日本の現場での応用ヒント  
  - マイクロサービス間のイベント処理、WebSocket の最新メッセージ優先、組み込みやリアルタイムパイプラインでの選択に有用。  
  - パフォーマンス要件や可観測性（ログ／トレーシング）を鑑みて combinator を選ぶこと。

この記事でのポイントを踏まえれば、非同期ストリーム設計で「順序を守るか・最新を優先するか」の判断が明確になります。
