---
layout: post
title: "Faster package builds using Icecream and a Mac - IcecreamとMacでパッケージビルドを高速化"
date: 2026-01-31T18:01:09.778Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://iovec.net/2026-01-26"
source_title: "Faster package builds using Icecream and a Mac"
source_id: 1352932624
excerpt: "Macの遊休コアでLinuxパッケージビルドを半分の時間に短縮する実践手順と回避策"
---

# Faster package builds using Icecream and a Mac - IcecreamとMacでパッケージビルドを高速化
Macの“遊んでいるコア”を使ってLinuxのソースパッケージを爆速化する方法

## 要約
Icecreamを使い、ローカル（x86_64）ホストとアイドル状態のM3 Mac（arm64）をクラスタ化してパッケージのビルド時間を大幅短縮。マルチアーキテクチャやmacOS側の制約に対する実務的な回避策も紹介する。

## この記事を読むべき理由
ソースベースのディストリ（例：KISS Linux）や大規模ビルドで時間を節約したい開発者、CIリソースを有効活用したい日本の開発者にとって即効性のある手法だから。

## 詳細解説
- 概要：icecream（icecc）は分散コンパイルツールで、プリプロセス済みソースを圧縮してリモートノードでコンパイルさせ、最終リンクはホストで行う。中央にschedulerを置き、動的にノード参加・離脱を扱えるのが強み。
- 他ツールとの違い：
  - distcc：pumpモードでプリプロ処理をオフロードするが失敗が出やすく、静的IP管理が弱点。
  - sccache：Rustやキャッシュに強いが、異なるアーキテクチャ混在クラスタでは問題が報告される。
- 動作構成：ホスト上でicecc-scheduler、各マシンでiceccd（デーモン）を実行。コンパイラ呼び出しはiceccラッパー経由で配信される。
- クロスアーキテクチャの課題：
  - icecreamはホストの最小ツールチェーンを.tar.gzにしてリモートでchroot実行する方式だが、アーキテクチャが異なるとそのままでは実行できない。
  - macOSでは共有ライブラリがファイルシステム上にないためLinux chrootが使えない。
  - Rosettaでx86_64をエミュするDockerはCPUを使い切るがコンパイル自体が遅くなる場合がある。
- 実務的解決：
  - arm64上でx86_64向けクロスコンパイラをビルド（muslベースで例示）。ホストとクロスのコンパイラ設定（例：--enable-default-pie 等）を揃えないとリンク時に失敗するためconfigを合わせる必要あり。
  - icecc-create-envで各アーキテクチャ用のchrootアーカイブを作り、ICECC_VERSIONで「arch:chroot」マッピングを渡す（これが最初のジョブで送られる）。
  - clang系ならネイティブでターゲット指定が可能なのでclang環境は比較的簡単。
- 運用上のポイント：schedulerはホストで動かす、MAKEFLAGSはクラスタの合計コア数に合わせて調整（プリプロはホストで走るためバッファを残す）。

## 実践ポイント
- 基本コマンド（ホスト）：
```bash
# scheduler とデーモンを起動
icecc-scheduler &
iceccd &
# ビルド並列度をクラスタに合わせて調整
export MAKEFLAGS="-j17"
```
- リモート（Mac上のDocker）：
```bash
# docker内で起動（ポート公開忘れずに）
iceccd -s <HOST_IP> -p <DAEMON_PORT>
```
- chroot作成と環境変数例：
```bash
# クロス/ネイティブのchrootを作成してファイルを配置
icecc-create-env /usr/bin/gcc   # 例: x86_64 chroot作成
export ICECC_VERSION="aarch64:/path/to/arm64.tar.gz,x86_64:/path/to/x86_64.tar.gz"
```
- 可能ならclangベースに移行するとクロス設定が楽になる。
- 実運用で見つかった修正パッチ（-Wp,MD、-imacros、大きなオブジェクトファイル対応など）を適用すると安定性が向上する。
- 監視：icecream-sundae等でクラスタ負荷とスロット割当を可視化すると運用が楽。

短期間で200パッケージ以上をビルドして体感でほぼ半分の時間になったという実例があるので、手元にアイドルなマシン（Mac含む）があるなら試す価値は高い。
