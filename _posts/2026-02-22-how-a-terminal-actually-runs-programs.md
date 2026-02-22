---
layout: post
title: "How a terminal actually runs programs. - ターミナルは実際にどうやってプログラムを実行しているのか"
date: 2026-02-22T08:00:12.474Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://sushantdhiman.dev/write-your-own-shell-terminal-from-scratch/"
source_title: "Write your own Shell (Terminal) from scratch."
source_id: 399614354
excerpt: "forkとexecで動く簡単シェル実装を学び、プロセスの挙動を可視化しよう"
image: "https://static.ghost.org/v5.0.0/images/publication-cover.jpg"
---

# How a terminal actually runs programs. - ターミナルは実際にどうやってプログラムを実行しているのか
0から作るシェル入門：fork と exec で「端末の中身」を動かしてみよう

## 要約
シェルはユーザーのコマンドを受け取り、プロセスを作ってその中で実行する。鍵は fork で子プロセスを作り、exec 系で子プロセスの実行イメージを置き換えること。

## この記事を読むべき理由
OSやコンテナ、組み込み、クラウド運用など日本のエンジニアが直面する領域で「プロセスの振る舞い」を理解しているとデバッグ・最適化力が格段に上がるため。

## 詳細解説
- 端末とシェルの違い：端末はUI（入力欄）で、シェルはコマンドを解釈してOSに実行させるプログラム。
- プロセス：実行中のプログラム。ディスク上の実行ファイルをOSが読み込み、RAM上でCPUが動かすとプロセスになる。
- fork(): 呼び出し元プロセス（親）をコピーして新しいプロセス（子）を作る。子は親と同じアドレス空間のコピーから始まる。fork は子で 0、親で子のPID（>0）を返す。
- execv(): 現在のプロセスの実行イメージを別の実行ファイルで置き換える。引数は実行ファイルのパスと argv 形式の文字列配列（最後は NULL）。
  - 例: execv("/bin/ls", (char*[]){"ls","-a",NULL});
- 親は通常 wait()/waitpid() で子の終了を待つ。これが「シェルがコマンド実行中に待つ」挙動の本質。
- シェルの基本的な流れ：プロンプト表示 → 入力取得 → 解析 → fork() → 子で exec → 親は wait → ループ。
- 実際のコマンドは /bin や PATH 上の実行ファイルなので、execv はフルパス、execvp は PATH 解決を使うと便利。

簡単な骨組み（要点のみ）:
```c
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <sys/wait.h>
#define MAX_INPUT 1024

int main() {
  char input[MAX_INPUT];
  while (1) {
    printf("mysh> "); fflush(stdout);
    if (fgets(input, MAX_INPUT, stdin) == NULL) break;
    input[strcspn(input, "\n")] = 0;
    if (strlen(input) == 0) continue;
    if (strcmp(input, "exit") == 0) break;

    pid_t pid = fork();
    if (pid == 0) {
      char *args[] = {"ls","-a",NULL};
      execv("/bin/ls", args);
      _exit(1); // execv が失敗した場合
    } else {
      wait(NULL);
    }
  }
  return 0;
}
```

## 実践ポイント
- まずは上のコードをコンパイルして実行してみる（Linux）。/bin の中身を確認すると理解が進む。  
- 次の拡張案：入力をトークン解析して任意コマンドを execvp で実行、引数解析、背景実行（&）、シグナル処理（Ctrl+C）、パイプ（pipe + dup2）を実装してみる。  
- 日本の現場では、プロセス管理やコンテナの挙動理解が運用効率と障害対応力に直結するので、小さなシェル実装は良い学習投資。
