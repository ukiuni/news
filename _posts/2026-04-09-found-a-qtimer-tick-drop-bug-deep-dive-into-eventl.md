---
layout: post
title: "Found a QTimer tick-drop bug : deep dive into EventLoop blocking and a minimal reproducer - QTimerのtick欠落バグ発見：EventLoopブロッキングの深掘りと最小再現コード"
date: 2026-04-09T11:12:43.652Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://prejudice.tistory.com/43"
source_title: "QTimer 지연/누락 버그 해결 - EventLoop 점유로 인한 tick 누락 원인과 테스트 코드"
source_id: 366209010
excerpt: "メインスレッドの僅かなブロックでQTimerがtick欠落、再現コードと対策を提示"
image: "https://img1.daumcdn.net/thumb/R800x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdna%2FcgIx8y%2FdJMcadIknXW%2FAAAAAAAAAAAAAAAAAAAAADM0X_NqN8zmULi6ffzy9zpn16iOnvW8908NPu66WdEL%2Fimg.png%3Fcredential%3DyqXZFxpELC7KVnFOS48ylbz2pIh7yKj8%26expires%3D1777561199%26allow_ip%3D%26allow_referer%3D%26signature%3D9iEHo2fUpHshVKeWuoIZV8ZEWwg%253D"
---

# Found a QTimer tick-drop bug : deep dive into EventLoop blocking and a minimal reproducer - QTimerのtick欠落バグ発見：EventLoopブロッキングの深掘りと最小再現コード
QTimerが“飛ぶ”原因を突き止めた：100msタイマーが76回しか動かなかった再現と原因解析

## 要約
QTimerのtimeoutが遅延・欠落する原因は、メインスレッドのEventLoopが他処理に占有されること。小さな再現コードで、100ms間隔のタイマーが実行回数を大きく欠損する現象を確認し、Qtのタイマー設計や対策（Qt::PreciseTimer／QChronoTimerの活用）を示す。

## この記事を読むべき理由
Qtでタイミングが重要な処理（組込み、UI更新、計測、通信など）を作る日本のエンジニアは、メインスレッドの僅かなブロッキングでタイマーが実際に「欠落」する可能性を把握しておくべきです。テストが不安定になる原因究明と実践的な対策が学べます。

## 詳細解説
- QTimerはQEventLoop上で動作し、Signal/Slot経由でtimeoutハンドラが呼ばれる。EventLoopがメインスレッドでブロックされると、timeoutコールが遅延し、その遅延が累積すると次のtickが「スキップ」されたように見える（実行回数の欠落）。
- 原因のイメージ：タイマーは予定時刻ベースで次の発火を計算するが、handler実行が長引くと「期待時刻」を超過し、その間に発生すべき複数のtimeoutが消化されずに失われる。
- Qt側のタイマー精度：既存のQTimerは省電力などの理由でタイマー処理を束ねるためマイクロ秒精度は期待できない。Qt::PreciseTimer（Qt5以降）は最適化を解除して改善するが、㎳単位のQTimerで100µs級の精度は難しい。Qt6.8で導入されたQChronoTimerはナノ秒単位の内部精度を提供するため、高精度用途ではこちらを検討。
- 再現コードの要点：メインスレッドにQTimer(100ms)、ワーカースレッドで約70msの処理を行い、処理終了をQueuedConnectionでメインに返す。メイン側のonTaskFinishedでさらに約45msブロック処理を行う設計により、タイマーが累積遅延を起こし、10秒間で100期待tickのうち実際は76しか動作しなかった。

重要な処理箇所（抜粋）：
```cpp
// cpp
m_cycleTrigger->setInterval(100);
connect(m_cycleTrigger, SIGNAL(timeout()), this, SLOT(onTaskTriggered()));

void onTaskTriggered() {
    if (m_busy) return;          // mainが忙しければスキップ（欠落シミュレート）
    m_busy = true;
    ++m_tickCount;
    QMetaObject::invokeMethod(m_runner, "runProcess", Qt::QueuedConnection);
}

void onTaskFinished() {
    // ここで数十msブロックするとEventLoopを占有してタイマー処理を遅らせる
    syncOutputs(); // ~40ms
    updateMonitor(); // ~5ms
    m_busy = false;
}
```

## 実践ポイント
- メインスレッドを軽く保つ：UIやタイマーのハンドラで数10ms以上の処理を行わない。重い処理はワーカースレッドへ完全に移す。
- シグナル受信後の処理は非同期化する：QueuedConnectionで戻す場合でも、メインで重い合成処理をしない（必要なら別スレッドへ再委譲）。
- 精度が必要ならQt::PreciseTimerを試し、さらに高精度が必要ならQt6.8のQChronoTimerを検討する。
- 再現テストを作る：問題の切り分けには最小再現コードを作るのが最速。QElapsedTimerで時刻ログを取り、期待時刻と実測のドリフトを出す。
- 代替設計：単純に「スキップ」させたくない場合は、次の期待発火時刻を計算してスケジュールし直す（自己補正型タイマー設計）。

興味があれば、再現コードをベースにしたシンプルな修正版（QChronoTimer版やメインでの非同期化例）を用意しますか？
