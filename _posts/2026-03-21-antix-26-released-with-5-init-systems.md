---
layout: post
title: "antiX-26 released with 5 init systems - antiX-26 リリース（5つの init を搭載）"
date: 2026-03-21T21:42:11.938Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://antixlinux.com/antix-26-released/"
source_title: "antiX-26 released &#8211; antiX Linux"
source_id: 1214271995
excerpt: "systemd不要で5種のinit搭載、古いPCも蘇る軽量Debian派生antiX-26"
---

# antiX-26 released with 5 init systems - antiX-26 リリース（5つの init を搭載）
軽量でカスタマイズ自在、しかも systemd を使わない新しい選択肢 — antiX-26 が示す「もう一つのLinux」

## 要約
Debian Trixie をベースに systemd/elogind を排した軽量ディストリビューション antiX の新版、antiX-26 が公開。runit をデフォルトに含む5種類の init をサポートし、古いPCから最新環境まで幅広く使える設計。

## この記事を読むべき理由
日本では古い社内端末やローエンドPCがまだ現役の現場が多く、systemd に依存しない軽量な選択肢は大きな価値を持ちます。学習やカスタマイズ性を重視する開発者・趣味ユーザーにも有用です。

## 詳細解説
- ベースと設計方針
  - Debian 13 (Trixie) ベースだが systemd/libsystemd0 や elogind を含めない方針。代替として eudev を採用。
  - 目的は軽量性・可搬性・systemd 非依存の柔軟な運用。

- init の多様性（学習・運用ニーズに最適）
  - サポートされる init: runit（デフォルト）、sysVinit、dinit、s6-rc、s6-66。
  - 複数の init を同梱することで、運用要件や好みに合わせた切り替えや検証が容易。

- カーネルとアーキテクチャ
  - カスタム 5.10.240 カーネル（全版）、カスタム 6.6.119（x64 フル版のみ）。
  - 64bit/32bit 両対応で、フル（約2GB）とコア（約660MB）の2フレーバーを提供。

- デスクトップ・アプリ群
  - ウィンドウマネージャ: IceWM（既定）, fluxbox, jwm, herbstluftwm（タイル型）。
  - GUI主要アプリ: LibreOffice, Firefox-ESR, Claws Mail, Evince 等。
  - メディア: pipewire/wireplumber（64bit フル既定）、ALSA（32bit フル既定）。mpv/celluloid/xine 等。
  - スナップ/Flatpak は非採用（systemd/elogind 不要の立場を保持）。

- 管理・便利ツール
  - App Select（アプリ起動以上の選択GUI）、antiX Control Centre、iso-snapshot/remaster tools（リマスター用）。
  - ネット接続: connman（簡単Wi-Fi管理）、ceni、gnome-ppp（ダイヤルアップ向け）。
  - ファイル管理: zzzFM, rox-filer, mc。
  - CLI 好き向けにも nano/vim-tiny, newsboat, irssi, mocp, rtorrent などを収録。

- 独自スクリプト・リポジトリの価値
  - antiX TV/Radio、antiX SAMBA manager、pipe-viewer（ブラウザ無しでYouTube視聴）などローカルで便利なツール群。
  - 1-to-1-voice/assistance や ssh-conduit といったリポジトリアプリは、プライベートで軽量なリモート連携を容易にする。

## 実践ポイント
- まずは Live ISO（full / core）で古いPCと最新PCの両方を試してみる。
- systemd に依存しない運用を検証したい場合、runit をデフォルトで試し、必要に応じて他の init を切り替えて挙動を比較する。
- 64bit フル版は pipewire/wireplumber を標準搭載。音声周りを試す際は64bit版が簡単。
- 軽量デスクトップ（IceWM 等）で旧式ハードウェアを再活用する、あるいは教育目的で複数 init を学ぶ教材としても最適。
- 日本語化は User Language 機能で対応。まずは App Select / antiX Control Centre を使って基本設定を固めると良い。

ダウンロードや詳細は公式ページで確認を（antiX-26 は公式サイトから入手可能）。
