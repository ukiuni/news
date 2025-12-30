---
layout: post
title: Commandry - A Command-Line Parser for Standard ML - Commandry - Standard ML用のコマンドラインパーサー
date: 2025-12-27 15:42:51.086000+00:00
categories:
- tech
- world-news
tags:
- tech-news
- japan
source_url: https://github.com/PerplexSystems/commandry
source_title: 'GitHub - PerplexSystems/commandry: A command-line parser for Standard
  ML'
source_id: 1137160111
excerpt: 単一ファイルで導入できる宣言的CLIライブラリでSMLの学術ツールを素早く作れる
---
# Commandry - A Command-Line Parser for Standard ML - Commandry - Standard ML用のコマンドラインパーサー

## 要約
Commandryは「単一ファイル」で使えるStandard ML向けの宣言型コマンドラインパーサー。サブコマンドや多様な引数タイプ、自動生成されるヘルプ/バージョン表示を簡潔なAPIで提供するため、研究ツールや小型ユーティリティの開発がぐっと楽になる。

## この記事を読むべき理由
日本では大学や研究開発、コンパイラ／言語処理系の教育・実験でStandard MLが今も根強く使われている。少ないコードで堅牢なCLIを実装できるCommandryは、プロトタイプ作成や学生向け演習、内部ツールの短期開発に非常に有用だ。

## 詳細解説
Commandryのポイント（技術的に重要な点）:

- 単一ファイル設計: ライブラリは src/cli.sml をプロジェクトにコピーするだけで利用可能。依存管理が簡単で、学術用途や小規模ツールに向く。
- 宣言的ビルダーパターン: 関数をチェーンしてCLIを組み立てるため、読みやすく拡張しやすい。副作用を最小限に抑えた設計。
- 多様な引数型: フラグ、文字列/整数オプション（デフォルト付き）、位置引数（必須・省略可・可変長）をサポート。
- ネストしたサブコマンド: 階層構造のサブコマンドを定義でき、git風のCLI設計が可能。
- 自動生成ヘルプ: --help や --version を自動で用意し、フォーマット済みの使用法を出力。

READMEにある基本的な使い方例（そのままプロジェクトへ貼れる）:

```sml
sml
val cli : string Cli.parser =
  Cli.app "hello" "1.0.0" "Says hello to someone" (fn name => name)
  |> Cli.positional { name = "name", help = "Someone's name" }
  |> Cli.cli

fun main () =
  Cli.exec (fn name => print ("Hello, " ^ name ^ "\n")) cli
```

内部実装はSMLの型システムを活かした設計で、パーサーは解析結果を安全に型付きで返す。エラーメッセージやヘルプのフォーマットも標準的なCLIのUXに沿っているため、ユーザーに親切なインターフェースがすぐに作れる。

## 実践ポイント
- 導入は簡単: src/cli.sml をプロジェクトにコピーし、既存のMLB/smlpm設定へ追加するだけ。
- 日本語ヘルプ対応: help文字列に日本語を入れて問題なし（端末のエンコーディングに注意）。
- テスト: repositoryには tests フォルダがあるので、既存のテスト例を参考にCLIの振る舞いを自動化すると保守が楽。
- 学習用途: 演習課題でCLIの入力処理を教える際、ボイラープレートをCommandryに任せると本質（アルゴリズムや型）に集中できる。
- 組み合わせ: Nix/flake や smlpm と組み合わせると再現可能なビルド環境で配布しやすい（リポジトリに flake.nix / smlpm.toml が含まれている）。
- 注意点: 高度な引数検証や複雑な型変換が必要な場合は、CommandryのAPIでラップして独自検証を追加すると良い。

