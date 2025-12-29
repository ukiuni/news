---
layout: post
title: T-Ruby is Ruby with syntax for types
date: 2025-12-27 02:06:01.519000+00:00
categories:
- tech
- world-news
tags:
- tech-news
- japan
source_url: https://type-ruby.github.io/
source_title: Type-safe Ruby | T-Ruby
source_id: 46395871
excerpt: T-RubyでTypeScript風の型注釈をRubyに導入、.rb/.rbsを生成
---
# Rubyに型の魔法を注入する — T-RubyでTypeScriptライクな静的型チェックがやってきた

## 要約
T-Rubyは、TypeScriptのように「型付き構文」をRubyに導入する実験的コンパイラ。`.trb`ファイルにインラインで型注釈を書き、標準の`.rb`と`.rbs`を生成して既存のRubyエコシステムと互換性を保つ。

## この記事を読むべき理由
Rubyは日本のWeb開発やレガシーシステムで根強い人気があるが、大規模化すると型の欠如が保守性の障害になる。T-Rubyはランタイム依存なしで静的型を導入でき、既存ツール（RBSやLSP、エディタ拡張）と連携するため、段階的導入やCIでの型チェックの実現に有用。

## 詳細解説
- 概要  
  T-RubyはRubyの文法を拡張して、メソッドや変数にインラインで型注釈を書くための`.trb`フォーマットを導入するコンパイラ。コンパイル結果として型情報を取り除いた通常の`.rb`と、型シグネチャを記述した`.rbs`を生成する点が特徴。実行時の依存を追加せず、RBS互換のため既存の型チェックツールやエコシステムと親和性が高い。

- TypeScript風の体験  
  TypeScript同様、コード内に直接型を書くことで、メソッドシグネチャの可視化・静的検査を行える。タイプミスや不整合を開発時に捕まえやすくなるため、リファクタや大人数チームでの開発にメリットがある。

- 既存ソリューションとの比較  
  - Sorbet: ランタイムgem（sorbet-runtime）に依存し、sigブロックというDSLで型を宣言する。実行時チェックや高度な型表現が可能だが導入コストがある。  
  - RBS/TypeProf: RBSは型定義を別ファイルで書くアプローチ（静的型の仕様）、TypeProfは型推論ツール。T-Rubyはインライン注釈からRBSを生成する点で差別化される。

- ワークフローと互換性  
  - インストール: `gem install t-ruby`  
  - 初期化とウォッチモード: `trc --init` / `trc --watch`（コンパイルして`.rb`と`.rbs`を出力）  
  - エディタ統合: VS Code拡張、JetBrainsプラグイン、Neovimプラグイン、LSP対応で既存の編集環境に溶け込む設計。  
  - 互換性: 生成物は標準のRubyとRBSなので、Rubyのどのバージョンや既存のgemとも基本的に併用可能。

- 制約と現状  
  T-Rubyは実験段階。コアコンパイラは動作するが未完成の部分があり、すべての型表現やRubyのダイナミズムを網羅しているわけではない。導入は段階的に行い、CIでの型チェック追加や現行コードとの整合性確認を推奨。

例（簡単な`.trb`入力と生成物）:

```ruby
# hello.trb
def greet(name: String) : String
  "Hello, #{name}!"
end

def add(a: Integer, b: Integer) : Integer
  a + b
end
```

生成される（抜粋）:

```ruby
# hello.rb (生成)
def greet(name)
  "Hello, #{name}!"
end

def add(a, b)
  a + b
end
```

```ruby
# hello.rbs (生成)
def greet: (name: String) -> String
def add: (a: Integer, b: Integer) -> Integer
```

## 実践ポイント
- まずは小さなモジュールやライブラリで試す：影響範囲を限定して型注釈を増やすことで安全性を評価する。  
- CIに型チェックを組み込む：`trc`の結果やLSPの型警告をCIでFailさせることで型品質を保てる。  
- RBS出力を活用する：生成された`.rbs`は既存の型チェッカー（Steepなど）やSorbetのRBSインポートに使える。  
- エディタ統合で体験を向上：VS Code拡張やLSPを導入してリアルタイムで型フィードバックを得る。  
- コントリビュートとフィードバック：まだ実験的なので、現場でのユースケースやバグ報告がプロジェクト改善に直結する。

