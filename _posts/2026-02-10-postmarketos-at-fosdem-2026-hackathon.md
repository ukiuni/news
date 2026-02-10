---
layout: post
title: "postmarketOS at FOSDEM 2026 + Hackathon - FOSDEM 2026 とハッカソンの報告"
date: 2026-02-10T17:45:04.194Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://postmarketos.org/blog/2026/02/10/fosdem-and-hackathon/"
source_title: "postmarketOS at FOSDEM 2026 + Hackathon"
source_id: 1053235214
excerpt: "postmarketOSがFOSDEMでHW‑CIとmain基準の実用化を示唆"
---

# postmarketOS at FOSDEM 2026 + Hackathon - FOSDEM 2026 とハッカソンの報告
Linuxスマホの「主流化」へ。postmarketOSがFOSDEM 2026で示した現実的ロードマップとHW‑CIの実用化

## 要約
postmarketOSチームがFOSDEM 2026と続くハッカソンで議論・実装したのは、「main（正式）デバイス基準の強化」「HW‑CI（ハードウェア継続的インテグレーション）実装」「主要モジュール（Phosh/パイプワイヤ等）や主要端末のメインライン化」。実作業と設計が混ざった、次段階に向けた充実したイベントでした。

## この記事を読むべき理由
日本でも「Linuxベースのモバイル」を現場で動かしたい開発者やコミュニティ運営者にとって、postmarketOSのHW‑CIやデバイス“main”基準は実用的で参考になる具体例です。メインライン化やパイプワイヤ移行は端末対応・保守の工数削減に直結します。

## 詳細解説
- スタンド／展示：phone‑harness PCB v0.3 が公開され注目を集めた。物理的なテスト治具でデバイス接続を自動化することで、デバイスごとの反復検証が現実的になっている。  
- 「Main」カテゴリ（PMCR 0009）：単にビルドが通るだけでなく、チームが「推奨・維持」する体制を前提にした高いハードルを設定する方針。デバイスごとに担当チームを置き継続的サポートを保証する運用を目指す。  
- HW‑CI と PCB ワークショップ：Federico と Nicola の設計で CI‑tron と連携するハードが動作。現場での接続・自動テスト導入が進み、将来的なスケールが見えてきた。  
- カーネル/端末の進展：Fairphone、Snapdragon 8 Gen 3、Unisoc Jolla C2 など主要端末のメインライン化／パッチ整備が進行中。これにより upstream 取り込み→長期保守の流れが強化される。  
- ミドルウェアとアプリ：Phosh の今後、PipeWire への移行検討、Collabora Office のモバイル対応、UnifiedPush の議論など、ユーザ体験を左右する層の整備も並行して進行。  
- コミュニティ運営・方針：AI利用に関するポリシー見直し（生成系AIの使用を禁じる方向）、法的実体（AISBL 等）検討、組織再編（役割の名付け直しとフラット化）など運営基盤の強化案が議論された。  
- ハック成果の例：Fairphone 5 のスピーカー音声出力修正など、短時間で機能を復旧・検証するワークフローが確立されつつある。

## 実践ポイント
- 講演録画を視聴して、Phosh／Kernel／HW‑CI の技術スライドと実例を確認する（FOSDEM録画が公開中）。  
- phone‑harness PCB v0.3 や CI‑tron のリポジトリをチェックして、手元で簡易テスト環境を再現してみる（ハード＋スクリプトで自動化を体験すると学びが早い）。  
- PMCR（main基準）の議論に目を通し、日本での端末サポートを想定した体制（担当者・テストカバレッジ）をローカルで検討する。  
- PipeWire マイグレーションや音声経路の修正は端末ごとに違うため、同様の端末を持つ日本の開発者はパッチ提出や検証で貢献可能。  
- コミュニティ参加：ポッドキャストやハッカソンの成果物、GitLab イシュー/マージリクエストに参加して、実務ベースの経験を積む。

短く言えば、postmarketOSは「理論」から「実装と運用」へ重心を移しており、日本のエンジニアやコミュニティにも具体的な貢献機会が増えています。興味があるなら録画とリポジトリをチェックして、まずは小さなパッチやテストから参加してみてください。
