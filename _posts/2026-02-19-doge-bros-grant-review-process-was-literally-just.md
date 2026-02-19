---
layout: post
title: "DOGE Bro’s Grant Review Process Was Literally Just Asking ChatGPT ‘Is This DEI?’ - DOGE系が助成金査定をChatGPTの「これDEI？」だけで決めていた"
date: 2026-02-19T19:14:53.400Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.techdirt.com/2026/02/19/doge-bros-grant-review-process-was-literally-just-asking-chatgpt-is-this-dei/"
source_title: "DOGE Bro’s Grant Review Process Was Literally Just Asking ChatGPT ‘Is This DEI?’"
source_id: 438904632
excerpt: "ChatGPTの一行判定でNEHの人文学助成が大量打ち切り、DEI基準丸投げの衝撃実態"
---

# DOGE Bro’s Grant Review Process Was Literally Just Asking ChatGPT ‘Is This DEI?’ - DOGE系が助成金査定をChatGPTの「これDEI？」だけで決めていた
チャットボットの一行判定で米国の人文学助成金が次々打ち切られた衝撃の実態

## 要約
米国のNEH（国立人文科学基金）で、DOGE系の担当者が助成金の「DEI（多様性・公平性・包含）」該当性を判断するために、ChatGPTに短文で判定させ、その結果を元に多くの助成金を即時打ち切っていたことが裁判資料で明らかになった。

## この記事を読むべき理由
AIを現場運用に使う流れは日本でも進んでいる。だが定義不明な基準と単一のLLM出力に依存すると、公的意思決定や研究支援が簡単に誤用される危険がある点を、技術者・管理者ともに理解しておく必要がある。

## 詳細解説
- 手法：担当者が各助成申請の短い説明文をChatGPTに投げ、命令は「DEIに関係するか？120文字以内で、'Yes.'か'No.'で始めよ」という一行プロンプト。返答のみで「終わり」と判断。
- 検出ワード：事前に作成した検出リスト（例：LGBTQ、BIPOC、tribal、immigrants等）を照合し、該当ワードがある申請を重点的にChatGPTへ投入。対称語（white, heterosexualなど）はリストに含まず、バイアスを助長。
- 問題点：
  - 「DEI」の定義をプロンプト内で明確化せず、モデル解釈に丸投げしている（仕様不在）。
  - 出力は短文で根拠やソースがなく、誤判定や誇張を検証できない。
  - 専門職員が訂正・介入する機会を制限、さらに通知は私的メールサーバと署名偽装の疑いありという運用面の問題。
  - 結果として人文・歴史研究や少数者の記録を扱う正当な研究が多数「DEI」として除外された。
- 技術的含意：LLMは分類器として使えるが、明確な定義・ラベル付きデータ・信頼度・説明可能性（explainability）がないと政策決定の根拠にはならない。キーワード照合＋短文判定は高偽陽性率を生みやすい。

## 実践ポイント
- 重要判断にLLMを使う場合は必ず「人間のレビュー（human-in-the-loop）」を組み込む。
- プロンプトで概念（例：DEI）の定義を明示し、根拠を要求する（短文のみで終わらせない）。
- 判定ログ、プロンプト、モデルバージョンを保存して監査可能にする。
- 事前にラベル付けデータで精度評価（偽陽性/偽陰性率）を行い、閾値を決定する。
- 日本の自治体・研究助成でAIを導入する場合は、透明性とガバナンス（外部監査や説明責任）を設計段階から入れる。
