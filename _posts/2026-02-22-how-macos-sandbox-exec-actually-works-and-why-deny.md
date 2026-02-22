---
layout: post
title: "How macOS sandbox-exec actually works — and why deny-default matters when your app is the exfiltration path - macOSのsandbox-execは実際にどう動くか ─ deny-defaultが重要な理由（アプリがデータ流出経路になる場合）"
date: 2026-02-22T01:41:57.268Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/goshtasb/omni-glass"
source_title: "GitHub - goshtasb/omni-glass"
source_id: 400963078
excerpt: "画面を即時修正するAIがローカルとカーネル級サンドボックスでデータ漏洩を防ぐ設計とは？"
image: "https://opengraph.githubassets.com/3b861b9c0f19b421cf5af98cf7c3f7610481ea6e89893410236c9ead19ebac31/goshtasb/omni-glass"
---

# How macOS sandbox-exec actually works — and why deny-default matters when your app is the exfiltration path - macOSのsandbox-execは実際にどう動くか ─ deny-defaultが重要な理由（アプリがデータ流出経路になる場合）
スクショを切り取って「その場で直す」AIアプリ、Omni-Glassの仕組みと日本で気をつけるべき安全設計

## 要約
Omni-Glassは画面をスニップしてOCR→LLMで解釈し、その場でコマンド実行やファイル保存などの操作を行うツール。プラグインはカーネル級のmacOSサンドボックス（sandbox-exec）で隔離され、ホームディレクトリやAPIキーをデフォルトで遮断する設計が特徴。

## この記事を読むべき理由
日本の企業や個人開発者にとって、画面データを扱うツールの「どこまで自動化して良いか」と「どこまで隔離すべきか」は法的・運用的に重要。Omni-GlassはローカルLLMやカーネル級サンドボックスを組み合わせ、実運用でのプライバシー設計や拡張性の参考になるからです。

## 詳細解説
- 基本動作：ユーザーが画面を矩形で指定 → ローカル/OSのOCRで文字抽出 → LLM（Claude/Gemini/ローカルQwen）に渡し、実行可能なアクションをJSONで生成 → ユーザー確認後にプラグインが実行。
- 実行層（MCPプラグイン）：プラグインは標準入出力ベースのMCPサーバとして実装可能。多くは100行程度で作れる設計で、GitHubやターミナル操作、CSVエクスポート等を「アクション」として提供。
- セキュリティ：各プラグインはsandbox-execによるカーネルレベルのサンドボックス内で動作。ホームディレクトリはデフォルトで遮断（ユーザーが個別許可するまでは/Users以下にアクセス不可）。環境変数やAPIキーはプロセスから除去。全てのシェルコマンドは実行前にユーザーが確認。
- オフライン対応：ローカルで動くQwen-2.5 via llama.cppを使えば、画面内容が外部に出ない完全オフライン運用が可能で、企業のデータ管理政策に適合しやすい。
- 実装・起動例：macOS 12+ が要件。リポジトリはRust/TypeScriptベースで、tauri + Node環境で動作する。プラグインテンプレートを使って素早く拡張可能。

## 実践ポイント
- まずローカルモードで動かす：機密データ扱うならQwenなどローカルモデルを試す。  
- プラグインは最小権限で：インストール前にアクセス許可ダイアログを必ず確認。deny-by-default（拒否をデフォルト）を徹底する。  
- コマンド実行は必ず目視確認：自動実行を信頼せず、ログとコマンド確認を運用ルールに組み込む。  
- 日本語ドキュメント/翻訳ワークフローに活用：日本語ドキュメントの要約・翻訳やIssue自動作成など、日本開発現場で即役立つユースケースが多い。  
- プラグイン開発を小さく始める：公式テンプレートで100行程度から作成し、社内ツール連携を安全に自動化する。

以上。
