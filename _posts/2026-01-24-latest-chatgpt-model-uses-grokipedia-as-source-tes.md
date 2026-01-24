---
layout: post
title: "Latest ChatGPT model uses Grokipedia as source, tests reveal - 最新のChatGPTモデルがGrokipediaを情報源にしていることが判明"
date: 2026-01-24T23:50:43.191Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.theguardian.com/technology/2026/jan/24/latest-chatgpt-model-uses-elon-musks-grokipedia-as-source-tests-reveal"
source_title: "Latest ChatGPT model uses Elon Musk’s Grokipedia as source, tests reveal | Grok AI | The Guardian"
source_id: 418470941
excerpt: "最新ChatGPTがGrokipediaを参照、政治・歴史で誤情報が流入する恐れあり"
image: "https://i.guim.co.uk/img/media/202d8061a28d8c1b855097fb90558014cb00d220/135_0_4675_3740/master/4675.jpg?width=1200&height=630&quality=85&auto=format&fit=crop&precrop=40:21,offset-x50,offset-y0&overlay-align=bottom%2Cleft&overlay-width=100p&overlay-base64=L2ltZy9zdGF0aWMvb3ZlcmxheXMvdGctZGVmYXVsdC5wbmc&enable=upscale&s=fc74f3ad623847f91b340f08501077e0"
---

# Latest ChatGPT model uses Grokipedia as source, tests reveal - 最新のChatGPTモデルがGrokipediaを情報源にしていることが判明
ChatGPTが“Grokipedia”を引用 — AI時代の情報信頼性に赤信号

## 要約
英ガーディアンの検証で、OpenAIの最新モデル（GPT-5.2）がイーロン・マスク系列のAI百科事典「Grokipedia」を引用しており、政治・歴史分野などで誤情報の流入が確認された。

## この記事を読むべき理由
日本でも英語ソースや海外モデルの出力を参照する場面は増えており、出力がどの情報源に依存しているかはプロダクト開発・メディア・研究で直接のリスクになるため必読。

## 詳細解説
- 検証結果：GPT-5.2が多数の問い合わせでGrokipediaを出典として挙げた。対象はイランの企業関係や、ホロコースト否定論に絡む人物像などの“やや専門的で曖昧な領域”。
- Grokipediaの性質：人間による直接編集を許さず、AIが記事を生成・更新するオンライン百科。既に右派的・論争的な記述が指摘されている。
- 参照の仕方：ChatGPTは常にGrokipediaを直接引用するわけではなく、顕著な誤情報については引用を避ける場合もある一方、扱いがあまり注目されないトピックで情報を引き込むケースが見られる。
- 広範な懸念：AnthropicのClaudeなど他モデルでも同様の参照が報告され、外部サイトを大量に生成してLLMに誤情報を“植え付ける”行為（LLM grooming）が問題視されている。
- プラットフォーマの主張：OpenAIは多様な公開情報源を参照し、安全フィルタを適用していると説明。ただし、研究者は「モデルが引用するとその情報源の信用が向上してしまう」と警鐘を鳴らす。
- 除去の難しさ：一度モデルに取り込まれた誤情報は、元ソースが訂正されてもモデル出力から完全に消えないことがある。

## 実践ポイント
- 出力の出典を必ず確認し、一次ソースや信頼ある第三者（学術論文、公的資料、主要メディア）で裏取りする。
- 不明確な歴史・政治情報は特にクロスチェックを徹底する（複数の独立ソースで一致するか）。
- プロダクト開発者は外部ウェブ参照機能のON/OFFやフィルタリング、ソース評価ルールを導入する。
- 研究者・メディアは「モデルが引用している＝正しい」を前提にしない運用ガイドを整備する。
- 誤情報を見つけたらプラットフォームに報告し、社内で再現テストを行ってモデルの脆弱性を評価する。
