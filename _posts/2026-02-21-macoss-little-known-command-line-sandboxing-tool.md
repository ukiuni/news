---
layout: post
title: "macOS's Little-Known Command-Line Sandboxing Tool - macOSのあまり知られていないコマンドラインサンドボックスツール"
date: 2026-02-21T15:21:52.323Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://igorstechnoclub.com/sandbox-exec/"
source_title: "sandbox-exec: macOS&#x27;s Little-Known Command-Line Sandboxing Tool | Igor&#x27;s Techno Club"
source_id: 47101200
excerpt: "sandbox-execでmacOSアプリを“監獄化”し未知コードを安全に検証する方法"
image: "https://bear-images.sfo2.cdn.digitaloceanspaces.com/herman-1683556668-0.png"
---

# macOS's Little-Known Command-Line Sandboxing Tool - macOSのあまり知られていないコマンドラインサンドボックスツール
クリックせずにいられないタイトル: macOS標準ツールで“アプリを監獄化”する方法 — sandbox-execで試す安全対策

## 要約
macOS標準のコマンドラインツール「sandbox-exec」は、任意のアプリやスクリプトを細かく制限して実行できる強力なサンドボックス機能を提供します。設定はプロファイル（LISP風構文）で定義し、デバッグログで拒否された操作を確認できます。

## この記事を読むべき理由
日本の個人開発者や企業エンジニアにとって、未知のバイナリやテスト用コードを安全に動かす手段は必須です。sandbox-execは追加ソフト不要でローカル検証やプライバシー保護、脆弱性検証に役立ちます（ただしAppleは開発者向けには非推奨の点に注意）。

## 詳細解説
- 基本概念  
  sandbox-execは「実行環境に明示的に許可した操作以外を制限する」ツール。プロファイルで許可/拒否ルールを記述します。

- プロファイルの構造（例）
  (version 1) や (deny default) / (allow default) を宣言し、リソース指定に literal, regex, subpath を使います。例:
```bash
# bash
# deny-by-default の典型
(version 1)
(deny default)
(allow file-read-data (regex "^/usr/lib"))
(allow process-exec (literal "/usr/bin/python3"))
```

- 2つの設計哲学  
  1) Deny by Default — 最小権限で安全。ただし動作させるには細かな許可設定が必要。  
  2) Allow by Default — 実装は楽だが危険を見落としやすい。

- 実用例：ネットワーク禁止のシェル
```bash
# bash
# terminal-sandbox.sb を作成
(version 1)
(allow default)
(deny network*)
(deny file-read-data (regex "^/Users/[^/]+/(Documents|Pictures|Desktop)"))

# 使い方
sandbox-exec -f terminal-sandbox.sb zsh
```

- システム付属プロファイルの活用  
  /System/Library/Sandbox/Profiles にサンプルがあるため、そこからインポートして拡張すると効率的です。

- デバッグ方法  
  Console.appで"sandbox"を検索、あるいはターミナルでリアルタイムログを確認:
```bash
# bash
log stream --style compact --predicate 'sender=="Sandbox"'
# アプリ名で絞る例
log stream --style compact --predicate 'sender=="Sandbox" and eventMessage contains "python"'
```
拒否（deny）された操作がログに出るので、プロファイル修正の手掛かりになります。

- 注意点（Modern macOSの落とし穴）  
  ・Appleは開発者向けにsandbox-execの直接利用を推奨していません。  
  ・GUIアプリやMach/XPCを使う複雑なアプリは期待通りに制限されないことがある（UI側の権限やプロセス構造で抜け道が生じる）。  
  ・macOSの大幅アップデートで挙動が変わる可能性あり。  

## 実践ポイント
- まずは deny-by-default の小さなプロファイルでシェルをテストし、ログを見ながら許可を増やす。  
- /System/Library/Sandbox/Profiles を読み、既存プロファイルを import して編集する。例:
```bash
# bash
# プロファイルのインポート例
(version 1)
(import "/System/Library/Sandbox/Profiles/bsd.sb")
(deny network*)
```
- GUIアプリを制限したい場合は、sandbox-execだけでは不十分なことがあるため、まずはCLIツールやテストスクリプトで運用を試す。  
- よく使う設定はシェルのエイリアスに登録する（ただしUIアプリで期待通り動かないケースあり）。  
- 企業で利用する場合は、MDMやApp Sandbox（Appleの公式機構）との組み合わせや、運用ポリシー検討を推奨。

短時間で安全性を確かめたい個人開発者、サンドボックスでの振る舞い検証が必要なQAエンジニア、社内で未確認バイナリを扱うセキュリティ担当者にとって、sandbox-execは知っておく価値の高いツールです。
