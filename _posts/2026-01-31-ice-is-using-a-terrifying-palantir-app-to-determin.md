---
layout: post
title: "ICE Is Using a Terrifying Palantir App to Determine Where to Raid - ICEがどこを襲撃するかを決める恐ろしいPalantirアプリ"
date: 2026-01-31T06:41:35.089Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://newrepublic.com/post/205333/ice-palantir-app-raid-deportation"
source_title: "ICE Is Using a Terrifying Palantir App to Determine Where to Raid | The New Republic"
source_id: 413058597
excerpt: "住所と写真を地図でピン打ち…Palantirが襲撃先を選ぶ衝撃"
image: "https://images.newrepublic.com/44d34e3e72aaf2e15517a9df4fb9bc10483faeff.jpeg?w=1200&amp;h=630&amp;crop=faces&amp;fit=crop&amp;fm=jpg"
---

# ICE Is Using a Terrifying Palantir App to Determine Where to Raid - ICEがどこを襲撃するかを決める恐ろしいPalantirアプリ
ピン1つで“家”がターゲットに──Palantir製アプリが変える捜査地図とプライバシーの危機

## 要約
ICE（米移民税関捜査局）はPalantir系のアプリ（ELITE）で地図上に“潜在的な強制送還対象”をプロットし、住所確信度や個人情報を含むドシエで襲撃候補を選別していると報じられた。

## この記事を読むべき理由
監視・分析ツールが現場の意思決定に直結する現代において、アルゴリズムやデータ結合がどのように「実弾の行動」に影響するかを技術面から理解しておく必要があるため。日本でも同様の技術・調達が議論されれば、同様のリスクが生じる可能性がある。

## 詳細解説
- ツール名・機能：報道によれば "ELITE（Enhanced Leads Identification & Targeting for Enforcement）" と呼ばれるターゲティングツール。地図UIでピンを表示し、個別ドシエに名前、生年月日、Alien Registration Number（米の固有ID）、写真、住所の「confidence score（0–100）」などを表示。  
- データソース：HHS（保健福祉省）、USCIS（市民権・移民局）、およびCLEAR（調査データベースと推定）など複数ソースの結合で人物情報を形成。  
- 空間選別：Geospatial Lead Sourcingタブで「Bios & IDs」「Criminality」「Location」「Operations」等の条件を指定、地図上で範囲を描画して複数ターゲットを一括選択できる。  
- 契約・拡張：Palantirとの数千万ドル規模の追加契約や、ImmigrationOSと呼ぶAIベースの追跡プラン、24/7のSNS監視といった運用拡大の記録がある。  
- リスク：データ結合による誤同定、confidence scoreの過信、ブラックボックス化、説明責任の欠如が現場判断を誤らせる可能性。アルゴリズムで「密度の高い地域」を優先する運用は低確率の誤りを見落としやすい。

## 実践ポイント
- 開発者／エンジニア：信頼度スコアのキャリブレーションと誤判定率（false positive/negative）の可視化、データラインエージ（provenance）をログ化し説明可能性を担保する。人間の最終判断（human-in-the-loop）を必須化する。  
- 組織／調達担当：外部ベンダー契約に独立監査・透明性条項を入れる。データ最小化・保存期間の制限・第三者レビューを求める。  
- 技術リテラシーを持つ市民／研究者：同様システム導入の際はインパクト評価（AIA）や公開された評価指標の要求、データ権利の確認を行う。

短い結論：地図とスコアで「人が選ばれる」時代。技術的な詳査と運用ルール、透明性がないまま導入すると重大な人権・安全リスクを招く。日本でも同様の技術導入が議論される際は、技術面と制度面の両方で事前チェックを。
