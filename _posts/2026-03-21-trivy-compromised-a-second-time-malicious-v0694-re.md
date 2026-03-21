---
layout: post
title: "Trivy Compromised a Second Time - Malicious v0.69.4 Release - Trivyが再び侵害、悪意ある v0.69.4 リリース"
date: 2026-03-21T02:34:34.136Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.stepsecurity.io/blog/trivy-compromised-a-second-time---malicious-v0-69-4-release"
source_title: "Trivy Compromised a Second Time - Malicious v0.69.4 Release, aquasecurity/setup-trivy, aquasecurity/trivy-action GitHub Actions Compromised - StepSecurity"
source_id: 1586120175
excerpt: "Trivyが再びマルウェア化、CI経由で秘密情報が大量流出の危険"
---

# Trivy Compromised a Second Time - Malicious v0.69.4 Release - Trivyが再び侵害、悪意ある v0.69.4 リリース
再び狙われたTrivy―あなたのCI/CDは感染していないか？

## 要約
人気のOSS脆弱性スキャナー「Trivy」が2度目の侵害を受け、v0.69.4にマルウェアが仕込まれて配布されました。さらにTrivy関連のGitHub Actions（setup-trivy / trivy-action）にも強力な資格情報窃取コードが注入され、広範なCI被害が確認されています。

## この記事を読むべき理由
Trivyは日本の多くの企業・OSSプロジェクトで使われており、CI経由で秘密情報やクラウド資格情報が流出するリスクが現実になりました。CI/CDを使う開発者・運用者は直ちに影響範囲と対策を確認する必要があります。

## 詳細解説
- 何が起きたか：3月19日にTrivyの自動リリースがv0.69.4として公開され、その実行ファイルが外部C2ドメインへ通信するマルウェアを含んでいました。2月28日の「hackerbot-claw」による最初の侵害（PAT窃取→リポジトリ乗っ取り）の後に再攻撃が行われています。  
- 影響範囲：Trivy本体だけでなく、CIでTrivyをインストール／実行するためのGitHub Actions（aquasecurity/setup-trivy、aquasecurity/trivy-action）にも同様の窃取ペイロードが注入。これらのActionはRunnerの環境やメモリを読み出し、SSH鍵、クラウド資格情報、Kubernetesシークレット、ウォレット鍵、Terraform状態など大量の機密を収集・暗号化して外部へ送信します。  
- 手口の特徴：悪意あるコミットはフォーク由来でタグが差し替えられる手口を利用。exfiltrationはまずtyposquatドメイン（scan.aquasecurtiy.org）へ送信、失敗時は被害者のアカウントに公開リポジトリ（tpcp-docs）を作成してデータをアップロードするフェールバックを持ちます。  
- 検出と対応：StepSecurityのHarden-Runnerはワークフローのネットワーク行動差分で異常通信（C2）を検出し、Homebrewは緊急でv0.69.3へロールバック。setup-trivyはタグを削除してクリーンなv0.2.6のみを残す対応がとられました。

## 実践ポイント
- 直ちにやること：aquasecurity/trivy-action と aquasecurity/setup-trivy の使用を停止。Trivy本体はv0.69.3（Homebrewのロールバック版）やプロジェクトが提示するクリーンなタグに戻す。  
- シークレット対応：CIで使うPAT、SSH鍵、クラウド（AWS/GCP/Azure）キー等を全て疑ってローテーション。GitHub側のトークンも再発行・無効化を検討。  
- 検査方法：ワークフロー実行ログにscan.aquasecurtiy.orgへの接続や、tpcp-docsのような不審な公開リポジトリ作成履歴がないか確認。Runnerログで不審なプロセス（メモリ読み取り）やbase64デコーダの実行を探す。  
- 予防策：外部Contribution向けに pull_request_target を避ける、ActionsはSHA固定（ダイジェスト）でピン留め、信頼できるソースのみ使用、可能なら自己管理Runnerや短命トークン・OIDCでの最小権限付与を徹底する。  
- 日本企業向け補足：日本のOSS／商用プロジェクトでもTrivy導入が進んでいるため、CIポリシーと監視（外部への不審通信の検出、ワークフロー差分監査）を早急に見直してください。

この記事を受け、CIの安全性を今一度チェックし、疑わしい実行履歴や外部通信を洗い出すことを強くおすすめします。
