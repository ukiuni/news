---
layout: post
title: "Show HN: CEL by Example - CEL by Exampleの紹介"
date: 2026-02-18T15:47:38.331Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://celbyexample.com/"
source_title: "CEL by Example"
source_id: 47061029
excerpt: "実例で学べるCEL入門：短い式で安全にポリシーを実装、KubernetesやGCPに即活用"
---

# Show HN: CEL by Example - CEL by Exampleの紹介
実例で覚えるCEL（Common Expression Language）：ポリシー／条件を短く安全に書く技術

## 要約
CELはJSON/Protobufに対して式を評価する軽量言語で、KubernetesのAdmission、GCP IAM、Firebaseルールなどで使われる。celbyexample.comは実例ベースで学べる良質なチュートリアルサイトです。

## この記事を読むべき理由
日本でもKubernetesやクラウドサービス、セキュリティルールの自動化需要が高まる中、短い式でポリシーやフィルタを安全に記述できるCELは実務価値が高い。サンプル中心の学習で導入ハードルが下がる。

## 詳細解説
CELの基本概念と代表的な操作を実データで確認する。

- 型と用途：文字列、数値、リスト、マップ、タイムスタンプ、Protobufのネイティブサポート。高速かつ移植性が高く、安全設計（実行コスト制御）がある。
- 比較・文字列操作：
```cel
user.age >= 18
user.email.endsWith("@example.com")
```
- コレクション操作：メンバーシップ、存在判定、フィルタ、変換。
```cel
"admin" in user.roles
user.roles.exists(r, r.startsWith("ad"))
user.roles.filter(r, r != "viewer")
user.roles.map(r, { "role": r, "elevated": r != "viewer" })
```
- 時刻と期間計算：タイムスタンプ同士の差分で期間比較。
```cel
user.email_verified - user.created < duration("24h")
```
- 論理・条件式：&&, ||, 三項演算子で複合条件を1行で表現。
```cel
user.age >= 18 && "admin" in user.roles
user.age >= 18 ? "adult" : "minor"
```
- 利用シーン：KubernetesのAdmission/Policy（Gatekeeper等）、GCP IAM条件、Firebaseルール、Envoyのルーティング、プロトコル検証ツール（Protovalidate）など。仕様と参照実装はGitHub／公式ドキュメントで公開されている。

## 実践ポイント
- まずcelbyexample.comのサンプルを真似して手を動かす。
- 既存のJSON/Protobufを用意して、小さな式（年齢判定・メールドメイン・役割フィルタ）から試す。
- list操作はexists/filter/mapを使い、ループを書かずに短く安全に書ける。
- タイムゾーンやdurationの扱いに注意して、テストデータで検証する。
- ポリシー用途では実行コスト制限や例外ケース（nullや型不一致）を明示的に扱う。
- KubernetesやCIに組み込む場合、まずオフラインで式を検証するワークフローを作る。

元記事（celbyexample.com）は実例が豊富なので、業務ルールのプロトタイプや教育教材として即戦力になります。
