---
layout: post
title: "Google is ending full-web search for niche search engines - ニッチ検索エンンジン向けの「全ウェブ検索」終了"
date: 2026-01-23T10:42:49.962Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://programmablesearchengine.googleblog.com/"
source_title: "Programmable Search Engine Blog"
source_id: 46730436
excerpt: "Googleがニッチ検索の全ウェブ対応を終了、Vertex AI移行が必要に"
---

# Google is ending full-web search for niche search engines - ニッチ検索エンンジン向けの「全ウェブ検索」終了
Googleの方針転換で、サイト内／限定ドメイン向け検索が主流に—あなたの検索戦略は間に合うか？

## 要約
GoogleがProgrammable Search Engine（PSE）の提供を整理し、Search Elementは「50ドメイン以内のサイト特化」に最適化、50超や“全ウェブ検索”は段階的に移行・登録制へ。Vertex AI Searchへの移行が推奨されます。

## この記事を読むべき理由
多くの日本企業やサービスがサイト内検索や複数ドメイン横断検索を使っています。方針変更は機能停止や課金・技術移行の必要性につながるため、早めの確認と準備が重要です。

## 詳細解説
- 何が変わるか
  - 新規のPSEエンジンは「Sites to search」機能（最大50ドメイン）を使う設定が必須に。既存エンジンは影響を受けないが、最終的に移行期限があります。
  - 50ドメインを超える、あるいは“Search the entire web”を必要とするケースは、Google側の全ウェブ検索ソリューション（登録フォームで要問い合わせ）に誘導されます。
- 代替と移行スケジュール
  - Custom Search Site Restricted JSON APIのエンドポイントは2025年1月8日に停止（既報）。このAPI利用者はVertex AI Searchへ移行する必要があります。
  - PSE関連の最終的な移行完了期限は2027年1月1日。
- Vertex AI Searchの利点
  - AI（生成AI）機能：要約・マルチターン検索
  - レイテンシ改善、ドメインカバレッジ向上、リバースイメージ検索、Vertex拡張との連携
  - エンタープライズ向けの会話型検索やグラウンディング（事実照合）対応
- 実務的影響
  - 新規で“全ウェブ”を前提にしたニッチ検索エンジンは、すぐに同じ構成で作れなくなる可能性あり。費用やSLA、機能差を検討する必要があります。

## 実践ポイント
- 早めの棚卸し：現状の検索エンジン（PSEやCustom Search）で「何ドメインを検索しているか」「Custom Search JSON APIを使っているか」を把握する。
- 期限を確認：Custom Search JSON API利用者は2025/01/08までに移行計画を立てる。PSE移行の最終期限は2027/01/01。
- 選択肢を検討：サイト特化（〜50ドメイン）はSearch Elementで継続検討。50超や全ウェブ検索はVertex AI SearchやGoogleのフルウェブ提供に問い合わせて見積もり・機能を確認。
- テスト運用：Vertex AI Searchの要約・多言語・マルチターン機能を小規模で試し、日本語対応やコスト見積りを行う。
- 登録／問い合わせ：フルウェブ検索が必要な場合はGoogleの案内フォームで興味登録を行い、移行条件と価格を確認する。

--- 
元記事のポイントを簡潔に整理しました。必要なら移行チェックリスト（テンプレ）を作成しますか？
