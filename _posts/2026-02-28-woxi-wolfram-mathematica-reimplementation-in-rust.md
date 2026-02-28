---
layout: post
title: "Woxi: Wolfram Mathematica Reimplementation in Rust - Woxi: Rustで書かれたWolfram Language/Mathematicaの再実装"
date: 2026-02-28T15:56:17.481Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/ad-si/Woxi"
source_title: "GitHub - ad-si/Woxi: Wolfram Language / Mathematica reimplementation in Rust (Wolfram oxidized)"
source_id: 47155526
excerpt: "Rust製Woxi：Mathematica互換を高速起動でJupyter上で試せる"
image: "https://opengraph.githubassets.com/ba8b2baafa6f492b6b9b074b37023ea0908516efda8c616a5c2f2af7b7dcaa9a/ad-si/Woxi"
---

# Woxi: Wolfram Mathematica Reimplementation in Rust - Woxi: Rustで書かれたWolfram Language/Mathematicaの再実装

Mathematica互換をRustで再構築した軽量インタプリタ「Woxi」が示す、オープンで高速な数式処理の可能性

## 要約
WoxiはWolfram Language（Mathematica）のサブセットをRustで実装したインタプリタで、CLIスクリプトやJupyterノートブックで動作し、WolframScriptより立ち上がりが速い点を売りにしています。

## この記事を読むべき理由
日本の研究者・教育現場やスタートアップは、Mathematicaの機能をライセンスや起動コストを気にせず試せる代替を求めています。Rust実装はパフォーマンスと安全性の利点があり、国内でのデータ解析・教育用途の選択肢になります。

## 詳細解説
- プロジェクト概要  
  WoxiはGitHub上のオープンソース（AGPL-3.0）プロジェクトで、RustでWolfram Languageの機能を再実装しています。現在は言語のサブセットに注力し、CLIでのeval/run、REPL、Jupyterカーネルのサポート、グラフィカル出力やJupyterLite（ブラウザ完結）での実行が可能です。

- 技術的ポイント  
  - 実装言語: Rust（パフォーマンスとメモリ安全性を活かす）  
  - テスト重視: CLIテスト群が用意され、WolframScriptとの出力互換を目標にしている（functions.csvで実装状況を管理）  
  - Jupyter対応: ローカル環境だけでなくブラウザ上のJupyterLiteで動かせるため、データの外部送信なしで試せる  
  - 速度面: カーネル起動やライセンスチェックが不要なため、スクリプト実行はWolframScriptより速くなるケースが多い

- 現状と制約  
  実装は完全互換ではなく未実装の関数もあるため、既存Mathematicaスクリプトの完全互換を期待するのは早計。商用利用はAGPL-3.0の条項を確認する必要があります。

## 実践ポイント
- まず試す（Rustが入っていれば簡単）:
```bash
# Rustのcargoでインストール
bash
cargo install woxi

# 簡単な評価
bash
woxi eval "1 + 2"

# スクリプト実行
bash
woxi run path/to/script.wls
```
- Jupyterで使う:
```bash
bash
woxi install-kernel
# その後 jupyter lab を起動してWoxiカーネルを選択
```
- 確認項目: functions.csvでサポート状況を確認し、CLIのtestsディレクトリで互換性テストを見る。パフォーマンスや未実装関数はローカルで検証する。  
- 貢献とライセンス: ソースはAGPL-3.0のため、組み込みや再配布の際はライセンス要件を確認してから貢献・導入する。

短時間でMathematica風のワークフローを試したい開発者や教育現場には、まずJupyterLiteでの動作確認をお勧めします。
