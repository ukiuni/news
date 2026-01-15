---
layout: post
title: "How to Make Architecture Decisions: RFCs, ADRs, and Getting Everyone Aligned - アーキテクチャ決定の方法：RFC、ADR、そして全員の合意を得る"
date: 2026-01-15T14:39:50.646Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://lukasniessen.medium.com/how-to-make-architecture-decisions-rfcs-adrs-and-getting-everyone-aligned-ab82e5384d2f"
source_title: "How to Make Architecture Decisions: RFCs, ADRs, and Getting Everyone Aligned"
source_id: 426237784
excerpt: "RFCで非同期検討→短時間会議で決定、ADRで正式記録して合意形成と後戻りを防ぐ方法を実践的に解説"
---

# How to Make Architecture Decisions: RFCs, ADRs, and Getting Everyone Aligned - アーキテクチャ決定の方法：RFC、ADR、そして全員の合意を得る
会議と“話し合い地獄”を終わらせる――RFCとADRでアーキテクチャを速く、確実に決める方法

## 要約
RFCで選択肢とトレードオフを非同期で議論し、短い決定会議で意思決定し、ADRで決定を記録する――この流れでアーキテクチャ決定の混乱を防げます。

## この記事を読むべき理由
日本の現場は合意形成や稟議文化で会議が長引きがち。RFC/ADRのワークフローを導入すれば、無駄な議論と後戻りを減らし、監査や引き継ぎにも強いドキュメントを残せます。

## 詳細解説
核となるプロセス（短縮）
- Write RFC（1–2日）→ Async Review（2–3日）→ Decision Meeting（30–60分）→ Write ADR（同日）

1) RFC（Request for Comments）
- 目的：問題、制約、複数案、推奨を整理してフィードバックを募るドラフト。会議での「その場の思いつき」を防ぐ。
- 置き場所：Confluence/Notion/Google Docs/専用リポジトリ。チームで一箇所に集約することが肝心。
- 推奨テンプレート（要点）
  - タイトル、著者、日付、ステータス、決定期限
  - Summary（1段落）、Context（現状と要件）
  - 提案案（Option A/B/C と pros/cons/工数/リスク）
  - Recommendation（著者の推奨）
  - Stakeholders（誰をタグするか）
  - Open Questions、Timeline

2) 非同期レビュー
- 2–3日程度でコメントを集める。非同期は熟考と調査を促進し、静かなメンバーの意見も拾いやすい。
- 良いコメントは「具体的な懸念」「過去の知見の共有」「代替案の提示」など。
- 著者はコメントに応答し、必要ならRFCを更新して合意形成を進める。

3) 決定会議（短く、集中して）
- 前提：参加者はRFCを読んでいること。読んでいない人には参加資格を問う。
- フォーマット（30–60分）
  - 2分：目的確認
  - 10–15分：未解決質問の整理
  - 15–30分：議論
  - 5–10分：意思決定（方法は事前合意）
- 参加者は5–8名程度に絞る。大人数は議論の拡散と雑談を招く。

意思決定の手法
- コンセンサス：理想だが時間がかかる
- コンセント（異論がないことを確認する）：「やっても良いか」を基準にする
- RAPID/DRI：最終判断者を明確にする（現場では実務責任者が決めやすい）
- 投票：軽微な案件向け。勝ち負けを生むため濫用は禁物

合意できない場合の対処
- エスカレーション、期間限定トライアル（3ヶ月など）、追加調査（スパイク）、スコープの分割。放置は技術的負債を生む。

4) ADR（Architecture Decision Record）
- 役割：何を決めたか・なぜ決めたかの永遠の記録。RFCは検討ログ、ADRは公式決定。
- 短く：Context、Decision、Consequences、Alternatives Considered。可能ならRFCへのリンクを張る。
- 書くタイミング：決定当日中に書くことを推奨。

どの決定にこのプロセスが必要か（目安）
- その場で決めてよい：チーム内限定、可逆性高い
- 軽量RFC：2–3チームに影響、やや中程度の影響
- フルプロセス：横断的、後戻り困難、コストや法令影響が大きい

AIの活用
- LLMはリサーチ、ドラフト作成、利害の洗い出しに有用。ただし「LLM任せでそのまま公開」は避け、著者が検証・補完する。

共通の落とし穴
- 分析麻痺（決められない）、利害者が多すぎる、ADRを書かない、黙っている人を無視する（非同期で拾う）。

## 実践ポイント
- RFC置き場を1箇所に固定し、命名規約を決める（例：RFC-2026-001-イベント駆動）
- RFCに決定期限（通常3–5日）を明記し、非同期レビュー期間を必ず設ける
- 会議は30–60分、参加者は5–8名に限定する。未読者の参加は原則不可
- 著者はコメントに能動的に返信し、会議翌日までにADRを作成するルールを定める
- 意思決定の方法（コンセント／DRIなど）をプロジェクト開始時に合意しておく
- 小さく試す文化をつくる（Time-boxed experiment）――合意できない場合の安全弁にする
- LLMは「下書きとチェックリスト作成」に使い、最終判断は人間が行う

短期的に試すなら、次の1週間で：
1) /Architecture/RFCs フォルダを作る  
2) まずは1件、3日レビュー・30分決定のRFCを回してみる

このやり方は日本のチーム文化にも馴染みやすく、書類による説明責任と効率的な合意形成の両立に役立ちます。
