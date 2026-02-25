---
layout: post
title: "Lambda World 2019 - Language-Oriented Programming with Racket - Matthias Felleisen - Racketによる言語指向プログラミング（Matthias Felleisen）"
date: 2026-02-25T16:26:48.745Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.youtube.com/watch?v=z8Pz4bJV3Tk"
source_title: "Lambda World 2019 - Language-Oriented Programming with Racket - Matthias Felleisen - YouTube"
source_id: 1380714032
excerpt: "Racketで短期間に業務特化のDSLを設計・実装する方法を学べる講演"
image: "https://i.ytimg.com/vi/z8Pz4bJV3Tk/maxresdefault.jpg"
---

# Lambda World 2019 - Language-Oriented Programming with Racket - Matthias Felleisen - Racketによる言語指向プログラミング（Matthias Felleisen）

現場でさっと作れる「自分専用言語」──Racketで始める言語指向プログラミング入門

## 要約
Racketを使った「言語指向プログラミング（Language-Oriented Programming, LOP）」の考え方と実践手法を紹介する講演で、言語（DSL）を素早く設計・実装・統合するための技術（マクロ、#lang、ツール連携など）を解説します。

## この記事を読むべき理由
DSLは業務ロジックの簡潔化やドメイン専門家との協業に強力です。日本のプロダクト開発や教育現場でも、Racketを使えば短期間で安全なDSLを作り、プロトタイピング〜運用に活かせます。

## 詳細解説
- 言語指向プログラミングとは：ライブラリではなく、目的に特化した小さな言語を作ってコードを表現力豊かにする手法。可読性・保守性・ドメイン表現力が向上する。  
- Racketの強み：言語を第一級として扱う設計。#langによる言語モジュール化、DrRacketなどのIDEサポート、豊富なマクロ（衛生マクロ／syntax objects／syntax-parse）で構文・意味の拡張が安全にできる。  
- マクロの役割：単なるテキスト置換ではなく、構文木レベルで変換するため名前衝突を避け、静的チェックや最適化がしやすい。  
- #langとモジュール：新しい言語をファイル単位で定義でき、既存言語と組み合わせたり、言語レベル（教育用から本番用まで）を切り替えたりできる。  
- ツール連携：REPL、テスト、ドキュメント生成、IDEのエラーメッセージを言語固有にカスタマイズ可能で、言語ユーザー体験を向上させる。  
- 実務上の注意点：DSLは運用コスト（メンテナ、学習コスト）を伴うため、適用範囲を限定しインターフェースを明確にすること。パフォーマンスは最適化手法やバックエンドで補う。

## 日本市場との関連性
- 金融やIoT、ゲーム開発、ビルドツール、業務ルールエンジンなど、ドメインが明確な領域ではDSLの効果が大きい。日本企業のレガシー置換やドメイン知識を持つ現場担当者と協働する場面で有効。  
- 教育分野でもRacketは親和性が高く、プログラミング教育や言語設計の学習教材として導入しやすい。

## 実践ポイント
1. RacketをインストールしてDrRacketで遊んでみる（https://racket-lang.org）。  
2. まずは小さな構文拡張を作る：define-syntax-rule→syntax-parseへと学ぶ。  
3. ファイル単位で言語を作る練習：#langで独自言語を定義し、簡単なパーサ／チェックを実装。  
4. DSLの適用領域を限定し、テストとドキュメントを自動化して運用コストを抑える。  
5. 社内PoCで短期間に価値を示す（サンプルDSLで業務フローを表現し、非開発者の理解を得る）。

オリジナル講演（Matthias Felleisen）はRacketの設計思想と実例が豊富なので、まずは動画を視聴して概観を掴み、上記の順で手を動かすことをおすすめします。
