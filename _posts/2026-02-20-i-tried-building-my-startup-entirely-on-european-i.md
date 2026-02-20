---
layout: post
title: "I tried building my startup entirely on European infrastructure - スタートアップをEUインフラだけで全部構築してみた"
date: 2026-02-20T10:05:10.573Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.coinerella.com/made-in-eu-it-was-harder-than-i-thought/"
source_title: "&quot;Made in EU&quot; - it was harder than I thought."
source_id: 47085483
excerpt: "EU限定インフラで起業しデータ主権とコスト優位を得つつ、メール配信やCI移行などの具体策を提示"
image: "https://images.unsplash.com/photo-1608817576203-3c27ed168bd2?crop&#x3D;entropy&amp;cs&#x3D;tinysrgb&amp;fit&#x3D;max&amp;fm&#x3D;jpg&amp;ixid&#x3D;M3wxMTc3M3wwfDF8c2VhcmNofDF8fGV1cm9wZXxlbnwwfHx8fDE3NzE0MDQ5Mjl8MA&amp;ixlib&#x3D;rb-4.1.0&amp;q&#x3D;80&amp;w&#x3D;2000"
---

# I tried building my startup entirely on European infrastructure - スタートアップをEUインフラだけで全部構築してみた
EUオンリーで作ったら想像より大変だったが、データ主権とコストで得た“勝ち筋”の話

## 要約
著者はAWSなど米国ハイパースケーラーを避け、ヨーロッパのサービスだけでプロダクトを構築。成功はしたが、想定外の摩擦（メール配信、GitHub離脱、TLD価格など）と米国依存から完全には逃れられなかった。

## この記事を読むべき理由
- EUインフラの実運用で直面する実務的な課題と回避策が分かる。  
- GDPRやデータ主権を重視する日本企業／開発者が取るべき現実的な選択肢を知れる。

## 詳細解説
- 採用スタック（主要プロバイダ）
  - Hetzner：コア計算（VM、LB、S3互換ストレージ）。コスト性能が高い。  
  - Scaleway：Transactional Email、コンテナレジストリ、観測系、ドメイン等の補完。  
  - Bunny.net：CDN・分散ストレージ・画像最適化・WAF・DDoS対策。エッジ性能が高い。  
  - Nebius：欧州で使えるGPU推論。フロンティアAIはまだ米国依存が強い。  
  - Hanko：ドイツ発の認証（パスキー・SNSログイン・ユーザ管理）。認証レイヤーを欧州に残せる。  
- 自己ホスティング群（Kubernetes + Rancher）
  - Gitea（ソース管理）、Plausible（解析）、Twenty CRM、Infisical（シークレット）、Bugsink（エラー追跡）などを自ホスティング。自由度とデータコントロールが上がるが運用コストが増大。
- 想定外に難しかった点
  - トランザクショナルメール：Deliverability・価格・開発者体験で米サービスに分がある。EU選択肢はエコシステムが薄い。  
  - GitHub離脱：Actionsや統合ワークフローが無い分CI/CD・ワークフローを再設計する必要。  
  - ドメインTLDの価格差：一部TLDがEUレジストラで2–3倍に跳ねる事例あり。理由が不透明。
- どうしても避けられない米国依存
  - モバイル配信（App Store / Play Store）、広告配信（Google Ads）、一部フロンティアAI（Anthropicなど）、およびSNS認証のOAuthフロー（Google/Apple）は実質的に米国サービス経由になる。

## 実践ポイント
- 初期判断：ターゲットがEU中心ならHetzner＋Bunny.net＋Scalewayでコスト・遅延優位を得やすい。  
- 認証戦略：Hanko等でユーザ管理をEUに置きつつ、SNSログインは補完として残す（UXとのトレードオフ）。  
- メール戦略：TEMは候補を比較し、必ず配達率テスト（SPF/DKIM/DMARC含む）とテンプレート要件を確認する。  
- Git移行計画：Gitea移行時はCI/CD、PRフロー、統合ツールの代替を一覧化して段階的移行する。  
- 運用コスト見積：自ホスティングは運用工数が増えるためSRE/運用時間のコストを事前に組み込む。  
- TLD購入前に複数レジストラの価格比較を実施すること（EU特有の価格差に注意）。  
- ハイブリッドで現実解を採る：完全排除を目指すより、データ主権が重要な部分をEU化して、不可避な依存は限定的に許容する。

短評：EUオンリーは「技術的に可能」であり、データ主権・コスト面でメリットも大きい。ただしエコシステムの薄さと運用負荷を見越した現実的な設計が必須。
