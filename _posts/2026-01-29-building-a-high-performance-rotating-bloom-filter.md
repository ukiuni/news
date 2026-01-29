---
layout: post
title: "Building a High-Performance Rotating Bloom Filter in Java - Javaで作る高性能回転ブルームフィルタ"
date: 2026-01-29T15:55:13.075Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://medium.com/@udaysagar.2177/building-a-high-performance-rotating-bloom-filter-in-java-a9e75de993bf"
source_title: "Building a High-Performance Rotating Bloom Filter in Java"
source_id: 46750220
excerpt: "Javaで数百万OPSを支える回転ブルームフィルタの設計とロックフリー実装を解説"
---

# Building a High-Performance Rotating Bloom Filter in Java - Javaで作る高性能回転ブルームフィルタ
一瞬で「見たことあるか」を判断する — 数百万OPSを支える時間窓付きブルームフィルタの実装と設計原則

## 要約
回転（時間窓）付きブルームフィルタは「最近見たか」を定額メモリで追跡できるデータ構造。この記事は、Javaで高スループット・スレッド安全に動く実装（lock-free書き込み、スナップショット化、回転同期、誤検出の扱い）を紹介します。

## この記事を読むべき理由
重複排除、リプレイ防止、キャッシュの出入り管理など「最近見たか」が重要な日本のサービス（ログ集約、広告トラッキング、APIレート制御）で即戦力になる設計が学べます。

## 詳細解説
- 基本コンセプト  
  回転フィルタは固定サイズの複数ウィンドウを連ね、古いウィンドウは期限切れで破棄する方式。LRUではなく「最初の挿入時刻で期限切れ」するため、突発的なバーストで保持量が短くなる点に注意。

- 課題と解決策（4点）
  1. ロックフリー書き込み  
     AtomicLongArrayとCPUレベルのCASでビットを原子的に立てる。衝突は稀で、ロックより3–4倍のスループットを実現。例（概念）：  
     ```java
     // Java
     do {
       long old = data.get(i);
       long neu = old | mask;
     } while (!data.compareAndSet(i, old, neu));
     ```
  2. アクティブ→読み取り専用スナップショット  
     期限切れウィンドウはAtomicLongArrayをplainな long[] にコピーして不変化。以降の読み取りは原子的コスト無しで高速。
  3. 回転の同期（書き込みの失われ防止）  
     チェーン参照自体はAtomicReferenceで交換するが、書き込みが「ゾンビフィルタ」に入る競合を防ぐために書き込みパスだけReadLockを取得し、回転はWriteLockで行う。クエリは完全にロックフリー。擬似コード：  
     ```java
     // Java
     rotationLock.readLock().lock();
     try {
       active.put(bits);
     } finally {
       rotationLock.readLock().unlock();
     }
     ```
  4. 誤検出率（False Positive Rate; FPR）の合成  
     N個のウィンドウを順にチェックすると誤検出は合算的に増える。合成FPRは次で表される：  
     $$\text{Combined FPR} = 1 - (1 - p)^N$$  
     例えば各ウィンドウ$p=0.01$を5個使うと合成は約5%に近づく。必要な合成FPRから逆算して各ウィンドウの$p$を小さく設計する（メモリ増加とトレードオフ）。

- パフォーマンス最適化
  - Bits事前計算: キーのハッシュ位置を一度計算して全ウィンドウで再利用（再ハッシュを削減）。
  - Double hashing: $h_1,h_2$ の2つで k 個の位置を生成し、ハッシュ呼び出しを2回に抑える。位置は (h1 + i * h2) mod m。
  - 高速ハッシュ(xxHash): 非暗号用で非常に高速。xxHash64 ならハッシュがサブナノ秒級。
  - BitsProvider抽象: 既にシリアライズ済みのバイト列がある場合はゼロコピーで使い、再シリアライズコストを回避。

- スタンドアロン用途  
  時間窓が不要ならStandalone BloomFilterを使えば回転やバックグラウンドスレッド無しで同じ高速性を享受可能。

## 実践ポイント
- ウィンドウ数と保持時間を業務要件（誤検出容認率・保持期間）で決め、合成FPRを式 $$1-(1-p)^N$$ で逆算して各ウィンドウの$p$を設定する。  
- 高スループット系ではBitsProviderを活用して既存バイナリをそのまま渡す（ゼロコピー）。  
- 多スレッド環境ではAtomicLongArray＋CASで書き込み、回転だけ短時間WriteLockで同期する設計を採る。  
- 匿名プロファイルの用途や短期重複排除は回転フィルタが有効。データ寿命を厳密に制御したい場合は別途TTL管理を検討。  
- Maven依存例（導入の足がかり）：  
  ```xml
  <!-- XML -->
  <dependency>
    <groupId>io.github.udaysagar2177</groupId>
    <artifactId>rotating-bloom-filters</artifactId>
    <version>0.0.1</version>
  </dependency>
  ```

元実装は GitHub (udaysagar2177/rotating-bloom-filters) で公開されているので、実運用向けの実装詳細やベンチマークを確認して自環境に合わせて調整してください。
