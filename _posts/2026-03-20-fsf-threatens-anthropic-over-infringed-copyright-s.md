---
layout: post
title: "FSF Threatens Anthropic over Infringed Copyright: Share Your LLMs Freel - FSF、Anthropicを著作権侵害で牽制：「LLMは自由に共有せよ」"
date: 2026-03-20T07:14:01.994Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.fsf.org/blogs/licensing/2026-anthropic-settlement"
source_title: "The FSF doesn't usually sue for copyright infringement, but when we do, we settle for freedom &mdash; Free Software Foundation &mdash; Working together for free software"
source_id: 47403905
excerpt: "FSF、Anthropicへ著作権問題で訓練データ・モデルの完全公開を要求"
---

# FSF Threatens Anthropic over Infringed Copyright: Share Your LLMs Freel - FSF、Anthropicを著作権侵害で牽制：「LLMは自由に共有せよ」
LLMの“黒箱訓練”に待った—著作権団体が求めるのは賠償ではなく「モデルの自由」だ

## 要約
FSF（Free Software Foundation）は、AnthropicがLibGenなどから取得した書籍をLLM訓練に用いた件での集団訴訟の和解通知を受け、著作権がFSF保有の作品にも及んでいるとして、金銭の代わりに「ユーザーの自由（完全な訓練データ・モデル・設定・ソースの公開）」を求める姿勢を明確にしました。

## この記事を読むべき理由
日本の開発者や企業も海外データやスクレイピングで学習データを収集することが多く、今後のLLM運用・配布ルールや事業リスクに直結するため、法的・倫理的な観点から早めに知っておくべきテーマです。

## 詳細解説
- 事件の背景：Bartz v. Anthropicは、LibGenやPirate Library Mirrorなどからダウンロードした書籍をLLM訓練に使ったことが著作権侵害に当たるかを争う集団訴訟。地区裁判所は「学習利用そのものはフェアユースと判断」した一方で、「ダウンロード自体の合法性」は審理の余地を残しました。結果として、当事者は裁判を待たず和解の道を選んでいます。  
- FSFの立場：FSFはGNUプロジェクトや書籍（例：Free as in Freedom）で著作権を保有し、GNU FDLの下で配布しています。GNU FDLは無償かつ自由な利用を許すライセンスのため、金銭補償より「ソフトウェア/データ/モデルの自由」を求めるのが筋だと主張しています。具体的には、訓練に使った完全な入力データ、学習済みモデル本体、訓練設定、ソースコードまでユーザーに開示・自由配布すべきだという要求です。  
- 意味するところ：訓練データの出所やライセンスが不明確なまま商用モデルを提供すると、法的リスクだけでなくコミュニティからの信頼失墜や再利用制約が生じる可能性があります。FSFの主張は、著作権侵害問題の解決策として「透明性と自由」を提示しており、モデルのブラックボックス化を正当化しません。

## 実践ポイント
- データ調達前にライセンス確認を必須化する（商用利用や再配布条項をチェック）。  
- 外部LLMを導入する際は、訓練データの出所とライセンス情報、モデルの公開ポリシーをベンダーに要求する。  
- 社内・自社でモデルを訓練する場合は、オープンかライセンス許諾済みデータを優先し、メタデータを記録する（プロビナンス管理）。  
- コミュニティ貢献：自由ライセンスのコーパスやデータ整備に参加すると、長期的なエコシステムの安定化につながる。  
- 法務リスクを低減するため、重大な公開前に法務チェックと外部助言を得る。

短期的には「透明性を要求する習慣」を社内外で作ることが、日本のプロダクトや研究開発を守る最も実践的な対策です。
