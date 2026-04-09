---
layout: post
title: "Signals Are Not Guarantees - e2eテストが「言っていること」と「実際に検査していること」のズレ"
date: 2026-04-09T11:11:58.407Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.abelenekes.com/p/signals-are-not-guarantees"
source_title: "Signals Are Not Guarantees"
source_id: 366184311
excerpt: "UIシグナル依存を捨て、ドメイン約束で壊れないE2Eを築きCIフレークを減らす"
image: "https://beehiiv-images-production.s3.amazonaws.com/uploads/asset/file/70a09069-6dd5-40b0-9e3e-e4a4fda2d079/banner.png?t=1775658134"
---

# Signals Are Not Guarantees - e2eテストが「言っていること」と「実際に検査していること」のズレ
UIのシグナルに頼らず「約束（Promise）」をテストする方法 — 壊れにくく意味の明確なE2Eに変える

## 要約
E2Eテストは挙動を守るために書くが、多くは挙動そのものを検証せず「スピナーが消えた」「バッジが見える」といった表層的なシグナルを検査しているに過ぎない。シグナルを意味のある状態（state）に翻訳し、テストはその「約束（promise）」を直接主張すべきだ、という主張。

## この記事を読むべき理由
UIの表現変更でテストが頻繁に壊れる問題は、日本のプロダクト開発現場でも深刻。CIのフレークや保守コストを減らし、テストを製品の言葉で語らせる実践法を知ることで、チームの信頼できる自動化を手に入れられる。

## 詳細解説
- シグナル vs ステート vs プロミス  
  - シグナル：UIが出す具体的な観測可能事象（visible, enabled, text等）。  
  - ステート：複数のシグナルを集約して命名した意味ある事実（例：importがcompleted）。  
  - プロミス：テストが実際に保証すべき振る舞い（例：インポート完了時にエラーレポートをダウンロードできる）。
- 問題の核心：多くのテストはシグナルを直接断言するため、表示やロジックの表現が変わるだけでテストが壊れる。読者は複数の細かな断言から「何を保証しているか」を推測しなければならない。
- 解決策の要点：シグナル→ステート変換レイヤーを作る。テストでは domain 用語（currentStatus, failedCount, errorReportAvailable 等）で非同期クエリを呼び出し、まとまった事実を一度だけ評価する。こうすればDOMやロケータは自由に変えられ、テストは製品の約束が変わったときだけ修正すればよい。
- 実装パターン：Pageオブジェクト等に async な問い合せメソッド（例：currentStatus(), failedCount(), errorReportAvailable()）を用意するか、小さなカスタムマッチャー（toHaveState）で複数の事実をまとめて待つ。重要なのは形ではなく「信号と事実の境界」を明確にすること。

## 実践ポイント
- ドメイン語で聞く：テスト内の断言はUI要素ではなく「意味のある状態」を使う（例：assert importStatus == 'completed'）。  
- 翻訳レイヤーを一箇所に集中：ロケータとシグナル→ステートの変換はPageオブジェクトやヘルパーに集約する。  
- カスタムマッチャーを検討：複数の非同期チェックをまとめて待つ小さなユーティリティ（toHaveState）で読みやすさと再利用性を確保。  
- テストを変えるのは「約束」が変わったときだけ：DOMや見た目のリファクタは翻訳レイヤーで吸収する運用にする。  
- 小さく始める：まずは壊れやすい重要なシナリオ1つに導入して効果を確認する。

（元記事: Signals Are Not Guarantees — Ábel Énekes）
