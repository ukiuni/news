---
layout: post
title: "One page of async Rust - async Rustを1ページでまとめる"
date: 2026-02-17T23:21:53.212Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://dotat.at/@/2026-02-16-async.html"
source_title: "One page of async Rust &ndash; Tony Finch"
source_id: 751795940
excerpt: "async RustのFuture/Wakerと簡易実行器を一ページで学べる"
---

# One page of async Rust - async Rustを1ページでまとめる
魅せる！「紙一枚」でわかるasync Rustの中身と疑問点

## 要約
async fnは呼ぶだけでは実行されずFutureを返す。実行にはpoll/Pin/Context/Wakerの仕組みを理解し、必要なら低レイヤでprimitive Future（例：Sleep）を自作して小さな実行器で動かせる、という話です。

## この記事を読むべき理由
Rustのasyncは高性能UI/サーバ/ゲーム/組込みで重要です。ランタイムの挙動やデバッグで詰まらないために、低レイヤの動作（Futureの状態遷移、Wakerの役割、簡易実行ループ）を初心者にも分かる形で把握できると実務で役立ちます。

## 詳細解説
- async fnの実体は「コンパイラ生成の状態機械」で、呼ぶとすぐFutureを返すだけ。実行するにはFuture::poll(Context)が必要。
- Futureは自己参照を含う可能性があるため移動不可にするPinが使われ、実例としてBox::pinでヒープに固定してTaskラッパーを作る。
- pollはContext（内部にWaker）を受け取る。Wakerは「このタスクを再スケジュールする方法」を表すが、標準ライブラリはRawWakerという低レイヤAPIを公開しているため、実装にはunsafeが絡む。
- primitive ops（著者はprimopsと呼ぶ）は手書きのFutureで、典型的には最初のpollで作業を予約してPoll::Pending、作業完了時に再びpollしてPoll::Readyを返す。これで.awaitはサスペンド／再開を実現する。
- シンプルな例：Sleep(u32)というFutureを自作し、delayが非ゼロのときはself.0を0にしてPoll::Pendingを返し、次回のpollでPoll::Readyにする。これだけで「一回サスペンドする」primitiveになる。
- Wakerの実装が面倒なら、著者は別案を採る：poll呼び出し側で「Yield」というコマンド置き場を用意し、その場所へのポインタをWakerのデータフィールドに詰める（Waker::noop()のvtableを流用）。Future側はContextを使ってその置き場を書き換し、Poll::Pendingで戻る。これによりpollから命令（Run/Sleep/Doneなど）を上位に「密輸」できる。
- Yield enumをPrimitive兼コマンドとして用い、トップレベルの実行ループは返ってきたYieldを見てタスクをタイマーキュー（min-heap）に再投入したり完了させたりする。これで「実時間を使わない偽の時間」で多数タスクを順序通り進められる。
- unsafe部分やRawWakerの設計に対する疑問（なぜもっと型安全にできないのか）や、借用のライフタイムに関する微妙な点は残る。既存のランタイム（tokio等）やcrateを調べる方が安全で実用的な場合も多い。

## 実践ポイント
- 小さく始める：async fnを呼んで返るFutureをBox::pinして自前でpollしてみると挙動が理解しやすい。
- primitive Futureを一つ作る（Sleepのような「一度Pendingを返す」物）で.awaitの低層動作を体験する。
- Waker/RawWakerはunsafeになるので最初はWaker::noopで挙動を見る。安全実装は既存ランタイムを参照する。
- 偽時間のシミュレーションやテスト用executorを自作すると、タスク順序やタイマーの検証が容易になる。
- 実運用では既製のランタイム（tokio/async-std/smol等）＋公式タイマーを使い、低層実装は学習用に留めるのが無難。
