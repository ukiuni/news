---
layout: post
title: "Almost Every infrastructure decision I endorse or regret after 4 years -（ほとんどの）4年間で支持した／後悔したインフラ判断"
date: 2026-02-20T07:55:35.878Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://cep.dev/posts/every-infrastructure-decision-i-endorse-or-regret-after-4-years-running-infrastructure-at-a-startup/"
source_title: "(Almost) Every infrastructure decision I endorse or regret after 4 years running infrastructure at a startup · Jack's home on the web"
source_id: 47043345
excerpt: "AWS/EKS/RDSの採用と後悔を4年分の実践で赤裸々に解説"
---

# Almost Every infrastructure decision I endorse or regret after 4 years -（ほとんどの）4年間で支持した／後悔したインフラ判断
スタートアップの現場で学んだ「やってよかった／やらなきゃよかった」インフラの教訓 — 日本のチームが直面する課題に役立つ実践まとめ

## 要約
著者は、スタートアップで4年インフラを回した中での主要な選択肢を振り返り、推奨するものと後悔したものを整理している。クラウド選定から運用プロセス、コスト管理まで実務的な示唆が多い。

## この記事を読むべき理由
日本のプロダクト／インフラ担当は、限られた人員でスピードと安定性を両立させる必要がある。本記事は具体的なサービス選び（AWS/EKS/RDSなど）や運用ルール、コスト管理の実践的ノウハウを短期間で学べる。

## 詳細解説
- クラウド選定（AWS vs GCP）  
  著者はAWSを支持。サポートの手厚さ、安定性、既存サービスとの連携が決め手。Kubernetes周りの統合が進んだ今、EKSが現実的選択に。

- EKSとアドオン運用  
  EKS自体は推奨。ただし「EKS managed addons」はカスタマイズ困難で後悔。代わりにHelmチャートと既存のGitOpsワークフローに合わせると管理しやすい。

- データ基盤（RDS, ElastiCache）  
  RDSは高コストだがデータ損失回避の価値が大きく推奨。Redis（ElastiCache）もキャッシュ以上の用途で有効。マネージドを選ぶことで運用負荷を軽減。

- コンテナレジストリと接続性  
  quay.ioは不安定で、ECRへ移行して安定・権限連携が楽になったという経験。

- ネットワークとVPN  
  単純明快なVPNを評価。Okta等ID基盤と組み合わせると運用がスムーズ。

- サポート契約（AWS Premium Support）  
  高コストで後悔。社内のAWS知見が薄ければ価値はあるが、費用対効果は要検討。

- アカウント管理（Control Tower + AFT）  
  Account Factory for Terraform導入でアカウント作成・タグ標準化が自動化され運用が楽に。

- インシデント運用とプロセス  
  Slackボットでポストモーテムのリマインド自動化は効果大。PagerDutyのテンプレート活用と定期的なアラートレビュー（月〜隔週）はノイズ低減に寄与。Datadog/PagerDutyのポストモーテム機能はカスタマイズ性が低く、Notion等のWiki的ツールを推奨。

- FaaSの採用不足  
  GPUワークロードでFaaSは難しいが、CPUバースト的な処理はLambda等をもっと活用すべき。コスト比較は単純に24/7のインスタンスと比べない点が重要。

- GitOpsとCI/CD  
  GitOpsは柔軟で推奨。ただし「デプロイされない理由」が分かるツール投資は必要。GitHub ActionsはMarketplaceが豊富で採用価値ありだが、セルフホストランナーの統合は改善余地あり。

- コスト管理  
  月次でSaaS・クラウドコストをエンジニアと経理でレビューすることを推奨。タグ＋アカウント＋サービスでボトルネックを可視化する。

- 組織・SaaS選定  
  早期にIdP（例：Okta）を採用すべき。Notionはドキュメント管理で高評価。Slackは運用ルール（スレッド活用／公開チャネル重視）で雑音を減らす。JIRAよりLinearが好評。

- アーキテクチャの注意点  
  複数アプリで単一DBを共有するのは「誰も責任を持たないDB」を生みやすく後悔の元。ドメインごとのDB所有や運用方針を決めるべき。

- ツール別のコスト・トレードオフ  
  Datadogは高機能だがKubernetesの短周期スケールやGPUノードでコストが肥大化する。計測粒度と価格モデルのマッチを確認。

## 実践ポイント
- まずはマネージドサービス（RDS, ElastiCache, ECR, EKS）を優先して運用コストを削減する。  
- EKSのアドオンはManagedに頼り切らず、Helm + GitOpsでカスタマイズ可能にする。  
- 早期にIdP（Okta等）を導入しSaaS選定を統一する。  
- 月次でエンジニア＋経理によるコストレビューを実施する（タグで分析）。  
- インシデント運用はテンプレート＋Slackボットで自動化し、定期的にアラートを見直す。  
- 共有DBは避けるか、所有権・ライフサイクルルールを明確化する。  
- CPUバースト系はLambda検討、GPU系は専有リソースで設計する。  
- ドキュメントとポストモーテムはNotion等の柔軟なツールに一元化する。

短い経験則としては「運用の単純さとサポートの手厚さを優先し、必要なところだけ自分たちでカスタマイズする」姿勢が実務で効く、という点が核です。
