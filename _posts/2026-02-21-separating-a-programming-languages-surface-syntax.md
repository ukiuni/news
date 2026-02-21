---
layout: post
title: "Separating a programming language's surface syntax from its semantic core: a multilingual interpreter approach - プログラミング言語の表層構文を意味論コアから分離する：多言語インタプリタの試み"
date: 2026-02-21T13:10:46.426Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://substack.com/@jsamwrites/note/p-188589806"
source_title: "One Program. Many Human Languages. One Semantic Core."
source_id: 400297906
excerpt: "多言語フロントで同一セマンティック核を共有し、英語以外でそのまま動くプログラムを実現する実験"
image: "https://substackcdn.com/image/fetch/$s_!4aBz!,w_1200,h_675,c_fill,f_jpg,q_auto:good,fl_progressive:steep,g_auto/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd5f6b9d8-83a2-479b-8def-23021dbe60af_1536x1024.png"
---

# Separating a programming language's surface syntax from its semantic core: a multilingual interpreter approach - プログラミング言語の表層構文を意味論コアから分離する：多言語インタプリタの試み
英語以外の言語で「そのまま動く」プログラムを作る──LLM時代に刺さる多言語フロントエンド実験、multilingualの全体像。

## 要約
同じ意味論コア（ASTと実行パイプライン）に対して、英語・日本語・フランス語など複数の自然言語を表層構文として載せ替えられるインタプリタのプロトタイプ。キーワード置換ではなく、同一の解析～実行パイプラインを共有する点が特徴。

## この記事を読むべき理由
- LLMで「自然言語→コード」の流れが増える中、出力されるコードの言語が利用者の理解性に直結するため。  
- 日本語話者が読み書きしやすいコード表層を持てば教育・現場の効率が上がる可能性がある。

## 詳細解説
- 基本設計：1つのセマンティックコア（ASTと実行チェーン）を固定し、複数の自然言語フロントエンド（トークナイザ／パーサの表層）を重ねる。パイプラインは lexer → parser → semantic checks → Python codegen → runtime を共通化。  
- 追加方式：言語追加はパーサを書き直すのではなく、キーワード・フレーズ登録データを追加する方式。単語単位だけでなく「句レベルの別表現」もサポートする。  
- サポート言語：英語・フランス語・スペイン語・ドイツ語・イタリア語・ポルトガル語・ヒンディー語・アラビア語・ベンガル語・タミル語・簡体字中国語・日本語など。RTL（右→左）言語にも配慮。  
- 実例（英語／仏語）：
```python
# English
let a = 10
let b = 3
print("a + b =", a + b)

# French
soit a = 10
soit b = 3
afficher("a + b =", a + b)
```
- 現状の限界：文法は「Python形」のままなので、語順・膠着語や動詞末尾言語で自然さが限定される。標準ライブラリ名はPython準拠のまま。完全な文法的自然さは未解決の研究課題。  
- Vibecodingとの関係：LLMが自然言語で要求を受け取りコードを生成する際、出力表層が利用者の言語に即していれば生成物の「所有と理解」が高まる。翻訳ステップを挟まず直接その言語で実行できる点が革新。

## 実践ポイント
- すぐ試す：multilingualのREPLで言語切替を試し、生成されるPythonコードを確認する（GitHub: https://github.com/johnsamuelwrites/multilingual）。  
- 教育利用：日本語話者の初学者向けにキーワードを日本語で提示し、学習の心理的障壁を下げられるか検証する。  
- Vibecoding統合：普段使っているLLMワークフローに「出力をmultilingualの表層で生成」するプロンプトを組み込み、読みやすさを評価する。  
- 貢献案：表層フレーズ辞書やIDEプラグイン（日本語対応）を作ってコミュニティに寄与する。

短評：思考とコードの言語的距離を縮める実験で、教育・LLM統合・多言語チームの生産性に直接効く可能性が高い。興味があればREPLを触ってみることを勧める。
