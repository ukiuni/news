---
layout: post
title: "Detecting file changes on macOS with kqueue - macOSでkqueueを使ってファイル変更を検知する"
date: 2026-03-28T20:26:07.345Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.vegardstikbakke.com/kqueue/"
source_title: "Detecting file changes on macOS with kqueue — Vegard Stikbakke"
source_id: 47508710
excerpt: "kqueueでmacの低遅延ファイル監視をGoで実装し確実な自動リロードを実現"
---

# Detecting file changes on macOS with kqueue - macOSでkqueueを使ってファイル変更を検知する
macの開発ループを一行で自動化する：kqueueで軽量かつ低レイテンシなファイル監視

## 要約
kqueueはmacOSのカーネルイベント通知機構で、ファイル単位の変更（書き込み）を効率的に検知できる。元記事はCでのテストからGo実装（reloadツール）への組み込みまで丁寧に解説している。

## この記事を読むべき理由
ローカル開発でファイル変更をトリガーにビルド／リロードするツールは必須。mac上で「何が」起きているかを理解すると、軽量で確実なウォッチャーを自作でき、既存ツールの選択理由（kqueue vs FSEvents vs ポーリング）が見えてきます。

## 詳細解説
- kqueueの基本
  - kqueue()でカーネル側のイベントキューを作成し、kevent()で登録・受信を行う。
  - kevent構造体の主要フィールド：ident（監視対象のfd）、filter（例：EVFILT_VNODE）、flags（EV_ADD, EV_CLEARなど）、fflags（NOTE_WRITE 等）、udata（ユーザデータ：ここではファイル名を格納）。
- ファイル監視の仕組み
  - ファイル単位の監視にはEVFILT_VNODEとfflagsのNOTE_WRITEを使うと「書き込み発生」を受け取れる。
  - EV_ADDで登録、EV_CLEARでイベント状態をクリアしないと同じ変更を繰り返し受け取る可能性がある。
- ディレクトリ監視の落とし穴
  - 既存ファイルの更新はディレクトリ自体のイベントだけでは検知できない（ディレクトリの書き込みは新規追加/削除を示す）。既存ファイルの変更は各ファイルを個別に開いて監視する必要がある。
  - そのため新規ファイルが作られたらそのファイルを追加登録するロジックが必要。
- 実装のポイント（C→Go）
  - CではO_EVTONLYでopenしてEV_SET／keventで登録する。  
    ```c
    // C: EV_SETでの登録例
    EV_SET(&changes[i], fd, EVFILT_VNODE, EV_ADD | EV_CLEAR, NOTE_WRITE, 0, (void*)filename);
    ```
  - Goではunix.Kqueue / unix.Keventを使い、ファイルは O_EVTONLY | O_CLOEXEC で開く。kqueue自体にも CloseOnExec を設定して、フォーク＋execで子プロセスにfdが漏れないようにする。
    ```go
    // Go: 追加時の骨子
    fd, _ := unix.Open(path, unix.O_EVTONLY|unix.O_CLOEXEC, 0)
    unix.Kevent(kq, []unix.Kevent_t{{Ident:uint64(fd), Filter:unix.EVFILT_VNODE, Flags:unix.EV_ADD|unix.EV_CLEAR, Fflags:uint32(unix.NOTE_WRITE)}}, nil, nil)
    ```
- 注意点とトレードオフ
  - kqueueは「監視対象ごとにopenしたfdが必要」→大規模ツリーではfd枯渇する可能性あり。
  - FSEventsはシステムワイドでスケーラブルだが粒度が粗い／APIが別。
  - 単純なポーリングは実装が楽だが効率が悪い。

## 実践ポイント
- 小〜中規模のプロジェクト（ファイル数が程々）で、低レイテンシに確実に変更を拾いたいならkqueueは良い選択。
- Go実装時は必ず O_CLOEXEC / CloseOnExec を設定して、子プロセスへfdを漏らさないこと。
- ディレクトリ監視は「ディレクトリ自体」と「その中の各ファイル」を両方監視する必要がある。新規作成時に追加登録する仕組みを入れること。
- 大規模ツリーや大量ファイルを監視するならFSEventsや既存のfsnotify（裏でFSEventsを使うことも）を検討する。
- 実装例を参照してまずは小さなreloadツールを作り、変更検知→短いバッチでコマンド再実行（デバウンス）を入れると実用的。

元記事のGo版reloadはGitHubで公開されているので、実際に動かして挙動を確かめると理解が深まります。
