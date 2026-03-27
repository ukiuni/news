---
layout: post
title: "Uses for nested promises - ネストしたPromiseの活用法"
date: 2026-03-27T18:55:54.524Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://blog.jcoglan.com//2026/03/23/uses-for-nested-promises/"
source_title: "Uses for nested promises &#8211; The If Works"
source_id: 1281101628
excerpt: "ネストしたPromiseで判定と実行を分離しRWロックの同時実行を可能にする解法"
---

# Uses for nested promises - ネストしたPromiseの活用法
「ネストされたPromiseが役に立つ瞬間――並行制御で見つけた意外なユースケース」

## 要約
Promise.then()が自動でPromiseを平坦化する設計は便利だが、並行処理の制御（例：Readers–Writersロック）では意図的に「ネストしたPromise」を使うことで正しい実行順序を保てる場面がある、という話。

## この記事を読むべき理由
JavaScriptで非同期処理や並列実行を扱うエンジニア（特にNode.jsバックエンドやブラウザでの高度なI/O最適化）は、単純なthen/awaitだけでは破綻するケースを理解しておくとデッドロックや不正な直列化を避けられます。日本のサービスで高レイテンシな外部ストレージや暗号処理を扱う場面にも直結します。

## 詳細解説
- 基本概念：  
  - functorのmapはコンテナを変換するがネストは増やさない。monadのflatMap（bind）は1層だけネストを潰す。Arrayの例:
```javascript
// javascript
['a b','c d'].map(s => s.split(' ')) // -> [['a','b'],['c','d']]
['a b','c d'].flatMap(s => s.split(' ')) // -> ['a','b','c','d']
```
  - Promise.then()は引数の戻り値が普通の値でもPromiseでも受け取り、内部で自動的に平坦化する（map/flatMapの区別を行わない）。これが便利だが型系や関数合成には齟齬を生む。

- 問題となる実用例（RWLock）：  
  - 読み手は同時に複数実行可、書き手は単独実行というルールを守るために、複数のQueue（限界付き実行キュー）を組み合わせる設計がある。ここで「inbox」をlimit=1で使い、各要求を直列に判定する。
  - 重要点：inbox.push()内でrunner.push(fn)のPromiseを直接返すと、自動平坦化によりinboxがrunner.push(fn)の完了（つまりfn()の実行終了）まで待ってしまい、並列読みに必要な同時投入が阻害される（結果的にmutex化してしまう）。
  - 解決法：inbox.push()からは「{ promise: runner.push(fn) }」のようにラップしたPromiseを返す（ネストさせる）。inboxはそのラップを取り出すが、inbox自身は内部でrunner.push(fn)が解決されるまで待たないため、複数の読者を同時に開始できる。

- なぜJSの実行モデルでこれが必要か：  
  - then/awaitは常にマイクロタスク遅延を導入するため、単に順序をawaitしてからすぐ次の同期処理でpushすると全員が「空」と判断してしまうタイミングが生じる。ネストにより「入出力の順序決定」と「実際の処理完了待ち」を分離できる。

- 最低限のコード例（肝の差分）：
```javascript
// javascript
// ネストあり（正しい動作）
let { promise } = await inbox.push(async () => {
  await blocker.onEmpty();
  return { promise: runner.push(fn) };
});
return promise;

// ネストなし（inboxがfn完了まで待ってしまう）
return await inbox.push(async () => {
  await blocker.onEmpty();
  return runner.push(fn);
});
```

## 実践ポイント
- 並行制御ライブラリやキュー設計で「判定を直列化しつつ実行は並列化したい」ならネストしたPromiseを検討する。  
- 単純にPromiseを平坦化する言語仕様は便利だが、API設計時は「平坦化されることで実行時順序がどう変わるか」を明示的に考える。  
- テスト：混合の読み書き要求でログ順序／同時実行数の期待値を必ず自動テストする。  
- 型安全や関数型スタイルを重視する場合はmap/flatMapの区別を模倣するラッパーを用意すると明瞭になる。

以上。
