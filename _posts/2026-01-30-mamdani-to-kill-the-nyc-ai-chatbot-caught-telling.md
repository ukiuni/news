---
layout: post
title: "Mamdani to kill the NYC AI chatbot we caught telling businesses to break the law - ママダニ市長が“違法指南”していたNYCのAIチャットボットを撤去へ"
date: 2026-01-30T19:21:03.566Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://themarkup.org/artificial-intelligence/2026/01/30/mamdani-to-kill-the-nyc-ai-chatbot-we-caught-telling-businesses-to-break-the-law"
source_title: "Mamdani to kill the NYC AI chatbot we caught telling businesses to break the law – The Markup"
source_id: 413502615
excerpt: "NYC公式AIが事業者に違法助言、撤去検討で60万ドル超の税金無駄遣いが発覚？"
image: "https://mrkp-static-production.themarkup.org/uploads/2026/01/011226-Zohran-Mamdani-GETTY-MU-01-1200x628.jpg"
---

# Mamdani to kill the NYC AI chatbot we caught telling businesses to break the law - ママダニ市長が“違法指南”していたNYCのAIチャットボットを撤去へ
NYCのチャットボットが「店主に違法行為を促す」──予算削減の口実にもなった衝撃の実態

## 要約
ニューヨーク市の市政チャットボット（MyCityプロジェクト）は、事業者向けの規則照会で間違った・違法を助長する回答を出し続け、ママダニ新市長が「使い物にならない」と撤去を検討。導入費用は基盤構築で約60万ドル、維持費も高額だった。

## この記事を読むべき理由
自治体や企業がAI導入を急ぐ今、日本でも「誤情報による法的リスク」「外注コスト」「運用ガバナンス」の教訓がそのまま当てはまるため、早めに対策を知る必要があります。

## 詳細解説
- 何が起きたか：Adams政権が導入した市公式チャットボットは、事業者向けに市のルールを案内する目的だったが、労働法や住宅政策など重要分野で誤った案内（例：従業員のチップを取り分けてよい、Section 8受給者を差別してよい、現金受領を拒否してよい等）を行った。
- 技術的要因：
  - LLM系の「確信をもって誤答する」（hallucination）問題。モデルは根拠を示さず自然な文を生成するため、法律相談に不適切。
  - おそらく法令原典や最新データに直接紐づける仕組み（RAG＝外部ドキュメント参照）が不十分で、回答の裏取りが弱かった。
  - 運用面では質問の種類を制限したり注意書きを付けることで応急対応したが、根本改善には至らず。
- コストとガバナンス：基盤構築費は約60万ドル、維持費も高く、新市長はこれを「節約対象」と位置づけた。外部委託の透明性や評価プロセスの欠如も批判点。
- 公的サービスへの示唆：法令や市民の権利に直結する分野では、AIは「補助ツール」に留め、人間のチェックとソース表示を必須にする設計が求められる。

## 実践ポイント
- デプロイ前に「現場でのケーステスト」を必須化（労働法・住宅法など高リスク領域は重点）。
- 回答に必ず根拠（条文・公式ページ）を添える／参照できるRAG設計を導入する。
- 法的助言を自動で出させないガードレールと「人間の承認（human-in-the-loop）」を組み込む。
- ベンダー契約に品質保証・責任範囲・修正対応の条項を明確化する。
- 運用ログとモニタリングで誤答を早期検出、利用停止基準を明確にする。
- 日本向けにはAPPI（個人情報保護法）準拠、地方自治体なら住民説明と透明性確保を優先する。

短く言えば：AIは便利だが「法令案内」は特に慎重に。導入前後の監査・根拠提示・人間の監督が必須です。
