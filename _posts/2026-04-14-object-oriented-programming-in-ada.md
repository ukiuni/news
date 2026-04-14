---
layout: post
title: "Object oriented programming in Ada - Adaにおけるオブジェクト指向プログラミング"
date: 2026-04-14T20:01:36.158Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://entropicthoughts.com/object-oriented-programming-in-ada"
source_title: "Object Oriented Programming in Ada"
source_id: 1004830045
excerpt: "Java例で学ぶAdaのOOPと明示的メモリ管理（Controlled活用）"
---

# Object oriented programming in Ada - Adaにおけるオブジェクト指向プログラミング
なぜAdaでオブジェクト指向の本質が見えるのか — Java例で学ぶ「機能の分解」と安全なメモリ設計

## 要約
Adaはオブジェクト指向を「カプセル化」「継承」「動的ディスパッチ」などの要素に分解して提供するため、使いたい機能だけを明示的に選べる。この記事は、Javaの簡単な車/エンジン例をAdaに置き換えつつ、その設計思想と実務的な注意点を解説する。

## この記事を読むべき理由
- 日本の組込み・安全クリティカル分野（航空、鉄道、産業機器、自動車）でAdaは依然強く、言語の設計意図を理解すると既存スキルの移行が早まる。  
- Javaなど参照型中心の言語に慣れていると見落としがちな「メモリ配置」「所有権」「初期化/終了処理」をAdaは明示的に扱うため、堅牢な設計が学べる。

## 詳細解説
- 分解されたOOP: Adaは「interface（抽象型）」「type extension（拡張）」「dynamic dispatch（動的呼び出し）」「encapsulation（パッケージによる可視性）」などを独立して提供する。Javaのclassキーワードで一気に有効になる多数機能を、Adaでは個別に選べる。
- パッケージ仕様と本体: Adaはパッケージ(spec)とbodyを分け、公開APIと実装を明確化するため、大規模開発で利点がある。
- 抽象インタフェース: 例では
  - type Engine is interface; procedure Run (Self : Engine) is abstract;
  のようにインタフェースを宣言し、Runは「プリミティブ操作（メソッド）」として扱われる。
- 動的ディスパッチとタグ型: interfaceや明示的に tagged とした型で動的ディスパッチが可能。静的に呼べる場面（具体型が分かるとき）は普通の手続き呼び出しでよい（Run(My_Engine)）。
- 参照（access）とメモリ管理: Javaの参照に相当する型は明示的に定義する（例: Engine_Access is access all Engine'Class）。Adaはガベージコレクタを持たないのが普通なので、必要なら Unchecked_Deallocation を用いて解放関数を生成するか、Controlled/Limited_Controlled を使ってFinalizeで解放を自動化する。
- Controlled types（RAII的振る舞い）: Vehicleを Limited_Controlled にして Finalize をオーバーライドすると、スコープ離脱時に自動で後片付けが呼ばれる。これによりC++に近い安全な資源管理が可能。
- 型階層の扱い: 手続きの第一引数は動的ディスパッチされるが、他の引数に対して多相性を許すには明示的に Other : Vehicle'Class と指定する必要がある（デフォルトは具体型）。
- コンストラクタ: Adaに組み込みのコンストラクタはないが、オブジェクトを返す関数を用いるのが一般的（例: function Create_Moped return Moped）。

## 実践ポイント
- Java→Ada移行時は「どのOOP要素を使うか」を明確に決める（特に所有権とメモリ確保策略）。  
- なるべく Controlled 型と Finalize を活用して資源解放を自動化する。直接 Unchecked_Deallocation を使うのは最終手段。  
- パッケージの仕様(spec)でAPIを先に設計し、本体で実装を分離すると大規模開発・レビューが楽になる。  
- 多相引数は 'Class を明示する必要がある点に注意（例: Other : Vehicle'Class）。  
- 小さなJavaサンプルをAdaで書き直してみると、言語設計の差分が身につく。まずは「Engine interface」「Engine_Access」「Vehicle（Limited_Controlled）」という最小構成を試そう。

以上を踏まえ、Adaは「安全性」と「明示性」を重視する現場に向いた言語です。まずは手軽な例を一つ移植して、パッケージ分割・access型・Finalizeの感触を掴んでみてください。
