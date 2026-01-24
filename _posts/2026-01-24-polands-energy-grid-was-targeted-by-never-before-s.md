---
layout: post
title: "Poland's energy grid was targeted by never-before-seen wiper malware - ポーランドの電力網が未確認のワイパー型マルウェアに狙われる"
date: 2026-01-24T23:51:16.259Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://arstechnica.com/security/2026/01/wiper-malware-targeted-poland-energy-grid-but-failed-to-knock-out-electricity/"
source_title: "Wiper malware targeted Poland energy grid, but failed to knock out electricity - Ars Technica"
source_id: 46747827
excerpt: "未確認ワイパーがポーランド電力網を狙い停電を目論みSandworm関与が示唆"
image: "https://cdn.arstechnica.net/wp-content/uploads/2026/01/data-wiper-malware-1152x648.jpg"
---

# Poland's energy grid was targeted by never-before-seen wiper malware - ポーランドの電力網が未確認のワイパー型マルウェアに狙われる
魅せる邦題: 「停電狙いの“消し去る”サイバー攻撃—ポーランド電力網に届いた未発見ワイパーの痕跡」

## 要約
ポーランドの電力網が、データを完全消去する“ワイパー”型マルウェア（DynoWiper）で攻撃されたが、発電・送配電の停止には至らなかった。調査ではロシア系のSandwormグループの関与が中程度の確信で示唆されている。

## この記事を読むべき理由
日本でも再生可能エネルギーの分散接続やOT/IT融合が進む中、電力インフラが国家レベルの破壊的サイバー攻撃にさらされる現実を知っておく必要があるからです。

## 詳細解説
- 攻撃の狙いと手法：対象は再生可能発電設備と配電事業者間の通信経路で、永久にデータ・コードを消去するワイパーを投入して「運用破壊」を狙った。ESETは新種と名付けたDynoWiperを調査し、過去のSandwormの手口（2015年ウクライナ停電、2017年NotPetya、2022年AcidRain等）との類似性を根拠に同グループを指摘。
- なぜ失敗したか：電力停止に至らなかった理由は公表されていない。意図的に被害を限定した可能性、あるいは防御策（分離、バックアップ、復旧手順、検知）が機能した可能性がある。
- 技術的示唆：ワイパーはブートやファイルシステム、デバイスファームウェアなどを標的にするため、伝統的なアンチウイルスだけで防げない。ICS/SCADAの正規機能を悪用するケースも多く、ネットワーク分離・認証強化・ログ収集とレスポンス体制が重要。

## 実践ポイント
- ICS/OTのネットワーク分離と最小権限を再確認する。  
- 再生可能発電やリモート端末の通信経路に対する可視化と監視を強化する（ログ、フロー、異常通信のアラート）。  
- 不変バックアップ（immutable）、オフサイト／エアギャップのバックアップを定期的に検証する。  
- エンドポイント（EDR）とファームウェア監視を導入し、ワイパー型活動の兆候（大量ファイル削除、マスターブートレコード変更、暗号化でない消去操作）を検出するルールを整備する。  
- 事業継続計画（BCP）とテーブルトップ演習で「OT破壊シナリオ」を含める。  
- インシデント発生時は早期に国内外の情報共有窓口（JPCERT、業界ISAC、同盟国の脅威インテリ）へ通報・共有する。

元記事の示唆は「電力インフラは現実的な破壊対象であり、防御と連携が命運を分ける」という点です。日本の電力事業者や自治体、ベンダーは即時の見直しを推奨します。
