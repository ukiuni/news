---
layout: post
title: "Making an LSP for great good - LSPを大いなる善のために作る"
date: 2026-01-21T16:44:49.368Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://thunderseethe.dev/posts/lsp-base/"
source_title: "Making an LSP for great good · Thunderseethe's Devlog"
source_id: 422444735
excerpt: "Rustでクエリ駆動・red-greenキャッシュのLSPを作り、瞬時で正確な補完と定義ジャンプを実現"
---

# Making an LSP for great good - LSPを大いなる善のために作る
魅せるコンパイラ：エディタ上で「速く」「正確に」答える言語サーバをRustで作る方法

## 要約
クイックに応答するLSP（Language Server Protocol）は、増え続ける言語×エディタの組合せ問題を解くために、インクリメンタルな「クエリベース」コンパイラを核に実装すると強力になる、という話。

## この記事を読むべき理由
日本の開発現場でもVSCodeやNeoVim等のエディタ利用が一般化しています。大規模コードベースや教育用途で「瞬時の型情報」「goto定義」「補完」が効くと生産性が跳ね上がるため、LSPとクエリ型コンパイラの仕組みを理解しておくと、自作言語・ツール開発や社内言語サポートで役立ちます。

## 詳細解説
- バッチ型コンパイラ（全体を順に処理する）と対照的に、クエリベースは「問い合わせ（query）」単位で結果をキャッシュし、依存のみを再計算する。これにより編集操作へ素早く反応できる。
- クエリの要件：純粋関数で副作用が無く、結果がキャッシュ可能で、依存関係はDAG（有向非巡回グラフ）で表現する。
- クエリエンジンの3つの役割：クエリ実行、結果キャッシュ、依存トラッキング。実装上は「入力クエリ（ファイル内容等）」にsetterを設け、更新時に影響するクエリのみ再評価する。
- red-greenアルゴリズム：各（引数付き）クエリキャッシュに red/green フラグを持たせる。依存が全てgreenなら再実行不要。再実行後に結果が変わればgreen→red（または逆）を適切に更新する。これで冗長な再計算を防止。
- 実装上の要素（Thunderseethe の要約）
  - QueryKey（クエリ識別子）を列挙型で定義し、各クエリと引数を一意化。
  - Database：各クエリ用のキャッシュ（例：content_of, cst_of…）を DashMap 等の並行マップで保持。color map と revision（変更カウンタ）を持つ。
  - DepGraph：petgraph の DiGraph で依存を記録し、あるクエリがどのクエリを参照したかを追えるようにする。
  - 実際のLSPは tower-lsp を使い、プロトコル処理はライブラリに委任。LSP側では hover, goto definition, autocomplete 等の代表機能を最小限実装すれば十分に体感できる。
- Rustでの実装例（抜粋イメージ）：

```rust
// rust
enum QueryKey {
    ContentOf(Uri),
    CstOf(Uri),
    NewlinesOf(Uri),
    // ...
}
```

```rust
// rust
impl QueryContext {
    fn query<V: PartialEq + Clone>(
        &self,
        key: QueryKey,
        cache: &DashMap<QueryKey, V>,
        producer: impl FnOnce(&Self, &QueryKey) -> V,
    ) -> V { /* red-green 実行ロジック */ }
}
```

## 実践ポイント
- まずは最小限の入力クエリ（file content → CST → AST → types）を作り、LSPではhover/goto/completionを繋いで動作確認する。
- キャッシュと依存関係の記録は外せない。並行処理が必要なら DashMap 等を使う。
- 実装を楽にするなら salsa のような既成クエリフレームワークを検討する（ただし学習コストあり）。
- LSP実装は tower-lsp で素早く立ち上げ、プロトコルの詳細よりレスポンス速度と正確さに注力する。
- 日本語ドキュメントやエディタ拡張（VSCode拡張など）で利用者体験を整えれば社内採用が進む。

このアプローチは「エディタで生のコンパイラ挙動を体感」させ、開発効率を実際に向上させる力があります。興味があれば、まずは小さな言語でQuery→LSPを構築してみてください。
