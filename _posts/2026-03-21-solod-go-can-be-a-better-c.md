---
layout: post
title: "Solod: Go can be a better C - Solod：Goはより良いCになれる"
date: 2026-03-21T18:33:31.356Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://antonz.org/solod/"
source_title: "Solod: Go can be a better C"
source_id: 837881504
excerpt: "Go風の文法でゼロランタイムの可読Cを生成し、組込みや低レイテンシ開発に最適なSolod。"
image: "https://antonz.org/solod/cover.png"
---

# Solod: Go can be a better C - Solod：Goはより良いCになれる
Goの文法で「ゼロランタイム」なCコードを生成する――シンプルで監査しやすいシステム言語、Solodの魅力

## 要約
Solod（So）はGoの厳密なサブセットで、可読なC11を出力するコンパイラ言語。デフォルトは全てスタック割り当て、ガベージコレクションや隠れた割当てなし、Cとソースレベルで直接相互運用できるのが特徴。

## この記事を読むべき理由
日本の組込み、ゲーム、低レイテンシ領域、既存C資産と連携する開発現場では「高速で挙動が明確なコード」が求められます。Goの文法・ツールに慣れた開発者が、学習コスト低くシステム寄りのコードを書ける点は実務で即戦力になり得ます。

## 詳細解説
- 言語設計
  - SoはGoの厳密なサブセット。チャネル、goroutine、クロージャ、ジェネリクスは除外し、構造体・メソッド・インターフェース・スライス・複数戻り値・deferなどをサポート。
  - 出力は可読なC11。ランタイムは最小（zero runtime）でGCや参照カウントはない。ヒープは標準ライブラリ経由で明示的に使う設計。

- メモリモデル
  - 既定でスタック割り当て。make()はスタック上にサイズ確保、append()は容量以内のみ。自動拡張はないため、動的拡張は標準ライブラリで明示的に行う。
  - any は void* にマッピング、nil は NULL。
  - 文字列は so_String 型（ptr, len）、スライスは so_Slice（ptr, len, cap）。rune/byte/int はそれぞれ so_rune/so_byte/so_int に対応（例：so_int は 64bit）。

- C相互運用
  - cgoを使わずに、SoからCを呼び、CからSoを呼べる。生成されるCはヘッダ＋実装に分かれ、外部連携やレビューがしやすい。
  - インターフェースは self ポインタ＋関数ポインタ群の構造体に変換（ランタイム型情報は持たない）。

- 制約とトレードオフ
  - 並行処理や高級抽象（クロージャ／ジェネリクス）は使えないため、用途は主に低レイヤ／システムプログラミング。
  - スタック中心の割り当てはパフォーマンスと予測可能性を高めるが、大きなデータや可変サイズデータには注意が必要。

- 例（抜粋）
  - So（Go風ソース）
```go
package main
type Person struct { Name string; Age int }
func (p *Person) Sleep() int { p.Age += 1; return p.Age }
func main() {
  p := Person{Name:"Alice", Age:30}
  p.Sleep()
  println(p.Name, "is now", p.Age, "years old.")
}
```
  - 生成されるCのヘッダ（例）
```c
#pragma once
#include "so/builtin/builtin.h"
typedef struct main_Person { so_String Name; so_int Age; } main_Person;
so_int main_Person_Sleep(void * self);
```

## 実践ポイント
- 小さめの性能クリティカルなモジュール（数値処理、ネイティブライブラリのラッパ、組込みドライバ）から試す。
- goroutine／チャネル／クロージャを使わない既存のGoコードは移植が容易。逆に並行処理が多い設計は向かない。
- スタック割り当ての特性を理解し、巨大な静的配列や深い再帰を避ける設計を心掛ける。
- 生成Cをコードレビュー・バイナリ監査ツールにかけられるため、セキュリティ重視のネイティブ開発に向く。
- まずは小さなライブラリをSoで書いて既存Cプロジェクトに組み込み、ビルド／デバッグ／プロファイルの流れを確かめることを推奨。
