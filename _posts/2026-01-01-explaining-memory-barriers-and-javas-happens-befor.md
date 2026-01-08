---
  layout: post
  title: "Explaining Memory Barriers and Java’s Happens Before Guarantees - JavaのメモリバリアとHappens‑Before保証を分かりやすく"
  date: 2026-01-01T15:45:02.877Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://medium.com/@kusoroadeolu/explaining-memory-barriers-and-javas-happens-before-guarantees-34309c5b60c0"
  source_title: "Explaining Memory Barriers and Java’s Happens Before Guarantees"
  source_id: 474954277
  excerpt: "volatileとsynchronizedで学ぶJMMのhappens‑beforeとメモリバリア"
---

# Explaining Memory Barriers and Java’s Happens Before Guarantees - JavaのメモリバリアとHappens‑Before保証を分かりやすく
CPUとコンパイラが「勝手に並べ替える」世界で、volatileとsynchronizedがスレッド間の可視性と順序をどう守るかを明快に解説する

## 要約
JavaのHappens‑Beforeは単なる仕様書の言葉ではなく、JVMが実装するメモリバリア（store-load, store-store, load-load, load-store）によって実際に保証される。volatileは軽量な可視性保証、synchronizedはより強い同期（エントリ／退出でのフラッシュと読み直し）を提供する。

## この記事を読むべき理由
マルチスレッド／マルチコア時代、可視性の誤解はバグの温床。特にAndroidアプリやサーバサイドJava（国内のミッションクリティカルなサービス）では、期待どおりの動作を得るための同期プリミティブの正しい使い方が必須である。

## 詳細解説
- プログラム順序（program order）  
  スレッド内部では命令の実行順序が保証されるが、他スレッドから「見える」順序は保証されない（＝データレースが起きる）。したがって単に順に書いたから安全とは限らない。

- 可視性とメモリリオーダリングの本質  
  「CPUやコンパイラは再順序化するが、JMMはどの再順序化が観測可能かを定義する」。別スレッドから見ると一部の書き込みだけ見えるなどの現象が生じる。

- 単純なデータレース例
```java
// java
class SomeClass {
    int x = 0;
    int y = 0;
    void write() { ++x; ++y; } // Thread1
    void read()  { System.out.println(x); System.out.println(y); } // Thread2
}
```
Thread2が0と1を読むような不整合が起こりうる。同期が必要。

- volatile の振る舞い（実装視点）
  - volatile書き込み前に store-store バリアを挿入：それより前の書き込みが後ろへ再順序化されないようにする。
  - volatile書き込み後に store-load バリアを挿入：その後の読みがvolatile書き込みより前に観測されないようにする（高コスト）。
  - volatile読み後にも load-load と load-store バリアを入れ、以後の操作が読みより前に実行されるのを防ぐ。  
  ボタン一つで「参照の最新値はすぐ見える」が、参照先オブジェクト内部の非volatileフィールドの可視性までは保証しない点に注意。

```java
// java
class Holder { int count; }
class SomeClass {
    private volatile Holder h;
    void publish(Holder p) { h = p; } // volatile ensures visibility of reference
    void updateCount(int c) { h.count = c; } // countはvolatile保証外
}
```

- synchronized の振る舞い（モニタの入退室）
  - 監視対象に入るとき：load-load / load-store バリア → キャッシュ無効化して最新値を読み込む。
  - 監視対象を出るとき：store-store / store-load バリア → 書き込みをフラッシュして他スレッドへ見えるようにする。  
  これにより「ロックの解放はその前の書き込みを他に見せる」「ロック取得は最新の値を読む」が成り立つ。

- 他のストレートなルール  
  - モニタのunlockは同一モニタの次のlockより先にhappens‑beforeする。  
  - Thread.start は開始スレッド内の全アクションより先にhappens‑before、スレッド終了の検出も同様に保証。  
  - これらは合成（推移性）される。

- JMMと実装の差分  
  JMM自体は抽象的な観測可能性を規定しており、具体的なメモリバリアは典型的なJVMの実装戦略（x86/ARM）を説明する便法である。

## 実践ポイント
- 単純なフラグだけなら volatile を使う（状態の全体整合が必要な場合は不可）。  
- 複数フィールドを一貫して更新するなら synchronized / Lock を使う。  
- 不変オブジェクト（finalフィールド）で安全な公開を行うとシンプルで高速。  
- 複合操作や高性能要件は java.util.concurrent（Atomic系、ConcurrentHashMap、Lockなど）を優先。  
- オブジェクト公開の正しい順序：初期化完了 → volatile参照に代入（またはロック経由で公開）。  
- テストには concurrency stress ツール（例：jcstress）やスレッドサニタイザ相当の検査を活用し、再現性の低いデータレースを検出する。

短くまとめると、volatileは「参照や単純なフラグの即時可視化」、synchronizedは「複数操作の原子性と確実な可視化」を保証するための道具であり、JMMはそれらの「どこまで保証するか」を定めたルールセットである。実運用では設計段階でどのレベルの保証が必要かを見極め、適切なプリミティブを選ぶことが重要。

