---
layout: post
title: "Node.js worker threads are problematic, but they work great for us - Node.jsのWorker Threadsは厄介だけど、私たちにはとても役立った"
date: 2026-03-22T13:34:59.597Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.inngest.com/blog/node-worker-threads"
source_title: "Node.js worker threads are problematic, but they work great for us - Inngest Blog"
source_id: 47428117
excerpt: "イベントループ飽和によるWebSocket切断をWorkerで解消した実例レポ"
image: "https://www.inngest.com/assets/blog/node-worker-threads/cover.png"
---

# Node.js worker threads are problematic, but they work great for us - Node.jsのWorker Threadsは厄介だけど、私たちにはとても役立った
「メインスレッドを守る」── Node.jsのWorker ThreadsでWebSocketの切断地獄を回避した話

## 要約
CPU重たいユーザーコードがNode.jsのイベントループを止め、心拍（heartbeat）が送れずにワーカーが「死んだ」と扱われる問題を、Connectの内部処理をWorker Threadに移すことで解決した実践レポートです。

## この記事を読むべき理由
Node.jsを使う日本の開発者にも起こり得る「イベントループ飽和」による接続切断問題と、その現実的な対策（Worker Threads導入と設計上の注意点）を、初心者にも分かりやすく実例ベースで学べます。

## 詳細解説
- 問題の本質：Node.jsは単一のイベントループで動くため、同期的に重い処理が走るとsetTimeoutやネットワークイベントが止まる。結果、WebSocketで送るべき心拍が止まり、サーバ側がワーカーを切断する。
- 解決策：worker_threadsでSDKの「接続管理（WebSocket・heartbeat・再接続・認証など）」をメインスレッドから分離。各ワーカーは独立したV8 isolateとイベントループを持ち、片方のCPU負荷がもう片方を止めない。
- 基本API（例）:
```javascript
// main.js
import { Worker } from "node:worker_threads";
const worker = new Worker("./worker.js", { workerData: { greeting: "hello" } });
worker.on("message", msg => console.log("from worker:", msg));
worker.postMessage({ type: "ping" });
```
```javascript
// worker.js
import { parentPort, workerData } from "node:worker_threads";
console.log(workerData.greeting); // "hello"
parentPort.on("message", msg => {
  if (msg.type === "ping") parentPort.postMessage({ type: "pong" });
});
```
- 制約と設計上の注意
  - 関数を渡せない：Workerはファイル単位で起動する。関数やクロージャはstructured cloneでシリアライズできないため、ロジックはワーカー側のエントリポイントに置く必要がある。
  - メッセージパッシング：データはstructured cloneでコピーされる。大きなオブジェクトはシリアライズコストとメモリ二重保持を招く。SharedArrayBuffer＋Atomicsは低レベルな数値配列共有に限定。
  - バンドラ問題：new Worker("...")は静的解析されないため、webpack/esbuild等でワーカーファイルを明示的にエントリに含める必要がある。TypeScriptでは拡張子（.ts/.js）対策も必要。
  - オーバーヘッド：各ワーカーはフルV8インスタンスなので数MB単位のメモリと起動コストがある。短命な多数のワーカーには不向き。長期的な接続や監視処理向け。
- Inngestの実装上の工夫
  - Connect内部をワーカー化して、実行要求（invocations）をメイン⇄ワーカーでメッセージ受け渡し。
  - ロガーなどユーザー渡しのオブジェクトはシリアライズ不可のため、ワーカーはログエントリを構造化してメインに送り、メインでユーザーのロガーを呼ぶプロトコルを作成。
  - ワーカーが落ちた場合に備え、メインスレッドで監視して指数バックオフ付きで再起動。即時ループを避ける。

## 実践ポイント
- まず疑うべきは「イベントループ飽和」：WebSocketやタイマーが遅れるならユーザーコードのCPU占有をチェック。
- ワーカーは「長寿命で重い処理から分離する」用途に使う。短時間タスクには向かない。
- ワーカーファイルはビルドに明示的に含める（ライブラリなら消費者のバンドラを考慮して出力に入れる）。
- ロギングやコールバック等のユーザー提供オブジェクトはメイン側で扱い、ワーカーとはメッセージプロトコルで連携する。
- 共有メモリが必要ならSharedArrayBuffer＋Atomicsを検討。ただし用途は数値配列向けに限定。
- ワーカー監視には指数バックオフを入れて再起動ループを防ぐ。

この手法は手間とトレードオフがありますが、イベントループを守りながら信頼性の高い永続接続を実現したい場面では非常に有効です。
