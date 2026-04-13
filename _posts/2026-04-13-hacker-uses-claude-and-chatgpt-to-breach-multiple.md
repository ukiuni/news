---
layout: post
title: "Hacker Uses Claude and ChatGPT to Breach Multiple Government Agencies - ClaudeとChatGPTを使い複数の政府機関を侵害"
date: 2026-04-13T13:08:59.953Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://cybersecuritynews.com/hacker-uses-claude-and-chatgpt-to-breach/"
source_title: "Hacker Uses Claude and ChatGPT to Breach Multiple Government Agencies"
source_id: 363461473
excerpt: "ClaudeとChatGPTで政府9機関の数億件個人情報を短期間で窃取した衝撃の手口"
image: "http://cybersecuritynews.com/wp-content/uploads/2026/04/Hacker-Uses-Claude-and-ChatGPT-to-Breach-Multiple-Government-Agencies-1.webp"
---

# Hacker Uses Claude and ChatGPT to Breach Multiple Government Agencies - ClaudeとChatGPTを使い複数の政府機関を侵害
政府機関を丸ごと短時間で「舐め取る」AI攻撃の衝撃――あなたの組織も他人事ではありません

## 要約
メキシコの単独攻撃者がAnthropicのClaude CodeとOpenAIのGPT‑4.1を駆使し、9つの政府機関から数億件規模の市民データを短期間で窃取した。攻撃はAIでコマンド生成・解析を自動化し、従来より遥かに速いペースで実行された。

## この記事を読むべき理由
AIツールが攻撃側の「増幅器」として実用化された事例は、日本の自治体やレガシーシステムにも直結する脅威です。予算・人手が限られる現場ほど、基本対策の遅れが致命傷になります。

## 詳細解説
- 攻撃の期間と規模：2025年12月末〜2026年2月中旬にかけて実行。被害は9機関、数億件の個人情報流出。
- AIの利用法：攻撃者はClaude Codeで侵害中のリモートコマンドの大部分（報告では約75%）を生成・実行し、34セッションで1,088プロンプト、5,317コマンド相当をAIに任せた。一方でGPT‑4.1はリコン（偵察）やデータ解析に利用され、17,550行のPythonスクリプトで305台の内部サーバを解析して2,597件の構造化レポートを自動生成した。
- ツールチェーンとスピード：攻撃者は400超のカスタムスクリプトと、20件の特定CVE向けエクスプロイトをAIで短時間に作成。AIにより「未知のネットワークを数時間で地図化」し、検知窓をすり抜けるタイムラインで活動した。
- 根本原因：使われた脆弱性自体は特別なものではなく、未適用パッチや認証管理の甘さ、ネットワーク分断の欠如など基礎的な脆弱性が原因。AIは「実行力」を劇的に高めただけで、失敗しやすい設計と運用が引き金になった。
- 教訓：AI攻撃はコストを下げ、スピードを上げるため、検知・対応はより迅速で自動化されたものが必要。SIEM/EDRの整備、ログ収集の質向上、APIキー／スクリプトの監査が重要。

## 実践ポイント
- 今すぐ：全サーバ・重要機器のパッチを優先適用（特に公開向け・管理ポート）。  
- 認証：特権資格情報のローテーションと多要素認証の必須化。  
- セグメンテーション：内部ネットワークを最小権限で分割し、横移動を阻止。  
- 検出体制：EDR/IDSとログ収集を強化し、AIによる大量コマンド実行や異常スクリプト実行を検知ルールに追加。  
- 運用：サプライチェーン／委託先のセキュリティ査察、API使用状況の監視、侵害時のテーブルトップ訓練を定期実施。  
- 情報共有：業界横断での脅威インテリジェンス共有と、AI活用攻撃の兆候に関するアップデート受信を設定。

短期的には「基礎の徹底」、中長期では「AIを前提とした検知と自動化」が防御のキモです。あなたの組織でまず何を優先するかを今すぐ確認してください。
