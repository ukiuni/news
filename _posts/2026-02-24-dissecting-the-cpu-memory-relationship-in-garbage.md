---
layout: post
title: "Dissecting the CPU-Memory Relationship in Garbage Collection - ガベージコレクションにおけるCPUとメモリの関係を分解する"
date: 2026-02-24T22:41:34.347Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://norlinder.nu/posts/GC-Cost-CPU-vs-Memory/"
source_title: "Dissecting the CPU-Memory Relationship in Garbage Collection | Jonas Norlinder"
source_id: 397325425
excerpt: "OpenJDK26のAPIで隠れたGCのCPU費用を可視化し無駄を暴く方法"
image: "https://norlinder.nu/assets/img/stopwatch.png"
---

# Dissecting the CPU-Memory Relationship in Garbage Collection - ガベージコレクションにおけるCPUとメモリの関係を分解する
クリックせずにはいられない！「遅延ゼロ」に見えて実はコストを隠すGCの盲点を可視化する方法

## 要約
現代のJava GCは「短い停止時間＝低コスト」とは限らない。OpenJDK 26で追加されたGC用CPU計測APIで、ガベージコレクタが隠れたCPU負荷をどれだけ消費しているかを定量化できるようになった。

## この記事を読むべき理由
短いGCポーズだけを監視していると、クラウドで余分なCPU代や電力を払い続けるリスクがあります。特に日本のSRE／プラットフォーム運用者やクラウド費用に敏感な開発チームは、メモリとCPUのトレードオフを正しく評価する必要があります。

## 詳細解説
- なぜ盲点が生まれるか  
  歴史的にはGCはアプリを停止して実行され、その「停止時間」がコスト指標でした。しかしマルチコア化と並行GC（G1、ZGC等）の登場で、コストは「停止時間」からバックグラウンドやアプリ実行中に分散され、可視性が低下しました。

- GCコストの3分類（簡潔）  
  1. 明示的コスト：GC専用スレッドが消費するCPU時間（トラバース、移動、参照更新など）  
  2. 暗黙的コスト：アプリコードに挿入されるバリア（事前/事後バリア）や参照更新のオーバーヘッド  
  3. マイクロアーキテクチャ影響：GCがL3キャッシュを追い出してキャッシュミスを増やす等

- マルチコアでの問題  
  並列GCはポーズ短縮と引き換えに総CPU時間を増やす（プロビジョニング非効率）。並行GCはポーズを小さくするが、総サイクルの多くをバックグラウンドで消費するため「見た目は低遅延でもコストが高い」ことがある。ZGCのようにポーズとコストがデカップリングされる実例も紹介されています。

- 可視化の重要性とOpenJDK 26の対応  
  プロセス全体のCPU時間だけではGC寄与を分離できないため、OpenJDK 26では以下の手段が追加されました：  
  - 統一ログ: -Xlog:cpu（JVM終了時出力）  
  - Java API: MemoryMXBean.getTotalGcCpuTime()（GCが消費したCPUナノ秒を返す）  
  これにより、GCの明示的なCPUコストをワークロード単位で計測可能になります。

- パフォーマンス分析での指標  
  応答性（wall-clock）とCPU利用（aggregate CPU time）は分離して考える必要があり、比率は $ \frac{\text{CPU time}}{\text{wall-clock time}} $ で表せます。高い比率は多コア利用を示しますが、GCがその内訳を占めていないか確認すべきです。

## 実践ポイント
- まずやること：OpenJDK 26以上で MemoryMXBean.getTotalGcCpuTime() を用いて、GCが消費するCPU量を定期的に計測する。  
- ベンチ方法：JITウォームアップや起動ノイズを避けるため、反復計測（複数イテレーション）でGC前後の差分を取得する。  
- メトリクス設計：pause時間＋GC CPU時間＋プロセス全体CPUを並べてダッシュボード化し、どの比率で費用が発生しているか可視化する。  
- 日本向け注意点：クラウド定額課金やコア数の多いインスタンスを使うケースでは、短ポーズでも非効率なCPU課金が発生しやすい。コスト試算にGC CPUを含めること。

短いサンプル（計測イメージ）
```java
import java.lang.management.ManagementFactory;
import java.lang.management.MemoryMXBean;
public class GcCpuSample {
  static final MemoryMXBean mem = ManagementFactory.getPlatformMXBean(MemoryMXBean.class);
  public static void main(String[] args) throws Exception {
    long startGc = mem.getTotalGcCpuTime(); // ナノ秒
    long startWall = System.nanoTime();
    // --- 実ワークロードをここで実行 ---
    long endWall = System.nanoTime();
    long endGc = mem.getTotalGcCpuTime();
    System.out.printf("wall=%.2fs gc_cpu=%.2fs%n",
      (endWall-startWall)/1e9, (endGc-startGc)/1e9);
  }
}
```

上記を運用ベンチに組み込み、ポーズ時間だけでなくGCが占めるCPU割合を必ず監視してください。これにより「見た目は速いがコスト高」の罠を回避できます。
