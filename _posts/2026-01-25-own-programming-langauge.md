---
layout: post
title: "Own programming langauge - 自作プログラミング言語"
date: 2026-01-25T21:12:31.123Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/SparkLessExploitCreator/ZydaScript"
source_title: "GitHub - SparkLessExploitCreator/ZydaScript"
source_id: 417632933
excerpt: "C++で作られた超小型言語ZydaScriptでコンパイラ実装を実地学習できる入門リポジトリ"
image: "https://opengraph.githubassets.com/3c197c11eed9aa7a97f053c9efe150279b5fcd570b3e978394b9795684607f60/SparkLessExploitCreator/ZydaScript"
---

# Own programming langauge - 自作プログラミング言語
自作ミニ言語「Zyra（ZydaScript）」を学習素材にする — C++で作られた小さな実験場

## 要約
GitHub上のZydaScript（READMEでは「Zyra」と表記）は、C++でゼロから実装された簡易プログラミング言語。変数宣言、算術・文字列結合、say(...)による出力、if/else条件分岐をサポートし、ループや関数など拡張予定が示されている。

## この記事を読むべき理由
自作言語はコンパイラ／インタプリタの基礎を学ぶ最短ルート。日本の学習者や若手エンジニアがC++での実装例を実地で追える小規模リポジトリは、実践的な教材として最適。

## 詳細解説
- 実装言語：C++でゼロから実装。
- サポート機能：型付き変数宣言（int, string, bool, group）、算術演算と文字列結合（+）、say(...)での出力、if/else と比較演算子（<, >, ==, !=）。
- サンプル（README抜粋）:

```zyra
var x: int = 10?
var name: string = "Zyra"?
say("Hello " + name + "!")?
if(x < 20) {
  say("x is less than 20")?
} else {
  say("x is greater or equal to 20")?
}
```

- 出力例：Hello Zyra! / x is less than 20
- 今後の計画（README記載）：while/forループ、関数とreturn、配列・辞書、例外処理、モジュール化。
- リポジトリ状況：小規模（コミット数少、スター/フォークなし）。言語名表記にZydaScriptとZyraの混在があるためREADMEとソースを突き合わせて確認が必要。

## 実践ポイント
- リポジトリをcloneしてソース（lexer/parser, AST, 実行部）を読む。  
- VS Codeで開き、統合ターミナルと出力パネルでビルド→実行を試す。  
- まずはループや関数の追加を実装して学ぶ（テストを小さく書きながら進めると安全）。  
- 学習の参考：字句解析→構文解析→AST→評価/コード生成の流れを意識。ANTLRやLLVMの導入を検討するとスケールしやすい。  
- 小さな改善（エラーメッセージ改善、ドキュメント追記、サンプル追加）をPRで貢献すると学びが深まる。
