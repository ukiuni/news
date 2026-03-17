---
layout: post
title: "Building a Shell - シェルを作る"
date: 2026-03-17T10:59:28.926Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://healeycodes.com/building-a-shell"
source_title: "Building a Shell — Andrew Healey"
source_id: 47410532
excerpt: "3時間で動くミニシェルを作りながらプロセス／パイプ／環境変数の仕組みを丸ごと理解する方法"
---

# Building a Shell - シェルを作る
「自作シェルでUnixの本質を掴む：3時間で動くミニシェルを作ってみよう」

## 要約
Andrew Healeyの「Building a Shell」を日本語で平易に再構成。対話ループ、トークン化、fork/exec、ビルトイン（cd）、環境変数展開、パイプ、そして行編集（readline）まで、実際に動く「おもちゃシェル」を段階的に作る流れを解説します。

## この記事を読むべき理由
シェルの仕組みは日々使うけど意外とブラックボックス。自作してみると、プロセス生成・入出力の接続・終了ステータスや信号処理など、実務で役立つOS／DevOpsの基礎が腹落ちします。日本の開発現場（ローカル開発、CI、コンテナ運用、WSL利用者）にも直結する知識です。

## 詳細解説
- REPL（Read–Eval–Print Loop）  
  シンプルなループ：プロンプト表示→行読み取り→評価→繰り返し。状態として最後の終了コードや対話モードフラグを保持します。

- 行のトークン化（tokenize）  
  空白で分割して argv 形式にする。まずは引用符やリダイレクションを無視して実装し、パイプ記号 '|' は構文として分離しておく。

- コマンド実行（fork + exec）  
  親シェルが生き続けるため、子プロセスを fork して execvp で置き換える。親は waitpid で子の終了を待ち、EINTR（割り込み）を受けたら再試行する実装が重要。子では _exit を使い標準ライブラリの重複クリーンアップを避けます。

  ```c
  // C
  pid = fork();
  if (pid == 0) {
      execvp(argv[0], argv);
      perror(argv[0]);
      _exit(errno == ENOENT ? 127 : 126);
  }
  while (waitpid(pid, &status, 0) < 0) {
      if (errno != EINTR) { perror("waitpid"); break; }
  }
  ```

- ビルトイン（cd の扱い）  
  chdir は子プロセスでやっても親に影響しないため、cd はシェル自身で実行する必要がある。単独の cd は HOME 環境変数を使うのが慣習。

- 環境変数展開（$NAME, $?）  
  トークン単位で簡易展開を適用。特に $? は直前コマンドの終了ステータス表示に使い、未設定変数は空文字に展開する設計が学習に向く。

- パイプ（|）の接続  
  N コマンドのパイプラインは N-1 個の pipe() を作り、dup2 で stdin/stdout を差し替える。親は不要なファイルディスクリプタを閉じつつ次のコマンドへ読み口を渡す。プロセス間の同期はカーネルのパイプバッファにより自動的に行われる。

- 行編集と補完（readline）  
  ターミナルのエスケープ列だけでは編集が難しいため、readline を使って履歴・タブ補完を実装。補完はジェネレータ関数で現在のディレクトリや $PATH をスキャンして候補を返す。

## 実践ポイント
- 学習順序：まず REPL → トークン化 → fork/exec → ビルトイン(cd) → 環境変数展開 → パイプ → readline の順で機能追加すると挫折しにくい。  
- 実行環境：Linux/Mac、または WSL があればすぐ動作確認できる。  
- デバッグのコツ：fork/exec の失敗は perror で原因確認、waitpid は EINTR を再試行。ファイルディスクリプタ漏れに注意。  
- 仕事での応用：シェル実装で学んだ知識は、コンテナエントリポイント、CI スクリプトのデバッグ、プロセス設計に直結する。  
- 参考実装を読み比べて、まずは小さく動くものを作ること（例：tokenize は簡易で良い）。
