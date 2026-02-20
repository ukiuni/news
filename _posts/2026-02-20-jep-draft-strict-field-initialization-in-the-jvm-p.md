---
layout: post
title: "JEP draft: Strict Field Initialization in the JVM - JVMにおける厳格なフィールド初期化（案）"
date: 2026-02-20T17:26:24.880Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://openjdk.org/jeps/8350458"
source_title: "JEP draft: Strict Field Initialization in the JVM (Preview)"
source_id: 402172598
excerpt: "JVMが既定値読み取りを禁止し初期化バグを防ぐ機能をプレビュー導入"
---

# JEP draft: Strict Field Initialization in the JVM - JVMにおける厳格なフィールド初期化（案）
魅力的タイトル: 「“nullでも0でもない”保証へ — JVMがフィールド初期化の抜け穴を封じる新仕様（プレビュー）」

## 要約
JVMに「厳格に初期化された（strictly-initialized）」フィールドを導入する提案。指定されたフィールドはデフォルト値（0/false/null）を読めず、finalなら常に同一値を観測することをランタイムが保証する。プレビュー機能でコンパイラがクラスファイルにフラグを付ける方式。

## この記事を読むべき理由
フィールドの“思いがけないデフォルト値”や初期化順序バグは大規模・レガシーなJavaシステムで致命的に見つけにくい。本提案はそのクラスのバグ源をランタイムで排除し、値クラスやnull制約など新言語機能の安全基盤を提供するため、日本のエンタープライズや組み込み開発でも耐障害性向上につながる可能性があります。

## 詳細解説
- 問題点の整理  
  - JVMはフィールドを生成時に暗黙のデフォルト（数値は0、参照はnull）で初期化する。これが意図しないデータとして読み出されてバグを生む（例：クラス初期化の循環依存で0が混入）。  
- 提案の本質  
  - クラスファイルのフィールドにACC_STRICT_INIT（0x0800）を付与すると、そのフィールドは「設定されるまで読めない」。finalであれば読まれた後に変更できない。これらはJVMが実行時に強制。  
- 静的フィールドへの扱い  
  - クラスの<classinit>実行中（larval状態）で、getstaticがstrictフィールドにアクセスすると未設定なら例外。putstaticでfinalフィールドを読まれた後に設定しようとすると例外。クラスが初期化完了する前にstrictな静的フィールドが未設定だと例外。  
- インスタンスフィールドへの扱い  
  - super()呼び出し前にstrictなインスタンスフィールドを読もうとしたり、super()到達経路で初期化されない可能性がある場合は検証失敗（バイトコード検証／例外）。finalインスタンスフィールドはsuper()後に変更不可などの制約。  
- 実装上の影響と最適化  
  - JITはstrictかつfinalなフィールドを「trusted」とみなし、読み値を再利用することでメモリアクセス削減・高速化が期待される。  
- 利用条件・互換性  
  - プレビュー機能（クラスファイル版番号 XX.65535）でのみ有効。実行時に --enable-preview が必要。既存プログラムに自動適用されない（コンパイラが明示的にフラグを付ける）。  
- 言語設計との連携  
  - Value Classes（値クラス）やnull非許容フィールド等の言語機能が安全に動作する基盤となる。JVM側の機能はJava固有ではなく、他のJVM言語のコンパイラでも利用可能。

簡単な発生例（循環初期化で0/nullが混入）
```java
// java
class App { public static final long appID = Log.currentPID(); public static void main(){ io.println("App["+appID+"] started"); Log.log("done"); } }
class Log { private static final String prefix = "App[" + App.appID + "]: "; public static void log(String m){ io.println(prefix + m); } public static long currentPID(){ return ProcessHandle.current().pid(); } }
```
上のような循環で、prefixに0が埋め込まれることがある。

## 実践ポイント
- 試す：Value Classesやstrict initを触るにはjavacとjava双方でプレビューを有効化（コンパイラ側でもプレビューサポートが必要）。実行時は java --enable-preview を付ける。  
- テスト：大規模コードベースではクラス初期化の循環や静的初期化ブロックを洗い出し、strict化による例外が出ないかCIで検証する。  
- 設計：新機能／新コンパイラでフィールドをstrictにすることで、nullチェックやfinalの一貫性をコンパイラ＋JVMで強制できる。既存のバイナリ互換性を壊さないため、移行は段階的に。  
- 注意点：AndroidのARTなどJVM互換実装や古いツールチェーンでは未対応の可能性。導入前にランタイムとツールの対応状況を確認すること。

以上。
