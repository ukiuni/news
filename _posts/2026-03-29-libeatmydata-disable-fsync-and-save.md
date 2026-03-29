---
layout: post
title: "libeatmydata - disable fsync and SAVE - libeatmydata - fsync と SAVE を無効化"
date: 2026-03-29T08:58:15.041Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.flamingspork.com/projects/libeatmydata/"
source_title: "libeatmydata - disable fsync and SAVE!"
source_id: 1338219330
excerpt: "libeatmydataでfsyncを無効化しCIやビルドを劇的に高速化、リスクと対策も解説"
---

# libeatmydata - disable fsync and SAVE - libeatmydata - fsync と SAVE を無効化
開発・CIを爆速にする「危険だけど便利な」裏ワザ：libeatmydata入門

## 要約
libeatmydata は LD_PRELOAD を使って fsync や同期フラグ付き open を無効化し、ディスク同期コストを丸ごと省くことでテストやビルドを大幅に高速化します。データの安全性は失われるため、本番データや重要な保存処理では絶対に使ってはいけません。

## この記事を読むべき理由
ローカル開発や CI のテスト実行時間を短縮したい日本のエンジニア／運用担当にとって、手軽に試せる「速さのトリック」として有益です。特に大量の fsync を伴うデータベースやパッケージビルドで効果が出やすいです。

## 詳細解説
- 仕組み：libeatmydata は LD_PRELOAD によってプロセスの fsync, fdatasync, fsync に相当する API をフックし、実際の同期処理をスキップして成功を返します。open(O_SYNC) 等も無視されます。  
- トレードオフ：書き込みのパフォーマンスは大幅改善しますが、クラッシュや電源断でデータが失われる／ファイルが破損するリスクが生じます。したがって「結果を失っても問題ない」用途に限定すべきです。  
- 対応環境：主に Linux で使われますが、MacOS や一部の Solaris 系でも報告例あり。多くのディストリで eatmydata 名でパッケージ提供されています。  
- インパクト例：MySQL のテストで総実行時間が 3m36s → 2m10s に短縮されるなど、ケースによっては実行時間が数割〜約1/3ほど改善する報告があります。

## 実践ポイント
- インストールと実行（ソースからの基本手順）:
```bash
git clone https://github.com/stewartsmith/libeatmydata.git
cd libeatmydata
autoreconf -i   # git からビルドする場合
./configure
make
make check
sudo make install
```
- 実行例:
```bash
eatmydata <コマンド>
# 例: eatmydata pytest tests/
```
- 使う場面：ローカルの単体テスト、CI の一時的な高速化（結果の永続性が不要なテスト専用のジョブ）、パッケージビルドやマイグレーションの検証。  
- 絶対に使ってはいけない場面：本番環境、バックアップ作成、ユーザーデータを書き込む処理。  
- 注意点：CI で導入する際は「速さ検証用のジョブ」として明確に分離し、失敗時や本番移行前には必ず fsync 有効な環境で再検証を行うこと。

元記事の公開リポジトリや配布パッケージ（GitHub / 各ディストリの eatmydata）を参照して導入を検討してください。
