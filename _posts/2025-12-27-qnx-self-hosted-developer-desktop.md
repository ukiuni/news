---
layout: post
title: "QNX Self-Hosted Developer Desktop"
date: 2025-12-27T03:05:45.202Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://devblog.qnx.com/qnx-self-hosted-developer-desktop-initial-release/"
source_title: "QNX Self-Hosted Developer Desktop"
source_id: 46398201
excerpt: "QNX8.0をQEMUで自己完結的にローカル実行・開発でき、クロス不要で即プロト検証可能"
---

# QNXが“自己ホスト型”開発デスクトップを初公開 — クロスコンパイル不要でQNX 8.0をローカルで動かす

## 要約
QNXはQNX 8.0上で動作する「Self-Hosted Developer Desktop」を初リリース。QEMU上で自己完結的に開発・ビルドでき、Linuxアプリの移植や学習コストを大幅に下げる狙い。

## この記事を読むべき理由
日本の組込み・自動車系エンジニアにとって、これまで煩雑だったクロス開発環境のハードルが下がる可能性が高い。社内ラボや個人学習でQNXを手早く試せる点は、プロトタイプ作成や技術習得に即効性がある。

## 詳細解説
- 何が出たか：QNX 8.0上で動くフルデスクトップ環境（XFCE on Wayland）と、ローカルでビルドできるツール群を含むQEMUイメージの初回公開。つまりターゲット上でclang/gcc/clang++、Python、make、cmake、gitなどが動作する。
- 同梱ソフト：ブラウザ、ターミナル、IDE/エディタ（Geany、Emacs、Neovim、vim）、ファイルマネージャ（Thunar）、C/C++/PythonのサンプルやGTK/OpenGL ESデモなど、学習と移植検証に必要な基本が揃う。
- 目的と利点：従来のクロスコンパイル＋ターゲットボードへのデプロイという手間を省き、QNX上で直接コンパイル→実行が可能。結果としてLinuxアプリやライブラリの移植作業や互換性チェックが効率化される。
- 配布と動かし方：Ubuntu 22.04/24.04上でQEMUを用いる形式。QNX Software Centerの「QNX SDP 8.0 Quick Start Target Image for QEMU」から取得し、インストールディレクトリ（通常 ~/qnx800/images）にあるイメージをREADME/PDFの手順で展開・起動する。トラブル時はPDFのTroubleshootingやDiscordコミュニティで相談可能。
- 今後の展望：Windows/macOS向けQEMUイメージやx86ネイティブ、Raspberry Pi対応、CI統合向け機能、ドキュメント拡充などが計画中。

## 実践ポイント
- 試す環境：Ubuntu 22.04/24.04を用意し、ホストでKVMを有効にしておくと起動が安定する。VMに十分なCPU/RAMを割り当てること（ビルドするなら特に重要）。
- 入手手順の要点：QNX Software Centerで「quick start」を検索 → QEMU用Quick Start Target Imageをインストール → ~/qnx800/images内のREADME/PDFに従って展開＆起動。
- すぐ試せる検証：同梱のHello WorldやGTK/OpenGL ESデモをまずコンパイルして動かし、ライブラリ互換性を確認する。既存のLinuxソースを持ち込んでビルドできるか試すのが移植性評価の近道。
- CI導入の準備：将来的にCI統合機能が来る想定で、現段階はQEMUイメージを使ったローカル検証→スクリプト化しておくとアップデート後の移行が楽。
- サポートを活用：公式DiscordやRedditでQNXチーム／コミュニティに質問すると、初期リリース固有の落とし穴を回避しやすい。

