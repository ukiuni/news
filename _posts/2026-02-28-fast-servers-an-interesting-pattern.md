---
layout: post
title: "fast-servers: an interesting pattern - fast-servers: 興味深いパターン"
date: 2026-02-28T19:06:38.909Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://geocar.sdf1.org/fast-servers.html"
source_title: "fast-servers"
source_id: 1557411990
excerpt: "各コアにスレッド＋専用epollでロックを排し100k req/sを目指す高速サーバ設計"
---

# fast-servers: an interesting pattern - fast-servers: 興味深いパターン
100k req/sを狙える――コアごとスレッド＋epoll/kqueueで作る“決定分岐のない”シンプル高速サーバ

## 要約
1コア＝1スレッド（CPUピン留め）、各スレッドが独自のepoll/kqueueを持ち、接続の状態遷移はファイルディスクリプタを別スレッドの待ち受けキューへ渡すことで行う設計。ロックや複雑な分岐を減らして容易に高スループットを達成する。

## この記事を読むべき理由
日本でもクラウドコスト抑制や低遅延サービスが重要になっており、少ないCPUとI/Oで高性能を引き出すサーバ設計は即戦力になります。特にHTTP系やプロキシ、エッジ用途で有効です。

## 詳細解説
- 背景：従来の「イベントループ＋共有ワーカ」パターンはlibevent等で簡単に使える反面、スレッド間競合や状態遷移の複雑化で性能頭打ちになりやすい。
- 提案パターンの要点：
  - システムの論理コア数に合わせてスレッドを生成（必要なら一部を予約）。
  - 各スレッドはCPUアフィニティを設定してピン留めし、自分専用の epoll/kqueue FD を作る。
  - 接続は「状態ごとに担当スレッド」が決まっており、ある状態→別状態への遷移はそのFDを別スレッドの epoll/kqueue に登録（渡す）して行う。
  - 受け入れループ（accept）は専用に回し、acceptしたFDを選んだワーカーの epoll/kqueue に追加するだけにする。
- 利点：スレッド内処理が単純（ブロッキングでOKな場面も多い）、ロックや判断分岐が少なくキャッシュ効果が上がる、スループットが伸びやすい。
- 実装メモ：
  - スレッド生成例（擬似C）：
```c
// c
for (i = 0; i < ncores; ++i) pthread_create(&id, &attr, run, (void*)i);
```
  - 各スレッドでepoll/kqueueを作り、アフィニティを設定：
```c
// c
set_affinity(id);
worker[id].q = epoll_create1(0); // または kqueue()
```
  - acceptループ例（受信FDを選んだワーカーのepollへ追加）：
```c
// c
f = accept(s, NULL, NULL);
ev.data.fd = f; ev.events = EPOLLIN|EPOLLRDHUP|EPOLLERR|EPOLLET;
epoll_ctl(worker_q, EPOLL_CTL_ADD, f, &ev);
```
  - OSごとの最適化：Linuxでは TCP_DEFER_ACCEPT、accept4()、非同期/エッジトリガー等を活用。macOSはスレッドアフィニティAPIが異なるので対応を用意する。
  - リソース設定：RLIMIT_NOFILE を増やし、SO_LINGER 無効化、ソケットは non-blocking に。タイムアウトは SO_RCVTIMEO で簡単に扱える場合もある。
  - スケジューリング：単純にラウンドロビンでFDを配布する pick() が基本。負荷特性に応じてバイアスを入れてもよい（ベンチマーク必須）。

## 実践ポイント
- まずはコア数分のスレッドを作り、各スレッドにepoll/kqueueを持たせてピン留めする。
- acceptループは軽くして、受け取ったFDは即座にワーカーの epoll/kqueue に登録するだけにする。
- FD上限（RLIMIT_NOFILE）と SO_LINGER を調整してFD枯渇を防ぐ。
- 非同期設定（O_NONBLOCK／accept4）や TCP_DEFER_ACCEPT を試し、レイテンシとスループットをベンチする。
- 各FDの状態を単一スレッドで扱う設計にすることで、バッファ管理やアルゴリズムを単純化できる。
