---
layout: post
title: "GameStop Says It's Shut Down a Nintendo Switch 2 Trade-in Exploit That Worked as an 'Infinite Money Glitch' - GameStopが任天堂Switch 2のトレードイン“無限マネー”不具合を封鎖したと発表"
date: 2026-01-21T21:54:55.689Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.ign.com/articles/gamestop-says-its-shut-down-a-nintendo-switch-2-trade-in-exploit-that-worked-as-an-infinite-money-glitch"
source_title: "GameStop Says It&#x27;s Shut Down a Nintendo Switch 2 Trade-in Exploit That Worked as an &#x27;Infinite Money Glitch&#x27; - IGN"
source_id: 422192519
excerpt: "GameStopのトレードイン不具合でSwitch 2が“無限クレジット”に、即パッチ適用"
image: "https://assets-prd.ignimgs.com/2026/01/21/i-found-the-gamestop-infinite-money-glitch-00-10-30-1-1768994964959.png?width=1280&amp;format=jpg&amp;auto=webp&amp;quality=80"
---

# GameStop Says It's Shut Down a Nintendo Switch 2 Trade-in Exploit That Worked as an 'Infinite Money Glitch' - GameStopが任天堂Switch 2のトレードイン“無限マネー”不具合を封鎖したと発表

GameStopで発見された「買ってすぐに下取り→再購入」を繰り返すだけで店舗クレジットが増え続ける“無限マネー”バグ、その仕組みと教訓。

## 要約
GameStopは、購入直後のSwitch 2を特定の下取りプロモで返却すると下取り額が新品価格を上回り、繰り返すことで毎回約$57相当のクレジットが得られる不具合（YouTuberが実演）を確認し、即時に修正したと発表しました。

## この記事を読むべき理由
小さなプロモの設計ミスが短時間で大きな金銭的抜け穴になる例は、製品販売・決済・プロモ施策を扱うエンジニアやマーケ担当、さらには消費者のリテラシー向上に直結します。日本の小売・EC運用にも同様のリスクがあるため必読です。

## 詳細解説
- 仕組み：あるプロモーション条件が「新品購入＋中古トレードでボーナス」を与える設定になっており、システムが中古トレード時の評価額を誤って高く算出。結果的に下取り額が新品価格を超えてしまった。
- 事例の数値例：購入価格 $414.99 に対して下取りクレジットが $472.50 となり、差額は $472.50 - 414.99 = 57.51 で、これを繰り返すことでクレジットが蓄積された。
- 実態：YouTuber（RJCmedia）が実演し、GameStopは動画と外部からの連絡で不具合を認知→即時パッチ適用。広範な悪用の証拠は少ないとされるが、短期間で多額の損失になり得た。
- 背景コンテキスト：同社は過去にもSNSで話題になる出来事をユーモアに変える傾向があり、また一部店舗閉鎖のニュースもあるため、運営面の脆弱性が注目されやすい。

## 実践ポイント
- 小売／開発者向け
  - プロモ仕様は「下取り額 ≤ 新品価格」のような整合性ルールで検証する。
  - プロモ発動条件に対する単体テスト・異常値テストを自動化する。
  - 同一SKUの短時間内の同一顧客による購入→下取りのループを検知するレートリミットやフラグを設ける。
  - 下取り品の物理シリアル管理・在庫ロックで即時再販を防ぐ。
  - モニタリングで異常なクレジット発行をアラート化する。
- 消費者向け
  - 明らかに不自然な利益を生む操作は法的・倫理的リスクがあるため試さない。
  - 見つけた場合は店舗や運営に報告する（脆弱性扱いで対応されることもある）。
  - トレードインやプロモの条件は事前に確認し、レシートを保管する。

短い事例ですが、設計漏れが即金銭的インパクトに直結する典型です。システム設計と運用監視の両面で学べるポイントが多く含まれています。
