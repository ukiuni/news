---
layout: post
title: "Ending 15 years of subprocess polling - 15年間続いたサブプロセスのポーリングを終わらせる"
date: 2026-02-02T11:39:05.798Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://gmpy.dev/blog/2026/event-driven-process-waiting"
source_title: "From Python 3.3 to today: ending 15 years of subprocess polling"
source_id: 935525085
excerpt: "Pythonのサブプロセス待機がポーリング廃止でCPUとバッテリーを大幅節約"
---

# Ending 15 years of subprocess polling - 15年間続いたサブプロセスのポーリングを終わらせる
ついに終止符：Pythonのサブプロセス待機をポーリングからイベント駆動へ

## 要約
Pythonのsubprocess（およびpsutil）は長年、タイムアウト付きwait()を実装するために短いスリープを繰り返す「busy-polling」を使ってきたが、LinuxのpidfdやBSD/macOSのkqueueを使ったイベント駆動待機で無駄なCPU起床を大幅に削減できるようになった。

## この記事を読むべき理由
ノートPCのバッテリー、CI環境や多数プロセスを監視するツールのスケーラビリティに直結する改善。日本の開発現場でも大量プロセス監視や低消費電力運用で実用的な恩恵がある。

## 詳細解説
- これまでの実装（例）: 非ブロッキングwaitpid +短いsleepを繰り返す。CPU wake-up が頻発し、検出遅延やスケール問題を生む。
```python
# Python
import os, time
def wait_busy(pid, timeout):
    end = time.monotonic() + timeout
    interval = 0.0001
    while time.monotonic() < end:
        pid_done, _ = os.waitpid(pid, os.WNOHANG)
        if pid_done:
            return
        time.sleep(interval)
        interval = min(interval * 2, 0.04)
    raise TimeoutExpired
```
- Linux (推奨): Linux 5.3で導入された pidfd_open を用い、得た pidfd を poll/select/epoll に登録してプロセス終了を待つ。ユーザ空間でのスピンが無く、カーネル通知でのみ起床するため効率的。
```python
# Python
import os, select
def wait_pidfd(pid, timeout):
    pidfd = os.pidfd_open(pid)
    poller = select.poll()
    poller.register(pidfd, select.POLLIN)
    events = poller.poll(timeout * 1000)
    if events:
        return
    raise TimeoutError
```
- macOS / BSD: kqueue/kevent にPIDを渡して KQ_FILTER_PROC / KQ_NOTE_EXIT を待つことで同様にイベント駆動で待機可能。
```python
# Python
import select
def wait_kqueue(pid, timeout):
    kq = select.kqueue()
    kev = select.kevent(pid, filter=select.KQ_FILTER_PROC,
                        flags=select.KQ_EV_ADD|select.KQ_EV_ONESHOT,
                        fflags=select.KQ_NOTE_EXIT)
    events = kq.control([kev], 1, timeout)
    if events:
        return
    raise TimeoutError
```
- Windows: 元々 WaitForSingleObject を使っており、イベント駆動的で変更不要。
- フォールバック: pidfd_open や kqueue が使えない/失敗する場合（EMFILE, EACCES 等）は、psutilは静かに従来のポーリングにフォールバックする実装。破壊的な例外は上げない設計。
- 効果の測定: 簡単な10秒待機テストで、ボリュンタリ/インボルンタリのコンテキストスイッチが「258→2」「4→1」など大幅に削減され、プロセスはカーネルのスリープ状態となる。

- 実装状況: psutil に実装が入り、同様の改善を CPython の subprocess に取り込むための PR（cpython/PR-144047）が提出されている（取り込み状況は環境の Python バージョンで確認を）。

互換性メモ:
- pidfd_open を利用するには Linux カーネル 5.3+ と Python の os.pidfd_open サポート（Python 3.9 以降で導入）が必要。
- macOS/BSD は kqueue サポート状況を確認。

## 実践ポイント
- まずは psutil を最新に更新して、Process.wait() の改善を利用する（リリースノートを確認）。
- サーバやCIで大量プロセスを監視するツールは、OSカーネル（Linux 5.3+）と Python バージョンを合わせることで恩恵を受けられる。
- 自前実装する場合は pidfd_open+poll（Linux）や kqueue（macOS/BSD）を使い、失敗時は従来のフォールバックを用意する。
- 効果確認は /usr/bin/time -v のコンテキストスイッチや ps/top でプロセス状態（S+）を見て測る。

以上。
