---
layout: post
title: "Wikipedia volunteers spent years cataloging AI tells. Now there’s a plugin to avoid them. - ウィキペディア志願者がAIの「らしさ」を数年かけて記録。今、それを回避するプラグインが登場"
date: 2026-01-21T16:41:35.782Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://arstechnica.com/ai/2026/01/new-ai-plugin-uses-wikipedias-ai-writing-detection-rules-to-help-it-sound-human/"
source_title: "Wikipedia volunteers spent years cataloging AI tells. Now there&#039;s a plugin to avoid them. - Ars Technica"
source_id: 421189709
excerpt: "ウィキペディアのAI検出を逆手に取るHumanizer登場、事実性は保証されない"
image: "https://cdn.arstechnica.net/wp-content/uploads/2023/10/ai_typewriter_getty-1152x648.jpg"
---

# Wikipedia volunteers spent years cataloging AI tells. Now there’s a plugin to avoid them. - ウィキペディア志願者がAIの「らしさ」を数年かけて記録。今、それを回避するプラグインが登場
「AIっぽさ」を消すプラグインが公開 — ウィキペディアの検出ルールを逆手に取る試み

## 要約
ウィキペディア編集者がまとめた「AIらしさ」の24パターンを、AnthropicのClaude向けプラグイン「Humanizer」が読み込んで出力をより“人間っぽく”する。だが事実性の向上は期待できず、用途次第で弊害もある。

## この記事を読むべき理由
日本でも自動生成コンテンツの利用や検出が話題になる中、検出ルールが「逃れる手引き」に変わる可能性と、その倫理・実務上の影響を押さえておく必要があるため。

## 詳細解説
- 元データ: WikiProject AI Cleanup（ウィキペディアのボランティアグループ）が2025年に公開した、チャットボット特有の文体や表現の観察リストが基になっている（約24項目）。
- ツール: Siqi Chenが公開した「Humanizer」はClaude Codeの“skill file”形式で、Markdownで書かれた指示をプロンプトに付与する。Claudeはこの標準化フォーマットを解釈するよう微調整されている（ただしカスタムスキルは有料プラン・コード実行が必要）。
- 仕組み: リスト化された“AIっぽい”表現（過度に膨らませた形容、観光パンフ調、分析のための形容詞句の付け足し等）を避ける指示を与え、出力を平易で曖昧さを含む“人間らしい”文に誘導する。
- 限界: 事実の正確性は改善しない。むしろ「意見を持て」などの指示は技術文書や厳密なコード生成では誤用を招く恐れがある。また、言語モデルは完全には従わないケースがある。
- 検出の本質: 研究は、人間の文章とLLM文章を確実に区別する一意の特徴は存在しないと示唆する。検出ルールは有用だが観察に基づくもので、誤判定（偽陽性）も発生する。

## 実践ポイント
- ツール試用: Humanizerのようなスキルでトーンや表現を調整するのは有効。ただし事実確認や出典付けは必須。
- 用途に応じた使い分け: 技術ドキュメントや正確性が必須の文章には「人間らしさ」強調は避ける。
- 倫理とルール作り: 検出ルールを悪用して生成物を隠す行為は透明性や信頼を損なう。組織内ガイドラインを整備すること。
- 日本語特有の注意: 英語で有効な「らしさ」指標がそのまま日本語に当てはまらない場合がある。日本語コンテンツ向けには別途観察・検証が必要。
- 参加する: WikiProjectのようなコミュニティの調査に注目・参加し、検出基準や実務的な対策に貢献する。
