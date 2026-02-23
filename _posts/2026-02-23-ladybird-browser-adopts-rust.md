---
layout: post
title: "Ladybird Browser adopts Rust - LadybirdがRustを採用"
date: 2026-02-23T11:42:35.285Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://ladybird.org/posts/adopting-rust/"
source_title: "Ladybird adopts Rust, with help from AI - Ladybird"
source_id: 47120899
excerpt: "AI支援で2週間・2.5万行をRustに移植、テスト回帰ゼロの実績でLadybirdがRust採用"
image: "/assets/img/plant.webp"
---

# Ladybird Browser adopts Rust - LadybirdがRustを採用
AI支援で「2週間・25k行」のLibJS移植を成し遂げた、ブラウザ開発の現場からの決断

## 要約
LadybirdはJavaScriptエンジン（LibJS）の一部をRustへ移植。AI（Claude Code、Codex）を補助に使い、人手で指揮して2週間・約25,000行の変換を完了、テストで互換性・性能ともに回帰ゼロを確認した。

## この記事を読むべき理由
メモリ安全性やセキュリティが重視される今、主要ブラウザ（Firefox/Chromium）に続き小さなブラウザプロジェクトがRust導入を進めた事例は、日本のエンジニアやプロダクト担当にとって実務的な示唆が多いから。

## 詳細解説
- 背景：LadybirdはC++の置き換え候補を長く検討。SwiftはC++相互運用性と非Appleプラットフォームの問題で断念し、成熟したエコシステムと安全性を理由にRustを採用。
- 対象と手法：最初のターゲットはLibJSの「lexer・parser・AST・バイトコード生成器」。test262による広範なテストカバレッジが移植先に適していた。
- AIの役割：Claude CodeとCodexを翻訳補助に使用。自動生成ではなく、移植の方針・順序・コードスタイルは人が決定。数百の小さなプロンプトでAIを誘導し、複数モデルによる敵対的レビューで誤りを潰した。
- 成果：約25,000行のRust化を約2週間で実施。ASTと生成バイトコードはC++版と完全一致。test262（52,898テスト）およびLadybird独自回帰テスト（12,461）がいずれも回帰ゼロ。性能にも悪影響なし。  
- 注意点：初期移植は互換性優先で「C++から翻訳した感」が強く、非イディオマティックなRust。将来的にC++パイプラインを退役させる段階でリファクタを行う計画。プロジェクト全体の主軸は引き続きC++で、Rust化は長期のサイドトラックとして管理される（着手はコアチームと調整必須）。

## 実践ポイント
- Rust学習：所有権・借用・ライフタイムの基礎を押さえる。ブラウザや低レイヤでの恩恵は大きい。  
- テスト戦略：test262のような既存テストスイートで「出力一致」を検証する手順を取り入れる。  
- AI活用法：AIは補助ツールとして「人が設計し、人がレビューする」ワークフローで使うのが現実的。  
- 小さく始める：lexerやparserなど独立性が高くテストのあるモジュールを最初に選ぶ。  
- 関与・連携：オープンソースプロジェクトに貢献する際はコアチームと方針をすり合わせる（無駄な作業を避けるため）。

（参考）Ladybirdの方針：当面はC++とRustの共存を継続し、段階的に移行。プロジェクトは移植時の互換性と安全性を最優先している。
