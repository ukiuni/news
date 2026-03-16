---
layout: post
title: "A practical step-by-step guide to debugging a real C bug with GDB - GDBで実際のCバグをステップバイステップでデバッグする実践ガイド"
date: 2026-03-16T23:13:57.583Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://levelup.gitconnected.com/how-to-use-gdb-to-debug-a-real-c-bug-step-by-step-86a9cde406a1"
source_title: "A practical step-by-step guide to debugging a real C bug with GDB"
source_id: 381101631
excerpt: "GDBとコアダンプで本番特有のCセグフォを短時間で突き止める手順解説"
---

# A practical step-by-step guide to debugging a real C bug with GDB - GDBで実際のCバグをステップバイステップでデバッグする実践ガイド
本番ログでしか出ない“あるある”なCのクラッシュを、GDBで短時間に突き止める実践テクニック

## 要約
実データで発生するセグメンテーションフォルトを例に、GDBの基本操作（実行・ブレーク・バックトレース・変数確認・ウォッチ）で原因を特定する手順をわかりやすく解説します。

## この記事を読むべき理由
テストでは動くのに本番ログで落ちる――日本のレガシーサービスや組込み系で頻出する問題を、IDE（VS Code）やCIで再現・解析できる実用ノウハウが得られます。

## 詳細解説
問題概略：ログ行をパースする小さなCプログラムがあり、ほとんどの行は3トークンだが、本番で「メッセージ部がない」行が来てNULL参照で落ちる、という典型例。

よく使う手順（要点）
- デバッグ情報付きでコンパイル: gcc -g -O0
- Coreダンプを残す: ulimit -c unlimited
- GDBで実行: gdb ./app → run < sample.log
- クラッシュ後は bt（backtrace）で呼び出し履歴確認
- frame N と info locals / print var でフレーム内状態を見る
- breakpoint / watch で疑わしい関数・変数を監視
- step / next で逐次実行し、どの行でNULLを参照したか特定

簡単なバグ例（トークンをチェックしていない実装）:
```c
#include <stdio.h>
#include <string.h>

int parse_line(char *line) {
  char *lvl = strtok(line, " ");
  char *src = strtok(NULL, " ");
  char *msg = strtok(NULL, "\n"); // msgがNULLの場合がある
  return strlen(msg); // NULL参照でクラッシュ
}
```

GDBでの典型的なやり取り:
```bash
# コンパイル
gcc -g -O0 -o parser parser.c

# 実行・クラッシュ
gdb ./parser
(gdb) run < bad_log.txt

# クラッシュ後
(gdb) bt
(gdb) frame 0
(gdb) info locals
(gdb) print msg
(gdb) break parse_line
(gdb) run < bad_log.txt
(gdb) next   # どこでNULLが来るか確認
```

補助ツール: valgrindでメモリ異常を検出。VS CodeならC/C++拡張でGDBをGUI操作でき、断片的なログ解析も統合可能。

## 日本市場との関連性
- 多くの日本企業はC/C++の既存実装や組込み機器を運用しており、本番データ由来の微妙な入力不整合で落ちるケースが多い。
- ログ文字コード（UTF-8／Shift_JIS）の扱いや、運用ログの多様性を考慮した堅牢なパース実装が重要です。
- 開発現場（オンプレ・組込み・金融バッチ）でGDBスキルは即戦力になります。

## 実践ポイント
- 常に -g でビルド、デバッグ用ビルドは -O0 を推奨。
- 入力は必ずNULLチェック／境界チェックを行う（strtokの戻り値を確認）。
- 本番でしか再現しない場合は core を取得して gdbで解析。
- VS Codeのデバッガ設定（launch.json）にGDBを組み込めば作業効率が上がる。
