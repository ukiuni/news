---
layout: post
title: "Two Catastrophic Failures Caused by \"Obvious\" Assumptions - 『当たり前』の想定が招いた2つの壊滅的失敗"
date: 2026-01-21T15:34:57.218Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://open.substack.com/pub/alexanderfashakin/p/make-it-make-sense-nobody-clicked-the-wrong-button?utm_campaign=post-expanded-share&amp;utm_medium=web"
source_title: "Make It Make Sense (1) - How a Spacecraft and a Bank Lost $700 Million Without Anyone Making a Mistake"
source_id: 422492638
excerpt: "火星探査機と銀行送金で判明、当たり前の誤解が深刻な数億ドル被害を生む"
image: "https://substackcdn.com/image/fetch/$s_!GHoM!,w_1200,h_675,c_fill,f_jpg,q_auto:good,fl_progressive:steep,g_auto/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F08a3be00-faad-45ec-adc5-4b5259a8cf1c_1536x1024.png"
---

# Two Catastrophic Failures Caused by "Obvious" Assumptions - 『当たり前』の想定が招いた2つの壊滅的失敗
「『当然でしょ？』が7億ドルを消す瞬間──サイレント・アサンプションの怖さ」

## 要約
単純な“当然”の共有が原因で、1999年の火星探査機の損失（約1.93億ドル）と2020年のシティの送金ミス（約5億ドル）が起きた。両者ともシステムは正しく動き、人は合理的に振る舞ったが、意味の齟齬が致命的な結果を招いた。

## この記事を読むべき理由
技術的ミスはコーディングバグだけではない。仕様やUI、単位、用語の“暗黙の前提”が大損害につながることを知れば、あなたのプロジェクトで防げるトラブルが増える。

## 詳細解説
- 火星探査機（Mars Climate Orbiter, 1999）  
  ロケットの推力データが片方はポンド（imperial）で、もう片方はニュートン（metric）で扱われていた。ファイル交換は9か月にわたり正常に処理されたが、単位の不一致が書かれておらず、機体は低高度に降下して燃え尽きた。被害額は約1.93億ドルと報告される。  
- 銀行のUIミス（Citibank, 2020）  
  レガシーの銀行端末（Flexcube）で「PRINCIPAL」というチェックボックスの意味が曖昧で、担当者は元本を“残す”つもりが“全額返済”を意図する操作をしてしまい、結果的に約9億ドルが送金され、最終的な損失は約5億ドル相当になった。  
- 共通点：サイレント・アサンプション（Silent Assumption）  
  技術は仕様どおりに動き、人も合理的に動く。問題は「意味が人の頭の中だけにある」こと。ドキュメントやUI、インターフェイスに明示されていない前提が危険を生む。近代的なツール（型、リンター、テスト）だけでは防げない。

（日本との関係）  
日本企業もレガシーシステム、海外委託、国際プロジェクトで同様のリスクを抱えがち。メトリックが一般的な日本でも、海外パートナーとの単位や用語の齟齬、曖昧なUI文言は重大インシデントに直結する。

## 実践ポイント
- インターフェイスに単位・意味を明示する（例：「推力（N）」など）。  
- API/ファイル仕様を必須フィールドで定義し、契約として共有する。  
- UI文言はアクションが明確になるように書く（例：「元本全額を返済する」 vs 「PRINCIPAL」）。  
- 重大操作にはコンテクスト付きの確認ダイアログ（影響額を明示）と二段階承認を導入。  
- 統合テスト／E2Eで「異常系」を含むシナリオを自動化する。  
- クロスチームのレビュー（仕様・用語・単位）を開発フローの必須ステップにする。  
- ドキュメントとUXライティングを優先度高で扱い、バックログの下に置かない。  

明確にしない“当たり前”は高くつく。まずは前提を書き出し、システムとユーザーの共通言語を作ること。
