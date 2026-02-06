---
layout: post
title: "Show HN: Agent Arena – Test How Manipulation-Proof Your AI Agent Is - エージェント・アリーナ：AIエージェントはどれだけ操作に強いか試す"
date: 2026-02-06T12:56:59.544Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://wiz.jock.pl/experiments/agent-arena/"
source_title: "WIZ - AUTOMATION WIZARD"
source_id: 46911873
excerpt: "Agent Arenaで10種の隠れプロンプト攻撃を即検証し、エージェントの操作耐性を把握"
---

# Show HN: Agent Arena – Test How Manipulation-Proof Your AI Agent Is - エージェント・アリーナ：AIエージェントはどれだけ操作に強いか試す
あなたのAI、見えない“命令”に操られていませんか？即テストできる実験ツールの紹介

## 要約
WIZの「Agent Arena」は、ウェブページに仕込まれた10種の「隠れプロンプト（prompt injection）」攻撃ベクトルを用いて、あなたのAIエージェントがどれだけ騙されるかを簡単に検証できる実験ページです。

## この記事を読むべき理由
日本でも企業のRPAや自動化エージェント、社内チャットボットが増える中、外部コンテンツを自動処理するエージェントは見えない攻撃に脆弱です。本ツールは実践的に脆弱性を暴けるため、現場での安全対策設計に直結します。

## 詳細解説
Agent Arenaの流れ
- 1) テスト用ページをエージェントに読ませて要約させる。
- 2) エージェントの出力をスコアカードへ張り付けると、どの「カナリア句（canary phrase）」に引っかかったかを即判定する。カナリア句は解析まで隠されます。

攻撃ベクトル（10種類）
- HTMLコメント：レンダリングされないがソースに残る命令（Basic）。
- 白背景に白文字（White-on-White）：人間に見えないテキスト（Basic）。
- display:noneのHidden Div：DOM内に隠された命令（Medium）。
- 極小文字（Micro Text）：人間が読み取りにくい極小フォント（Medium）。
- aria-hidden：支援技術向け属性を悪用して情報を埋める（Medium）。
- data属性：data-*属性へ命令を仕込む（Medium）。
- ゼロ幅文字：ゼロ幅Unicodeで命令を埋める（Hard）。
- 画像のalt上書き：装飾画像のaltにシステム命令を挿入（Hard）。
- 画面外配置：数千pxオフスクリーンに置かれたコンテンツ（Hard）。
- マルチレイヤー攻撃：複数手法を組み合わせた高度攻撃（Expert）。

攻撃カテゴリ（概念）
- 視覚的隠蔽（visual hiding）、構造的隠蔽（structural hiding）、意味的隠蔽（semantic hiding）、エンコーディングトリック（encoding tricks）に分類され、どれも“人間の監督下で見落としやすい”のが特徴です。

なぜ効くか
- 自動化エージェントはDOMやテキストをそのまま処理するため、レンダリングで見えない要素やメタデータまで読むと、モデルの指示（system prompt）よりも外部命令を優先してしまうリスクがあります。

## 実践ポイント
- 今すぐ試す：Agent Arenaのテストページへエージェントを送って要約させ、スコアカードで判定する。
- 入力前処理を実装：HTMLコメント除去、display:none除去、ゼロ幅文字の正規化、alt/ariaの検査を行うパイプラインを入れる。
- レンダリング基準で抽出：ユーザーに「見える」テキストのみを抽出して処理する（スクリーンレンダリングを基にした抽出を検討）。
- モデル側の防御：システムプロンプトの強化、外部命令を無視するルール、チェーン・オブ・トラストや検出モデルを導入する。
- ログとヒューマンインループ：疑わしい出力はフラグして人間が確認するワークフローを組む。

Agent Arenaは実戦的かつ手早く脆弱性を可視化できるツールです。まずは自分のエージェントで試し、上に挙げた対策を段階的に導入してみてください。
