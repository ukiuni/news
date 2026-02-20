---
layout: post
title: "Pi for Excel: AI sidebar add-in for Excel, powered by Pi - Excel向けAIサイドバーアドイン「Pi for Excel」"
date: 2026-02-20T03:57:33.865Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/tmustier/pi-for-excel"
source_title: "GitHub - tmustier/pi-for-excel: Experimental Excel sidebar agent add-in. Multi-model. Powered by Pi."
source_id: 47082854
excerpt: "Excel内でセル読み書き・数式説明や複数LLM切替で作業自動化、1クリック復元も可能なサイドバー"
image: "https://opengraph.githubassets.com/13c6d7493bb440ebd3022233fb67fd40f52dc05a24a5a403e1d33a5a967a80c5/tmustier/pi-for-excel"
---

# Pi for Excel: AI sidebar add-in for Excel, powered by Pi - Excel向けAIサイドバーアドイン「Pi for Excel」
Excelが「会話する」未来へ：セルを読み書きして作業を自動化するAIサイドバーを今すぐ試したくなる理由

## 要約
Pi for Excelは、Excel内部で動作するオープンソースのAIエージェント拡張です。ワークブックを読み取り・変更・調査でき、多様なLLMプロバイダ（Anthropic、OpenAI、Google Gemini、GitHub Copilot等）を切り替えて使えます。

## この記事を読むべき理由
日本ではExcelが業務の中心であり、定型作業やレポート作成の自動化ニーズが高いです。本ツールは「セル単位の操作」「式の説明」「書式の統一」「変更のワンクリック復元」など実務で即使える機能を備え、社内データを扱う日本企業の生産性向上に直結します。

## 詳細解説
- コア機能（代表例）
  - get_workbook_overview：ブック構造の自動把握（シート、ヘッダ、テーブル等）
  - read_range / write_cells：セルの読み取り・書き込み（CSV/Markdown形式や書式付き詳細）
  - fill_formula：相対参照を保ったままのオートフィル
  - search_workbook / modify_structure：全シート検索、行列挿入・削除、シート操作
  - explain_formula / trace_dependencies：式の平易な説明と依存関係追跡
  - format_cells / conditional_format：通貨・小数桁等の一括整形と条件付き書式
  - workbook_history：変更ごとにチェックポイントを作成、1クリックでロールバック可能
  - comments / view_settings：コメント管理や表示設定の操作
- マルチモデル対応
  - APIキー持込またはOAuthでAnthropic、OpenAI、Google、GitHub Copilotが利用可能。会話中にモデルを切り替えられる。
- セッション・コンテキスト設計
  - 複数タブのセッション管理、自動コンテキスト注入（現在の選択範囲や最近の変更を毎ターン添付）で説明不要。
- 拡張性と安全策
  - サイドバー拡張（iframeサンドボックス）をインストール可能。拡張は権限管理と実験フラグで制御。
  - 変更前チェックポイント、監査ログ、実行ポリシー分類（読み取り／変更）で安全性を担保。
- 開発・導入
  - 技術スタック：Vite、Lit、Office.js、pi-agent-core / pi-ai / pi-web-ui。
  - インストール：manifest.prod.xmlをダウンロードしてExcelに追加（macOS/Windows対応）。開発時はNode.js≥20＋mkcertでローカルHTTPSを用意してsideload。
  - OAuthのCORS問題対策としてプロキシ（pi-for-excel-proxy / npm run proxy:https）が用意されている。
- ローカルブリッジ（実験）
  - Python / LibreOfficeブリッジやtmuxブリッジでローカルスクリプト実行や端末操作をつなげられる（実験機能、要追加インストール）。

## 実践ポイント
- まず試す：manifest.prod.xmlをダウンロードしてExcelに追加し、Piサイドバーを開いて「What sheets do I have?」「Summarize my current selection」等を投げてみる。
- BYOポリシー：業務データを扱う場合は自社のAPIキー運用・プロキシ方針に合わせて利用（OAuthがCORSで詰まる場合はプロキシを設定）。
- 日本向け設定：Conventionsで通貨記号を「¥」、小数桁や負数表示を社内基準に設定して整形を自動化。
- 安全運用：自動チェックポイントとauditログを有効化して、書き込み操作の監査／復元フローを整備する。
- 開発者向け：カスタムSkillや拡張を作って社内テンプレートや定型処理を組み込み、Viteでローカル開発→manifestでサイドロードして動作確認する。

参考：リポジトリ／デプロイ手順やセキュリティモデルはREADMEとdocs配下に詳細があるため、導入前に docs/security-threat-model.md を確認してください。
