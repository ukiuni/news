---
layout: post
title: "TypeScript inventor Anders Hejlsberg calls AI \"a big regurgitator of stuff someone else has done\" but still sees it changing the way software dev is done and reshaping programming tools - TypeScriptの生みの親が語る「AIは既存の再利用者」だが、それでも開発とツールを変える"
date: 2026-01-29T09:16:05.736Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://devclass.com/2026/01/28/typescript-inventor-anders-hejlsberg-ai-is-a-big-regurgitator-of-stuff-someone-has-done/"
source_title: "TypeScript inventor Anders Hejlsberg: AI is &#039;a big regurgitator of stuff someone has done&#039; &#8226; DEVCLASS"
source_id: 415877298
excerpt: "TypeScript創始者が語るAIの限界とGo移植が示す開発ツール革新"
image: "http://devclass.com/wp-content/uploads/2026/01/anders_hejlsberg.jpg"
---

# TypeScript inventor Anders Hejlsberg calls AI "a big regurgitator of stuff someone else has done" but still sees it changing the way software dev is done and reshaping programming tools - TypeScriptの生みの親が語る「AIは既存の再利用者」だが、それでも開発とツールを変える

TypeScriptの父が語る、AI時代の“言語・コンパイラ移行”と「ツールの劇的な変化」

## 要約
TypeScript創始者のAnders Hejlsbergは、AIを「既存の蓄積を再出力するもの」と評しつつ、AIが開発ツールや言語サービスを劇的に変えると予測。TypeScript 7でのネイティブコンパイラ移植（Go採用）やAIの活用実例・限界について率直に語っています。

## この記事を読むべき理由
TypeScriptやJavaScriptは日本のウェブ/フロント開発で中心的存在。コンパイラの大幅改修やAIの実務的な使い方・注意点は、日本の開発現場やツール選定に直接影響します。

## 詳細解説
- ネイティブコンパイラ移植の背景  
  TypeScript 7では、従来のTypeScript製コンパイラ（V8上のJS実行）をネイティブ実装に移すことで実行速度を約10倍化。実装は既存の型チェッカの厳密な振る舞いを保つため「関数単位での逐次移植」を選択し、結果の差異を避けています。

- 言語選定（Go採用）の理由  
  移植要件（循環データ構造、GCの必要性）からRustは不適、C#も検討されたが最終的にGoが選ばれました。互換性や実装の忠実性を優先した判断であり、C#コミュニティからは賛否が出ました。

- AIの現実的な役割と限界  
  HejlsbergはAIを「既存の成果物を再利用して多少の推論をするもの」と評し、半ミリオン行規模の厳密な移植をAIに丸投げするのは危険だと指摘。AIは「翻訳で誤記（hallucination）が出る」ため、決定的な移植には不向き。一方で、移植後の新しいプルリクの自動移行や、言語サービス（シンタックスチェックや修正提案）の強化など、補助的・自動化ツールとしては既に有効に使われています。

- ツールチェンジの本質  
  大きな言語仕様の改変よりも、IDEや言語サービスの「AI化」が開発フローを変えると予測。IDEは「AIを監督する場」へと進化し、LLMやエージェント的な手法で意味的質問やリファクタを行う方向が重要になります。

- 歴史的メモ  
  TypeScript誕生はOutlook WebチームのScript#運用にヒントを得たもので、「既存のJavaScriptを拡張して壊れている点を直す」アプローチが根底にあります。

## 実践ポイント
- AIに丸投げしない：大規模で厳密なコード移行はAI単独では危険。AIは補助ツールや移行補助プログラム生成に使う。  
- ツール連携を整備する：言語サーバー/LSPや「MCP的」サービス（言語サービスとAIの接続）を導入し、AIに意味情報を渡せるようにする。  
- PR自動化にAIを活用：移植後の小規模なPRマイグレーションやテンプレート生成には効果的。導入でレビュー負荷を下げられる。  
- 言語・ランタイム選定の観点：パフォーマンスやGC/データ構造要件がある場合、実装言語の選択がプロジェクト全体に影響する点を意識する。  
- 学習投資：TypeScript自体の大改変は期待薄。むしろAI対応の開発ツールや言語サービスの使いこなしが差を生みます。

短く言えば、AIは便利だが“チェック可能な確実性”を求められる場面では人間主導の設計と検証が不可欠。日本の現場でも、ツールとプロセスの整備が今後の競争力を左右します。
