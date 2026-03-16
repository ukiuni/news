---
layout: post
title: "Comparing Python Type Checkers: Typing Spec Conformance - Python型チェッカー比較：Typing仕様への準拠"
date: 2026-03-16T13:39:22.707Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://pyrefly.org/blog/typing-conformance-comparison/"
source_title: "Python Type Checker Comparison: Typing Spec Conformance | Pyrefly"
source_id: 382541541
excerpt: "仕様準拠率で主要Python型チェッカーを比較し、実務での誤検出や選定のコツを具体的に解説"
image: "/img/Pyrefly-Preview-Symbol.png"
---

# Comparing Python Type Checkers: Typing Spec Conformance - Python型チェッカー比較：Typing仕様への準拠
Python型チェッカーの「仕様準拠度」で比べると、実務でのストレスが減るかもしれません — どれを選ぶべきかを分かりやすく整理しました。

## どの型チェッカーが“仕様通り”動く？Python型チェックの実力判定

## 要約
Pythonの型仕様（typing spec）には公式の準拠テストがあり、主要な型チェッカーはその合格率で比較できます。準拠率は重要指標ですが、推論やIDE統合など他の要素も評価に入れるべきです。

## この記事を読むべき理由
型注釈を増やす日本の開発現場では、型チェッカー選定が開発効率や外部ライブラリの導入に直結します。仕様準拠の違いは、思わぬ型エラーや回避策のコストにつながるため、選定判断に役立ちます。

## 詳細解説
- 背景：PEP 484以降、mypy実装が事実上の仕様を担ってきましたが、Pyright、Pytype、Pyreなど複数のツール登場とともに仕様を一本化する「typing specification」と準拠テストスイートが整備されました。
- 準拠テスト：およそ100ファイルのテストがあり、各行に「エラー期待／非期待」を注釈。実行結果は「合格」「誤検出（False positive）」「見逃し（False negative）」で評価されます。
  - 誤検出（False positive）：仕様上OKなコードをエラー扱いする（例：TypedDictのextra_itemsを未対応で余剰キーを誤判定）。
  - 見逃し（False negative）：仕様で禁止されているケースをエラーにしない（仕様を守れていない）。
- スナップショット（2026年3月初旬の例）：
  - Pyright: 136/139 (97.8%) — FP 15 / FN 4  
  - Zuban: 134/139 (96.4%) — FP 10 / FN 0  
  - Pyrefly: 122/139 (87.8%) — FP 52 / FN 21  
  - mypy: 81/139 (58.3%) — FP 231 / FN 76  
  - ty: 74/139 (53.2%) — FP 159 / FN 211  
  ※ツールは活発に更新されており数値は変動します。
- 注意点：準拠度は「仕様に従う・従わない」の指標であって、実務で重要な以下の点は計測対象外です。
  - 型推論の精度（注釈がない箇所での挙動）
  - 型の絞り込み（narrowing）やTypeGuardなどの実用的パターン対応
  - パフォーマンス、IDE統合、エラーメッセージの分かりやすさ、DjangoやPydanticといったサードパーティ対応

## 実践ポイント
- まずは自分のコードベースで主要ツール（pyright/mypy/pyrefly等）を試運用して、実際に出るエラーの傾向を比較する。  
- ライブラリ依存が強いプロジェクト（Django、Pydantic、NumPy等）は、対象ライブラリのサポート状況を重視する。  
- 高度なtyping機能（TypedDictの設定、交差型、否定型など）を使うなら、仕様準拠度が高いツールを優先検討する。  
- CIに入れて検出・抑制ルールを運用し、誤検出が多い場合はツールの設定や代替ツールを検討する。

短期的には「何が出るか」を見て選び、長期的には推論品質・IDE体験・エコシステム対応を総合評価してください。
