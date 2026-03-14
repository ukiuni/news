---
layout: post
title: "Optimizing Content for Agents - エージェント向けコンテンツ最適化"
date: 2026-03-14T03:29:57.235Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://cra.mr/optimizing-content-for-agents/"
source_title: "Optimizing Content for Agents"
source_id: 47372672
excerpt: "エージェント目線でMarkdownを返す最適化実践ガイドで精度向上"
image: "https://cra.mr/ai-content/optimizing-content-for-agents.png"
---

# Optimizing Content for Agents - エージェント向けコンテンツ最適化
エージェントに「読ませる」ためのドキュメント設計術 — 今すぐ始めるべき実践ガイド

## 要約
AIエージェントは人間と同じではないため、ウェブやドキュメントを「エージェント目線」で最適化すると精度と効率が劇的に改善します。Accept: text/markdown などによるコンテンツネゴシエーションが有効です。

## この記事を読むべき理由
日本の開発チームやドキュメント担当者も、社内ボットやCI／自動レビューの普及で「エージェントが読むコンテンツ」の重要性が急増しています。今すぐ実装できる具体策が得られます。

## 詳細解説
- エージェントの振る舞いと制約  
  多くのモデル/エージェントはコンテキストサイズを節約するためファイルの先頭Nバイトだけを読む、あるいは「情報が存在すると明示されている」場合と自力で探索する場合で挙動が大きく変わります。これを理解して設計する必要があります。

- コンテンツネゴシエーションの活用  
  リクエストヘッダ（例: Accept: text/markdown）を見て、機械向けのプレーン／構造化フォーマットを返す。これが「エージェント向け最適化」のフックになります。

- 実例（Sentryのアプローチの要点）  
  1) 真のMarkdownを返す：トークンコスト削減と精度向上。  
  2) ブラウザ専用要素（ナビゲーション、JSなど）を排除。  
  3) インデックスはサイトマップ的にして発見性を高める。  
  4) ヘッドレスアクセス時に認証ページを出さず、MCP/CLI/APIなどのプログラム的入口を明示する。  
  5) エージェントが実行する「スキル」をMarkdownファイルで定義（Wardenのような設計）。  
  これらはMDXやパーサーの調整で実現できます。

## 実践ポイント
- Acceptヘッダで機械判定し、機械向けMarkdown/JSONを返すエンドポイントを用意する。  
- ドキュメントは「先頭に要約＋リンク階層」を置き、重要情報が先に来るようにする。  
- ブラウザ専用UIを取り除いた軽量版を用意し、代わりにMCP/CLI/APIの接続情報を明示する。  
- スキルやチェックリストはMarkdownで公開し、エージェントにそのまま読ませられる形式にする。  
- CIやローカルで動くエージェント向けに、認証フローやアクセス方法（OAuth/トークン/ストリーミング）を整備する。

簡単な判別例（受け取ったAcceptがtext/markdownならMarkdownを返す）:
```bash
# 簡易curl例（エージェントを想定）
curl -H "Accept: text/markdown" https://your.docs.example/
```

まずは既存ドキュメントの先頭を見直し、エージェント向けサブパスを1つ作ることを推奨します。
