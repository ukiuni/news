---
layout: post
title: "I Put a Full JVM Inside a Browser Tab. It \"Works\". Technically. Eventually. - ブラウザタブにフルJVMを入れてみた。技術的には動く、でも遅い"
date: 2026-03-03T02:26:27.558Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://bmarti44.substack.com/p/i-put-a-full-jvm-inside-a-browser"
source_title: "I Put a Full JVM Inside a Browser Tab. It &quot;Works&quot;. Technically. Eventually."
source_id: 392372513
excerpt: "ブラウザだけで227MBのWASM上にフルJVMを起動し、約55秒で動くデモの仕組みを詳解"
image: "https://substackcdn.com/image/fetch/$s_!Jt88!,w_1200,h_675,c_fill,f_jpg,q_auto:good,fl_progressive:steep,g_auto/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F35345332-86f8-4688-a27f-00f872c33bdd_1024x608.png"
---

# I Put a Full JVM Inside a Browser Tab. It "Works". Technically. Eventually. - ブラウザタブにフルJVMを入れてみた。技術的には動く、でも遅い

55秒でHello World？ブラウザ内に丸ごとJVMを詰め込んだ“やってみた系”プロジェクトの全貌

## 要約
ブラウザでサーバ不要にJavaを動かす実験「JavaBox」。227MBのWASMにEmscripten版QEMUを詰め、Alpine Linux＋OpenJDKを復元するスナップショットでブラウザ内に“温まった”JVMを持ち込み、最短で約55秒でHello Worldが出る仕組みを実現している。

## この記事を読むべき理由
ブラウザだけでJDK環境を提供するという発想は、ドキュメント上の「Try it」機能やシェア可能なコードスニペットの提供に新たな選択肢を与える。日本の教育現場や技術ドキュメント運営者が“インストール不要”で体験を配る方法として興味深い実験例です。

## 詳細解説
- 全体の構成（6層の“ロシア人形”）
  - ブラウザ -> Cloudflare Worker -> 227MBのWebAssembly blob  
  - BlobはEmscriptenでビルドしたQEMU（ソフトウェアCPUエミュレーター）を含む  
  - QEMUがLinuxカーネルを起動し、Alpine Linux上でOpenJDK 21を動かす
- 性能の問題と解決
  - 直接javacを毎回立ち上げると、QEMU(TCG)＋WASMの下でJVM起動だけで「12分」かかるケースが発生  
  - 対策として作ったのが CompileServer（常駐JVMデーモン）  
    - javax.tools.JavaCompilerをプロセス内で使い、stdin経由でソースを受け取りその場でコンパイル・実行  
    - URLClassLoaderでクラスをロードして実行するためJVM再起動が不要に
- スナップショットの活用
  - container2wasmのスナップショット機能で、ビルド時に起動・ウォームアップした状態を保存  
  - ブラウザ側ではスナップショット復元で起動時間を短縮（約20秒でCompileServerが準備完了）
- プロトコルと実行時間
  - シンプルなテキストプロトコル（例: JBOX_PING → JBOX_PONG、JBOX_COMPILE…JBOX_END）でやり取り  
  - 実測：ページ読み込みからCompileServer準備約20秒、HelloWorldの初回コンパイル＋実行に約35秒、合計約55秒
- 実行環境の制約
  - ゲストに128MBメモリ、JVMは -Xmx64m、JITは -Xint（JIT無効）で動作 — エミュレーション下ではJITの恩恵が薄いため
  - SharedArrayBufferなどブラウザ側の要件（特定のHTTPヘッダやクロスオリジン設定）に注意
- トレードオフ
  - ペイロードが大きい（227MB）・起動遅延があるため、実運用のオンラインIDEやビルドサーバーの代替にはならないが、教育・ドキュメントの「体験用」には可能性あり

## 実践ポイント
- まずデモで感触を掴む（作者のデモ／GitHubリポジトリを確認）  
- ブラウザ内で言語環境を提供する場合：
  - 常駐コンパイラ／ランタイムを用意して「起動コスト」を避ける  
  - スナップショットで“ウォームアップ済み”イメージを配る  
  - エミュレーション環境ではJVMヒープを小さくしJITを無効化する（-Xmx, -Xint）  
  - ペイロード削減（圧縮・分割配信）や背景プリフェッチでUX改善を検討する
- 応用例：ドキュメントの「Try it」ボタン、共有可能なJavaスニペット、オフサーバ型の学習プラットフォーム

参考: 実装はGitHub上で公開されており、ブラウザで動くデモも存在する（元記事作者のデモ／リポジトリを参照）。
