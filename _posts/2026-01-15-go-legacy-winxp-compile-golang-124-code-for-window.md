---
layout: post
title: "Go-legacy-winxp: Compile Golang 1.24 code for Windows XP - Go-legacy-winxp：Golang 1.24コードをWindows XP向けにコンパイルする方法"
date: 2026-01-15T22:30:18.334Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/syncguy/go-legacy-winxp/tree/winxp-compat"
source_title: "GitHub - syncguy/go-legacy-winxp at winxp-compat"
source_id: 46588243
excerpt: "古いPCを再活用！Windows XPで動くGo 1.24バイナリを作る実践手順"
image: "https://opengraph.githubassets.com/f17136583dcdece1135681fc9e0f353dbd1539a039eba80333cc77fa9f5038ee/syncguy/go-legacy-winxp"
---

# Go-legacy-winxp: Compile Golang 1.24 code for Windows XP - Go-legacy-winxp：Golang 1.24コードをWindows XP向けにコンパイルする方法
魅力タイトル：古いPCを再活用！Windows XPでも動くGoバイナリを作る方法（実践ガイド）

## 要約
syncguy の go-legacy-winxp は、Go のフォークで Windows XP（winxp-compat ブランチ）向けに互換性を戻したものです。古い Windows 環境で Go を動かしたい・レガシー対応が必要な場面で役立ちます。

## この記事を読むべき理由
日本の現場でも産業機器、組み込み端末、閉域ネットワークの古いPCで XP が残っているケースはあります。最新の公式 Go がサポートしない環境向けに、実用的な対応策と注意点を短時間で把握できます。

## 詳細解説
- 何をしているか：このリポジトリは公式 Go から派生したフォークで、Windows XP / 旧 Windows のためにいくつかの変更・巻き戻しを行っています。主な変更点は、XP で壊れる recente な API 変更を元に戻したり、古い動作（例：deprecated な go get の挙動）を復活させることです。
- 技術的ポイント（主要な差分）
  - RtlGenRandom に戻す（ProcessPrng ベースの変更を戻す）：古い Windows の乱数生成互換性確保。
  - LoadLibraryA フォールバックの復活：システムライブラリのロード互換性を確保。
  - sysSocket フォールバックの追加：ソケット系システムコールの互換処理。
  - Windows 7 / XP 用コンソールハンドル回避処理の復活。
  - (*Process).Wait に 5ms スリープを入れる古い挙動の復元。
  - GO111MODULE="off" / "auto" 時の古い go get 動作を復元（GOPATH モードの動作サポート）。
- 配布とインストール：リポジトリはバイナリ配布（release ページ）を用意しています。手動ビルドも可能（ソースを clone → winxp-compat をチェックアウト → ビルド）。
- 制約：すべての最新機能が XP で動くわけではなく、セキュリティや新しい API の欠如は残ります。公式の長期サポートではない点に注意。

## 実践ポイント
- まず試す（リポジトリ取得とビルド）
  - GitHub からクローンしてブランチをチェックアウト：
```bash
# bash
git clone https://github.com/syncguy/go-legacy-winxp.git
cd go-legacy-winxp
git checkout winxp-compat
```
  - ビルド（Linux/macOS）:
```bash
# bash (Unix系)
cd src
./make.bash
```
  - ビルド（Windows）: src\make.bat を実行（PowerShell / コマンドプロンプト上で）。
- 環境変数設定（Windows での基本）
  - GOROOT をビルド/展開先に、PATH に %GOROOT%\bin を追加。GOPATH は通常 %USERPROFILE%\go。
- 動作確認
  - go version を実行してビルド結果を確認。
  - XP 実機や仮想マシン（VirtualBox / QEMU / Hyper-V）で hello world を実行して検証する。
- セキュリティと運用上の注意
  - XP は既知の脆弱性が多数あるため、インターネット直結や重要データの扱いは避ける。可能なら隔離ネットワークやアップグレードを検討する。
- 代替案
  - 可能であればアプリ側で互換レイヤを作る、もしくは対外的には最新のサーバを使い XP はクライアント限定の役割に限定する。
  - 必要最小限だけ XP 向けバイナリを用意し、将来的には段階的に移行する計画を立てる。

短くまとめると、このフォークは「どうしてもXPを捨てられない」状況に対する実用的な選択肢です。ただしセキュリティや長期保守の観点からは最終手段と考え、移行計画を並行で進めることをおすすめします。
