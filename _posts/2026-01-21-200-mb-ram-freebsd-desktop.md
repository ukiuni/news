---
layout: post
title: "200 MB RAM FreeBSD Desktop - 200 MB RAM の FreeBSD デスクトップ"
date: 2026-01-21T08:02:20.055Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://vermaden.wordpress.com/2026/01/18/200-mb-ram-freebsd-desktop/"
source_title: "200 MB RAM FreeBSD Desktop | 𝚟𝚎𝚛𝚖𝚊𝚍𝚎𝚗"
source_id: 46665987
excerpt: "FreeBSD＋XLibreで約200MBの超軽量デスクトップを古いPCやVMで実現する手順を詳細に解説"
image: "https://vermaden.wordpress.com/wp-content/uploads/2026/01/x11-kill-social-media.png"
---

# 200 MB RAM FreeBSD Desktop - 200 MB RAM の FreeBSD デスクトップ
220MB以下でも動く！FreeBSD＋XLibreで作る超軽量デスクトップ実践レポート

## 要約
FreeBSD 15.0 と XLibre（Xorg の代替 X11 サーバ）を使い、Openbox + Tint2 + Dzen2 の最小構成でデスクトップを動かした結果、実働メモリは約 $230 - 19 - 5 = 206$ MB。小さなVM（220 MB）でもさらに省メモリ化でき、Openbox デスクトップは約 $142 + 14 - 18 - 4 = 134$ MB で動作しました。

## この記事を読むべき理由
古いノートPCや低スペックマシンの活用、コンテナ／仮想環境での軽量デスクトップ運用、あるいは「リソースを節約しつつ快適に使う」手法を学ぶのに最適。日本でもローエンドマシンの再利用や組み込み用途で需要が高いトピックです。

## 詳細解説
- 基本構成  
  - OS: FreeBSD 15.0-RELEASE（PKGBASE を利用）  
  - ファイルシステム: UFS（ZFS を使わず UFS+Soft Updates Journaling） — ZFS のブート環境は使えないが、UFS 用の代替手法あり。  
  - X サーバ: XLibre（Xorg の問題から代替として採用。Xorg と競合せず置換可能）  
  - ウィンドウマネージャ: Openbox、ランチャー/パネル: Tint2 + Dzen2  
  - パッケージ例: xlibre, openbox, tint2, dzen2, xterm, htop, ifstat, doas, アイコンテーマ等

- 主要なチューニングポイント（抜粋）  
  - /boot/loader.conf: コンソール解像度、不要な diskid/gptid 無効化、USB のブート待ち無効化、AHCI の省電力ヒントなどで起動時やドライバの挙動を軽くする。  
  - /etc/rc.conf: dbus を有効にしつつ不要なサービス（sendmail、unbound など）は無効化。devfs のルールセットを軽量に設定。  
  - /etc/sysctl.conf: ランダム収集マスク、コアダンプ無効化、スケジューラ／共有メモリのデスクトップ向け調整などで動作性とメモリ利用を最適化。  
  - /etc/devfs.rules: デバイスノードのパーミッション最適化で余分なプロセスを減らす。  
  - 起動方法: xdm 等のログインマネージャを使わず `xinit -- -dpi 75 -nolisten tcp` で直接 X を起動（ログインマネージャ分で約 12MB を節約）。  
  - ~/.xinitrc: 環境変数（LANG、QT/GTK 設定、XDG）、dbus-launch 経由で Openbox を起動し、起動後に panel/launcher を遅延起動。セッション終了時に親プロセスを確実に終了させるスクリプトも入れている。

- メモリ測定と結果  
  - 通常の測定で xterm＋htop を起動して 230MB を観測し、xterm(19MB) と htop(5MB) を差し引いて実働は 206MB。  
  - 小メモリ VM（UEFI 起動で 220MB 割当）では、ベース FreeBSD が 82MB、Openbox デスクトップ全体は約 134MB（上のとおり計算）で動作を確認。  
  - カーネルを再コンパイルすればさらに削れる余地あり。

- なぜ XLibre？  
  XLibre は Xorg と競合せず置き換え可能で、作者は Xorg の保守方針や実装上の問題を理由に XLibre を選択している（詳細は元記事参照）。

## 実践ポイント
- まずは仮想環境で試す（bhyve 等）：VM を 256MB → 220MB と下げながら動作確認すると効果がわかりやすい。  
- 最小構成でインストール：FreeBSD を UFS でインストールし、不要なサービスは rc.conf で切る。  
- X はログインマネージャを使わず xinit を推奨：`xinit -- -dpi 75 -nolisten tcp`。ログインマネージャ（xdm 等）は約 12MB の上乗せ。  
- .xinitrc を整備：dbus-launch 経由で WM を起動、パネルやランチャは遅延起動、終了時に親プロセスを確実に kill する一文を入れるとログアウトがクリーン。  
- 測定方法：htop/xterm で測定し、測定用アプリのメモリを差し引いて実働値を出す（例：$230 - 19 - 5 = 206$ MB）。  
- 日本向けの追加点：ロケールを ja_JP.UTF-8 に設定、キーボード設定やフォントを日本語向けに調整すると日常利用が快適。  
- 注意点：ハードウェアドライバや Wi‑Fi、GPU ドライバによっては追加メモリや設定が必要になるため、事前に互換性を確認すること。

元記事のアプローチは「軽さを最優先にして実用性を保つ」良い参考になります。古いノートPCをリフレッシュしたり、最小構成のデスクトップを研究したい人におすすめです。
