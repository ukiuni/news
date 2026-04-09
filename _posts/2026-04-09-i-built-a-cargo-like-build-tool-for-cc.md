---
layout: post
title: "I built a Cargo-like build tool for C/C++ - C/C++向けCargo風ビルドツールを作った"
date: 2026-04-09T17:27:02.313Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/randerson112/craft"
source_title: "GitHub - randerson112/craft: A lightweight build and workflow tool for C/C++ · GitHub"
source_id: 47705413
excerpt: "1つのcraft.tomlで依存管理とCMake生成を自動化し、C/C++のビルドを再現性高く簡素化するツール"
image: "https://opengraph.githubassets.com/112bbc4c6fc12e3f973a9a707ce14134dc75fd136c08ec8f56c907fb2fe1087b/randerson112/craft"
---

# I built a Cargo-like build tool for C/C++ - C/C++向けCargo風ビルドツールを作った
C/C++のビルドが一気にスムーズに — Cargo的ワークフローを目指した「Craft」

## 要約
Craftは1つのcraft.tomlでプロジェクトを定義し、CMakeファイルを自動生成・依存取得・ビルド実行までを提供する軽量ツールです。C/C++の定常的なCMakeの手間や依存管理をシンプルにします。

## この記事を読むべき理由
日本では組み込み、ゲーム、ライブラリ開発などC/C++案件が多く、CMakeや手作業での依存管理がボトルネックになりがちです。Craftは初心者の立ち上がりを速め、少人数チームでの再現性あるビルド環境構築に役立ちます。

## 詳細解説
- 基本概念  
  - craft.toml：プロジェクトの単一ソース（名前、言語、規格、ソース/インクルードディレクトリ、ビルド種別など）を宣言。  
  - 自動生成：Craftがcraft.tomlからCMakeLists.txtを生成し、CMakeでビルドを行う。直接CMakeを編集する必要は基本的にない。  
  - 依存管理：git依存は`.craft/deps/`にクローンされ、`craft add` / `craft remove` / `craft update`で管理。タグ固定やリンクターゲット指定も可能。  
  - テンプレート：実行可能／静的／共有／ヘッダのみ等のテンプレートがあり、独自テンプレートを保存してプロジェクト作成を高速化できる。  
  - 既存プロジェクト対応：`craft init`は既存のCMakeLists.txtをバックアップ（CMakeLists.backup.cmake）して移行を支援。カスタムCMakeはCMakeLists.extra.cmakeで差分を注入できる。  
  - コマンド群（代表）  
    - craft project / craft init — プロジェクト作成・初期化  
    - craft add / remove / update — 依存追加・削除・更新  
    - craft build / run / clean — ビルド・実行・クリーン  
    - craft gen — ボイラープレート生成  
    - craft template / config / upgrade — テンプレート・設定・自己更新  
- 要件と導入方法  
  - 必要：gitとcmake。インストールはシェル/PowerShellワンライナーで可能。  
- サンプル（craft.tomlの例）
```toml
[project]
name = "my_app"
version = "0.1.0"
language = "cpp"
cpp_standard = 17

[build]
type = "executable"
include_dirs = ["include"]
source_dirs = ["src"]
```
- クイック操作例
```bash
# 新規作成
craft project my_app
cd my_app

# 依存追加（例：raylib）
craft add --git https://github.com/raysan5/raylib.git --links raylib

# ビルドと実行
craft build
craft run
```
- 現状の成熟度と注意点  
  - 軽量で便利だがOSSの規模は小さくスター数も控えめ（執筆時点）。大規模レポジトリや社内ポリシーでの適用は事前評価が必要。CMakeの全機能を自動化するわけではなく、CMakeLists.extra.cmakeでの補完が推奨される。

## 実践ポイント
- 小さな新規プロジェクトでまず試す（学習コストが低い）。  
- 既存プロジェクトは`craft init`で安全に移行（既存CMakeはバックアップされる）。  
- 外部ライブラリは`craft add --git ... --tag <ver> --links ...`でタグ固定して再現性を確保。  
- CI導入時はローカルに依存がキャッシュされる構成やネットワークポリシーを確認。  
- 日本の組み込み／ゲームチームはテンプレートとgenコマンドでオンボーディング時間を短縮できる。  

導入検討時は小さなPoCで互換性（社内ライブラリ・ビルドフロー）を確かめ、CMakeのカスタム部分はCMakeLists.extra.cmakeで残す運用が現実的です。
