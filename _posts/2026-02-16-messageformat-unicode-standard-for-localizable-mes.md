---
layout: post
title: "MessageFormat: Unicode standard for localizable message strings - ローカライズ可能なメッセージ文字列のためのUnicode標準"
date: 2026-02-16T11:00:12.632Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/unicode-org/message-format-wg"
source_title: "GitHub - unicode-org/message-format-wg: Developing a standard for localizable message strings"
source_id: 47033328
excerpt: "MessageFormat 2.0が国際化を標準化、翻訳・実装の互換性と効率化を実現"
image: "https://opengraph.githubassets.com/dd8821e2984a28fc9fe4f929f9d67485f8b23a9bf071274a49ca6fa0b3d743de/unicode-org/message-format-wg"
---

# MessageFormat: Unicode standard for localizable message strings - ローカライズ可能なメッセージ文字列のためのUnicode標準
魅せる多言語表示を標準化する「MessageFormat 2.0」が実装の鍵に — 国際化（i18n）を次のレベルへ導く新基準

## 要約
Unicode の MessageFormat ワーキンググループが、プログラム的に安全で相互運用可能な「ローカライズ用メッセージ表現」の標準（MessageFormat / TR35）を策定。複雑な複数形、性別、語形変化、スピーチ出力などを扱いやすくすることが目的。

## この記事を読むべき理由
グローバル対応する日本のプロダクトでは、翻訳作業の効率化や表示の一貫性が直接 UX／運用コストに直結する。MessageFormat を理解すると、翻訳者とエンジニアの連携改善や既存 ICU ベース実装からの移行判断に役立つ。

## 詳細解説
- 背景: MessageFormat は CLDR（Unicode のロケールデータ）と連携し、メッセージの構文・データモデル・処理方法を標準化する取り組み。TR35 に準拠した「MessageFormat 2.0」として安定化済み（編集用リポジトリは GitHub で公開）。
- 目的: 翻訳者が意味を保ちながら、数値・日付・単位・性別・語形変化などロケール依存の表現を安全に扱えるようにする。UI フレームワークやランタイムが共通仕様で実装できることで互換性が向上する。
- 技術ポイント:
  - 構文とメッセージデータモデルを規定し、フロー言語（fluent）風の表現をサポート。
  - 複数形（plural）、選択（select）、性別や語尾変化のハンドリング、カスタム関数（u: namespace）などを規定。いくつかはドラフト段階でフィードバック待ち。
  - 旧 ICU 組み込みの機能を置き換える目標（互換性と拡張性の両立）。
- コミュニティと貢献: 実装報告やバグ、要望を歓迎。参加には CLA（Contributor License Agreement）登録が必要な点に注意。

短い例（MessageFormat の典型的な複数形の書き方）:
```javascript
const msg = "{count, plural, =0{項目はありません} =1{項目が1件あります} other{項目が#件あります}}";
```

## 実践ポイント
- まずは既存ライブラリ（MessageFormat 対応版）を試し、アプリの多言語メッセージを置き換えてみる。  
- ICU ベース実装から移行する場合は互換性テストを用意し、u: 名前空間などドラフト機能は慎重に扱う。  
- 翻訳チームとテンプレート構文を共有し、ローカルテスト（日本語の敬体／敬語、助数詞など）を行う。  
- フィードバックや困りごとは GitHub リポジトリに issue 提出、あるいはメーリングリスト参加で貢献可能。CLA 要件を事前確認すること。
