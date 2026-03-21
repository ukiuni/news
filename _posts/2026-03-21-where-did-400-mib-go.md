---
layout: post
title: "Where did 400 MiB go? - 400 MiBはどこへ消えた？"
date: 2026-03-21T21:39:19.262Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://frn.sh/pmem/"
source_title: "Where did 400 MiB go?"
source_id: 376888950
excerpt: "一部ポッドだけ増える約400MiBはV8未回収とglibc断片化で、設定で解消可能"
---

# Where did 400 MiB go? - 400 MiBはどこへ消えた？
Node.jsポッドで「消えた」400MiBを取り戻す──V8とglibc、両方に原因があった実地調査レポート

## 要約
1つのStatefulSetポッドだけが他より約400MiB多くメモリを消費していた原因は、V8が大量の不要ページを確保したままGCしなかったこと（~270MiB）と、glibcのアリーナ断片化によるネイティブ領域の保持（~70MiB）の両方だった。対策は --max-old-space-size と MALLOC_ARENA_MAX の組合せで効果的。

## この記事を読むべき理由
KubernetesでNode.jsを運用していると、「同一アプリなのに一部のポッドだけメモリを喰っている」現象に遭遇しやすい。余分なメモリはクラウドコストにつながるため、原因の切り分けと実用的な対処法がすぐ役立つ。

## 詳細解説
- 観察：Grafanaでメモリが段階的にジャンプして止まるパターン。問題ポッドのプロセスRSSは約640MiBで、他は約330MiB。
- プロセス解析：コンテナ内で node プロセスのみが増大。/proc/<pid>/smaps_rollup を見ると増分は「Private Dirty Anonymous」（プロセス単独で変更された匿名ページ）に集中。
- V8の誤解点：process.memoryUsage() や heapUsed は「JavaScriptから見えるライブオブジェクト量」を報告するだけで、V8がOSからmmapで確保している割当ページ全体（空きガベージを含む）を示さない。結果、RSSとheapUsedの乖離が生じる。
- 決定的手がかり：/proc/<pid>/smaps を見ると多数の同一サイズ（256KiB）の匿名マッピングが存在 → V8がページ単位で mmap() して確保している領域と一致。強制GCで大量のRSSが解放され、V8の未回収ガベージが主因であることが確認できた。
- 追加の要因：OpenSSL/zlib/llhttpなどネイティブ側の短命なmalloc/freeが多く、glibcの複数アリーナが断片化してメモリをカーネルに返せない状況も発生していた。

## 実践ポイント
- まず切り分け：
  - smaps_rollupを確認：cat /proc/<pid>/smaps_rollup（Pss_Anon 等を見る）
  - RSS と process.memoryUsage()（Inspector経由）を比較。SIGUSR1でInspectorを有効化し、nsenterで接続して Runtime.evaluate("process.memoryUsage()") を取得する。  
- 有効だった対策（実運用例）：
  - 環境変数/コンテナ設定例：
```yaml
# yaml
env:
  - name: MALLOC_ARENA_MAX
    value: "2"
  - name: NODE_OPTIONS
    value: "--max-old-space-size=256"
```
  - 意図：--max-old-space-size=256 によりV8のold世代が小さくなり早めにフルGCを走らせて未回収ページを解放。MALLOC_ARENA_MAX=2 によりglibcのアリーナ数を絞って断片化を軽減し、ネイティブ領域の返却を助ける。
- 注意点：CPU集約で頻繁に割当てるワークロードだとGC頻度増やして遅延やMALLOCロック競合が起きる可能性があるので事前検証を必ず行う。  
- 継続監視：RSS vs heapUsed の差分、/proc/<pid>/smaps のマッピング数、GC頻度を監視し、閾値でアラート設定を。

短くまとめると、「見えないメモリ」はV8の保有ページ（GCが走らないため）とglibc断片化の二重奏。適切なヒープ上限とglibc設定で大幅に改善できる。
