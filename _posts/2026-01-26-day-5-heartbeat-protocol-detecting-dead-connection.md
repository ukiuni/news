---
layout: post
title: "Day 5: Heartbeat Protocol – Detecting Dead Connections at Scale - Day 5: ハートビートプロトコル（大規模接続でのデッド検出）"
date: 2026-01-26T01:17:55.917Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://javatsc.substack.com/p/day-5-heartbeat-protocol-detecting"
source_title: "Day 5: Heartbeat Protocol – Detecting Dead Connections at Scale"
source_id: 418765305
excerpt: "GCやコンテキストスイッチ回避、ゼロ割当てで数十万WebSocketの心拍検出を実装"
image: "https://substackcdn.com/image/fetch/$s_!VHTa!,w_1200,h_675,c_fill,f_jpg,q_auto:good,fl_progressive:steep,g_auto/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F06cd7ceb-e403-40b2-b080-807abb3ba475_4000x3000.png"
---

# Day 5: Heartbeat Protocol – Detecting Dead Connections at Scale - Day 5: ハートビートプロトコル（大規模接続でのデッド検出）
思わず試したくなる――「1秒たりとも止められない」リアルタイム接続を支えるGC対策と軽量監視術

## 要約
高並列WebSocketで「keep-alive」を単純に送るとGCやコンテキストスイッチでサービスが落ちる。この記事は、ゼロ/低割当て設計（プリミティブ配列＋VarHandle＋ByteBuffer再利用＋バーチャルスレッドのリーパー）でスケールする心拍検出を解説する。

## この記事を読むべき理由
日本のSaaSやゲーム、チャット系サービスでも数十万接続は現実的な要求。誤った「スケジュール＋オブジェクト生成」でクラッシュする失敗を避け、安定した運用設計を学べるから。

## 詳細解説
問題点（短く）
- ScheduledでTextMessageやByteBufferを大量に割当てるとYoung Genが頻繁に回り、Stop-the-Worldで多数のクライアントが再接続して嵐（reconnection storm）を起こす。
- Thread-per-connectionやボクシングされたタイムスタンプ格納はOS/GCを圧迫する。

解法の核（3つのゼロ割当てパーツ）
1) Connection Registry（プリミティブ配列）
- オブジェクトではなく long[] を使い、時刻をネイティブ配列に直接書く。読み書きで不要なヒープ割当てを避ける。
- VarHandle を使ってメモリ順序を制御し、同期コストを抑える。

例（ack 記録）
```java
// java
private static final VarHandle LAST_ACK = MethodHandles.arrayElementVarHandle(long[].class);
private final long[] lastAckReceived;

public void recordAck(int id) {
    LAST_ACK.setRelease(lastAckReceived, id, System.nanoTime());
}
```

2) Opcode ハンドラ（ACKの受信処理）
- クライアントからの Opcode 11（HEARTBEAT_ACK）到着時は配列へ単一書き込みのみ。バッファ/解析で割当てを行わない。

3) Reaper（タイムアウト検出）—バーチャルスレッドで低コストに待機
- 全接続をスキャンして期限切れを強制クローズ。ブロッキング待機は Virtual Thread で行いプラットフォームスレッドを浪費しない。
```java
// java
Thread.ofVirtual().name("heartbeat-reaper").start(() -> {
  while (running) {
    long now = System.nanoTime();
    for (int i = 0; i < maxConn; i++) {
      if (isTimedOut(i, now)) connectionManager.forceClose(i, "heartbeat_timeout");
    }
    LockSupport.parkNanos(SCAN_INTERVAL_NANOS);
  }
});
```

I/O 最適化：ByteBuffer の再利用
- 毎回 ByteBuffer.allocate を呼ぶと大量割当て。代わりに direct ByteBuffer のテンプレートを作り duplicate() で使う（ラッパーは小さいが実用上十分軽量）。
```java
// java
private static final ByteBuffer HEARTBEAT_TEMPLATE =
    ByteBuffer.allocateDirect(14).put(/* bytes */).flip().asReadOnlyBuffer();

public void sendHeartbeat(SocketChannel ch) {
    ByteBuffer msg = HEARTBEAT_TEMPLATE.duplicate();
    ch.write(msg);
}
```
- さらに割当てを徹底的に減らしたければ ByteBuffer プールを導入（課題として提示されている）。

運用で見るべき指標
- 割当率（Allocation rate）: 目標 < 500 KB/sec（最終的に <100 KB/sec を目指す）
- GC pause（Young Gen <~5ms）
- コンテキストスイッチ（Virtual Threads により大幅削減）
- False timeout の割合（heartbeat_timeouts_total）

実装注意点
- System.nanoTime() を基準にし、VM/ホストでの時刻挙動を確認する
- VarHandle のメモリモデルを理解しておく（setRelease 等）
- DirectByteBuffer のリークに注意（クリーンアップ処理）

## 実践ポイント
- まずは設計の意識変更：「ステートはプリミティブ配列で持つ」「ホットパスはオブジェクト割当てゼロを目指す」。
- VarHandle を使って long[] を書き込む実装を試す（上記コードを参考）。
- HEARTBEAT_TEMPLATE.duplicate() を使い、ByteBuffer の毎回割当てをやめる。さらに改善するなら ByteBufferPool を追加。
- Virtual Threads を使って周期スキャン／待機を実装し、コンテキストスイッチを測定して効果を確認する。
- VisualVM/jconsole などで割当率・GC時間・スレッド数を必ず計測し、閾値をダッシュボード化する。

参考（実装サンプル）
- 元記事のサンプル実装リポジトリ: https://github.com/sysdr/discord-flux/tree/main/day5/flux-day5-heartbeat

以上のパターンは日本のクラウド環境（EKS/GKE/オンプレVMいずれでも）での高同時接続サービスに直接応用でき、GC暴走による大規模障害を未然に防ぐ実務的な手法です。
