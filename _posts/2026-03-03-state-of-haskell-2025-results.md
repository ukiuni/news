---
layout: post
title: "State of Haskell 2025 results - Haskellの現状（2025）調査結果"
date: 2026-03-03T00:18:04.023Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://discourse.haskell.org/t/state-of-haskell-2025-results/13755"
source_title: "State of Haskell 2025 results - Haskell Foundation - Haskell Community"
source_id: 393599505
excerpt: "若手増・ghcup/Cabal成熟でHaskellが実務導入の本命に"
image: "https://us1.discourse-cdn.com/flex002/uploads/haskell/original/1X/89166504e40f4869ea825dd70048017861ec8578.png"
---

# State of Haskell 2025 results - Haskellの現状（2025）調査結果
Haskellは“古参だけの言語”じゃない──新規ユーザー増とエコシステム成熟の兆し

## 要約
Haskell Foundationの2025年調査は回答数が増加し、若手ユーザーの割合増、GHCやインストール周りの改善、Cabal/Nixの台頭などエコシステムの変化が明確になった。

## この記事を読むべき理由
日本でも関心が高まる関数型言語採用や社内導入検討にあたり、現状の採用率・ツールチェーン・障壁が一目で分かるため、技術方針や学習投資の判断材料になる。

## 詳細解説
- 調査規模とユーザー層  
  - 回答約1,413件。Haskell利用者は約72%で、非利用者も増加。過去より回答者数が増えており関心の広がりを示す。  
  - 利用継続期間では「6年未満」が約49%と、近年（COVID以降）に入門したユーザーが多い。  
- 仕事での利用状況  
  - 「職場で使っている（常・時々）」が合わせて約49%で、産業利用は着実に存在。ただし「使いたいが使えていない」層も約43%あり社内説得や導入支援が課題。  
- ツール／コンパイラ動向  
  - GHCが圧倒的（約99%）。MicroHSなど新顔も少数存在。  
  - インストール方法はghcup（約63%）とNix（約42%）が成長。ghcup普及でGHC導入が簡便になった影響が大きい。  
  - GHCのアップグレードでコードが壊れた経験は約27%にとどまり、以前より安定化傾向。  
- ビルドとバージョン分布  
  - ビルドツールはCabalが約84%と優勢、Stackは約40%、Nixも約39%で主要ツールに。CabalとStackの勢力図が逆転しつつある。  
  - GHC 9.10〜9.12の利用が多く、バージョン分布が一極化している（アップグレードが進む好転サイン）。  
- コミュニティとニーズ  
  - オンライン交流はReddit/Discourse/GitHubが中心。Discourseが実質的ハブ化。  
  - ユーザーがもっと読みたいテーマは「ベストプラクティス（63%）」「設計パターン（51%）」「パフォーマンス解析（46%）」など、実務志向のコンテンツ需要が高い。

## 実践ポイント
- 学ぶべき優先順位：まずGHC+ghcupでローカル環境を整え、Cabal/Nixの基本を抑える。  
- 企業導入を目指す個人：社内向けケーススタディ（小〜中規模の成功例）と移行コストの定量化で説得力を高める。  
- 日本のコミュニティ活動：DiscourseやGitHubで英語情報を追いつつ、国内向けに「ベストプラクティス翻訳・事例集」を作る価値が大きい。  
- アップグレード対策：依存関係管理と再現可能ビルド（Nixやロックファイル）を導入して、GHC更新による破壊を低減する。

参考：調査は生データ公開あり（詳細解析は原典参照を推奨）。
