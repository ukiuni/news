---
layout: post
title: "What has Docker become? - Dockerは何になったのか?"
date: 2026-01-23T13:47:09.974Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://tuananh.net/2026/01/20/what-has-docker-become/"
source_title: "What has Docker become? - Tuan-Anh Tran"
source_id: 46731748
excerpt: "コンテナの覇者DockerはAI・セキュリティへ舵を切り、ビジネスモデルとベンダーリスクが問われる"
---

# What has Docker become? - Dockerは何になったのか?
魅力的なタイトル: Dockerは迷走か再出発か――コンテナ時代を作った会社の“次の一手”を読み解く

## 要約
Dockerは技術としては不可欠になった一方、企業としては複数回の戦略ピボットを繰り返しており、現在は開発者ツール・AI・セキュリティといった分野に進出しているが、ビジネスモデルは不透明だ。

## この記事を読むべき理由
日本のプロダクト開発・SRE・クラウド導入担当者にとって、Dockerの方針変化はツール選定・セキュリティ戦略・ベンダーリスクに直結するため、今後の対策を考えるうえで必読の内容です。

## 詳細解説
- アイデンティティの危機  
  Dockerはコンテナという標準を作り「インフラになった」結果、コア技術の直接収益化が難しくなった。結果として会社は何を売るかで迷走している。

- Swarmの撤退  
  Kubernetesに市場を譲り、オーケストレーションのフルスタック路線を断念。Swarm売却は「プラットフォーム化」は諦め、差別化領域へ集中する決定の表れ。

- 開発者ツールへの軸足  
  Atomist買収から生まれたDocker Scout（ソフトウェアサプライチェーン可視化）やTestcontainers系の機能獲得で、開発体験とシフトレフトの価値を強化。これは開発現場での効率化とセキュリティ向上に直結する動き。

- AIへの大きな舵取り  
  Docker Model Runner、ComposeのAI対応、OffloadによるGPU実行など、AIモデル実行プラットフォーム寄りの戦略を採用。大手クラウド（GCP、Azure）との連携やAI向けSDKとの統合も進む。

- セキュアイメージの公開（Hardened Images）  
  Chainguardの台頭に対抗し、2025年末に1,000超の「Docker Hardened Images」をApache 2.0で無料公開。脆弱性低減を訴求する一方で、無料化が収益モデルに与える課題は残る。

- 経営交代と買収観測  
  CEO交代など経営面の動きから、買収（大手クラウドによる吸収）を視野に入れた動きと見る向きもある。独立屋台骨の構築よりは出口戦略の色が濃くなっている可能性。

## 実践ポイント
- 依存度を可視化する：社内でDocker依存サービスと商用機能の使用状況を棚卸しする。  
- 代替技術を評価する：podman / containerd / OCI準拠ツールやChainguardのようなセキュアイメージを検討。  
- 画像サプライチェーン対策：Docker Scout相当のSBOM／脆弱性スキャン導入とCIへの組み込みを進める。  
- テストの現実感向上：Testcontainersなどで統合テストを本番環境に近づける。  
- AIワークロードの設計：GPUオフロードやモデル実行の運用要件を事前に調査し、クラウド連携のコスト／運用性を評価する。  
- ベンダーリスク管理：Docker Inc.の戦略変化がサービス提供に与える影響を想定し、買収や機能廃止シナリオの対応計画を用意する。

（出典：Tuan-Anh Tran「What has Docker become?」の要旨を翻訳・再構成）
