---
layout: post
title: "The Periodicity Paradox: Why sleep() breaks your Event Loop - 周期性の逆説：sleep()がイベントループを壊す理由"
date: 2026-02-03T17:25:18.151Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://qianarthurwang.substack.com/p/the-heartbeat-of-tetris-what-a-1x1"
source_title: "The Heartbeat of Tetris 🟥🟥🟥🟥: What a 1x1 Pixel Taught Me About Concurrency"
source_id: 410131423
excerpt: "sleep()でイベントループが固まる罠と、非ブロッキング単一ループで応答性を保つ手法を解説"
image: "https://substackcdn.com/image/fetch/$s_!PNv2!,w_1200,h_675,c_fill,f_jpg,q_auto:good,fl_progressive:steep,g_auto/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F214853e8-fab5-40ff-a8b5-4132bf8cc81f_2048x1117.png"
---

# The Periodicity Paradox: Why sleep() breaks your Event Loop - 周期性の逆説：sleep()がイベントループを壊す理由

1ピクセルの落下が教える「待つ」でなく「聴く」設計 — sleep()に頼らないイベントループの作り方

## 要約
sleep()やブロッキング呼び出しで周期処理を実装すると入力応答性を失う（＝周期性の逆説）。単一のディスパッチャ（イベントループ）と非ブロッキングI/O／タイム管理で解決する。

## この記事を読むべき理由
ゲームやリアルタイムUI、ネットワークサーバー――日本のモバイルゲーム開発やクラウドサービスでも、応答性と効率は重要です。初歩的な間違いを避けることでバグやスケーリング問題を減らせます。

## 詳細解説
- 問題点（周期性の逆説）  
  単純な実装で while + time.sleep(1) にすると、入力待ちや sleep によりループが固まり、ブロックが落ちるタイミングとユーザ入力の両立ができない。

- 解決方針：ディスパッチャ（イベントループ）  
  ループを短周期で回し、2つの問いを高速に繰り返す：ユーザ入力があるか？ブロックを落とす時間か？。待機（sleep）で制御を譲らず「聴く」設計にする。

- 実装の鍵  
  1) 非ブロッキング入力（例：curses の nodelay）で getch が即帰る。  
  2) 手動で時刻を追跡し、固定刻み（tick）で処理する。jitter を防ぐために last += tick_rate のように前回タイムスタンプに加算する（last = now はドリフトを生む）。  
  3) Polite polling：小さな sleep（例 10ms）でCPU占有を下げる。  
  これらで応答性・安定性・効率を両立する。

- スレッドの落とし穴  
  重い処理を別スレッドに分けても共有状態の競合→ロックが必要になり、結果的にブロッキングやデッドロックのリスクが増える。単一スレッドのディスパッチャは順序性・原子性の面で有利。

- スケールのための次段階  
  単純なポーリングは高並列ネットワークでは非効率。Linux の epoll／macOS の kqueue のようなカーネル主導の通知（割り込み的）を使うと、アイドル時の消費をほぼゼロにできる（Nginx 等のアプローチ）。

- 短い参考コード（概念例）
```python
# python
import curses, time

def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    y, x = 0, 10
    last = time.time()
    tick = 1.0
    while True:
        now = time.time()
        key = stdscr.getch()
        if key == ord('q'): break
        if key == curses.KEY_LEFT: x -= 1
        if key == curses.KEY_RIGHT: x += 1
        if now - last >= tick:
            y += 1
            last += tick  # jitter補正
        stdscr.erase(); stdscr.addstr(y, x, "[]"); stdscr.refresh()
        time.sleep(0.01)  # polite polling
```

## 実践ポイント
- UI/ゲーム：固定タイムステップ（tick）＋加算で時刻を管理し、レンダリング遅延を累積させない。  
- サーバ／ネットワーク：可能なら select/epoll/kqueue 等のイベント通知を使い、busy-wait を避ける。  
- 並列化：共有状態があるならまず単一スレッドのディスパッチャで設計し、どうしても重い処理は非同期キューやワーカーに切り出す。  
- 計測：CPU使用率と入力遅延を両方測り、poll間隔（sleep）のトレードオフを調整する。

日本の現場でも、リアルタイム性とスケーラビリティは必須項目です。1ピクセルから始めて、まずは「待つ」ではなく「聴く」設計を試してみてください。
