---
layout: post
title: "Italy Fines Cloudflare €14 Million for Refusing to Filter Pirate Sites on Public 1.1.1.1 DNS - イタリアがCloudflareに公衆DNSの海賊版サイト未遮断で€1420万の罰金"
date: 2026-01-09T13:28:58.416Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://torrentfreak.com/italy-fines-cloudflare-e14-million-for-refusing-to-filter-pirate-sites-on-public-1-1-1-1-dns/"
source_title: "Italy Fines Cloudflare €14 Million for Refusing to Filter Pirate Sites on Public 1.1.1.1 DNS * TorrentFreak"
source_id: 468549611
excerpt: "イタリアがCloudflareに1.1.1.1遮断拒否で約€1425万の罰金、DNS運用に波及か"
image: "https://torrentfreak.com/images/fea-dark-clouds.jpg"
---

# Italy Fines Cloudflare €14 Million for Refusing to Filter Pirate Sites on Public 1.1.1.1 DNS - イタリアがCloudflareに公衆DNSの海賊版サイト未遮断で€1420万の罰金

世界の”1.1.1.1”が標的に——Cloudflareに史上級の罰金、あなたのネット運用にも影響する理由

## 要約
イタリアの通信規制当局AGCOMが、Cloudflareが公衆DNS「1.1.1.1」で海賊版サイトの遮断要請に従わなかったとして約€14.25Mの罰金を課した。AGCOMはCloudflareが遮断措置に協力すべき重要な事業者だと判断した。

## この記事を読むべき理由
- 日本でも多くの事業者や開発者がCloudflareやパブリックDNS、CDN、VPNを利用しており、この判例的な制裁は運用・法務・ユーザープライバシーのバランスに直接関わるため。  
- DNSレイヤでのブロッキングが世界的な技術・ビジネス慣行にどんな影響を与えるかを知ることで、サービス設計やコンプライアンス対応の優先順位が見えてくる。

## 詳細解説
- 背景：イタリアは2024年に「Piracy Shield」と呼ばれる迅速な海賊版対策を導入。ライブスポーツ等の違法配信に対応するため、ドメインやIPの遮断を30分以内に実行できる権限を持つ。運用の過程で正当なサイトの「オーバーブロッキング」報告も相次いだ。  
- 問題の核心：AGCOMは2025年2月の命令（Order 49/25/CONS）で、DNSプロバイダやVPNに対し指定リストのドメイン/IPの名前解決遮断やトラフィック遮断を求めた。Cloudflareは自社の公衆DNS（1.1.1.1）での遮断を拒否。理由として「世界中で発生する数十億のクエリに対しフィルタリングを入れると遅延などでサービス品質を損ねる」「実装は不合理／過度である」と主張した。  
- AGCOMの判断：規制当局はCloudflareが高度なトラフィック管理能力とリソースを持ち、遮断は技術的に可能だと反論。Cloudflareのサービスが遮断回避に寄与している点も指摘し、同社の不履行を理由に€14,247,698（同社の世界収益の約1%）の罰金を科した。法的には最大2%まで認められる。  
- 意義と余波：AGCOMは同種の罰則としては最大級とし、Cloudflareが対象サイトの約70%に関与していると報告。Cloudflareは異議申し立て（控訴）を行う見込みで、Google Public DNSや他のDNS事業者にも波及する可能性がある。さらに、透明性や手続き上の問題点を巡る論争も継続中。

## 実践ポイント
- 技術運用者（SRE/ネットワーク）向け
  - DNSレベルのフィルタリング設計を見直す：影響範囲を可視化し、意図しないオーバーブロッキングを防ぐためのテスト環境とロールバック手順を整備する。  
  - レイテンシと可用性の対策：フィルタリングによる遅延を最小化するためのキャッシュ戦略や分散実装、サーキットブレーカー設計を検討する。  
- プロダクト／法務向け
  - 事業継続計画に法的リスクを組み込む：海外当局からの遮断命令や罰則リスクを事業リスク評価に入れ、対応フロー（通知、異議申立て、透明性報告）を定義する。  
  - ユーザー透明性の確保：ユーザーや顧客に対する遮断方針、影響説明、ログ／監査の開示ルールを整備する。  
- 日本市場への示唆
  - 日本のISPやクラウド事業者も同様の要請に直面する可能性があるため、国内での運用ポリシー整理、規制対応チームの準備、国際的な事例を踏まえた社内ガイドライン作成が有効。

今回の事例は「大規模なパブリックインフラだから遮断は無理だ」という論法と、「重要事業者だからこそ協力が求められる」という規制側の主張が真正面から衝突した典型です。技術的対応と法的・倫理的判断をどう折り合いをつけるかが、今後グローバルに問われ続けます。
