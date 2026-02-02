---
layout: post
title: "Time Machine-style Backups with rsync (2018) - rsyncで作るTime Machine風バックアップ"
date: 2026-02-02T02:04:23.263Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://samuelhewitt.com/blog/2018-06-05-time-machine-style-backups-with-rsync"
source_title: "Time Machine-style Backups with rsync &mdash; Sam Hewitt"
source_id: 46850709
excerpt: "rsyncの--link-destでTime Machine風差分バックアップを低コストで実現"
image: "https://samuelhewitt.com/img/icon.png"
---

# Time Machine-style Backups with rsync (2018) - rsyncで作るTime Machine風バックアップ
Time Machineに頼らない「差分スナップショット」をrsyncで手軽に再現する方法

## 要約
rsyncの--link-destを使って、データを重複させずに時刻付きスナップショット（Time Machine風）を作る手法を紹介する記事の要約と実践ガイド。

## この記事を読むべき理由
MacのTime Machineに依存せず、低コストなLinux/NAS環境で安全に過去状態へ戻せる仕組みを作れる。写真や個人データを大量に保存する日本のユーザー／小規模運用者に特に有益。

## 詳細解説
- 基本概念：rsyncの--link-destオプションは「変更がないファイルはハードリンクで前回のスナップショットを指す」ことで、ファイル内容を重複保存せずに過去の状態を保持する。見た目はフルバックアップが並んでいるがディスク使用量はほぼ増えない。
- 利点：古いスナップショットを自由に削除でき、差分だけを保存するため容量効率が高い。rsyncは広く使われるので導入が容易。
- 注意点：
  - ハードリンクは同一ファイルシステム上でしか動作しない（ターゲットが別ディスクでマウントされている場合は同一パーティションである必要あり）。
  - --link-destで指定する参照先は存在していること（初回は空ディレクトリを用意）。
  - 古いスナップショットを消す前に新しい完全スナップショットを作るなど運用ルールを決める。
  - rsync実行前にdry-run（-n）で挙動確認を推奨。

- オプションの意味（よく使うもの）
  - -a : アーカイブ（再帰・権限維持等）
  - -v : 詳細出力
  - -P : 進捗・部分ファイル保存
  - -h : 人間向けサイズ表示
  - --delete : 参照元に無いファイルを削除（運用注意）
  - --link-dest=DIR : 変更がなければDIRのファイルをハードリンクする

- 運用例：スクリプトをcronで定期実行して自動化。SynologyなどのNASでもrsync/SSH経由で同様の仕組みが作れる（ただし同一ボリューム制約に注意）。

## 実践ポイント
- 準備：バックアップ先は十分な容量と同一ファイルシステムであることを確認。ログディレクトリと参照用のcurrentディレクトリを作る。
- テスト：まずは小さなディレクトリでrsync -n を実行して動作を確認する。
- 保守：古いスナップショットはfindコマンド等で一定期間経過後に削除する運用を作る。
- Synology/日本のNAS事情：多くのNASはrsync/SSHをサポートするため、Time Machine非対応環境でも同様の差分スナップショットが作れる。業務・個人ともコスト効率が高い。

サンプルスクリプト（実用的に修正済み）：
```bash
#!/bin/sh
TIMESTAMP=$(date "+%Y-%m-%dT%H-%M-%S")
USER=user
SOURCEDIR="/var/data/backups"
TARGETDIR="/var/redundancy"
LOGDIR="/var/log/rsync"

mkdir -p "$TARGETDIR" "$LOGDIR" "$TARGETDIR/current"

# 新しいスナップショット用ディレクトリ名
DEST="$TARGETDIR/$USER-$TIMESTAMP"

# rsync実行（--link-destはcurrentを参照）
rsync -avPh --delete --link-dest="$TARGETDIR/current" "$SOURCEDIR/" "$DEST" > "$LOGDIR/$TIMESTAMP.log" 2>&1

if [ $? -eq 0 ]; then
  # 成功なら current を新しいスナップショットへ差し替え
  rm -f "$TARGETDIR/current"
  ln -s "$DEST" "$TARGETDIR/current"
else
  # 失敗時は失敗フォルダへ移動
  mv "$DEST" "$TARGETDIR/failed-$USER-$TIMESTAMP"
fi
```

cron例（毎日5時に実行）：
```
0 5 * * * bash /usr/local/bin/rsync-time-machine.sh
```

実践的な次の一歩：まず1回だけ手動で実行→ログ確認→dry-run→定期実行へ移行。NASや外付けHDDを使う場合はファイルシステムの制約（同一ボリューム）を必ず確認すること。
