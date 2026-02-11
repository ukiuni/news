---
layout: post
title: "Programming Aphorisms - プログラミングの格言集"
date: 2026-02-11T22:10:56.916Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://matklad.github.io/2026/02/11/programming-aphorisms.html"
source_title: "Programming Aphorisms"
source_id: 1157264889
excerpt: "Zigの環境変数方針から学ぶ、Options構造体と位置注入で設計を磨く実践術"
---

# Programming Aphorisms - プログラミングの格言集
コードの“トリック語彙化”：Zigの環境変数処理から学ぶ設計のコツ

## 要約
未知の問題を既知の「トリック」語彙へ還元する思考法を、Zigでの環境変数扱い変更の例を通して解説する。設計・命名・依存性注入の小さな決断が可読性と拡張性を左右する。

## この記事を読むべき理由
Zigのような言語設計の変化は、API設計やモジュール分割の普遍的な教訓になる。日本の現場でも、ライブラリ設計・コードレビュー・テストしやすさの観点で即実践できる技法が得られる。

## 詳細解説
背景：Zigがグローバルに使えていた環境変数アクセス（std.process.getEnvVarOwned）をやめ、mainから明示的に std.process.Environ.Map を渡す設計に移行中。この文脈で、readHistory 関数の設計案をどうするかが議題。

著者の提案（要点）：
- 局所的な引数より「設定オブジェクト」を定義して抽象度を上げる（HistoryOptions）。
- 環境からの生成を行う便利コンストラクタ（from_environment）を用意して、抽象化と実用性を両立させる。
- 依存性（I/Oやアロケータ）は型で明確なリソースとして位置的に注入し、挙動を変えるパラメータは Options に集約する（「positional DI」）。
- 命名にも思想があり（alloc→gpa、optionsという語彙など）、これらはチームでの伝達効率に寄与する。
- 「midlayer mistake」を避ける（中間層で責務が曖昧にならないよう、オプションはすべてユーザが設定可能にする）。
- 小さな「ショートカット（convenience）」関数は抽象層を跨いで利便性を高めるが、責務を壊さない設計が必要。

例（簡略化）：
```zig
const std = @import("std");

pub const HistoryOptions = struct {
    file: []const u8,
    pub fn fromEnvironment(env: *const std.process.Environ.Map) HistoryOptions { /*...*/ }
};

pub fn readHistory(io: std.Io, gpa: std.mem.Allocator, options: HistoryOptions) !void { /*...*/ }
```

メタ観察：著者は「コードの知識＝命名されたトリックの辞書」と捉え、他分野から効果的な手法を横取りする（horizontal gene transfer）。トリックを名前で覚えておくと瞬時に適用できる。

## 実践ポイント
- 設計時は「Options」構造体で設定を集約し、依存リソースは位置的に注入する（positional DI）。
- 環境依存の初期化は便利関数（from_environment）で提供し、コアAPIは純粋に保つ。
- 命名規約を揃える（gpa, io, options など）。命名はコミュニケーションコストを下げる。
- 中間層で責務が増えないようチェック（midlayer mistake を回避）。
- 日常的に他言語・ライブラリの「良いトリック」をメモし、チームで再利用する習慣を作る。

このアプローチはZig固有の話でありつつ、可搬性の高い設計原則として日本の開発現場でもすぐに役立つ。
