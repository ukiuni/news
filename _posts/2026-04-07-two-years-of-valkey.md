---
layout: post
title: "Two Years of Valkey - Valkeyの2年"
date: 2026-04-07T16:33:48.128Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://redmonk.com/sogrady/2026/04/06/valkey-at-two/"
source_title: "Two Years of Valkey &#8211; tecosystems"
source_id: 1711101728
excerpt: "Valkeyは2年で企業支援と安定開発を確立、移行検討の有力候補に"
image: "http://redmonk.com/sogrady/files/2026/04/01_commit_velocity-1024x809.png"
---

# Two Years of Valkey - Valkeyの2年
Redisフォーク「Valkey」は衰退せず、持続可能な開発体制を築けたのか？

## 要約
Redisのライセンス変更をきっかけに生まれたValkeyは、2年経っても落ち着いたコミット速度と複数企業からの貢献を維持しており、「典型的な衰退するフォーク」とは異なる振る舞いを見せている。

## この記事を読むべき理由
Redisは多くの日本企業でコア技術になっており、ライセンスとコミュニティの変化は採用・運用・法務に直結するため、Valkeyの現状は国内エンジニアやプロダクト責任者にとって重要な判断材料になる。

## 詳細解説
- 発端：RedisがBSDからRSALv2／SSPLv1などのソース可視化（source-available）ライセンスへ移行したことを受け、元コントリビュータがValkeyをフォーク。後にRedisはAGPLへ回帰し、創始者も復帰した。  
- 開発活動の比較：非マージのコミット速度はフォーク直後にValkeyが急増。ピークは持続しないが、過去2年でRedisよりわずかに高い月が多い。  
- 貢献者と組織多様性：Valkeyはフェデレーション的で組織の多様性が高く、活動する個人数もRedisに比べて単位差で上回ることが多い。Gmail等の個人アドレスでのコミットが両プロジェクトで多い点も特徴。  
- 主な企業：Valkey側はAmazonの貢献者数が突出。Aiven、Alibaba、ByteDance、Google、Perconaなども複数名で関与。Redis側は大口利用者による戦略的上流寄与の色が濃い。  
- 限界：コミットデータは利用実態や採用度を示すものではないが、Valkeyは「消えゆくフォーク」ではなく持続可能な開発ペースを確保していると考えられる。

## 実践ポイント
- ライセンス確認：RSAL/SSPL/AGPLなどの違いを法務と合わせて評価する。  
- エコシステム観察：コミット速度だけでなく企業参加の多様性やクラウドベンダーの支援状況を追う。  
- 移行検証：Valkeyへ乗り換える場合は互換性・パフォーマンス・運用手順を事前にテストする。  
- リスク分散：商用サポートやベンダー依存の影響を見越した運用計画を立てる。  
- コミュニティ貢献：自社で使うならIssue・PRで関与してエコシステムに発言力を持つ。

---
