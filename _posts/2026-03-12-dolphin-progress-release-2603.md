---
layout: post
title: "Dolphin Progress Release 2603 - Dolphin進捗レポート：リリース2603"
date: 2026-03-12T14:20:59.992Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://dolphin-emu.org/blog/2026/03/12/dolphin-progress-report-release-2603/"
source_title: "Dolphin Emulator - Dolphin Progress Report: Release 2603"
source_id: 47348304
excerpt: "2603でページテーブル高速化、Rogue Squadron IIIが実機並に快適化"
image: "https://dolphin-emu.org/m/user/uploads/zinnia/2026/03/12/progressreportheader2603-social.jpg"
---

# Dolphin Progress Release 2603 - Dolphin進捗レポート：リリース2603
18年ぶりの「新機種」対応＋大幅MMU最適化で、Rogue Squadron IIIがついに動く――Dolphin 2603の注目ポイントを初心者向けに噛みくだいて解説

## 要約
Dolphin 2603でアーケード向けのTriforce対応が加わり、MMU（ページテーブル）用の「fastmem」サポート実装で多くのゲームの速度が大幅改善。特にRogue Squadronシリーズは実機に近い快適さを得られるようになった。

## この記事を読むべき理由
・エミュレーション性能改善の中身が分かると、ゲームや開発テストで何を期待すべきかが分かる。  
・日本で人気のタイトルやレトロゲーム検証にも影響するため、実機比較や検証をする読者に有用。

## 詳細解説
- fastmemの仕組み（初心者向け）
  - ゲーム機（GameCube/Wii）のメモリアクセスは「通常RAM」と「MMIO（入出力）」に分かれる。全アドレス空間をホスト（PC）メモリにマップしておき、MMIOアクセスだけ例外（CPUフォルト）で捕まえて処理することで、大部分のメモリアクセスをホストCPUで高速実行するのがfastmemのトリック。

- なぜページテーブルが厄介だったか
  - GameCubeではBT（BAT）とページテーブルの2通りのマッピングがあり、ページテーブルを使うゲームは従来fastmemの恩恵を受けられず、エミュレータが逐一アドレス翻訳していたため重かった。特にFactor 5のRogue Squadronシリーズは独自のページテーブル／ARAM（Audio RAM）運用で負荷が高かった。

- ARAMとページフォルトによる拡張メモリ
  - 一部ゲームはCPUから直接使えないARAMを、ページフォルト＋DMAでスワップすることで「追加RAMのように見せる」テクニックを使う。これをエミュレータ側でどう扱うかが鍵。

- 今回の技術的突破点
  - PowerPC命令のtlbieをトリガーとしてページテーブル変更を検知し、ページ単位でfastmemマッピングを差分更新（64バイト単位の比較）する仕組みを実装。必要な部分だけを高速マップすることで、全部を手で翻訳するより速くした。
  - その結果、ページテーブルを多用するゲーム（Rogue Squadron II/IIIなど）は大幅高速化。逆に追跡オーバーヘッドがあるタイトル（例：ある種のカスタムハンドラを持つSpider-Man 2）は微減速することもあるが、読み込み時の「カクつき」は減って動きが滑らかになる。

- Rogue Squadron向けの追加最適化
  - JIT（動的コンパイル）の「Branch Following」をゲーム個別に無効化したり、JITブロック管理のデータ構造を効率化して、視点切替時の数百ミリ秒級の大ひっかかりを大幅に軽減。

- そのほか
  - 18年ぶりにTriforce（Sega/Namco/Nintendoのアーケード基板）をサポート。  
  - コミュニティとエミュレーションの専門家が協力して解決した、長年の物理挙動バグ（例：Mario Strikers Chargedの小さな物理バグ）への修正も含む。

## 実践ポイント
- 今すぐやること：DolphinをRelease 2603にアップデートして、Rogue Squadron II/IIIやCars 2などを試す。強力なCPU環境ならFull MMUゲームがフルスピードで動く可能性大。  
- 設定面の注意：ページテーブルfastmemは今回のリリースで導入済み。特定ゲームで逆に微減速する場合は、フォーラムやGitHubで報告／設定調整（例：MMU Speedhackや個別のJIT設定）を確認。  
- 開発・検証者向け：Triforce対応はアーケード検証・アーカイブに重要。エミュレーション精度やパフォーマンスの比較実験に良い機会。問題は公式GitHubやDiscordで共有すると修正に貢献できる。

以上を踏まえ、Dolphin 2603は「これまで遊べなかった重めのタイトルをまともに遊べる」段階に入った重要なリリースです。興味があれば実機比較や設定調整の簡単な検証から始めてください。
