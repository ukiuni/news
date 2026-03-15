---
layout: post
title: "SBCL Fibers – Lightweight Cooperative Threads - SBCL Fibers：軽量協調スレッド"
date: 2026-03-15T01:21:26.766Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://atgreen.github.io/repl-yell/posts/sbcl-fibers/"
source_title: "SBCL Fibers: Lightweight Cooperative Threads | REPL Yell!"
source_id: 47382398
excerpt: "SBCLのFibersで数万接続を逐次コードのまま軽量かつ高速に処理"
---

# SBCL Fibers – Lightweight Cooperative Threads - SBCL Fibers：軽量協調スレッド
SBCLで「スレッド感覚」のまま大規模同時接続を扱う——Fibersで作るシンプルで高速な並行処理

## 要約
SBCL用のユーザ空間協調スレッド実装「Fibers」は、OSスレッドより遥かに軽量なスタックと低コストなコンテキスト切替で、数万コネクション級のI/O多めワークロードをシンプルな逐次コードで扱えるようにする技術です。

## この記事を読むべき理由
日本でも高同時接続を扱うサーバやIoTゲートウェイ、研究用途の並列処理で「スレッド数が増えすぎる」「イベント駆動でコードが複雑化する」といった課題は身近です。Fibersはメモリ効率と可読性（逐次コード維持）を両立する現実的な選択肢を提供します。

## 詳細解説
- 背景と利点：OSスレッドは制御スタック（典型的に8MB）やカーネルコストが重く、10k接続だとスタック領域だけで膨大になる。イベントループはスケーラブルだが制御フローが分かれ、デバッグや例外処理が辛くなる。Fibersはユーザ空間で協調的にスケジューリングされ、逐次的なプログラミングを保ちながら軽量に多数を動かせる。
- リソース設計：デフォルト制御スタックは約256KB、バインディングスタックは約16KB。スタックはプール化され madvise(MADV_DONTNEED) で再利用されるため、作成コストは低い。
- 高速切替：文脈切替はユーザ空間で呼び出される手書きアセンブリを使い、callee-savedレジスタのみを保存／復元。ヒープ割当やロックを避け、サブマイクロ秒レベルの切替を目指す。
- GC統合と正確性：SBCLの世代別・圧縮GCに対応するため、サスペンド中のファイバーのスタック／binding情報はGCが確実に見つけられるよう設計されている。動的バインディング、unwind-protect、handler-case等もファイバー内で正しく動作する。
- スケジューラ設計：各OSキャリアスレッドに対して一つのスケジューラを持ち、Chase–Levロックフリーデックでワークステーリングを行い、マルチコアを自動活用。アイドル検出や期限管理（ヒープによる期限スケジューリング）、I/O多重化（epoll/kqueue等）との統合も備える。
- ファイバーAPIの要点：
  - make-fiber (function &key name stack-size binding-stack-size initial-bindings)：ファイバー生成。initial-bindingsで特別変数の初期値を渡せる。
  - fiber-yield (&optional wake-condition)：自発的に一時停止。wake-conditionを与えるとその述語で再開タイミングを決められる。
  - fiber-sleep seconds：期限付き待ち（スケジューラの期限ヒープと統合）。
  - fiber-join / fiber-result：終了結果の取得。例外は結果としてキャプチャされる。
  - ピン（pin）機能：FFIなどで安全に中断不可にしたいときはピン。ピン中はブロッキングプリミティブがOS実装にフォールスルーする。
- I/O連携：ファイルディスクリプタ→ファイバーの待ち表を保持し、epoll/kqueueを使った効率的な待ち合わせを行う。エッジトリガ＋ワンショットで過剰ポーリングを回避。
- 実装上の工夫：ゼロ割当てパス、スタックガードページでオーバーフロー検出、バインディングスタックの保存/復元方式、キャリア間移動時のレジスタパッチなど。

## 実践ポイント
- 試す方法：SBCLの:sb-fiber機能を有効にして使う（local-target-features.lisp-expr に :sb-fiber を追加）。実験ブランチは atgreen/sbcl の fibers-v2。
- すぐに使えるAPI：make-fiberで逐次処理を書く感覚のまま多数の接続処理を実装し、fiber-yield／fiber-sleepでI/O待ちを協調的に行わせる。
- メリットの活かしどころ：I/O待ちが主で、各リクエストの計算が軽いWebサーバやプロキシ、コネクション大量のサービスでメモリとデバッグ性が劇的に改善する。
- 注意点：
  - FFIや長時間ブロッキング処理はpinで保護すること（さもないとキャリアをブロックしてしまう）。
  - 深い再帰や大量のネストされた特殊変数がある場合はスタックサイズ（binding-stack-size）を調整する。
  - GC連携に敏感な実装なので、ランタイム更新や未テストの低レイヤ変更には注意。
- 実用例：既存のHunchentootなどのサーバをファイバー対応にすると、イベント駆動への全面書き換えをせずにスケール改善が期待できる（SSLや外部ライブラリの扱いは要確認）。

興味があればfibers-v2ブランチで触ってみると、効果（メモリ削減、切替コスト、開発体験の改善）が実感できるはずです。
