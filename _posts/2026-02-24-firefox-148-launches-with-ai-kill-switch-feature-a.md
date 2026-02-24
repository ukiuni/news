---
layout: post
title: "Firefox 148 Launches with AI Kill Switch Feature and More Enhancements - Firefox 148、AIキルスイッチ搭載で登場（その他多数の改善）"
date: 2026-02-24T07:12:23.692Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://serverhost.com/blog/firefox-148-launches-with-exciting-ai-kill-switch-feature-and-more-enhancements/"
source_title: "Firefox 148 Launches with Exciting AI Kill Switch Feature and More Enhancements! - ServerHost Hosting Solutions Blog"
source_id: 47133313
excerpt: "AIを恒久無効化できるFirefox 148で運用・プライバシーとXSS対策を強化"
---

# Firefox 148 Launches with AI Kill Switch Feature and More Enhancements - Firefox 148、AIキルスイッチ搭載で登場（その他多数の改善）

魅力的タイトル: AIを完全オフできるFirefox 148――プライバシー重視の新機能と実務で使える強化点まとめ

## 要約
Firefox 148は「AIキルスイッチ」でAI機能を恒久的に無効化できるほか、リモート更新の制御、XSS対策APIの導入、スクリーンリーダーの数式対応など実務的な改善を多数含むアップデートです。

## この記事を読むべき理由
プライバシーや企業ポリシーを重視する日本の開発者・利用者にとって、AI機能の恒久的な無効化や更新制御は運用・セキュリティ面で即効性のある改善です。国内で増える多言語対応やアクセシビリティ要件にも直結します。

## 詳細解説
- AIキルスイッチ: 設定(Settings) > AI Controls で「Block AI Enhancements」をONにすると、チャットプロンプトやAI生成のリンク要約などAI関連機能を無効化。オフにした選択は今後の更新で上書きされないと明言されているため、企業のポリシー運用に適する。
- 選択的ブロック: 完全無効化の代わりに、オンデバイス翻訳のようにローカルで完結する機能は残し、クラウド依存のAIだけ遮断する設定が可能。
- リモート更新制御: Settings > Privacy & Settings > Firefox Data Collection からリモート更新の挙動を制御しつつ、データ収集は最小化できる。
- セキュリティAPI: Trusted Types API と Sanitizer API を採用。これらは危険なHTML/スクリプト挿入を抑え、クロスサイトスクリプティング（XSS）攻撃のリスクを減らすためのブラウザ側の防御機能。
- アクセシビリティと多言語: PDF内の数式をスクリーンリーダーで読み上げやすくした改善、Windows 10向けのFirefox Backup有効化、ベトナム語・繁体字中国語の翻訳サポート追加。
- その他: 新しいコンテナタブに壁紙表示、WebGPU向けにService Workerサポート追加など開発者向けの基盤強化。

## 実践ポイント
- 今すぐAIを完全にオフにする: Firefoxを148に更新 → Settings > AI Controls → Block AI Enhancements を有効化。
- 部分的に許可したい場合: 選択的ブロックで「オンデバイス翻訳」などローカル処理のみ許可する。
- 企業運用: リモート更新のポリシーを見直し、Settings > Privacy & Settings > Firefox Data Collection で収集を最小化・更新挙動を設定。
- セキュリティ対策: Trusted Types／Sanitizer対応を活用するため、既存ウェブアプリの輸入HTMLやDOM操作箇所を点検する。
- アクセシビリティ対応: PDF内数式の読み上げが必要なユーザーがいる場合は、最新版に更新して動作確認を行う。

公式リリースノートを確認して自環境での影響範囲を評価することをおすすめします。
