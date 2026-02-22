---
layout: post
title: "Writing Helper — open source grammar checker using Rust→WASM and Chrome's local AI (zero cloud calls) - Rust→WASMとChromeローカルAIで動くオープンソース文法チェッカー（クラウド不要）"
date: 2026-02-22T12:30:50.313Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/ravigadgil/writing-helper"
source_title: "GitHub - ravigadgil/writing-helper: This is a plugin which help in writing in chromium based browser."
source_id: 399461465
excerpt: "完全ローカルで動くRust→WASM×Chrome内蔵AIの高速プライバシー重視文法チェッカー"
image: "https://opengraph.githubassets.com/e6b58cce99352d73af45a3694b9da4a59c57741316621e90cddaf65d41a1ab11/ravigadgil/writing-helper"
---

# Writing Helper — open source grammar checker using Rust→WASM and Chrome's local AI (zero cloud calls) - Rust→WASMとChromeローカルAIで動くオープンソース文法チェッカー（クラウド不要）

魅力的なタイトル: 完全ローカルで動く“Grammarly代替”──Rust→WASMとChrome内蔵AIでプライバシー重視の文章校正を手元で

## 要約
Writing HelperはRust製の文法エンジンをWASM化し、ChromeのローカルAI（Gemini Nano）と組み合わせて動くChrome拡張。すべてローカル実行でクラウドに送信せず、綴り・文法・スタイルの指摘とAIによるリライトを提供する。

## この記事を読むべき理由
個人情報や機密文をクラウドに出せない日本の開発者・ライターや、英語ドキュメントの品質を高速に改善したい人にとって、データを外に出さない点と拡張性（カスタムルール追加）が大きな魅力になるため。

## 詳細解説
- コア技術：Harper.js（Rustで書かれた文法エンジン）をWASMで読み込み、ブラウザ内で即時にLintを実行。さらに50以上の正規表現ベースのカスタムルールと約250のよくある綴り誤り辞書で補強する。  
- 二段階パイプライン：Phase 1はHarper＋カスタムルールで約50msで即時表示。Phase 2はオフスクリーンドキュメント経由でChrome内蔵のGemini Nanoを呼び、200–2000msで説明付きのAIリントやリライト結果を追加する（AI機能は任意）。  
- UI/レンダリング：textarea/inputはミラーディブオーバーレイ、contenteditableはRange APIで下線を正確に描画。下線色でカテゴリを判別（赤=綴り、青=文法、琥珀=スタイル、紫=AI）。クリックで提案表示、Tabで一括修正。  
- プライバシーと要件：AI機能を使わなければ完全オフラインで動作。AIを使う場合はChrome 137–141以上と高めのローカルリソース（例：GPU 4GB VRAM または CPU 16GB RAM、22GB空き）を推奨。  
- 拡張性：src/background/custom-rules.jsに新ルールを追加でき、npm run buildで再構築。OSSなので組織ルールや用語集の反映が容易。

## 実践ポイント
- すぐ試す：最新リリースのZIPをダウンロード→chrome://extensions で「デベロッパーモード」→「パッケージ化されていない拡張機能を読み込む」で展開フォルダを指定。  
- 開発・カスタム化：git clone → npm install → npm run build。custom-rules.jsに独自ルールや業務用の単語を追加して再ビルド。  
- 活用例（日本の現場向け）：社内英語メールや技術ドキュメントのドラフトチェックに最適。個人情報やAPIキーを外部に出せない契約書や顧客対応文書にも有効。  
- 注意点：現状は英語向けのルールが中心のため日本語校正は限定的。日本語対応を進めるにはカスタムルールや別エンジンの組み込みが必要。

以上。興味があれば、導入手順やcustom-rulesの具体的な書き方を次に案内しますか？
