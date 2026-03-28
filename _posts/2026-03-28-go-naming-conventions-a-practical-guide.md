---
layout: post
title: "Go Naming Conventions: A Practical Guide - Go命名規則：実践ガイド"
date: 2026-03-28T10:49:27.455Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.alexedwards.net/blog/go-naming-conventions"
source_title: "Go Naming Conventions: A Practical Guide&ndash; Alex Edwards"
source_id: 47509031
excerpt: "チームで即使えるGo命名ルール集：可読性・保守性を劇的に高める具体チェックリスト付き"
---

# Go Naming Conventions: A Practical Guide - Go命名規則：実践ガイド
読みやすさで差がつく！チームでも個人でも使えるGoの“正しい”命名ルール

## 要約
Goでは識別子やパッケージ名に関する厳密なルールと慣習があり、正しい命名は可読性・保守性・API設計に直結する。本記事は識別子、パッケージ、ファイル名ごとの実践ルールと注意点をまとめる。

## この記事を読むべき理由
命名は小さな作業に見えるが、チーム開発・ライブラリ設計・将来的なリファクタでのコストを左右します。日本のプロジェクトでも読みやすく安全なコードベースを保つための、すぐ使えるチェックリストが得られます。

## 詳細解説
- 識別子の「硬いルール」  
  - 使用可能文字：Unicode文字・数字・アンダースコア。先頭は数字不可。Goキーワードは不可。  
- 大文字・小文字とエクスポート性  
  - 先頭大文字＝エクスポート（パッケージ外から見える）。意図がある場合のみ大文字にする（shy codeの原則）。mainパッケージ内は基本小文字。  
- 命名の慣習  
  - 非公開は camelCase、小文字始まり。公開は PascalCase。snake_case / ALLCAPS 等は避ける。  
  - 頭字語（API, URL, HTTP, ID）は一貫して扱う（例：APIKey, userID）。ApiKey や userId は避ける。  
  - 非ASCII文字は可読性低下のため原則避ける（π → pi）。  
  - 組み込み型・標準関数名（int, len, max など）と衝突させない。  
  - 変換後の変数名に型を添えるのは許容（userIDStr など）。  
  - import しているパッケージ名と同名の識別子は避ける（url, mail 等）。  
- 識別子の長さとスコープ  
  - 近接・短スコープなら短名（一文字）で可。広範囲で使うものは説明的に。  
- パッケージ命名  
  - 小文字ASCIIのみ、短くタイプしやすい名（orders, slug）。複数単語は連結（ordermanager）。util や helpers のような総花的名称は避ける。internal / vendor / testdata は特別扱い（使用に注意）。  
- ファイル命名  
  - 1語で要旨を表す（cookie.go）。複数語はプロジェクトで一貫させる（concat か underscore）。特殊接頭辞「.」「_」やサフィックス「_test.go」「_linux.go」等はツール側の意味あり。  
- 「チャター」を避ける  
  - パッケージ名を繰り返す冗長な公開名は避ける（customer.New() を使い、customer.NewCustomer() は不要）。

## 実践ポイント
- 基本ルールチェックリスト：識別子がキーワードでない／先頭が数字でない／ASCII中心／エクスポートは先頭大文字のみ。
- 命名スタイル：非公開→camelCase、公開→PascalCase、頭字語は全大文字（API, ID）。  
- 名前衝突対策：組み込み・インポート済みパッケージ名との衝突をCIで検出。  
- スコープに応じた長さ：短スコープは短名、広スコープは説明的に。  
- パッケージ設計：helpers/util を作る前に分割を検討。短い名で責務を明確に。  
- ファイル命名：プロジェクト内で「underscore 使うか否か」を決めて統一。テスト・OS/archサフィックスは用途を理解して使う。  
- エクスポートは最小限：外部公開は慎重に、フィールドはJSON等で必要な場合のみ公開。

以上を日常のコードレビューやCIルールに落とし込めば、チームで読みやすく変更しやすいGoコードを維持できます。
