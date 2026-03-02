---
layout: post
title: "xuv: X11 user daemon to automatically run commands triggered by user specified events - xuv：ユーザー指定イベントで自動的にコマンドを実行するX11ユーザーデーモン"
date: 2026-03-02T06:59:42.907Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://codeberg.org/NRK/xuv"
source_title: "xuv: X11 user daemon to automatically run commands triggered by user specified events"
source_id: 1069176048
excerpt: "X11ウィンドウイベントで任意コマンドを自動実行、軽量デーモンxuvでデスクトップを自在に最適化"
---

# xuv: X11 user daemon to automatically run commands triggered by user specified events - xuv：ユーザー指定イベントで自動的にコマンドを実行するX11ユーザーデーモン
思わず設定したくなる！X11のウィンドウイベントで自動化を行う軽量デーモン

## 要約
xuvはX11上で動作する小さなユーザーデーモンで、ウィンドウの作成・破棄、フォーカスやアクティブ化、フルスクリーンの出入りなどのイベントに応じて任意のコマンドを自動実行します。設定はテキストのxuv.confで行います。

## この記事を読むべき理由
Linuxデスクトップを自分好みに自動化したい人（軽量環境やタイル型ウィンドウマネージャー利用者、動画再生やゲーム時にコンポジタを停止したい人など）にとって、手軽に使えてソースからビルドできるツールは強力な武器です。Waylandが増えているとはいえ、X11環境は未だ多く存在するため日本の開発者・ユーザーにも有用です。

## 詳細解説
- 何をするか：xuvはXlibを使い、X11の各種ウィンドウイベントを監視して設定にマッチしたときに外部コマンドを起動します。プロセスはユーザー空間で動くデーモンです。  
- トリガー可能なイベント例：WindowCreate / WindowDestroy / Focus / Active（アクティブ化） / Map/Unmap / ActiveFS（アクティブなフルスクリーンに入る/出る）など。  
- マッチング：ウィンドウのWM_CLASSやWM_INSTANCEなどに対してexactやcaseなどのマッチング指定が可能で、細かく条件を作れます。  
- 設定：デフォルトは `$XDG_CONFIG_HOME/xuv.conf` に書くINI風のルールファイル。READMEとmanページ（xuv(1)、xuv.conf(5)）で詳細が確認できます。  
- 実装と依存：C（C11）で書かれ、ランタイムはX11サーバとXlibが必要。Waylandネイティブ環境では動作しません（XWayland下なら可）。  
- ビルド／インストール例：非常にシンプルに1ファイルをコンパイルしてインストールできます。

設定例（抜粋）：
```ini
# Disable xbanish when window with the instance name selx0 is created.
[XbanishOffSelx]
event = WindowCreate
wm_instance = selx0
wm_instance.match = exact,case
cmd = pkill xbanish

# Re-enable when destroyed
[XbanishOnSelx]
event = WindowDestroy
wm_instance = selx0
wm_instance.match = exact,case
cmd = xbanish
```

ビルド例：
```bash
cc -o xuv xuv.c -O3 -s -l X11
# デバッグ例（gcc）
gcc -o xuv xuv.c -std=c11 -Wall -Wextra -g3 -D DEBUG -O0 -fsanitize=address,undefined -l X11
```

## 実践ポイント
- すぐ試す手順：
  1. ソースをcloneしてビルド（上のccコマンド）。  
  2. `$XDG_CONFIG_HOME/xuv.conf` にルールを作成。  
  3. `./xuv` をユーザーセッションで起動。systemd --userで管理しても良い。  
- 代表的ユースケース：フルスクリーン動画でコンポジタ停止、特定アプリ起動時にキーバインドやデバイス設定を切替、通知やログを外部スクリプトで処理。  
- 注意点：Waylandネイティブ環境では動作しないため、Waylandユーザーは代替ツール（Wayland対応の自動化フレームワーク）を検討してください。  
- 配布／導入：実行ファイルとmanページを/usr/local配下にinstallするだけで使えます（Makefileも同梱）。

元リポジトリ（ドキュメント・manページ・例）を参照して、自分のデスクトップワークフローに合わせた自動化ルールを作ってみてください。
