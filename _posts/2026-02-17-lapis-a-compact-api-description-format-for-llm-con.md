---
layout: post
title: "LAPIS: A compact API description format for LLM context windows (80% fewer tokens than OpenAPI) - LAPIS：LLMコンテキスト用のコンパクトなAPI記述フォーマット（OpenAPIより80%少ないトークン）"
date: 2026-02-17T22:08:59.777Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/cr0hn/LAPIS"
source_title: "GitHub - cr0hn/LAPIS: Lightweight API Specification for Intelligent Systems"
source_id: 439199958
excerpt: "OpenAPIを.lapis化してLLMトークンを約80%削減、コストと誤認を劇的に減らす"
image: "https://opengraph.githubassets.com/ffe8de2b4c4206b5aa817389dc25731f7ea5ddc7874c6f3c0b09feab4ab91cfd/cr0hn/LAPIS"
---

# LAPIS: A compact API description format for LLM context windows (80% fewer tokens than OpenAPI) - LAPIS：LLMコンテキスト用のコンパクトなAPI記述フォーマット（OpenAPIより80%少ないトークン）

コンテキストをスリム化してLLMコストを激減：LAPISでAPIを「LLM向け最適化」する方法

## 要約
LAPISはOpenAPIと同等の意味情報を保ちながら、LLMに与えるAPIの文脈を最大約80%削減する軽量フォーマット。LLMを使うアプリでトークンコストと誤解を減らし、推論精度を上げることを目的としています。

## この記事を読むべき理由
日本のSaaS／FinTech／チャットボット開発では、LLM呼び出しが増えるほどトークンコストが重くなります。LAPISを導入すれば、毎日の大量API呼び出しでのコスト削減、応答精度向上、限られたコンテキスト領域の有効活用が期待できます。

## 詳細解説
- 問題点：OpenAPIはドキュメント・コード生成向けに設計されており、ネストや重複が多くLLMコンテキストを無駄に消費する（例：ある中規模APIでOpenAPI YAMLは約6,500トークン）。  
- 解決策：LAPISは「LLMネイティブ」な記述スタイルで、同等情報を保持しつつトークンを削減（例：LAPISで約1,500トークン、約80%削減）。  
- 文法と構成：LAPIS文書は最大7セクション（[meta],[types],[ops],[webhooks],[errors],[limits],[flows]）を持ち、関数シグネチャ風の簡潔な記述で型・操作・フローを表現します。  
- 主要機能：
  - 中央集約されたエラー定義により重複を排除。
  - フロー記述（operationsの連鎖やウェブフックのトリガ条件）を明示化。
  - オプション／デフォルト／列挙／配列などを簡潔に表現。+paginatedや+idempotentなどの操作修飾子をサポート。
- 運用上の位置づけ：LAPISはOpenAPIの代替ではなく「LLM向けの変換ターゲット」。ドキュメントやテストはOpenAPIをソース・オブ・トゥルースとして残し、LLMには.lapisを渡すワークフローを推奨します。  
- ツール群：ブラウザ上のオンラインコンバータ（specをドラッグ＆ドロップで変換）、CLI（pipで lapis-spec を導入して変換）、VS Code用シンタックス拡張などが提供されています。  
- 仕様・ライセンス：v0.1相当の仕様で、OpenAPI→LAPISの自動変換ルールやEBNF文法が公開。CC BY 4.0で利用可能。

## 実践ポイント
- まずは試す：オンラインコンバータで既存のOpenAPIを.lapisに変換し、LLMプロンプト内での挙動とトークン差を測る。  
- 運用ルール：OpenAPIはそのまま維持。LLM向け配布は.lapisを生成して使う（CIで自動生成するのが理想）。  
- コスト試算：大量のLLM呼び出しがある場合、トークン80%削減は実運用コストに直結するため短期的にROIが見込める。  
- ツール導入：社内CIに lapis-spec を組み込み、VS Code拡張で編集・レビューしやすくする。  
- 注意点：仕様はまだ初期（breaking changesの可能性あり）。本番導入前に変換結果の検証と回帰テストを必ず行う。

（元リポジトリ：cr0hn/LAPIS — オンラインコンバータや仕様、ツール類が公開されています）
