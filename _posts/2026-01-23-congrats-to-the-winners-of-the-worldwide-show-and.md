---
layout: post
title: "Congrats to the Winners of the \"Worldwide Show and Tell Challenge\" Presented by Mux! - Mux主催「Worldwide Show and Tell Challenge」受賞者発表"
date: 2026-01-23T14:52:46.165Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://dev.to/devteam/congrats-to-the-winners-of-the-worldwide-show-and-tell-challenge-presented-by-mux-10o9"
source_title: "Congrats to the Winners of the &quot;Worldwide Show and Tell Challenge&quot; Presented by Mux! - DEV Community"
source_id: 3191956
excerpt: "Mux活用のBOLDとFragmentsが受賞、動画を瞬時に検索・再利用可能に"
image: "https://media2.dev.to/dynamic/image/width=1000,height=500,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Fcsvriagqjgkefji8z369.png"
---

# Congrats to the Winners of the "Worldwide Show and Tell Challenge" Presented by Mux! - Mux主催「Worldwide Show and Tell Challenge」受賞者発表
世界が注目した“動画×検索”と“瞬間を蓄積する創作ツール”──受賞プロジェクトが示す次の一手

## 要約
DEVのグローバルチャレンジで、動画ライブラリを「Ctrl+F化」するBOLDと、動画の瞬間を蓄積・再利用するFragmentsが受賞。どちらもMuxの動画基盤と自動文字起こし／再生同期を活用しています。

## この記事を読むべき理由
動画コンテンツが増え続ける日本市場で、検索性・再利用性を高める設計はプロダクト差別化の肝。小規模チームでも実装可能な技術パターンが具体的に示されています。

## 詳細解説
- 全体像：DEVの「Show and Tell Challenge」はコミュニティの制作物を発表・審査する場。今回の注目は“動画をどう扱うか”に集中しています。
- BOLD（総合優勝）
  - 問題：大量の動画から目的の箇所を見つけられない。
  - 解決法：複数の文字起こしプロバイダを組み合わせてドメイン語彙を補正し、文字起こしとタイムスタンプを紐付けてクエリ結果から動画の該当時刻に跳べるUXを提供。
  - 技術ポイント：トランスクリプトの正規化、時刻インデックス、Muxでのエンコードとタイムスタンプ再生。
- Fragments（Best Use of Mux）
  - 概要：Webアプリ＋Chrome拡張で動画の“瞬間”（クリップ・メモ）を取り、タグ付けして再発見する「視覚的セカンドブレイン」。
  - Mux活用：直接アップロード、AI自動文字起こし、動的サムネ・GIFプレビュー、MP4静止版生成、モデレーション用Webhook、Mux Player（React）などを組み合わせたパイプライン。
  - 技術ポイント：クライアント→Mux→Webhook→ストレージ/DB のイベント駆動ワークフロー、プレイヤー組込みでのタイムリンク生成。
- 賞・協賛：賞金＋DEVメンバーシップ等。スポンサーは動画インフラのMuxで、スケーラブルな動画体験構築を支援。

## 実践ポイント
- まずは試す：Muxのトライアルでアップロード→再生→プレイヤー埋め込みを体験する。
- 動画検索の基本：音声文字起こしを取得し、タイムスタンプ付き索引を作る（ElasticsearchやSQLiteでも可）。
- UXの肝：検索結果から「その瞬間へジャンプ」できるUIを最優先で作る。
- モデレーションとパイプライン：Webhookで自動処理（サムネ生成、トランスコーディング、モデレーション）を組む。
- 小さく公開：短いデモ動画＋pitchでプロダクトを見せる練習をし、コミュニティのフィードバックを得る。

以上。興味があれば、受賞作（BOLD／Fragments）の公開デモや、Muxの導入ハンズオン記事も案内できます。
