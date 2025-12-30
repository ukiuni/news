---
layout: post
title: "Thread scheduler in c ( green threads) - Cで書かれたスレッドスケジューラ（グリーンスレッド）"
date: 2025-12-30T10:20:08.108Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/FreezB11/thread_scheduler"
source_title: "Thread scheduler in c ( green threads)"
source_id: 434758868
excerpt: "x86_64アセンブリで学ぶ、シグナル駆動のユーザ空間プリエンプティブ・グリーンスレッド実装"
---

# Thread scheduler in c ( green threads) - Cで書かれたスレッドスケジューラ（グリーンスレッド）
誰でも分かる：Cとx86_64アセンブリで学ぶ「ユーザ空間のプリエンプティブ・グリーンスレッド」入門

## 要約
ユーザ空間でコンテキスト切替・スケジューリング・同期を実装した教育向けライブラリ。x86_64アセンブリによるコンテキスト保存とシグナルベースのプリエンプションでラウンドロビンを実現する軽量実装です。

## この記事を読むべき理由
OSや並列処理の内部を実際に動くコードで理解したいエンジニア／学生に最適。日本の大学の授業や社内勉強会での教材、低レイヤ実装の学習教材としてすぐに試せる点が魅力です。

## 詳細解説
- コア設計
  - ユーザ空間でのコンテキスト切替をx86_64アセンブリで実装。ucontext.h を使わずレジスタとスタックを直接保存・復元することで、低レベルの挙動を学べます。
  - スケジューラはラウンドロビン方式。シグナル（タイマー）でプリエンプションを行い、現在スレッドを離脱させて次のスレッドに切り替えます。
  - 同期プリミティブとしてミューテックス（mutex_lock / mutex_unlock）と条件変数（cond_wait / cond_signal）を提供。

- 実装のポイント
  - スレッドはユーザ空間スタック上で動作。スレッド生成時にスタック領域と初期コンテキストを構築します。
  - シグナルハンドラ内で安全にスケジューリングするための注意（非再入可能関数の使用回避、状態保存）を要します。
  - ライブラリは静的 (.a) と共有 (.so) の両方でビルド可能。外部依存は標準Cライブラリのみ。

- 使いどころと制限
  - 学習目的・プロトタイピングに最適。カーネルスレッドやpthreadとの完全互換を期待する用途（高信頼のプロダクション環境など）には不向き。
  - ブロッキングなシステムコールはプロセス全体をブロックするため、実際のアプリで使う場合は注意が必要（非同期I/Oやノンブロッキング設計が必要）。

- 開発体験
  - Makefileでビルド、付属の例やベンチマーク（ex_basic, benchmark_contention）で動作確認が可能。
  - ドキュメント（doc.md）で内部設計の詳細やアセンブリ実装の解説あり。

## 実践ポイント
- まず動かす：リポジトリをクローンして例をビルド・実行し、どのようにスレッドが切替わるかを確認する。
  ```bash
  git clone https://github.com/FreezB11/thread_scheduler.git
  cd thread_scheduler
  make
  ./ex_basic
  ```
- 自分の小さなテストプログラムで thread_create / thread_join を試す（以下はREADMEの例）。
  ```c
  #include "include/thread_lt.h"
  #include <stdio.h>

  void worker(void *arg) {
      printf("Hello from thread %d!\n", (int)arg);
  }

  int main() {
      thread_init();
      int id = 1;
      thread_t *t1 = thread_create(worker, &id);
      thread_join(t1);
      printf("Thread finished execution.\n");
      return 0;
  }
  ```
- 学習の発展：シグナルベースのプリエンプションを理解したら、別のスケジューリング戦略（優先度付き、フェアネス改善）を実装して比較してみる。
- 日本の環境での注意点：x86_64向け実装なので、ARM系（Raspberry Pi等）で試す場合はアセンブリ部分の移植が必要。ビルドは一般的なGCC/clangで動作します。
- 貢献・拡張案：スタックオーバーフロー検知、IO待ちの回避策、より堅牢なシグナルハンドリング、ドキュメントの日本語化などが貢献しやすい箇所です。

## 引用元
- タイトル: Thread scheduler in c ( green threads)
- URL: https://github.com/FreezB11/thread_scheduler
