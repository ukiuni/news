---
layout: post
title: "The Slopacolypse is here: Karpathy warns of \"Disuse Atrophy\" in 2026 workflows. Are we becoming high-level architects or just lazy auditors? - 「スローパカリプス到来：カーパシーが警告する2026年の“使用停止性萎縮” — 我々は高位の建築家か、それとも怠惰な監査者か？」"
date: 2026-02-12T07:10:32.474Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://eu.36kr.com/en/p/3668658715829123"
source_title: "Programming&#x27;s Demise? Claude Code Father&#x27;s Bombshell Quotes in Conversation with Karpathy"
source_id: 443714612
excerpt: "AIが設計から実装まで自律化する2026年、技術者は高位設計者か怠惰な監査者か？"
image: "https://img.36krcdn.com/hsossms/20260204/v2_e84c6a0cd7c34122ab5a20043dcc0d68@5888275@ai_oswg1106700oswg1053oswg495_img_png~tplv-1marlgjv7f-ai-v3:600:400:600:400:q70.jpg"
---

# The Slopacolypse is here: Karpathy warns of "Disuse Atrophy" in 2026 workflows. Are we becoming high-level architects or just lazy auditors? - 「スローパカリプス到来：カーパシーが警告する2026年の“使用停止性萎縮” — 我々は高位の建築家か、それとも怠惰な監査者か？」

最先端LLMが「コード作成」を完全に担う時代へ — あなたの仕事はどう変わるのか？

## 要約
KarpathyとClaude Codeの開発者Boris Chernyの会話は、AIがコード生成と修正をループで実行する「Agentic Coding」時代の到来を示し、一方で人間の手を使わないことで生じる「disuse atrophy（使用停止性萎縮）」やAI生成コードの質低下（=Slopacolypse）への懸念を投げかけている。

## この記事を読むべき理由
日本の開発現場でも、大手企業やスタートアップが生成AIを導入し始めている今、単なるツールの話を超えて「職能の再定義」「採用基準」「品質管理」の方針を先手で考える必要があるため。

## 詳細解説
- パラダイムシフト：Software 2.0（ルール→データ）を提唱したKarpathyの議論はさらに進み、「Agentic Coding」へ。人は「実装手順」ではなく「達成基準（意図）」を与え、AIが設計・実装・テスト・リファクタを自律で回す。
- 実例（要約）：Claude CodeチームはOpus 4.5等の大規模モデルを複数インスタンスで並列利用し、PR作成〜テスト〜マージまでAI主導で高速化。これにより一人分の生産性が小規模チームに匹敵する場面が生まれている。
- 新しいスキル像：記憶して細部を叩き込む「職人型」から、要件定義・設計・AI指揮・受け入れ基準設定ができる「総合者（generalist／アーキテクト兼PM）」へ。AIはマイクロタスクを得意とするため、真の差別化は上流設計能力や批判的思考。
- 危険性：Karpathyが指摘する「disuse atrophy」は、手でコード書かなくなることでデバッグ力や低レイヤ理解が衰えるリスク。さらにAI生成コードが膨大に増え、メンテ不能・脆弱な“ガラクタ”が蓄積する「Slopacolypse」の懸念。モデル自身によるレビュー（AIがAIを査読）で相互改善するのが一つの対策だが、運用ルールとガバナンスが必須。

## 実践ポイント
- 基礎は維持する：定期的に手でコードを書き、低レイヤの問題（メモリ・並行処理・パフォーマンス）を自分で解く訓練を続ける。
- 要件精度を上げる：AIに投げる「成功条件」「非機能要件」「境界ケース」を明確に定義するプロンプト設計を習得する。
- CI＋AIレビューを導入：AI生成コードは自動テスト・静的解析・モデルによるPRレビューの複合ループで検証する。重要箇所は人間の専門家が最終承認を行う。
- 採用と育成を見直す：日本企業は「幅広い思考力」と「ドメイン理解」を重視するジェネラリストを評価する方針にシフトすべき。
- 依存管理と可観測性：サードパーティやAI生成モジュールの出所、テストカバレッジ、ログ・トレースを厳格に管理すること。

短い結論：プログラミング「のしかた」は変わるが、本質は残る。ツールに任せきりにせず、設計・検証・運用の統合スキルを磨けば、この変化は大きな追い風になる。
