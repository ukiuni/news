---
layout: post
title: "Stargaze: SpaceX's Space Situational Awareness System - Stargaze：SpaceXの宇宙状況認識システム"
date: 2026-01-30T06:10:57.614Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://starlink.com/updates/stargaze"
source_title: "Starlink | Stargaze: SpaceX’s Space Situational Awareness System"
source_id: 46820113
excerpt: "約3万個のセンサでLEOの衝突を秒単位で検知、無償CDM共有で衛星運用を激変させるStargaze"
image: "null"
---

# Stargaze: SpaceX's Space Situational Awareness System - Stargaze：SpaceXの宇宙状況認識システム
30,000個の「星読みセンサ」が守る軌道――StargazeがLEOの衝突リスクを秒速で発見する理由

## 要約
SpaceXのStargazeは、Starlink衛星群に搭載された約3万個の星追跡器（star tracker）から得た観測を使い、毎日約3,000万回の通過データを生成して近リアルタイムで軌道予測と衝突警報（CDM）を出すSSA（Space Situational Awareness）システムです。数分以内に結合判定を出せる点と、そのデータを無償で他事業者に提供する点が画期的です。

## この記事を読むべき理由
日本も衛星打ち上げや宇宙ビジネスが急拡大中で、低軌道（LEO）での混雑・衝突リスクは国内外の事業者に直接関係します。低遅延の衝突検知と「軌道情報（エフェメリス）共有」の実践は、運用コストと事故リスクの低減につながります。

## 詳細解説
- 仕組み：Starlink衛星に搭載された多数の星追跡器が、背景の星に対する「衛星やデブリの通過（transit）」を継続観測。個々の観測を自動集約して精度の高い位置・速度（軌道要素）を算出する。従来の地上レーダーより観測頻度が桁違いに高いのが特徴。
- 出力：得られた軌道推定はスペーストラフィック管理プラットフォームに流れ、潜在的な接近（conjunction）を検出してConjunction Data Message（CDM）を生成。従来は数時間かかっていた流れを「数分」に短縮する。
- 実運用の実例：ある事例では、接近5時間前には約9,000mの安全余裕が見積もられていたが、相手衛星が5時間前に機動して約60mまで接近が急変。Stargazeが即座に機動を検出して更新CDMを配信し、Starlinkは検出から1時間以内に回避機動を実行して衝突を回避した。
- 運用上の注記：Stargazeは検知力を大幅に高めるが、最も確実な軌道情報は各オペレータが自ら提供するエフェメリス。SpaceXはStarlinkのエフェメリスを毎時更新・公開しており、他事業者にも同水準の共有を促している。航空機のフライトプラン共有になぞらえた説明が示される。

## 実践ポイント
- 日本の衛星事業者へ：エフェメリスの低遅延（例：毎時更新）共有を仕組み化すること。自動配信APIやファイル形式（TLE/プロプライエタリ）対応を検討する。  
- 運用ツール：低遅延CDMを受け取り自動で衝突評価→回避案生成→自動/半自動承認に繋げるワークフローを構築する。  
- 政策・産業界：JAXAや総務省／経産省レベルでエフェメリス共有のガイドライン整備を推進すると日本の衛星運用安全性が向上する。  
- 参加方法：SpaceXはStargazeのCDMをプラットフォーム経由で無償提供予定。既存オペレータはエフェメリス提出の仕組みを準備し、低遅延データの受信テストに参加する価値あり。

短く言えば、LEO時代の安全運航は「検知頻度」と「情報共有」の両立が鍵です。Stargazeは前者を大きく改善し、後者を促すことで業界全体の安全基準を引き上げようとしています。
