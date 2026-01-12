---
layout: post
title: "YAML? That’s Norway problem - YAML？それは「ノルウェー問題」"
date: 2026-01-12T11:54:10.603Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://lab174.com/blog/202601-yaml-norway/"
source_title: "YAML? That’s Norway problem"
source_id: 428777581
excerpt: "YAMLの「NO」がfalse化する原因とすぐ使える対策を図解で解説"
---

# YAML? That’s Norway problem - YAML？それは「ノルウェー問題」
YAMLで"NO"が勝手にfalseに変わる？──その正体と、今すぐできる対策

## 要約
YAMLの過去仕様では英語の yes/no が暗黙的に真偽値へ変換されました（いわゆる「ノルウェー問題」）。仕様は v1.2 でこの振る舞いをやめましたが、現実のライブラリはまだ古い挙動を残していることが多く、設定ファイルで国コードやトークンが意図せず boolean になる事故が続いています。

## この記事を読むべき理由
日本の現場でも YAML は CI、Kubernetes、GitHub Actions、設定ファイルで広く使われています。国コード（NO）や ON/OFF などが誤って boolean に変換されると、デプロイ失敗やサービス停止につながる可能性があるため、原因と対策を知っておくことは実務上重要です。

## 詳細解説
- 問題の核心  
  YAML の初期仕様（v1.0 / v1.1）では plain scalar（引用符なしの文字列）として書かれた yes/no/on/off などを暗黙に true/false に変換する規則がありました。たとえば countries: - NO の NO は boolean の false として扱われうるため、意図しない型変換が起きます。これが俗に「Norway problem（ノルウェー問題）」と呼ばれるものです。

- 仕様の変遷（要点）  
  - v1.0 / v1.1: yes/no を含む英語語彙で暗黙的に boolean にする挙動が存在。互換性のため多くの実装がこれを踏襲。  
  - v1.2（2009年）: JSON 互換性を目指し、暗黙的な英語 boolean のルールを撤廃。生の "no" は文字列扱いに変更。  
  仕様上は解決済みですが、実装（ライブラリ）の状況が追いついていません。

- 実装状況（実例）  
  - PyYAML / libyaml: 長年 v1.2 を完全実装しておらず、暗黙的な boolean を残す実装が多い。  
  - ruamel.yaml / libfyaml: v1.2 相当の挙動をサポートするライブラリ（代替として有効）。  
  - Go の yaml ライブラリ: プロジェクトによって v1.1 挙動を残したり v1.2 を採用したり混在。  
  - Kubernetes 周辺では kyaml のように予測しやすい方言を用いる動きもある（2025年以降の流れ）。

- なぜまだ起きるのか  
  YAML は仕様も実装も複雑で、依存関係の深いライブラリ（C の libyaml 等）を変えるのはリスクが大きい。既存の設定や既存ユーザーとの互換性を壊さないため、古い挙動が残ることが多いです。

## 実践ポイント
- すぐできる安全策  
  1. 曖昧な値は必ず引用する：NO, ON, YES, OFF などを使うときは "NO" のようにクォートする。  
  2. 明示的に文字列タグを使う：`!!str NO` と書くと文字列として扱われる。  
  3. CI や lint でチェック：設定ファイルに unquoted の NO/yes 等がないか静的チェックを入れる（yamllint 等のルールや自作スクリプトで検出）。

- ライブラリ運用の指針  
  - 新規プロジェクトでは v1.2 準拠の実装を選ぶ（例：ruamel.yaml や libfyaml を検討）。  
  - 既存の依存が深い場合は、パース結果の型チェックとテストを充実させる。  
  - Kubernetes やプロダクション構成ファイルでは、明示的な quoting をプロジェクトのコーディング規約に盛り込む。

- 動作確認用の簡単スニペット（Python）  
  ```python
  # python
  import yaml
  s = "countries:\n  - DE\n  - FR\n  - NO\n"
  data = yaml.safe_load(s)
  print(data)               # 古いライブラリだと NO が False になっている可能性あり
  print(type(data["countries"][2]))
  ```
  扱っているライブラリで実際にどの型になるかを必ず確認してください。

まとめ：YAML の仕様は v1.2 で「ノルウェー問題」を仕様的に解消しましたが、現実のエコシステムではまだ影響を受けます。設定ファイルの安全性を上げる最速の対策は「曖昧な値をクォートすること」と「パーサーの挙動をCIで検証すること」です。
