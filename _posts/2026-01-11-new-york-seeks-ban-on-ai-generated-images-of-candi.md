---
layout: post
title: "New York Seeks Ban on A.I.-Generated Images of Candidates | Last year, the Cuomo campaign released a video created by artificial intelligence that depicted Zohran Mamdani eating rice with his hands. Gov. Kathy Hochul wants to ban such tactics. - ニューヨーク州、候補者のAI生成映像禁止を検討｜昨年クオモ陣営がゾフラン・マムダニ氏の“手食い”をAIで捏造、ホウチュル州知事はこうした手法を禁じたい"
date: 2026-01-11T18:33:23.401Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.nytimes.com/2026/01/11/nyregion/ny-hochul-ai-candidates.html"
source_title: "New York Seeks Ban on A.I.-Generated Images of Candidates | Last year, the Cuomo campaign released a video created by artificial intelligence that depicted Zohran Mamdani eating rice with his hands. Gov. Kathy Hochul wants to ban such tactics."
source_id: 430632676
excerpt: "クオモ陣営が手食いをAI捏造、NY州が候補者のAI映像禁止を検討"
---

# New York Seeks Ban on A.I.-Generated Images of Candidates | Last year, the Cuomo campaign released a video created by artificial intelligence that depicted Zohran Mamdani eating rice with his hands. Gov. Kathy Hochul wants to ban such tactics. - ニューヨーク州、候補者のAI生成映像禁止を検討｜昨年クオモ陣営がゾフラン・マムダニ氏の“手食い”をAIで捏造、ホウチュル州知事はこうした手法を禁じたい

選挙戦で拡散されたAI合成映像が「現実」を作り出す時代──ニューヨーク州が候補者のAI生成画像・映像を禁止する動きを見せ、法整備と技術対策の両方が焦点になっている。

## 要約
AIで合成した候補者の画像・動画が選挙に悪用された事件を受け、ニューヨーク州がこうした合成メディアの禁止を検討。技術的には生成モデルの普及で偽情報作成は容易になり、対策として検出・透かし（provenance）・法規制の組合せが必要とされる。

## この記事を読むべき理由
日本でもSNS経由でのフェイク画像・動画は既に問題化しており、選挙や世論形成に与える影響は無視できない。技術者・メディア関係者・製品担当者は、生成AIがもたらすリスクと現実的な防御策を理解しておく必要がある。

## 詳細解説
- 何が起きたか：米ニューヨークで、政治陣営がAIを使ってある候補者の不利な映像を作成・公開した例が報じられ、州知事が「候補者を標的にしたAI合成映像の禁止」を提案。政治的ディスインフォメーション（偽情報）対策が目的。
- 技術の背景：近年の生成AI（GANや拡散モデル＝diffusion models）は、写真や短い動画を高品質で合成可能。顔の置換、表情合成、音声合成を組み合わせれば説得力のある偽映像を短時間で作れる。
- 検出の難しさ：圧縮や編集で痕跡が消えやすく、生成モデルも常に進化するため単一の検出器で完全に防げない。既知の検出手法は周波数解析、時間的整合性チェック、顔・唇の微妙な不一致検出、機械学習による微細なアーチファクト検出など。
- 透かし・証拠強化の技術：C2PAなどのコンテンツ認証標準で生成元の署名とメタデータを付与する、モデル出力にロバストなデジタルウォーターマークを埋め込む（目に見えない署名）、出力ログ（プロンプト・ツールチェーン）を保存する、などが対策の柱。
- 法規制と実務のあいだ：禁止法が作られても、定義（何を「AI生成」とするか）、表現の自由とのバランス、越境での拡散、実効的な執行方法が課題。プラットフォーム側のポリシー強化と技術的検知が補完的に必要になる。

## 実践ポイント
- 開発者・プロダクト担当者向け
  - 生成ツールで出力するメディアにC2PAなどのメタデータ署名を付与する仕組みを導入する。
  - 出力時に不可視ウォーターマークを埋め込み、改変検出用のログ（プロンプト、モデルバージョン、タイムスタンプ）を保存する。
  - モニタリングパイプラインを構築し、SNS上の疑わしい合成メディアを速やかに検出・報告できる体制を整える。
  - モデルカードや利用規約で「政治利用の制限」「透明性要件」を明示する。
- 一般ユーザー・編集者向け
  - 衝撃的・違和感のある映像はまず出所を確認し、逆画像検索や複数の報道ソースで裏取りする。
  - プラットフォームが提供する「合成である」という表示やコンテンツクレデンシャル（出典情報）をチェックする習慣をつける。
- 政策担当者・法務向け
  - 技術的な透かしや証跡方式を前提にした現実的な規制設計を検討する（即時削除や罰則だけでなく、追跡・識別の仕組みを法整備に含める）。
  - プラットフォーム、メディア、技術コミュニティと協調して検出・対応のオペレーションを確立する。

ニューヨークの動きは単なる米国の事例に留まらない。生成AIが日常的に利用される今、日本でも同様の議論と具体的な防御設計が急務である。技術者は「作る側」だけでなく「検知・証明する側」のツールとプロセス整備に責任を持つべきだ。
