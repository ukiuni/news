---
layout: post
title: "One Method Was Using 71% of CPU. Here's the Flame Graph. - あるメソッドがCPUの71%を使っていた。フレームグラフで原因を見つけた話"
date: 2026-04-10T04:51:48.470Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://jvogel.me/posts/2026/one-method-using-71-percent-of-cpu"
source_title: "One Method Was Using 71% of CPU. Here&#39;s the Flame Graph. | Jonathan Vogel"
source_id: 366905113
excerpt: "フレームグラフでCPU71%のO(n²)ボトルネックを特定し応答5倍・メモリ10倍改善"
image: "https://jvogel.me/_astro/its_hot_no_ac.DB6Qm9Mm.jpg"
---

# One Method Was Using 71% of CPU. Here's the Flame Graph. - あるメソッドがCPUの71%を使っていた。フレームグラフで原因を見つけた話

たった一つのホットスポットがシステム全体を遅くしていた — JFR（Java Flight Recorder）とJMCで段階的に直し、レスポンスが約5倍、メモリピークが10倍改善した実例。

## 要約
Javaアプリのプロファイルで1箇所がCPUの約70%を占有しており、フレームグラフからO(n²)なストリーム内ループを特定。段階的に直すことで最終的に処理時間とメモリを大幅に削減した。

## この記事を読むべき理由
日本のサービスでも、トラフィック増加やコスト削減が課題です。小さなコードアンチパターンが大きなランニングコストやスケーラビリティ問題に直結します。JFRで「何を直すべきか」を見抜く実践的手順が学べます。

## 詳細解説
- アプリ概要：注文解析パイプライン（合成注文生成・検証・通貨別集計・不正スコア等）。負荷は100,000件を100仮想スレッドで処理。
- 観測：JMCのMethod Profiling（フレームグラフ）でjava.util.stream.ReduceOps$3ReducingSink.accept()が幅を占め、呼び元を辿るとTrendDetector.detect()内で「要素ごとに全リストをストリームで数える」処理が原因（1,000×1,000のO(n²)）。
- 代表的な問題点と修正例：
  - before: ストリーム内ループ（O(n²））
```java
// before
for (Order order : orders) {
  int hour = order.timestamp().atZone(ZoneId.systemDefault()).getHour();
  long countForHour = orders.stream()
    .filter(o -> o.timestamp().atZone(ZoneId.systemDefault()).getHour() == hour)
    .collect(Collectors.counting());
  ordersByHour.put(hour, countForHour);
}
```
  - after: 単一走査で集計（O(n)）
```java
// after
for (Order order : orders) {
  int hour = order.timestamp().atZone(ZoneId.systemDefault()).getHour();
  ordersByHour.merge(hour, 1L, Long::sum);
}
```
  - String連結をStringBuilderへ、Pattern.compileをstatic finalで一回だけ、String.formatを手作りパディングや単純連結に置換、オートボクシングの回避、コレクション選定の見直しなど。
- ラウンドごとの効果：大きいホットスポットをまず潰す → 新たに隠れていた問題が見える（例：String.formatが300k回呼ばれていた）。
- コンテション（ロック待ち）：デフォルトでは100仮想スレッドで目立たないが、2,500スレッドでAnalyticsAccumulatorのsynchronizedがボトルネックに。JFRのContentionタブで監視可能。対策はクリティカルセクションを短くする＋ReentrantLock等の導入。

## 実践ポイント
- まずJFRでRecordingを取り、JMCで開く：
```bash
# 起動時に記録
java -XX:StartFlightRecording=filename=myapp.jfr,settings=profile -jar myapp.jar
# 実行中にアタッチ
jcmd <pid> JFR.start duration=120s filename=myapp.jfr settings=profile
```
- 調査手順（優先順位）：
  1. Overviewタブ：Heap/Garbage/Threadsの形を見る
  2. Heapが上がる → Allocation（割当て）へ
  3. CPU高い → Method Profiling（フレームグラフ）へ
  4. 応答遅いのにCPU低い → Contentionへ（高負荷で再現して確認）
- 改善の基本ルール：
  - 「大きい問題を1つ直す → 再プロファイル」を繰り返す
  - ストリーム内ループでの全走査、繰り返しのフォーマッタ/正規表現コンパイル、不要な文字列生成、ボクシング、粗い同期は優先して見直す
  - プロダクションでの負荷（スループット／同時スレッド数）でプロファイルすること
- 効果試算：単一ノードでの5x、メモリピーク10x削減は、クラウド運用コスト削減に直結する可能性が高い。

元記事はJonathan Vogel（AWS）による検証事例。実務で使える手順がそのまま学べるので、自分のサービスでJFRを回して「何を先に直すべきか」を見つけてください。
