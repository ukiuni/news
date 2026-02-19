---
layout: post
title: "How I Turned an Ugly Spreadsheet into an AI Assisted App with Antigravity - 醜いスプレッドシートをAntigravityでAI支援アプリに変えた方法"
date: 2026-02-19T05:51:42.231Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://dev.to/googleai/how-i-turned-an-ugly-spreadsheet-into-an-ai-assisted-app-with-antigravity-3j52"
source_title: "How I Turned an Ugly Spreadsheet into an AI Assisted App with Antigravity - DEV Community"
source_id: 3263874
excerpt: "AntigravityでスプレッドシートをAIレビュー向けダッシュボード化し数分で実現する方法"
image: "https://media2.dev.to/dynamic/image/width=1000,height=500,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Fuknvizo2wsfbkv2byuki.png"
---

# How I Turned an Ugly Spreadsheet into an AI Assisted App with Antigravity - 醜いスプレッドシートをAntigravityでAI支援アプリに変えた方法
スプレッドシートの地獄を数分で解消！AIとクラウドで「レビュー専用ダッシュボード」を作る実録

## 要約
大量の会議発表応募CSVを、GoogleのAIツール（Gemini + Antigravity）で対話的に設計・生成し、SNSで裏取りした評価を付けるダッシュボードに変え、Cloud Runへ自動展開した事例。

## この記事を読むべき理由
手作業で表を眺めて消耗している日本のイベント運営者やプロダクト担当者にとって、AIでレビュー業務を自動化・可視化する具体的ワークフローと注意点がわかるから。

## 詳細解説
- 発端：大量の応募を小さなセルで見るのは非効率。UI化＋AI支援で意思決定を速めたいという課題。
- Step 1（メタプロンプト）：まずGemini（大規模言語モデル）に「要件を普通の言葉で説明」→それを技術仕様（コンポーネント構成、データモデル）に整えてもらう。これをAntigravity（コーディングエージェント）に渡す。
- Step 2（UI生成）：AntigravityがCSVアップロード、高コントラストで読みやすいレビュー画面、ステータス管理などのフロント／バックエンドを自動生成。フロントで出たReactの「hydration error（サーバレンダリングとクライアントDOMの不一致）」も、エラーメッセージを渡せばエージェントが修正。
- Step 3（Grounded Intelligence）：AI評価をそのまま信じないために「Search Grounding」を導入。Reddit/X/LinkedInなどを検索して実際の開発者の反応や話題性を根拠にすることで、ハルシネーション（虚偽生成）を減らす。
- Step 4（キャリブレーション）：Few-shotプロンプトで評価基準を調整。例を与え「マーケティングっぽければ減点」「学びや実例があれば加点」といったルールを学習させる。
- Step 5（バッチ処理）：逐一評価を待つのは非効率。バックエンドをバッチ処理モードにリファクタし、全応募を非同期に処理して「AIドラフト」列を埋める。
- Step 6（デプロイ）：AntigravityがGCPプロジェクトを認識し、コンテナ化〜Cloud Runへのデプロイコマンドまで自動生成・実行。共有可能なURLが得られる。

注意点：データプライバシー、外部検索でのAPI利用制限、コスト監視、AI評価の偏りは必ず運用ルールで補正する必要あり。

## 実践ポイント
- まずは「メタプロンプト」で要件を図解的にまとめてLLMに書かせる。  
- Groundingで外部ソースを参照させ、評価の根拠を付ける（誤情報を減らす）。  
- Few-shotで自分の採点ルールを例で示し、好みをAIに学習させる。  
- バッチ処理でスケール化し、レビューは「最終判断」に集中する。  
- デプロイ先はCloud Runが手軽だが、社内ルールやコストに合わせて選択（GCP以外でも同様の流れは可能）。  

この手法はイベント審査だけでなく、採用候補レビューやRFP選定、PR原稿の一次スクリーニングなど日本の現場で即応用可能です。
