---
layout: post
title: "Open-source game engine Godot is drowning in 'AI slop' code contributions: 'I don't know how long we can keep it up' - オープンソースのゲームエンジンGodotが「AIスロップ」なコード寄稿で溺れかけている：「どれだけ持ちこたえられるか分からない」"
date: 2026-02-18T00:23:08.162Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.pcgamer.com/software/platforms/open-source-game-engine-godot-is-drowning-in-ai-slop-code-contributions-i-dont-know-how-long-we-can-keep-it-up/"
source_title: "Open-source game engine Godot is drowning in 'AI slop' code contributions: 'I don't know how long we can keep it up' | PC Gamer"
source_id: 439085288
excerpt: "AI生成の低品質PRでGodotが疲弊、深刻な運営危機の現場とは"
image: "https://cdn.mos.cms.futurecdn.net/JVBMNVgT9xT6HFkTbDsqfe-1920-80.jpg"
---

# Open-source game engine Godot is drowning in 'AI slop' code contributions: 'I don't know how long we can keep it up' - オープンソースのゲームエンジンGodotが「AIスロップ」なコード寄稿で溺れかけている：「どれだけ持ちこたえられるか分からない」
GodotがAI生成の“ゴミPR”に押しつぶされそう――インディ／OSSコミュニティに直結する緊急事態

## 要約
Godotの主要メンテナーが、LLM（言語モデル）による低品質なプルリクエスト（“AIスロップ”）の急増で疲弊していると告白。人手と資金が追いつかず、プロジェクト運営に深刻な影響が出ている。

## この記事を読むべき理由
日本のインディ開発者やOSS利用者にとって、Godotは身近な選択肢。エンジンの健全性低下はツールの信頼性やエコシステム全体に波及するため、今何が起きているか知っておく価値がある。

## 詳細解説
- 問題の本質：大量のPRがLLMベースで生成され、説明文は流暢でもコードが誤りだったりテストが不実だったりする。メンテナーは「人間が理解しているか」を逐一疑わねばならず、レビューのコストが増大している。  
- メンテナー負担：レビューだけでなく、新規寄稿者を指導してマージ可能な状態にする作業が増大。維持に要する時間と精神的コストが限界に近づいている。  
- 対策の議論：自動検出（AIでAIを検出する皮肉）、GitHubのPR制限（コラボレーターのみ許可など）、別プラットフォームへの移行検討、そして最も現実的なのは「資金でメンテナーを雇う」こと。GitHub側も低品質PR問題を認め、部分的な機能を提供し始めているが利害の衝突も指摘される。  
- 倫理・実務のジレンマ：AI活用を完全否定しつつも、言語の壁や効率化を理由にAIを利用する寄稿者が増える。結果、品質保証とオープン性の両立が困難になっている。

## 実践ポイント
- 寄稿者向け（日本の開発者がすぐできること）
  - AIを補助に使う場合でも、必ず自分で理解し説明する。PR本文に「どこをどう直したか」「テスト結果」を明記する。  
  - 単にAI出力を貼るだけのPRは避け、ユニットテスト／動作確認のスクリーンショットやCIログを添付する。  
- メンテナー／プロジェクト運営者向け
  - 貢献ガイドラインを明確化し、AI利用のポリシーと必要な証跡（テスト、説明）を要求する。CIで自動検査・テストを充実させる。  
  - 企業やユーザーコミュニティに対して資金提供（寄付やスポンサー）を呼びかけ、レビュー人員を確保する。fund.godotengine.org 等の窓口を活用。  
- 企業・日本のユーザーとして
  - OSSを重要インフラで使うなら、単なる利用者で終わらずスポンサリングやメンテナー支援を検討する。短期の工数節約が長期的な保守コスト増に繋がるリスクに留意する。

短く言えば：AIは便利だが「出力を鵜呑みにする貢献」はOSSの維持を壊す可能性がある。日本の開発者コミュニティも当事者意識を持って、品質管理と資金支援の両輪で守る必要がある。
