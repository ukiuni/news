---
layout: post
title: "Parse Me, Baby, One More Time: Bypassing HTML Sanitizer via Parsing Differentials - パースしてもう一度：パーサ差分を突くHTMLサニタイザ回避"
date: 2026-02-25T06:51:28.735Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.ias.cs.tu-bs.de/publications/parsing_differentials.pdf"
source_title: "Parse Me, Baby, One More Time: Bypassing HTML Sanitizer via Parsing Differentials"
source_id: 397234117
excerpt: "ブラウザとサニタイザのパーサ差分を突いてXSSを通す新攻撃手法と対策解説"
---

# Parse Me, Baby, One More Time: Bypassing HTML Sanitizer via Parsing Differentials - パースしてもう一度：パーサ差分を突くHTMLサニタイザ回避
クリック不可避！「ブラウザとサニタイザの“解釈のズレ”」を突いてXSSを通す最新手法

## 要約
HTMLの正規化やサニタイズは「同じ解釈」を前提にしているが、実際はブラウザやライブラリごとにパーサ挙動が異なる。著者らはその差分（parsing differentials）を使ってサニタイザを回避する現実的な攻撃チェーンを示し、多数の実装で実証的な脆弱性を発見した。

## この記事を読むべき理由
多くの日本企業が運用するWebサービスやCMSは外部入力のサニタイズに依存している。サニタイズが破られるとXSSによるセッション乗っ取りやフィッシングが現実化するため、開発者・運用者は「パーサ差分」という見落としやすいリスクを知っておく必要がある。

## 詳細解説
- 基本概念：HTMLサニタイズは入力を解析→無害化→出力の流れだが、解析（パース）仕様が実装間で異なると同一入力が異なるDOMに変わる。攻撃者はサニタイザが安全と見なすがブラウザが別の意味で解釈するようなバイト列を作る。
- 攻撃手法：著者らは差分検出と変異生成（fuzzing）を組み合わせ、サニタイザ通過後にブラウザでアクティブ化するペイロード（属性切り替え、不正なコメント、複数エンコーディングの混在など）を自動探索した。
- 実証結果：複数の実装（サーバー側ライブラリ、フレームワーク、ブラウザ群）で多数の回避パターンを見つけ、実際のサービスでも再現可能なケースを報告している。
- 根本原因：サニタイズが「文字列操作」や独自の簡易パーサで済ませられている点、HTML5準拠のパーサ挙動に合わせた正規化・検証が不十分な点。

## 実践ポイント
- サニタイズは「出力コンテキスト」ごとに行う（HTML本文、属性、JavaScript内、URLなど）。context-aware escapingを徹底する。
- サニタイズ実装はHTML5パーサに準拠したライブラリを使い、出力前にブラウザ実装での表示を検証する（複数ブラウザでのテスト）。  
- 入力の正規化（canonicalization）を行い、エンコーディング・エスケープの混在を避ける。  
- Content Security Policy（CSP）を導入して万が一のXSSを緩和する。  
- 自動化された差分テスト（fuzzing）で自社のサニタイズ処理を定期的に検査する。OWASPの推奨ライブラリや実装例を参考にすること。

この研究は「見えないパーサの違い」が実運用で致命的になり得ることを示しています。まずは利用中のサニタイザがどのパーサ仕様を前提にしているか、そして複数ブラウザでの挙動確認を実施してください。
