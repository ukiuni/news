---
layout: post
title: "Show HN: AWS-doctor – A terminal-based AWS health check and cost optimizer in Go - ターミナルで動くAWSの健康診断ツール「aws-doctor」"
date: 2026-01-19T06:41:21.617Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/elC0mpa/aws-doctor"
source_title: "GitHub - elC0mpa/aws-doctor: Diagnose AWS costs, detect idle resources, and optimize cloud spending directly from your terminal. 🩺 ☁️"
source_id: 46675092
excerpt: "ターミナルで即座にAWSの無駄を可視化し、コスト削減策を提示するGo製CLIツール"
image: "https://opengraph.githubassets.com/936c805c72cf500f092959f33432c90d9cb656643d7416470eafe1c4ed93b35e/elC0mpa/aws-doctor"
---

# Show HN: AWS-doctor – A terminal-based AWS health check and cost optimizer in Go - ターミナルで動くAWSの健康診断ツール「aws-doctor」
ターミナルだけでAWSの無駄を発見し、コスト最適化の第一歩を踏み出せる無料ツール

## 要約
Go製のCLI「aws-doctor」は、請求データの比較や6ヶ月トレンド解析、未使用リソースの検出などをターミナルから実行でき、AWS Trusted Advisorの一部機能をサポートプランなしで代替します。

## この記事を読むべき理由
日本の企業・スタートアップでもAWS利用が広がる中、クラウドコストの無駄削減は直接的な利益に結びつきます。コンソールを開かずに素早く診断できるツールは、運用負荷を下げつつコスト意識を高める実務的価値があります。

## 詳細解説
- 概要  
  aws-doctorはGoで書かれたCLIツールで、ターミナルからAWSアカウントをスキャンして「どこでお金が無駄になっているか」を可視化します。MITライセンスで公開されており、ローカルやCI上で簡単に導入できます。

- 主な機能  
  - コスト比較：同じ期間（例：1月1日–15日と2月1日–15日）で前月比を比較し、支出の「速度」を評価。  
  - トレンド解析：過去6か月のコスト推移を可視化し、長期的な異常を発見。  
  - Waste（無駄）検出：「ゾンビ」リソースや料金を無駄にしている構成を自動検出。検出対象の代表例は以下。  
    - 未アタッチのEBSボリューム  
    - 停止中インスタンスにアタッチされたEBS  
    - 未関連のElastic IP  
    - 期限切れ／間もなく期限切れのリザーブドインスタンス  
    - 30日以上停止しているEC2インスタンス  
    - ターゲットグループがないロードバランサー  
    - 非アクティブなVPCインターフェイスエンドポイント／NATゲートウェイ  
    - アイドルなロードバランサーやRDSインスタンス  
  - 設定フラグ：--profile（AWSプロファイル指定）、--region、--trend、--waste などで柔軟に実行可能。

- 技術的背景  
  Go製のためバイナリ配布やCI統合が容易で、クロスプラットフォームで動作します。AWSの課金系・リソースAPI（Cost Explorerや各種リソース情報）を組み合わせ、コンソールの生データに対して文脈を与える診断を行います。Trusted Advisorの有料提案を補完する目的で作られており、特にサポートプランに予算を割けないチームに有益です。

- 現状とロードマップ  
  現在はトレンド解析と無駄検出が実装済み。将来的にCSV/PDFエクスポートや各OSディストリ用の配布パッケージ化が予定されています。

## 実践ポイント
1. インストールと基本実行（例）  
```bash
go install github.com/elC0mpa/aws-doctor@latest
aws-doctor --profile myprofile --region ap-northeast-1 --trend --waste
```

2. まずは非本番アカウントで試す  
   読み取り系APIで動きますが、初回は権限と出力内容を確認するためにSandboxや監査用アカウントで実行しましょう。

3. 定期実行の組み込み  
   CIや社内運用用のスケジュール（例：週次ジョブ）に組み込み、自動レポート（将来的にCSV/PDF出力予定）で経営・開発チームに共有すると効果的。

4. 優先対応の判断基準  
   コストインパクト（￥/month）と運用リスク（停止して影響が出るか）で優先順位を付け、まずは低リスクで高効果な「未アタッチEBS」「未関連Elastic IP」などからクリーンアップ。

5. 日本市場での活用アイデア  
   - マルチアカウント体制が多い企業ではアカウント単位でスキャンしてダッシュボードに集約。  
   - スタートアップはサポートプランに頼らずコスト診断を自動化してキャッシュを確保。  
   - SIerやクラウド運用チームは初回導入で顧客の「見落とし」を短時間で発見できるツールとして利用可能。

短時間で導入でき、まずは「何が無駄か」を把握するのに向いたツールです。興味があれば公式リポジトリでREADMEや検出ロジックを確認し、社内運用にどう組み込むかを検討してみてください。
