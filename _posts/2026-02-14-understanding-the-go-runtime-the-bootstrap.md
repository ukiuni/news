---
layout: post
title: "Understanding the Go Runtime: The Bootstrap - Goランタイム入門：ブートストラップ"
date: 2026-02-14T13:02:34.883Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://internals-for-interns.com/posts/understanding-go-runtime/"
source_title: "The Bootstrap | Internals for Interns"
source_id: 951106522
excerpt: "空のGoが大きく遅い理由をランタイム起動処理から解剖し、起動時間とサイズ改善策を提示"
image: "https://internals-for-interns.com/images/go-runtime-header.webp"
---

# Understanding the Go Runtime: The Bootstrap - Goランタイム入門：ブートストラップ
魅せるタイトル: なぜ「何もしない」Goプログラムが大きくて遅いのか？Goランタイムの起動処理をやさしく解剖する

## 要約
Goバイナリに組み込まれるランタイムは、main()が呼ばれる前にメモリアロケータ、GC、スケジューラなど多数の初期化を行う。この「ブートストラップ」処理を理解すると起動時間や挙動の原因がわかる。

## この記事を読むべき理由
スタートアップやサーバーレス、低レイテンシサービスで「起動時間」「バイナリサイズ」「並列性」が課題になることが多い日本の現場にとって、Goが実行される最初の段階（何がいつ起きるか）を押さえることはパフォーマンス改善やデバッグに直結します。

## 詳細解説
- なぜ「何もしない」プログラムでも違いが出るか  
  Cの空プログラムとGoの空プログラムを比べると、Goの方がバイナリが大きく起動はわずかに遅い。理由はGoバイナリにランタイム全体（メモリアロケータ、ガベージコレクタ、スケジューラなど）が組み込まれ、mainより前に多くの初期化を行うため。

- 実際のエントリポイント  
  実行時の最初の関数はmain.mainではなく、アセンブリのエントリ（例: _rt0_amd64_linux）で、ここからrt0_goにジャンプしてブート処理が始まる。

- 初期に作られるもの（g0 と m0）  
  g0：ランタイム専用のgoroutine（スケジューラ等のため）。  
  m0：最初のOSスレッド。これらがないとgoroutineやスケジューラは動けない。

- TLSとCPU機能チェック  
  スレッドローカルストレージを使って「今実行中のgoroutine」を高速に特定。CPU命令セット（AES等）を事前チェックし、動かない環境では早期にエラーを出す。

- 重要なGo側初期化（rt0_go → schedinit）  
  schedinitは起動処理の中核で、以下を順に構築する：
  - worldを停止した状態で初期化（安全な初期化のため）
  - stackinit：goroutine用のスタックプール（初期は小さく、動的に拡張）
  - mallocinit：アロケータ（サイズクラスと各Pごとのキャッシュでロック競合を減らす）
  - cpuinit / alginit：CPUフラグの詳細確認とmapハッシュ選定（AES利用可否で性能差）
  - modules/typelinks/itabsの構築：型情報・インターフェース解決のためのテーブル
  - goargs / goenvs / secure / checkfds：コマンドライン・環境・セキュリティ検査
  - GODEBUGのパース：inittrace, schedtrace, gctrace 等のデバッグオプションを適用

- GCとP（Processor）の初期化  
  gcinitでGCのパーサー・ペーサー・スイーパー構造を用意するが、GCはすぐには有効化されない（後でgcenableを呼ぶ）。PはGOMAXPROCSに基づく「作業台」で、各Pは実行キューとローカルアロケータを持つ。

- worldStart → runtime.main → sysmon  
  すべて整った段階でworldを開始し、最初の実行goroutine（runtime.main）を起動。runtime.mainは最大スタックサイズの設定、sysmon（システム監視スレッド）の起動、メインgoroutineのメインスレッド固定などを行い、最終的にユーザーのmainが呼ばれる。

## 実践ポイント
- 起動時間が気になるときは「initやグローバル初期化」を見直す（ブート時に動く処理は全て影響する）。  
- バイナリのサイズ削減：ビルド時にデバッグ情報やシンボルを削る（例: リリースビルドでstrip/ldflagsを検討）※環境依存の副作用に注意。  
- 並列度調整：GOMAXPROCSを環境やワークロードに合わせて設定するとP数とアロケータ挙動に影響。  
- デバッグと計測：GODEBUGでinittrace / gctrace / schedtraceを有効にして起動処理やGC、スケジューラの挙動を可視化する。  
- 内部を覗くコマンド（診断に便利）:
```bash
# バイナリのエントリポイント確認
readelf -h your_binary | grep "Entry point"

# アドレス→シンボル参照（Go固有）
go tool nm your_binary | grep <address>
```

以上を押さえれば、なぜGoが「ちょっと重い」か、そしてその恩恵（軽量goroutineや高速アロケーション）をどう現場で活かすかが見えてきます。
