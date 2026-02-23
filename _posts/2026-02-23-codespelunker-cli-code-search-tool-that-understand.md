---
layout: post
title: "codespelunker - CLI code search tool that understands code structure and ranks results by relevance. No indexing required - インデックス不要で「実装」を見つけるCLI検索ツール：codespelunker (cs)"
date: 2026-02-23T01:03:38.457Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/boyter/cs"
source_title: "GitHub - boyter/cs: codespelunker - CLI code search tool that understands code structure and ranks results by relevance. No indexing required"
source_id: 1050321826
excerpt: "インデックス不要で構造解析し複雑度で実装を上位表示するCLI検索"
image: "https://opengraph.githubassets.com/7f2eda70cd6a1415a56bf0e5093c021d8bbdd4102d148f679f51f94ecda9f581/boyter/cs"
---

# codespelunker - CLI code search tool that understands code structure and ranks results by relevance. No indexing required - インデックス不要で「実装」を見つけるCLI検索ツール：codespelunker (cs)
インデックス不要でコードの構造を理解し、「実装」を上位に出すCLI検索――手元リポジトリの探索効率を劇的に上げる cs の紹介

## 要約
cs はファイルをオンザフライで字句解析・構造化して検索結果を BM25 と独自の「構造重み／複雑度」でランク付けするCLIツール。インデックス不要で、コメントや文字列、宣言／使用箇所を区別して絞り込みできるのが特徴。

## この記事を読むべき理由
大規模リポジトリや古いコードベースで「実装箇所がコメントや設定に埋もれる」問題は世界共通。日本の現場でもローカルで高速に“意味ある”検索が欲しい場面が多く、Sourcegraph のような重い索引ソリューションなしで実装中心の検索ができる点は即戦力になります。

## 詳細解説
- 構造認識：各ファイルを解析して「コード」「コメント」「文字列」「宣言（func/class/def）」を識別。検索時にこれらを別々のフィールド扱いにして重み付けする。  
- スコアリング：BM25 をベースにしつつ、構造フィールドごとに重み（例：コード=1.0, 文字列=0.5, コメント=0.2）を与える。ファイル長やテストファイルの減衰も考慮する。  
- 複雑度（Complexity Gravity）：scc によるサイクロマティック複雑度をランキングシグナルに利用。実装が複雑なファイルを上位に出す (--gravity=brain など) ことで「実際に処理している箇所」を探しやすくする。  
- フィルタリング：--only-code / --only-comments / --only-strings / --only-declarations / --only-usages といった厳密フィルタでノイズを排除可能。  
- 重複排除：--dedup でバイト単位の重複（vendored 等）をまとめる。  
- インターフェース：標準コンソール出力、TUI（引数なしで起動）、HTTPサーバ（cs -d）やLLM連携用のMCPサーバを提供。テンプレートで見た目カスタマイズ可。  
- 言語対応：Go, Python, JS/TS/TSX, Rust, Java, C/C++/C#, Ruby, PHP, Kotlin, Swift, Shell, …多数。未対応言語はテキストマッチ扱い。  
- パフォーマンスとトレードオフ：ripgrep のようなバイトスキャンよりは重い（字句解析＋複雑度計算）が、インデックスを作らずに“意味ある順位付け”をその場で行える点が差別化。目安として高速マシンで大規模コードベースを数秒で検索可能という報告あり。  
- インストール：Go >= 1.25.2 なら go install で入る。バイナリは各OS用リリースも有。

例（よく使うコマンド）：
```bash
# 実装（複雑な本体）を優先して検索
cs "authenticate" --gravity=brain

# コメントだけを検索（TODO/FIXME 等）
cs "TODO" --only-comments

# 文字列リテラルのみ（エラーメッセージ等）
cs "error" --only-strings

# 宣言だけにジャンプ（関数/クラス定義）
cs "handleRequest" --only-declarations

# ベンダー重複をまとめる
cs "error" --dedup

# TUI 起動
cs

# HTTP インターフェース起動（ブラウザで探索）
cs -d
```

## 実践ポイント
- まずはローカルで go install かリリースバイナリを入れ、手持ちの大きなリポジトリで cs を試す。ripgrep と使い分けると効果的。  
- 「実装を見つけたい」時は --gravity=brain、設定やインターフェースを探すなら --gravity=low を使い分ける。  
- セミオートメーション：VS Code のターミナルから直接実行したり、タスクやキーバインドに登録して素早く検索を呼び出す。HTTPモードを使えばブラウザで結果確認・共有も可能。  
- ベンダーやコピー多発するプロジェクトでは --dedup が有効。テスト騒音が気になるならノイズ設定やテスト抑制オプションを活用する。  

まずは数回の検索で「ripgrep では見つからなかった『実装』が上位に来る」体験をしてください。現場のデバッグ・コードリーディング効率が期待以上に向上します。
