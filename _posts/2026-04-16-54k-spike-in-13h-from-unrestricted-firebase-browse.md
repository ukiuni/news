---
layout: post
title: "€54k spike in 13h from unrestricted Firebase browser key accessing Gemini APIs - 13時間で€54k急増：API制限なしのFirebaseブラウザキーがGemini APIへアクセス"
date: 2026-04-16T13:04:21.372Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://discuss.ai.google.dev/t/unexpected-54k-billing-spike-in-13-hours-firebase-browser-key-without-api-restrictions-used-for-gemini-requests/140262"
source_title: "Unexpected €54k billing spike in 13 hours: Firebase browser key without API restrictions used for Gemini requests - Gemini API - Google AI Developers Forum"
source_id: 47791871
excerpt: "API制限なしのFirebaseブラウザキーで13時間に€54k超の不正請求、設定見直し必須"
image: "https://d3qe71uytubmmx.cloudfront.net/original/3X/a/b/abef8e8a2f13f217175a82ce05cb66d1d02610e2.png"
---

# €54k spike in 13h from unrestricted Firebase browser key accessing Gemini APIs - 13時間で€54k急増：API制限なしのFirebaseブラウザキーがGemini APIへアクセス
わずか一晩で€54,000—Firebaseキー放置が招く悪夢と防御策

## 要約
FirebaseプロジェクトにFirebase AI Logicを有効化した直後、API制限なしのブラウザキー経由で自動化されたリクエストが発生し、13時間で€54,000超の課金が発生した事例。アラート遅延や課金認定により事後救済が得られなかった。

## この記事を読むべき理由
FirebaseやGoogleのAIサービスを利用する日本のスタートアップ／開発チームは、同様の設定ミスや運用監視不足で短時間に重大なコスト被害を受けるリスクがあります。初級者でも取れる防御策を押さえておく価値があります。

## 詳細解説
- 発端：既存Firebaseプロジェクトに簡単なAI機能を追加し、Firebase AI Logicを有効化。ブラウザ向けのAPIキーに「API制限（どのAPIを呼べるか）」が設定されておらず、外部からGemini API呼び出しに悪用された。  
- 挙動：ユーザー実行に関連しない自動化トラフィックが短時間に集中。運用側は夜間に異常を検出したが、アラートや課金レポートに遅延があり、対応時には既に大きなコストが発生していた。  
- 対応と結果：API無効化と鍵のローテーションで攻撃は止まったが、Googleはログ上「プロジェクト発信の有効な利用」として課金を維持し、請求調整は否認された。  
- 背景知見：過去の議論（例：Truffle Security）でも「GoogleのAPIキーは秘匿情報ではない」という前提が変化し、ブラウザキー運用には厳格な制限が必要になっている。

## 実践ポイント
1. ブラウザキーには必ずAPI制限（呼び出し可能なAPIを限定）とリファラ制限を設定する。  
2. 可能な場合はクライアント→サーバー経由でAPI呼び出しを行い、サーバー側で認証（サービスアカウント等）を行う。  
3. Firebase App Checkを有効化して不正なクライアントからの呼び出しを防ぐ。  
4. プロジェクト毎に厳しいクォータと料金アラートを設定し、課金エクスポート（BigQuery等）でリアルタイム監視を行う。  
5. 鍵を漏洩したら即時無効化・ローテーションし、ログを保存してサポートへ提出する。  
6. 組織レベルでのポリシー（IAM、VPC Service Controls等）導入を検討する。

短時間で大きな被害になるため、設定の「初期確認」と監視ルールの整備を今すぐ見直すことを推奨します。
