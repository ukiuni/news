---
  layout: post
  title: "coco: a simple stackless, single-threaded, and header-only C++20 coroutine library - coco: シンプルなスタックレス／シングルスレッド／ヘッダーオンリーな C++20 コルーチンライブラリ"
  date: 2026-01-02T04:17:32.662Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "http://luajit.io/posts/coco-cpp20-coroutine/"
  source_title: "coco: a simple stackless, single-threaded, and header-only C&#43;&#43;20 coroutine library | Jinhua Blog"
  source_id: 473223575
  excerpt: "C++20のヘッダーオンリーなコルーチンでGo風awaitとio_uring高速I/Oを実現"
  image: "//luajit.io:80/magic_shield.png"
---

# coco: a simple stackless, single-threaded, and header-only C++20 coroutine library - coco: シンプルなスタックレス／シングルスレッド／ヘッダーオンリーな C++20 コルーチンライブラリ
驚くほど「Goっぽく」書けるC++20コルーチン。io_uring と組み合わせて、高性能かつ読みやすい非同期コードが実現できる小型ライブラリの紹介。

## 要約
coco はヘッダーオンリーで C++20 のネイティブコルーチンを使い、Go のチャネルや waitgroup に似たプリミティブを提供するシングルスレッド向けライブラリ。コールバック地獄を排して、io_uring 等の高性能 I/O と親和性の高い非同期/await スタイルを実現する。

## この記事を読むべき理由
- 日本でも io_uring や epoll ベースの高性能サーバを C++ で書く需要が増えている。
- コールバックや状態マシンで分散したロジックに苦しんでいるエンジニアに、読みやすく保守しやすい代替を提示する。
- 小さなヘッダーライブラリで採用コストが低く、既存コードへ段階的に導入しやすい。

## 詳細解説
- 基本設計
  - C++20 のコルーチン機能をそのまま利用（async/await）。コンパイラが状態管理を生成するため、マクロや手作りの state-machine より型安全でデバッグしやすい。
  - ヘッダーオンリー、外部依存なし。スタックレス（コルーチンフレームはヒープ上に確保）、単一スレッドでロック不要という方針。
  - シンプルな FIFO スケジューラで協調的スケジューリングを行うため再入でのスタック枯渇を防ぐ。

- 主要プリミティブ
  - chan_t<T>：Go のチャネルに近い API。read/write は co_await で待てる。待機者の復帰は scheduler によるスケジュールで行われるため安全。
  - wg_t（waitgroup）：複数ワーカーの完了待ち。wg.add()/done()/wait() を使って同期。
  - go() と join()：コルーチンを生成してスケジュールし、join() で完了を待つ（co_await go(...).join(); の形）。

- io_uring と組み合わせた利用
  - io_uring の完了を awaiter に結びつけ、完了イベントで scheduler にコルーチンハンドルを登録して再開するという設計。結果として I/O イベントループは「スケジュールするだけ」の役割に集約され、ビジネスロジックは直線的に記述できる。
  - 結果として callback ベースの実装に比べて可読性と保守性が大幅に向上する。

- パフォーマンス特性
  - コルーチンフレーム以外に毎回ヒープ割当てが発生しないよう設計され、ゼロコスト抽象に近い。
  - シングルスレッド設計によりロック競合がなく、FIFO スケジューリングで実行順序は予測可能。
  - スタックレスなので Boost.Context 等のスタックフル実装よりメモリ効率が良い。

- 重要な注意点
  - co_await / co_yield は「トップレベルのコルーチン関数内」でのみ期待通りに使える。補助関数内で co_await する場合は join() を使う設計を守る必要がある。
  - ローカル変数への参照／ポインタはサスペンドを跨ぐと危険（コルーチンフレームの移動や寿命に注意）。RAII オブジェクト自体はコルーチン内で正常に動くが、生ポインタや参照を跨がないこと。
  - スケジューラ方式のため、即時再開（直ちに resume）で深い再帰的呼び出しが発生するケースを避け、スケジュールキューによる復帰が行われる。

- 典型的な使い方（簡潔な例）
```cpp
// C++
co_t my_coroutine(int id) {
    std::cout << "Coroutine " << id << " started\n";
    co_yield resched; // 再スケジュールして一度制御を返す
    std::cout << "Coroutine " << id << " resumed\n";
    co_return;
}

int main() {
    auto coro = my_coroutine(1);
    coro.resume();
    scheduler_t::instance().run();
}
```

## 実践ポイント
- まずは examples ディレクトリの小さな producer/consumer や waitgroup のサンプルで試す。GitHub リポジトリをクローンしてヘッダーをプロジェクトに追加するだけで試用可能。
- epoll / io_uring ベースの既存コードを置き換える際は、I/O の completion→awaiter の結びつけと scheduler.schedule(handle) の流れを実装すれば段階的移行が可能。
- co_await を補助関数内で直接使わない設計規約をチームで徹底する（代わりに go(...).join() を使う）。
- ローカル参照や生ポインタを跨いだサスペンドは禁止。代わりにスマートポインタや値渡しで安全性を保つ。

