---
layout: post
title: "Resolving Names Once and for All"
date: 2025-12-28T01:13:15.686Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://thunderseethe.dev/posts/nameres-base/"
source_title: "Resolving Names Once and for All"
source_id: 436643208
excerpt: "Rust風実装で学ぶ、スコープとシャドーイングを一度で解決して識別子を一意IDへ変換する方法"
---

# 名前解決を完全制覇 — スコープとシャドーイングを一度で「機械向け」に変える技術

## 要約
ソース中の人間可読な名前（識別子）を、コンパイラが扱いやすい一意な変数IDに置き換える「名前解決（name resolution）」の狙いと実装要点を分かりやすく解説する。

## この記事を読むべき理由
名前解決は型推論や最適化、エラーメッセージの精度に直結する基盤処理で、言語実装やコンパイラ設計に取り組む日本のエンジニアにとって不可欠な知識。特に Rust で小さな言語や DSL を作る際、スコープ／シャドーイングの扱いを正しく実装することでバグを大幅に減らせる。

## 詳細解説
- 問題の本質  
  人間が読み書きする識別子（例: x, y, add）は便利だが、コンピュータは「どのメモリ位置／変数を指しているか」を知りたい。スコープとシャドーイングにより同じ名前が複数の意味を持つため、名前解決はソース木（Ast<String>）を「機械向けの形」へ変換し、以後の型推論や最適化で名前の検索を不要にする処理。

- 目標形態  
  各識別子を一意な整数IDに置換した Ast<Var> を生成する。Var は単純に $Var(\text{usize})$ のような一意IDとして表現される。

- 基本アルゴリズム（通例）  
  1. AST を走査する（再帰降下）。  
  2. 束縛（let、関数引数など）に遭遇したら、新しい一意IDを割り当て、現在のスコープ（スタック上のマップ）に登録する。  
  3. 式内の識別子は、スコープスタックのトップから順に名前を検索して最初に見つかったIDで置換する（シャドーイング対応）。  
  4. スコープを抜けるときは登録を削除（スタックをポップ）する。  
  単一走査でスコープ構造とシャドーイングを解決し、後段の型推論は名前検索を気にせずIDを参照できる。

- 実装上の注意点  
  - 再帰束縛（自身を参照する let）をサポートする場合、束縛名に先にIDを割り当ててから本体を解決する必要がある（事前割当）。  
  - 前方参照は言語仕様次第（通常は同じスコープ内の前方参照は不可）。  
  - モジュール／名前空間やインポートを扱う場合はスコープの境界と解決ルールを拡張する。  
  - デバッグ用にソース位置（Span）とIDの対応を保持しておくと、エラー報告が格段に良くなる。

- なぜ効率的か（直感）  
  実行時に毎回名前を上から辿るのではなく、コンパイル時に一度だけ解決して整数参照にすることで、その後の解析や変換が高速かつ単純になる。

## 実践ポイント
- 最小実装（Rust風の擬似コード）でまず動かしてみる。以下は解決の核になる処理例：

```rust
// rust
type Name = String;
struct Var(usize);

struct Resolver {
    stack: Vec<HashMap<Name, Var>>,
    next_id: usize,
}

impl Resolver {
    fn push_scope(&mut self) { self.stack.push(HashMap::new()); }
    fn pop_scope(&mut self) { self.stack.pop(); }

    fn bind(&mut self, name: Name) -> Var {
        let id = Var(self.next_id);
        self.next_id += 1;
        self.stack.last_mut().unwrap().insert(name, id.clone());
        id
    }

    fn resolve_name(&self, name: &Name) -> Option<Var> {
        for scope in self.stack.iter().rev() {
            if let Some(v) = scope.get(name) { return Some(v.clone()); }
        }
        None
    }
}
```

- テストとデバッグ  
  - VS Code の統合テスト機能で多数の小さな入力プログラムを用意し、期待される Var 割当とスコープ処理を検証する。  
  - 出力パネルや統合ターミナルで解決マップ（名前→ID）をログし、シャドーイングや再帰の挙動を可視化する。  
  - AST に元のソース位置を紐付けておくと、解決失敗時のエラーメッセージが分かりやすくなる。

- 日本の現場での利用シーン  
  小規模な言語実装、教育用コンパイラ、DSL、静的解析ツールに特に重要。Rust の普及に伴い、Rust での言語実装を学ぶ日本のエンジニアにとって即戦力になる知見。

## 引用元
- タイトル: Resolving Names Once and for All  
- URL: https://thunderseethe.dev/posts/nameres-base/
