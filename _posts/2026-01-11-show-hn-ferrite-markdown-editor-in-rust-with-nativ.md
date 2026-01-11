---
layout: post
title: "Show HN: Ferrite – Markdown editor in Rust with native Mermaid diagram rendering - Ferrite：Mermaidをネイティブ描画するRust製Markdownエディタ"
date: 2026-01-11T02:29:53.505Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/OlaProeis/Ferrite"
source_title: "GitHub - OlaProeis/Ferrite: A fast, lightweight text editor for Markdown, JSON, YAML, and TOML files. Built with Rust and egui for a native, responsive experience."
source_id: 46571980
excerpt: "オフラインでMermaid図をネイティブ描画する軽量Rust製Markdownエディタ"
image: "https://opengraph.githubassets.com/cbacc38607d55dd8e3f0a0fd33f93d5f079caf1548489d85a413db2159502872/OlaProeis/Ferrite"
---

# Show HN: Ferrite – Markdown editor in Rust with native Mermaid diagram rendering - Ferrite：Mermaidをネイティブ描画するRust製Markdownエディタ
Mermaid図をオフラインでサクッと描ける！Rust＋eguiで作られた軽量Markdownエディタ「Ferrite」の注目ポイント

## 要約
FerriteはRustとeguiで作られた軽量なネイティブMarkdownエディタで、11種類のMermaid図をプレビュー内でネイティブにレンダリングします。WYSIWYG編集、スプリットビュー、JSON/YAML/TOMLのツリー編集やGit統合など、ローカル作業に便利な機能が揃っています。

## この記事を読むべき理由
- Mermaidをクラウドに頼らずローカルで描きたい人（社内ドキュメントや機密資料の可搬性向上）に最適。  
- Rust製で軽量・高速、VS CodeやObsidianの代替または補完ツールとして検討できる。  
- 日本のエンジニアやドキュメンテーション担当がオフラインで図を扱う場面（社内仕様書・設計書・ナレッジ共有）で即戦力になる可能性が高い。

## 詳細解説
- コア設計
  - 言語・UI: Rust 1.70+、egui/eframeを採用。即時描画（immediate-mode）によるネイティブな反応性を重視。
  - Markdownパース: comrak（CommonMark + GFM互換）で安定したレンダリング。
  - シンタックスハイライト: syntectを利用し40+言語に対応。
- 主な機能
  - WYSIWYG編集とライブプレビュー（Raw/Rendered/Splitの3モード）。双方向スクロールで編集とプレビューが同期。
  - Mermaidのネイティブレンダリング（Flowchart, Sequence, Pie, State, Mindmap, Class, ER, Git Graph, Gantt, Timeline, User Journey をサポート）。v0.2.1ではシーケンスの制御フロー（loop/alt/opt/par）やactivation boxes、ノート、サブグラフ、ネスト状態などを強化。
  - JSON/YAML/TOMLのツリー表示とインライン編集、パスコピーや折りたたみ。
  - ミニマップ、括弧一致、コード折りたたみ、行番号、オートセーブなどエディタ系機能。
  - ワークスペースモード（フォルダ開き、ファイルツリー、Ctrl+Pでクイックスイッチ）、Gitステータス表示、セッション復元。
- 配布とビルド
  - Windows向けに主にテスト済み。Linux/macOSも動くがテストは限定的との注意あり。
  - 公式リリースで事前ビルドバイナリ（Windows .zip、Linux .deb / .tar.gz、macOS .tar.gz）を提供。ソースからのビルドはcargoで可能（Rust環境・プラットフォーム依存ライブラリが必要）。
  - 例（ビルド／インストールの基本）:
```bash
# ソースからリリースビルド
git clone https://github.com/OlaProeis/Ferrite.git
cd Ferrite
cargo build --release

# Debian系で配布バイナリを使う場合
sudo apt install ./ferrite-editor_amd64.deb
```
- 制約・現状
  - Windowsでの開発・テストが中心。Linux/macOSでは問題が出たら報告が推奨されている。  
  - 一部のUI/機能はまだロードマップ上にあり（例：テキスト非表示の完璧な折りたたみはv0.3.0へ）。

## 実践ポイント
- すぐ試す
  - まずはGitHub Releasesからプラットフォーム用バイナリを落として試用。Mermaidを含むREADMEや小さなドキュメントを開いてレンダリングの挙動を確認する。
- 社内ドキュメント活用法
  - 社内設計書やフローチャートを外部サービスに上げたくない場合、FerriteでMermaidを作成／編集してHTMLエクスポート／コピーして社内Wikiに貼るワークフローが便利。
- 開発者の取り組み
  - Rust環境があるならソースからビルドして、プラットフォーム固有の問題（特にLinux/macOS）を検証・報告することでプロジェクトに貢献できる。
- 既存ツールとの使い分け
  - 軽量で高速にローカル編集したい場合はFerrite、プラグインや拡張が必要ならVS CodeやObsidianを併用するのが現実的。
- 貢献・カスタマイズ
  - 貢献ガイド(CONTRIBUTING.md)に沿ってフォーク→ブランチで変更。Rust/eguiに興味がある日本のOSSコントリビュータにとって学習用にも良い題材。

短くまとめると、Ferriteは「オフラインでMermaid図を手早く扱いたい」「軽量でネイティブなMarkdown体験がほしい」日本のエンジニア／ドキュメント担当に刺さる選択肢です。まずはリリースバイナリで試し、社内ユースケースに合えば導入やカスタム貢献を検討してみてください。
