---
layout: post
title: "Gathering Linux Syscall Numbers in a C Table - CのテーブルにLinuxシステムコール番号を集める"
date: 2026-01-22T08:36:57.410Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://t-cadet.github.io/programming-wisdom/#2026-01-17-gathering-linux-syscall-numbers"
source_title: "Programming Wisdom"
source_id: 46659016
excerpt: "カーネルヘッダを解析してビルド時にsyscall番号表を自動生成し不整合を防ぐ"
---

# Gathering Linux Syscall Numbers in a C Table - CのテーブルにLinuxシステムコール番号を集める
面倒なSyscall番号の差分もこれで解決！ビルド時に自動生成するCテーブルの作り方

## 要約
Linuxのシステムコール番号はアーキテクチャやカーネル版で変わるため、カーネルヘッダやsyscallテーブルから番号を抽出してCの配列（テーブル）を自動生成すると運用が楽になる、という手法の紹介。

## この記事を読むべき理由
- 日本でも多い組込み・クロスコンパイル（Raspberry Pi、IoT、Androidカスタムカーネル等）ではsyscall番号の不一致でバグになりがち。  
- セキュリティ・フォレンジック・低レイヤツール開発で「名前→番号」のマッピングが必須になる場面があるため、有用な実践知だから。

## 詳細解説
- 背景：syscall番号はアーキテクチャ（x86_64, arm64, i386 など）やカーネルの定義ファイル（例: arch/*/entry/syscalls/syscall_*.tbl、include/uapi/asm/unistd.h）によって決まる。ユーザー空間のヘッダだけに頼るとターゲット環境とずれることがある。  
- アプローチ：ターゲットのカーネルソースかインストール済みのヘッダをパースして、"名前"と"番号"のペアを抽出し、ビルドプロセスでCソース／ヘッダを生成する。生成物は例えば下記のような構造体配列になる。  
- 抽出手段の例：
  - カーネルソースの syscall_64.tbl などをawk/grepでパース（各行に番号・ABI・名前が並ぶ）。  
  - Debian系なら /usr/include/x86_64-linux-gnu/asm/unistd_64.h や /usr/include/asm-generic/unistd.h を利用。  
  - auditパッケージの ausyscall --dump でもダンプ可能（環境依存）。  
- 注意点：必ずターゲット環境（実行環境と同じカーネル版／アーキ）から生成する。生成はビルド時に自動化して差分を防ぐ。

例：kernelの syscall_64.tbl をパースしてCヘッダを作る簡易スクリプト（抜粋）

```bash
# bash
# syscall_64.tbl をパースして syscalls_generated.h を作る（簡易版）
grep -E '^[0-9]+' syscall_64.tbl | awk '{print $1, $3}' | \
awk 'BEGIN{print "/* auto-generated */\n#include <stddef.h>\nstruct syscall_entry { const char *name; int num; };\nstatic const struct syscall_entry syscall_table[] = {"}
{ printf "  {\"%s\", %s},\n", $2, $1 }
END{print "};\nstatic const size_t syscall_table_len = sizeof(syscall_table)/sizeof(*syscall_table);"}' > syscalls_generated.h
```

生成されたヘッダを使うCの検索関数（抜粋）：

```c
// c
#include <string.h>
#include "syscalls_generated.h"

int lookup_syscall(const char *name) {
    for (size_t i = 0; i < syscall_table_len; ++i) {
        if (strcmp(syscall_table[i].name, name) == 0)
            return syscall_table[i].num;
    }
    return -1; // not found
}
```

## 実践ポイント
- 1) ターゲットのカーネルソース/ヘッダから必ず生成する（開発環境と実行環境の不整合を防ぐ）。  
- 2) 生成はMakefile/CMakeのビルドステップに組み込む（手作業でコミットしない）。  
- 3) 既存ツールの活用：ausyscallやlibauditのダンプ機能、あるいはディストリのkernel-headersを参照する。  
- 4) セキュリティ注意：番号を直打ちしてsyscallを呼ぶ場合は、ABI差異や権限問題がないか確認する。  
- 5) 日本の組込み/IoT現場では、Raspberry Piや独自ボードでの移植性確保に特に役立つ。

簡潔に言えば、「syscall番号は環境ごとに変わる」→ 「ビルド時にカーネル定義から自動生成してCテーブルにする」のが実用的な解決法です。
