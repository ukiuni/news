---
layout: post
title: "When “just spin” hurts performance and breaks under real schedulers - 「ただスピンするだけ」が性能を壊す理由"
date: 2026-01-27T10:14:08.977Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.siliceum.com/en/blog/post/spinning-around/?s=r"
source_title: "Spinning around: Please don&#39;t! - siliceum"
source_id: 417544774
excerpt: "単純スピンがSMT/NUMAで性能と公平性を壊す—PAUSE/TSCとハイブリッドで対処"
image: "https://www.siliceum.com/_astro/CmOoXvsz_Z2jEEGT.png"
---

# When “just spin” hurts performance and breaks under real schedulers - 「ただスピンするだけ」が性能を壊す理由
CPUを燃やし、スケジューラで崩壊する“ただのスピン”をやめさせる方法

## 要約
単純なスピンループ（busy-wait）は正しく実装しないとデータ競合を招き、正しく実装してもPAUSEやバックオフの挙動で性能・消費電力・公平性を大きく損ないます。本稿は問題点と実践的な対策を分かりやすくまとめます。

## この記事を読むべき理由
日本の組込み・サーバー・デスクトップ開発者は、マルチコア／NUMA／SMT環境でスピン実装が思わぬボトルネックや電力問題を生むことを知らないことが多く、正しい実装と代替手段を知るだけで安定性と効率が大きく改善できます。

## 詳細解説
- まずの落とし穴：単純なチェック→書き込みの実装はレースを招きます。atomic.exchangeを使えば「誰が取ったか」を原子操作で判定できます。
```cpp
// C++
std::atomic<int> isLocked{0};
void lock() {
  while (isLocked.exchange(1) != 0) {
    // spin
  }
}
void unlock() { isLocked.store(0); }
```

- ただし空ループはCPUを無駄に回し、特にHT/SMTや多数コアのCPUでは他スレッド性能に深刻な影響を与えます。x86では PAUSE 命令を挿入してメモリ要求のレートを制御します。
```cpp
// C++
void cpu_pause() {
#if defined(__x86_64__) || defined(__i386__)
  _mm_pause();
#elif defined(__aarch64__) || defined(__arm__)
  __yield();
#endif
}
void lock_with_pause() {
  while (isLocked.exchange(1) != 0) cpu_pause();
}
```

- バックオフ：単純にPAUSEを繰り返すより指数バックオフ＋ジッタで競合を緩和します。PAUSEの「長さ」はCPU世代で大きく変わる（10サイクル台→100+サイクルなど）ため、回数ベースだけでなく時間（TSC）で制限するのが現実的です。つまり、PAUSE回数は増やすが「合計で最大何サイクルまで」という上限を持たせます。

- なぜTSCで制限するか：PAUSE命令のサイクル長が世代や実クロックで変動するため、$3200\ \text{cycles}/\mu s$ のようなTSC換算で「最大待ち時間」を決めると過待ちや短すぎる待ちを避けられます。実装上はRDTSCで終端時刻を決め、ループ内で__rdtsc()を参照します。

- 残る選択肢：多くの場合、OSの同期プリミティブ（futex/condition variable/semaphore）やハイブリッドロック（短時間はスピン、長期はブロック）を使うのが最も安全で効率的。

## 実践ポイント
- まずはスピンを使わない設計を検討する（条件変数／futex等）。  
- スピンが必須なら atomic exchange を使い、cpu_pause() を必ず入れる。  
- 指数バックオフ＋ジッタを入れ、PAUSEの回数ではなく「最大サイクル（TSC）」で上限を制御する。  
- 実行対象のCPU（クラウドVM含む）でPAUSE遅延やTSC周波数を実測してチューニングする。  
- NUMAやSMT環境ではスピンの悪影響が顕著になるため、優先的にブロッキング設計へ切替えを考える。  

実装例や計測方法が必要なら、ターゲット環境（Linux/Windows、ARM/x86）を教えてください。より具体的なコードとチューニング値を提示します。
