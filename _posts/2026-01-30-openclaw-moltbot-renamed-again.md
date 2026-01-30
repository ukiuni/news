---
layout: post
title: "OpenClaw – Moltbot Renamed Again - OpenClaw — Moltbotが再改名"
date: 2026-01-30T08:19:25.386Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://openclaw.ai/blog/introducing-openclaw"
source_title: "Introducing OpenClaw — OpenClaw Blog"
source_id: 46820783
excerpt: "ローカルで動く個人用AIエージェントOpenClawが名前刷新、プライバシー重視で即導入可能に"
image: "https://openclaw.ai/og-image.png"
---

# OpenClaw – Moltbot Renamed Again - OpenClaw — Moltbotが再改名
ローカルで動く“あなた専用”AIエージェント、OpenClawが本格始動 — 名前も機能も磨き上げて再出発

## 要約
週末ハックから急成長したプロジェクトが「OpenClaw」に改名。ローカルで動くオープンなエージェント基盤として、チャットアプリ連携や新モデル対応、セキュリティ強化を推進する。

## この記事を読むべき理由
データ主権や企業の情報管理が重要な日本市場で、サーバーにデータを預けない「ローカル実行」の選択肢は即戦力になるため。OSSコミュニティの急成長事例としても学びが多い。

## 詳細解説
- 名前の変遷：Clawd → Moltbot → OpenClaw。商標チェックとドメイン確保を経て最終名称に決定。ロブスター（lobster）を象徴するマスコットは継続。
- 成長指標：GitHubで10万+スター、単週で200万訪問のトラフィックを記録するなど爆発的な注目を獲得。
- プラットフォーム概要：ユーザーのマシン（ノートPC、homelab、VPS等）上で動作するオープンエージェント。WhatsApp、Telegram、Discord、Slack、Teamsなど既存チャット経由で“自分の”AIが稼働。
- 今回のアップデート：
  - 新チャネル：Twitch、Google Chatプラグイン追加
  - モデル対応：KIMI K2.5、Xiaomi MiMo-V2-Flash対応
  - Webチャット：メッセージ同様に画像送信が可能に
  - セキュリティ：34件のセキュリティ関連コミットと「機械判定可能なセキュリティモデル」公開
- セキュリティ上の注意点：プロンプトインジェクションは業界課題のまま。強力なモデル選択とプロジェクトのセキュリティBest Practiceの確認が必須。
- コミュニティ運営：増加するPR/Issueに対応するためメンテナと運営体制を整備中。寄付やスポンサー、コントリビュートを歓迎。

## 実践ポイント
- まず試す（ワンライナー）：  
  ```bash
  curl -fsSL https://openclaw.ai/install.sh | bash
  ```
- 日本での着目点：データローカル運用が企業のコンプライアンスやAPPI対応に有利。LINE対応の有無は国内普及の鍵なので注目ポイント。
- セキュリティ対策：公開されたセキュリティモデルを読み込み、プロンプトインジェクション対策やキー管理を厳格に。
- コントリビューション：バグ報告、翻訳、メンテ支援、スポンサー検討でプロジェクト継続に貢献可能。

元記事：OpenClaw — Introducing OpenClaw（openclaw.ai/blog/introducing-openclaw）
