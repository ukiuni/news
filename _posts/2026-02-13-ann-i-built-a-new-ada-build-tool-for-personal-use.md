---
layout: post
title: "ANN: I built a new Ada build tool for personal use - 発表: 個人用に新しいAdaビルドツールを作りました"
date: 2026-02-13T21:25:23.399Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/tomekw/tada"
source_title: "GitHub - tomekw/tada: Tomek&#39;s Ada tool"
source_id: 990264415
excerpt: "tadaでtada.tomlだけでAdaの小規模プロジェクトを簡単に構築・テスト"
image: "https://opengraph.githubassets.com/468a3a7dd2a6f9bdef3c189a1ed72e51a959aa7ce1a5b236788df8a3e5d78fe4/tomekw/tada"
---

# ANN: I built a new Ada build tool for personal use - 発表: 個人用に新しいAdaビルドツールを作りました
Ada開発がぐっと楽になる「Tada」——面倒なビルドスクリプトから解放される小型ツール

## 要約
TadaはAda向けの意見的（opinionated）プロジェクト管理ツールで、gprbuildをラップしてシンプルなmanifest（tada.toml）でビルド・テスト・実行を簡単にします。個人開発や小規模プロジェクトのビルド負担を軽減することを目的としています。

## この記事を読むべき理由
日本でも組込み・航空・鉄道など安全性重視分野でAdaが使われます。Tadaは手軽にプロジェクトを立ち上げ・運用できるため、学習用や小規模プロトタイプ、CI導入の起点として有用です。

## 詳細解説
- 目的：GPRbuildの煩雑な設定を減らし、標準的なワークフロー（init / build / run / test / clean）をワンツールで提供。tada.tomlによるシンプルなプロジェクト宣言が中心。
- 仕組み：内部ではgprbuildを呼び出し、AUnit（libaunit）を使ったテスト実行をサポート。意見的なデフォルトにより明示的なビルドスクリプトをほぼ不要にします。
- 主なコマンド例：
```bash
# 新規プロジェクト作成（実行ファイル）
tada init my_project

# ライブラリプロジェクト
tada init my_project --lib

# ビルド（デフォルトはdebug）
tada build
tada build --profile release

# 実行（ビルドして実行）
tada run
tada run --profile debug -- --flag arg

# テスト（AUnit）
tada test
tada test --profile release

# クリーン
tada clean
```
- 前提環境（Debian/Ubuntu例）：GNAT（Adaコンパイラ）、gprbuild、libaunit-devが必要。
```bash
sudo apt install gnat gprbuild libaunit-dev
```
- インストールはリリースバイナリをダウンロードしてPATHへ配置するだけ：
```bash
curl -L https://github.com/tomekw/tada/releases/download/VERSION/tada-VERSION-PLATFORM -o tada && chmod +x tada
cp tada ~/.local/bin/
```
- ライセンスはMIT。プロジェクト自身は自身をTadaでビルド可能。

## 実践ポイント
- まずはローカルで既存の小さなAdaプロジェクトをtada init→tada buildで試す。設定の簡素さを体感するのが早道。
- CIに組み込む際は、DebianベースのランナーにGNAT/gprbuild/libaunitを入れてtadaコマンドでビルド→テストを回すと設定が楽。
- 教育用途や社内プロトタイプに最適。安全クリティカル系の本番導入前にTadaで開発効率を確認してから、より厳格なビルドポリシーへ移行する運用も有効。
