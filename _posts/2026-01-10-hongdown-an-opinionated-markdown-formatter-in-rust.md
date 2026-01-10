---
layout: post
title: "Hongdown: An opinionated Markdown formatter in Rust - Hongdown：Hong Minhee流Markdownスタイルを強制するフォーマッタ"
date: 2026-01-10T11:14:31.671Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/dahlia/hongdown"
source_title: "GitHub - dahlia/hongdown: A Markdown formatter that enforces Hong Minhee&#39;s Markdown style conventions"
source_id: 1379552495
excerpt: "東アジア文字幅に配慮し日本語文書を一貫整形するRust製Markdownフォーマッタ"
image: "https://opengraph.githubassets.com/396dc36666304caee6ab2672e9b8d0e05f6ddaa217a1bd4ad1fc5dce836eb614/dahlia/hongdown"
---

# Hongdown: An opinionated Markdown formatter in Rust - Hongdown：Hong Minhee流Markdownスタイルを強制するフォーマッタ
日本語ドキュメントにも効く！一貫したMarkdownスタイルを自動で守る「Hongdown」入門

## 要約
HongdownはRust製のMarkdown整形ツールで、Hong Minhee氏の明確なスタイル規約に沿ってMarkdownを自動整形する。東アジア文字幅対応や細かなリスト／コードブロック規約など、日本語文書にも有益な機能を備える。

## この記事を読むべき理由
- 日本語を含むドキュメントで文字幅（全角）の扱いを考慮するフォーマッタは稀。HongdownはEast Asian幅を考慮し、レイアウト崩れを減らせる。  
- OSSや社内WikiのMarkdownスタイルを統一してレビュー負荷を下げたい開発チーム、ドキュメント運用者に実用的。

## 詳細解説
- 実装と依存：Rustで書かれ、Comrak（CommonMarkパーサ）を利用。CLIとライブラリ両方で利用可能。
- 主要スタイルルール（デフォルト）
  - h1・h2はSetext（underlines: === / ---）、それ以降はATX（###）を使用。
  - 箇条書きはハイフン（"-"）＋1スペース＋マーカー後2スペース。ネストは4スペース。
  - 順序付きリストはレベルによってマーカーが交互（"." と ")"）に変わる。番号位置の揃え方も設定可能。
  - コードブロックは4つのチルダ（~~~~）を既定。言語識別子を付けられる。
  - 行幅は既定80カラム。東アジア幅文字を2カラムとしてカウントするため、日本語の折り返しに配慮。
  - 外部リンクは参照スタイルに変換し、セクション末尾に参照を集約。ローカルリンクはインラインのまま。
  - テーブルは全角文字を考慮して列幅を整列。
- CLIと設定
  - インストール：cargo install hongdown、npm版や事前ビルドバイナリも提供。
  - よく使うオプション：--write / -w（上書き）、--check / -c（整形済みかチェック、非整形時にexit 1）、--diff / -d、--stdin、--line-width、--config。
  - 設定ファイル：`.hongdown.toml` をカレントまたは親ディレクトリから検索。多くのフォーマット挙動を細かく調整可能。
- 無整形ディレクティブ
  - HTMLコメントで一部を整形除外できる（例: <!-- hongdown-disable-file -->、<!-- hongdown-disable-next-line -->、<!-- hongdown-disable --> / <!-- hongdown-enable -->）。
- ライブラリ利用例（Rust）：APIで文字列を受け取り整形結果を返す関数が提供される。
- 開発ワークフロー：miseを使ったタスク管理や、pre-commitフック設定でコミット前チェックを自動化。ライセンスはGPL-3.0-or-later。

## 実践ポイント
- まずローカルで差分確認：
```bash
# diff を確認して問題ないか見る
hongdown --diff README.md
# 整形を適用する
hongdown --write README.md
```
- CIに組み込み、プルリクで自動チェック：
```bash
# CIではフォーマットチェックだけ実行（失敗でジョブを落とす）
hongdown --check .
```
- 日本語プロジェクト向け設定例
  - 行幅を100にする、テーブル最小幅を広げるなどを .hongdown.toml に設定して日本語表示崩れを抑える。
- 例外扱いの箇所は無整形ディレクティブで保護。翻訳やサンプルコードなど整形されたくない部分に有用。
- Rustプロジェクトならライブラリとして組み込み、ビルド中に自動整形を行うことも可能：
```rust
use hongdown::{format, Options};

let input = "# タイトル\n本文です。";
let out = format(input, &Options::default()).unwrap();
println!("{}", out);
```
- ライセンスに注意：GPL-3.0のため商用組み込みや配布の際はライセンス条件を確認する。

Hongdownは「スタイルの押し付け」ではなく「一貫性を自動化するツール」と考えると導入しやすい。まずはプロジェクトのREADMEやドキュメント群で試し、CI連携で運用に乗せるのがおすすめ。
