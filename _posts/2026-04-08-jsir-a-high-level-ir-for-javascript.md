---
layout: post
title: "JSIR: A High-Level IR for JavaScript - JavaScript向け高レベル中間表現「JSIR」"
date: 2026-04-08T02:38:30.490Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://discourse.llvm.org/t/rfc-jsir-a-high-level-ir-for-javascript/90456"
source_title: "[RFC] JSIR: A High-Level IR for JavaScript - MLIR - LLVM Discussion Forums"
source_id: 47683376
excerpt: "ASTをほぼ無欠損で保持するJSIRで高度解析・復元や最適化が可能に"
image: "https://us1.discourse-cdn.com/flex021/uploads/llvm/original/3X/a/5/a5e2f18e2787b0f7493d9aa43cc2f4d488794c53.png"
---

# JSIR: A High-Level IR for JavaScript - JavaScript向け高レベル中間表現「JSIR」
魅せるJS解析の新基盤——ASTを丸ごと保持する「JSIR」でソース変換と解析がもっと楽になる

## 要約
JSIRはASTの情報をほぼ完全に保持しつつ、MLIRの領域（regions）で制御フローを表現し、実用的なデータフロー解析APIを備えた高レベルのJavaScript向けIRです。Googleで実運用され、ソース⇄AST⇄IRの高忠実度ラウンドトリップを目指します。

## この記事を読むべき理由
- BabelやClosureの次の世代ツールとして、ASTベースでは難しい高度な解析・変換が可能になるため、トランスパイラや最適化、難読化解除など日本の開発現場でも直接恩恵があります。  
- MLIR上に作られた設計は学術・実務双方で注目度が高く、言語ツールチェーンの新潮流を知るうえで有益です。

## 詳細解説
- 設計方針：JSIRはESTreeに対応する1対1マッピングを目標にし、元ソース情報を失わずにIRへ落とし込む（＝ロスレスなラウンドトリップを目指す）。  
- 構造表現：各種制御構造（if/while/論理式など）を専用のopで表し、ネストブロックはMLIRのregionで保持するため、制御フローの意味がそのまま残る。whileの条件がregionになる等、評価タイミングに応じた表現差がある点も特徴。  
- 値の扱い：識別子をl-value（参照）とr-value（値）で区別することで代入や副作用の意味を明確にする。  
- データフロー：MLIR上の分析APIを拡張して使いやすいラッパー（JsirDataFlowAnalysis等）を提供。状態変更の伝播や疎/密状態の扱いを簡潔化しており、独自のWorklist管理など使い勝手改善が盛り込まれている。  
- 実運用例：GoogleではHermesのバイトコードからJSへの復元（decompilation）や、LLMと組み合わせた難読化解除などに利用されている。  
- MLIRコミュニティへの貢献：JSIRは「MLIRで高レベル言語のASTを表現できる」ことを示す試金石であり、シンボルテーブルやメモリ効果、データフローAPIの改善を通じて上流にフィードバックを意図している。

簡単なJSIR例（式のポストオーダー表現）:
```mlir
%1 = jsir.numeric_literal {1}
%2 = jsir.numeric_literal {2}
%1_plus_2 = jsir.binary_expression {'+'} (%1, %2)
%3 = jsir.numeric_literal {3}
%sum = jsir.binary_expression {'+'} (%1_plus_2, %3)
jsir.expression_statement (%sum)
```

## 実践ポイント
- まずリポジトリを確認：github.com/google/jsir をクローンしてREADMEと中間表現定義を読む。  
- 小さな変換から試す：AST→JSIR→ASTのラウンドトリップで元ソースが戻るか確認する（サンプルで99.9%成功と報告）。  
- データフロー解析を作る：JsirDataFlowAnalysisのベースクラスを使い、簡単な定数伝播や到達定義解析を実装してみる。  
- 日本向けユースケース：バンドル/最適化プラグイン、Web向け難読化解除ツール、社内コード解析パイプラインへの組込みを検討する。
