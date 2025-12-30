---
layout: post
title: "loss32: let's build a Win32/Linux - Win32上のデスクトップをLinuxで再現する試み"
date: 2025-12-30T04:15:17.007Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://loss32.org/"
source_title: "loss32: let's build a Win32/Linux"
source_id: 1207146162
excerpt: "WINEとLinuxで.exeをそのまま動かす、Win32中心デスクトップ実験"
---

# loss32: let's build a Win32/Linux - Win32上のデスクトップをLinuxで再現する試み
「.exeをそのまま動かす」Linux──loss32が描くWin32ベースのデスクトップ構想

## 要約
loss32は「Linux上でWin32ソフトだけでデスクトップを構成する」実験的ディストリビューション構想。Linuxカーネル＋WINE（と必要ならReactOSのユーランド）を土台に、長年のWin32資産をネイティブに近い感覚で使える環境を目指すプロジェクトです。

## この記事を読むべき理由
- 多くのクリエイティブ／ゲーム系ツールがWindows専用である日本の現場にとって、ネイティブ感のあるWin32互換環境は実務的価値が高い。  
- WINE改善やデスクトップ統合のノウハウは、日常のLinux運用や移行計画に直結するため知っておくと有利です。

## 詳細解説
- 基本コンセプト  
  loss32はReactOSとは異なり、Windows NTカーネルを再実装するのではなく、Linuxカーネル＋WINEを「デスクトップの主役」に据える。必要に応じてReactOSのユーランド要素を組み合わせ、.exeがそのまま使える「Win32中心のデスクトップ体験」を実現しようというものです。

- なぜこれが現実的か  
  WINEは30年以上のWin32互換性の蓄積があり、単一の安定したABI（Win32）を通じて膨大なソフト資産にアクセスできる。ReactOSがカーネル互換で苦戦している点に対し、loss32は既存のLinuxハードウェア互換性を活かせるため現実的なアプローチです。

- 技術的な鍵と課題  
  - WINE本体の改善（explorer.exe / shell32.dll の挙動、スタートメニューやシェル統合、HiDPI対応）  
  - デスクトップ環境としてのパッケージ化（Debianなどのログイン画面にセッションとして表示させる仕組み）  
  - Wayland上での互換性（Waylandコンポジタがデスクトップ環境を強制しないことが望ましい — mutterのスタンドアロン利用等）  
  - 配布形態の検討（静的リンクしたWINE + musl/freetypeなど、既存のGNUユーランドをどこまで採用するか）  
  - ReactOSユーランドとの連携差分（ReactOS側のexplorer/shellの利点を取り込む可能性）

- 期待される効果  
  完全にWin32中心のデスクトップ環境はWINEの改善を刺激し、結果的にLinux上でのWindowsアプリ互換性全体を底上げします。日本のクリエイターやレトロゲーム保存、特定業務アプリの移行コスト低減にも寄与します。

## 実践ポイント
- まず試す（今すぐできること）
  - Debian 13等にWINEを入れて手持ちの.exeを動かしてみる（winecfg, winetricksを活用）  
  - mutterのスタンドアロンや軽量WaylandコンポジタでWINEアプリの描画を試す（HiDPI挙動を確認）  
  - LutrisやProton互換レイヤーでゲーム動作を検証する

- 貢献／開発でできること
  - Debian等で「loss32セッション」を表示するための.desktop／sessionファイル作成やパッケージング支援  
  - WINEのshell/explorer回り（スタートメニュー統合、HiDPI対応）のバグ報告・パッチ提出  
  - ReactOSユーランドの差分調査、必要なコンポーネントの移植・統合検討  
  - static-linked WINEビルドや依存軽量化（musl, freetype等）に関する実験

- コミュニケーション
  - プロジェクトはIRC（#loss32 on irc.libera.chat）などで議論中。興味ある技術分野（WINE、ReactOS、Wayland、パッケージング等）で参加してみるのが早道です。

## 引用元
- タイトル: loss32: let's build a Win32/Linux
- URL: https://loss32.org/
