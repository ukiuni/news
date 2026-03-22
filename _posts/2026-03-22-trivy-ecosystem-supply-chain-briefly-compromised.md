---
layout: post
title: "Trivy ecosystem supply chain briefly compromised - Trivyエコシステムのサプライチェーンが一時的に侵害される"
date: 2026-03-22T00:53:26.542Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/aquasecurity/trivy/security/advisories/GHSA-69fq-xp46-6x23"
source_title: "Trivy ecosystem supply chain briefly compromised · Advisory · aquasecurity/trivy · GitHub"
source_id: 47450142
excerpt: "Trivyの公式リリースとアクションが改ざんされ、シークレット窃取の可能性—今すぐ緊急対応を。"
image: "https://opengraph.githubassets.com/0988760f7897540bf66fdee8f66ae98b523eebe201a9e4998076dd8e8aec9f14/aquasecurity/trivy/security/advisories/GHSA-69fq-xp46-6x23"
---

# Trivy ecosystem supply chain briefly compromised - Trivyエコシステムのサプライチェーンが一時的に侵害される
Trivyサプライチェーン乗っ取りの全貌と、今すぐ取るべき5つの対策

## 要約
3月19日に攻撃者が流出した資格情報でTrivy関連リポジトリを改ざんし、Trivy v0.69.4の悪意あるリリース公開、trivy-actionのほぼ全タグ（76/77）を強制プッシュで差し替え、setup-trivyの全7タグを悪意あるコミットに置換しました。機密情報の窃取を目的としたインフォスティーラーが注入されています。

## この記事を読むべき理由
日本の開発/CI環境でもTrivyは広く使われており、同様のワークフロー（GitHub Actions・パッケージレジストリ・コンテナ）を使う組織は即時対応が必要だからです。

## 詳細解説
- 何が起きたか：攻撃者は漏洩したトークンで
  - Trivyのリリースを改ざん（v0.69.4に悪意あるバイナリ・イメージを配置）
  - trivy-actionのタグを多数強制プッシュしてentrypoint.shに情報窃取コードを注入
  - setup-trivyの全タグを悪意あるコミットに置換
- 侵害の根本原因：2月末に始まった供給連鎖攻撃後の資格情報ローテーションが「原子的」でなく、ローテーション期間中に有効トークンで機密を持ち出せた可能性があること
- 悪意あるコードの挙動（trivy-action / setup-trivy共通）
  - /proc/<pid>/mem を使ったランナーのメモリダンプでシークレット抽出
  - SSH鍵、AWS/GCP/Azure資格情報、Kubeトークン、Docker設定、.env、DB資格情報、暗号資産ウォレット等をファイルパスから収集
  - AES-256-CBC + RSA-4096 のハイブリッド暗号で暗号化して外部に送信
  - 送信失敗時かつ INPUT_GITHUB_PAT が設定されている場合、被害者アカウントに公開リポジトリ（tpcp-docs）を作成しリリースアセットとして盗んだデータを上げるフォールバック機能
- 配布経路：GHCR、ECR Public、Docker Hub、deb/rpm、get.trivy.dev 等、多チャネルで配布
- 影響範囲と安全版：
  - Trivyバイナリ：悪意ある v0.69.4（最新タグも影響）。安全版は v0.69.2 / v0.69.3
  - trivy-action：0.0.1–0.34.2 のうち76タグが書き換え済。安全版は v0.35.0（またはコミットSHA固定）
  - setup-trivy：全7タグが書き換え。安全版は v0.2.6（安全コミットで再作成）
- 被害確認の目安：2026-03-19 〜 03-20 のワークフロー実行ログ、tpcp-docs の存在、リポジトリやランナー上の不審なアーティファクト

## 実践ポイント
- まず安全版へ差し戻す（即時）
  - trivy: v0.69.2 または v0.69.3
  - trivy-action: v0.35.0 もしくはコミットSHA
  - setup-trivy: v0.2.6（再作成済）
- すべての可能性あるシークレットを即ローテーション（公開済みのアーティファクトが実行された可能性がある場合は必須）
- ワークフロー監査
  - aquasecurity/trivy-action や aquasecurity/setup-trivy をタグ指定で参照していないか確認。タグ指定なら 2026-03-19〜20 の実行ログを精査
  - 可能な限り GitHub Actions をフルコミットSHAでピン留めする
- アーティファクトの監査
  - tpcp-docs 等の不審な公開リポジトリを検索
  - 影響のある trivy バイナリ/イメージを取得していないか確認し、あれば削除
- アーティファクト検証（cosign / rekor の例）
  - バイナリ検証（例）
  ```bash
  # bash
  curl -sLO "https://github.com/aquasecurity/trivy/releases/download/v0.69.2/trivy_0.69.2_Linux-64bit.tar.gz"
  curl -sLO "https://github.com/aquasecurity/trivy/releases/download/v0.69.2/trivy_0.69.2_Linux-64bit.tar.gz.sigstore.json"
  cosign verify-blob \
    --certificate-identity-regexp 'https://github\.com/aquasecurity/' \
    --certificate-oidc-issuer 'https://token.actions.githubusercontent.com' \
    --bundle trivy_0.69.2_Linux-64bit.tar.gz.sigstore.json \
    trivy_0.69.2_Linux-64bit.tar.gz
  ```
  - コンテナ署名確認（例）
  ```bash
  # bash
  cosign verify \
    --certificate-identity-regexp 'https://github\.com/aquasecurity/' \
    --certificate-oidc-issuer 'https://token.actions.githubusercontent.com' \
    --new-bundle-format \
    ghcr.io/aquasecurity/trivy:0.69.2
  ```
- 今後の対策（推奨）
  - CI用トークンの最小権限化とローテーションの原子的運用
  - サードパーティActionはコミットSHA固定もしくはレジストリのダイジェストで参照
  - ワークフロー監視と異常検出（実行時アウトバウンド接続や不審なリポジトリ作成をアラート）

以上。早急にワークフローとシークレット管理を点検し、必要なローテーションと署名検証を行ってください。
