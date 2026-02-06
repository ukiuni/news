---
layout: post
title: "Things Unix can do atomically - UNIXが「原子的」にできること"
date: 2026-02-06T06:00:19.882Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://rcrowley.org/2010/01/06/things-unix-can-do-atomically.html"
source_title: "Things UNIX can do atomically &#8212; Crowley Code!"
source_id: 46909468
excerpt: "renameやopen(O_EXCL)でカーネル原子操作を使い安全なデプロイと同期を実現する"
---

# Things Unix can do atomically - UNIXが「原子的」にできること
運用とデプロイで神頼みしなくなる！カーネル任せで安全に動かす「原子操作」テクニック集

## 要約
UNIX/POSIX系OSがカーネルレベルで保証する「原子的」操作を利用すると、プロセス間の同期やデプロイ、ロックを簡潔かつ高速に実装できます。カーネルを信頼してムダなユーザ空間ロックを避けるのがポイントです。

## この記事を読むべき理由
複数プロセスや複数スレッドで動くアプリやデプロイ処理は、競合や不整合を起こしがちです。日本の現場（CI/CD、Webサービス、バッチ処理、オンプレの運用）でも役立つ「確実で簡単な同期手法」を知ることで、運用負荷とバグを減らせます。

## 詳細解説
以下はUNIX系システムが「原子的」に実現してくれる代表的な操作とその意味・注意点です。

- rename(old, new)  
  - 同一ファイルシステム内でパス名を原子的に置き換えます。デプロイのロールアウト（新しいバイナリや設定を即時切替）でよく使われます。注意：別ファイルシステム間では不可。macOSのmvは内部実装が違う場合があります。

- link(oldpath, newpath) / symlink(old, new)  
  - linkはハードリンクを増やすことで「存在しなければ作る」原子性を利用したロックに使えます（既存ならEEXISTで失敗）。symlinkはディレクトリを扱える類似手段。ただしシンボリックのダングリングやinode枯渇に注意。

- open(path, O_CREAT | O_EXCL, mode)  
  - ファイルを「存在しなければ作成」しつつ開きます。これに成功したプロセスがそのタスクを担当する、というリーダー選出に便利。

- mkdir(dirname, mode)  
  - ディレクトリ版の「存在しなければ作成」。これも原子的なのでディレクトリ名を合意できるとロック用途になります。

- mv -T oldsymlink newsymlink（実行時にrenameを使う実装の場合）  
  - シンボリックの差し替えをatomicに行えるケースがあり、デプロイで「切替」の役に立ちます（実装依存。ln -Tfs は原子的でないことがある）。

- fcntl(fd, F_SETLK / F_SETLKW / F_GETLK)  
  - ファイル領域ロック。協調的ロックなら有効。Linuxの「強制（mandatory）ロック」は実装の問題があるため注意。

- fcntlのファイルリース（F_SETLEASE）と通知（SIGIO）  
  - 他プロセスがopen/truncateしたら通知を受ける仕組み。排他制御では使い方に注意。

- mmap + msync（MAP_SHARED）  
  - メモリ操作として複数プロセス間でファイルを共有。同期にはmsyncやinvalidateが必要。

- GCCのアトミックビルトイン（例: __sync_fetch_and_add, __sync_val_compare_and_swap）  
  - ユーザ空間でのロックフリーデータ構造や同期原語として利用。CPUバリアやメモリ順序を保証する。

注意点:
- NFSなど複数マシン・複数カーネルが関わるファイルシステムでは原子性が保証されない操作があるため使えない/危険。
- プラットフォーム差（macOSのmvや実装差）を確認すること。
- inodesは有限なので大量のsymlink/lockファイルの乱用は避ける。

## 実践ポイント
- デプロイ：新バージョンを一時ファイルで用意し、最後に rename(, ) で切替える（ロールバックも簡単）。
- リーダー選出/ジョブ実行：open(..., O_CREAT|O_EXCL) や mkdir を使って「成功したプロセスだけ処理」を担わせる。
- ロックファイル：見えるロックが欲しければ link を使う（lsで確認可能）。不要になったら unlink。
- ファイル領域ロックが適切な場合は fcntl を使う。ただし mandatory locking は信用しすぎない。
- NFSや異種環境では上記手法が破綻するので、使えるファイルシステムか事前に検証する。
- まずは単純なカーネル原語（rename, link, open(O_EXCL)）で済ませ、必要なら mmap やアトミックビルトインに進む。

この考え方は「カーネルが保証してくれる原子性を根拠にシンプルに設計する」ことを促します。まずは小さなケース（デプロイや単純なリーダー選出）で試してみてください。
