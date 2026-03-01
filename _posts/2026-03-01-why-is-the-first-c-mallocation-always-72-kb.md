---
layout: post
title: "Why is the first C++ (m)allocation always 72 KB? - なぜ最初のC++の(m)allocは常に72KBなのか？"
date: 2026-03-01T11:01:59.308Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://joelsiks.com/posts/cpp-emergency-pool-72kb-allocation/"
source_title: "Why is the first C&#43;&#43; (m)allocation always 72 KB?"
source_id: 47205129
excerpt: "起動直後の謎72KBはlibstdc++の非常用プールで、GLIBCXX_TUNABLESで調整可能"
---

# Why is the first C++ (m)allocation always 72 KB? - なぜ最初のC++の(m)allocは常に72KBなのか？
起動直後に勝手に現れる「72KB」の正体 — libstdc++の非常用（exception）プールを読み解く

## 要約
多くのC++プログラムで起動直後に約72KBのmallocが発生するのは、libstdc++が例外を投げられるようにするための「非常用プール（emergency pool）」を遅延初期化するため。これは意図的な確保でありメモリリークではない。

## この記事を読むべき理由
- 起動時の不可解なメモリ割当（約72KB）を目にして「リーク？」と混乱する開発者が多い。  
- カスタムmallocやLD_PRELOADでのテスト、Valgrind結果の解釈、組み込みやメモリ制約環境での挙動理解に直結する知識だから。

## 詳細解説
- 発生源：libstdc++の例外処理用コード（libsupc++の eh_alloc.cc）が、mallocが失敗したときに例外オブジェクトを確保するためのバッファを確保する。これが「非常用プール」。起動時に遅延（lazy）初期化されるため、多くのプログラムで最初のmallocがこのサイズになる。  
- サイズの決まり方：プールバッファの大きさは大まかに N * (S * P + R + D) という式で計算され、デフォルトではマクロで次が設定される。  
  - EMERGENCY_OBJ_SIZE = 6（例外オブジェクトを見積もる単位、sizeof(void*) 単位）  
  - EMERGENCY_OBJ_COUNT = 4 * __SIZEOF_POINTER__ * __SIZEOF_POINTER__  
  - P = sizeof(void*)（64-bitなら8）などのパラメータに依存するため、環境（64/32bit、ライブラリ版）で最終サイズが変わり、典型的に64bit環境で約72KBとなる。  
- 実証：GLIBCXX_TUNABLESを使ってobj_countを下げると最初の確保量が減る（例えば10にすると数KBになる）。逆に0にすればプール確保を無効化できる（あるいはビルド時にstaticプールオプションを使う）。  
- Valgrindとの関係：古いValgrindはこのメモリを「still reachable（解放されていないが到達可能）」と報告しやすく、誤ってリークと判断されることがあった。新しいツール側で__freeres相当を呼んで解放する仕組みが入れられ、誤認は減っている。

例：LD_PRELOADでカスタムmallocを試すとプール確保が観察されるコマンド例
```bash
# カスタムmallocを挟んで実行（デバッグログ収集など）
LD_PRELOAD=/home/you/mymalloc/libmymalloc.so LOG_ALLOC=log.txt ls
```

GLIBCXX_TUNABLESでオブジェクト数を変える例
```bash
GLIBCXX_TUNABLES=glibcxx.eh_pool.obj_count=10 LD_PRELOAD=/home/you/mymalloc/libmymalloc.so LOG_ALLOC=log.txt ls
# 確認: log.txt の最初の行が小さくなる
```

## 日本市場との関連性
- 日本の企業でも組み込み機器、金融系の長時間稼働サービス、パフォーマンスクリティカルなC++アプリで「起動時の予期しないメモリ確保」は運用・監査で問題視されることがある。  
- LD_PRELOADでメモリ挙動を調査する開発・検証文化は国内でも広く行われるため、この知見はデバッグ効率向上に直結する。  
- メモリ制約の強い組み込み案件では、libstdc++をビルドする際のオプション（static pool など）やチューニングが現場の選択肢になる。

## 実践ポイント
- 「72KB = バグ」ではない：まずはlibstdc++の非常用プールを疑う。  
- サイズを変える：GLIBCXX_TUNABLES=glibcxx.eh_pool.obj_count=<n> で起動時の確保量を調整可能。  
- 無効化／静的化：obj_count=0で確保を避けられる。あるいは libstdc++ を --enable-libstdcxx-static-eh-pool でビルドする。  
- Valgrindの誤検出に遭遇したら、ツールのバージョンと __freeres 対応を確認する（新しいValgrindでは改善されている）。  
- カスタムmallocのテスト時は、この初回確保を想定しておく（特にLD_PRELOADでの比較テストではノイズになる）。

以上を知っておけば、起動直後の不可解なメモリ確保に慌てる必要はありません — まずは非常用プールの存在とチューニング方法をチェックしましょう。
