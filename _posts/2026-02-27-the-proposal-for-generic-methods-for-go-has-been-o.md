---
layout: post
title: "The proposal for generic methods for Go has been officially accepted - Goのジェネリックメソッド提案が正式に受理されました"
date: 2026-02-27T16:23:02.588Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/golang/go/issues/77273#issuecomment-3962618141"
source_title: "spec: generic methods for Go · Issue #77273 · golang/go · GitHub"
source_id: 395111025
excerpt: "Go言語でメソッド単位のジェネリクス導入、API設計やインターフェース互換性に直接影響"
image: "https://opengraph.githubassets.com/6515c1e60fa78736dd1059ddae6e2e1024b07893384db33ec60b95eefac7809e/golang/go/issues/77273"
---

# The proposal for generic methods for Go has been officially accepted - Goのジェネリックメソッド提案が正式に受理されました

Goにジェネリックメソッドが来る――実務で使えるかを端的に解説

## 要約
Goの言語仕様が「メソッド自身が型パラメータを持てる」ことを許容する方向で受理されました。メソッド宣言の構文拡張と呼び出し時の型引数指定／型推論が導入されますが、インターフェースのメソッドはジェネリック化されません。

## この記事を読むべき理由
サーバー開発やクラウドネイティブ実装でGoを使う日本のエンジニアは、API設計・ライブラリ設計に直接影響します。特に型安全なユーティリティやコレクション設計で新しい選択肢が生まれます。

## 詳細解説
- 何が変わるか  
  - メソッド宣言で関数と同様に型パラメータを宣言可能に。構文は関数のTypeParametersをメソッド名の直後に置く形に変わります。  
  - メソッド呼び出しは明示的な型引数指定（s.M[int](42)）か、呼び出し側の引数からの型推論で行われます。  

- インターフェースとの関係（重要）  
  - インターフェースのメソッド自体は型パラメータを持てないため、ジェネリックメソッドをもつ型はそのメソッドを理由にインターフェース実装と見なされません。つまり「ジェネリックメソッド = インターフェース互換」にはなりません。  
  - 例: 非ジェネリックな io.Reader をジェネリックReadで満たすことはできません（(*Reader).Read[E any] は io.Reader を実装しない）。  

- メソッド式/メソッド値  
  - ジェネリックメソッドから得られるメソッド式やメソッド値はジェネリック関数として扱われ、既存のジェネリック関数ルールが適用されます。  

- 実装面の影響  
  - パーサや型チェックは比較的小さな修正で済みますが、コンパイラのバックエンドでの実装やランタイム・インポート/エクスポートフォーマットは注意が必要。  
  - リフレクションでは未インスタンス化のジェネリックメソッドを名前やインデックスで参照できない制約が残ります。

- 例（要約）  
  - 単純なジェネリックメソッド:
```go
type S struct{}
func (s *S) M[P any](x P) {}
s := S{}
s.M[int](42)     // 明示指定
s.M("hello")     // 推論
```
  - ジェネリック受信型＋メソッド:
```go
type G[P any] struct{}
func (g *G[P]) M[Q any](x Q) {}
var g G[string]
g.M(123)
```
  - インターフェース非互換の例:
```go
type I interface { M(string) }
type H struct{}
func (H) M[P any](P) {}
var h H
var _ I = h // コンパイルエラー: ジェネリックメソッドは I に適合しない
```

## 実践ポイント
- 公開API設計では「ジェネリックメソッドだからインターフェース実装になる」と期待しないこと。インターフェースと組み合わせる設計は要検討。  
- まずは内部ユーティリティや非公開ライブラリで試験的に導入して互換性とツールチェーン（linters, codegen, reflection利用箇所）を確認する。  
- リリースノートとGoツール（コンパイラ、gofmt、vet、reflect）の対応状況を確認してから本番採用する。  
- 既存の型デザイン（特に io 系やミドルウェアの抽象化）を見直し、ジェネリックメソッドでコードが読みやすくなる箇所を優先的に検討する。

出典: golang/go issue #77273（提案受理）
