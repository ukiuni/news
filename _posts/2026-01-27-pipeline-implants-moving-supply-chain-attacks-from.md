---
layout: post
title: "Pipeline Implants: Moving Supply Chain Attacks from Dependencies to the CI/CD Runner - 依存関係からCI/CDランナーへ：サプライチェーン攻撃の最前線"
date: 2026-01-27T12:12:15.667Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://instatunnel.my/blog/pipeline-implants-moving-supply-chain-attacks-from-dependencies-to-the-cicd-runner"
source_title: "Pipeline Implants: Hijacking CI/CD Runners in Supply Chain | InstaTunnel Blog"
source_id: 416317618
excerpt: "CI/CDランナーを狙うパイプラインインプラントが秘密流出とビルド汚染を実現する手口と対策"
image: "https://i.ibb.co/rRJ63S7T/Pipeline-Implants-Moving-Supply-Chain-Attacks-from-Dependencies-to-the-CICD-Runner.png"
---

# Pipeline Implants: Moving Supply Chain Attacks from Dependencies to the CI/CD Runner - 依存関係からCI/CDランナーへ：サプライチェーン攻撃の最前線
あなたのビルドが襲われる日：CI/CDランナーを狙う「パイプラインインプラント」がもたらす現実的な危機

## 要約
サプライチェーン攻撃の重心が「ライブラリ」から「ビルドを行うCI/CDランナー」へ移行している。攻撃者はPR経由でパイプライン内のスクリプトを改変し、秘密情報の窃取やプロダクションアーティファクトへのバックドア埋め込みを行う。

## この記事を読むべき理由
日本の開発チームもGitHub ActionsやGitLab CI、自己ホストRunnerを広く利用しており、CI/CDが侵害されるとクラウド資産・パッケージ公開権限・プロダクト整合性が一挙に危険に晒されるからです。国内のOSS利用やクラウド移行が進む今こそ対策が急務です。

## 詳細解説
- 背景：従来は悪意ある依存パッケージが主流だったが、SCA/SASTで防御が進むと攻撃者はより上流の「ビルド基盤」を狙うようになった。CI/CDランナーはデプロイ権限やシークレットを持ち、「短時間で痕跡が消える」ため格好の標的となる。  
- Poisoned Pipeline Execution (PPE)：パイプライン設定や参照スクリプトを改変してランナー上で任意コードを実行させる攻撃手法。主に3種類ある：  
  1. Direct PPE：workflow YAML自体をPRで改変してコマンド実行。  
  2. Indirect PPE：YAMLは保護されていても参照するスクリプト（npmスクリプト、Makefile等）を改変して実行。  
  3. Public PPE：外部PRで自動実行されるOSSリポジトリに対する典型的手口。  
- 攻撃の流れ（簡略）：攻撃者がPRを送る → ランナー上で環境変数やトークンを外部に送信（exfiltrate） → ビルド成果物（Dockerイメージやバイナリ）に小さなバックドアを埋め込んで署名・プッシュ。結果、信頼されたまま汚染されたアーティファクトが本番へ。  
- pull_request_targetの危険性：権限が高いコンテキストで外部PRのコードをチェックアウトすると、リポジトリのシークレットを使って悪意あるコードが走る重大なミスコンフィグになる。  
- なぜ危険か：コードレビューやSCAではビルドスクリプトの一行や外部コマンドに気づきにくく、ランナーの痕跡は短命でフォレンジックが困難。結果として「何が本当にビルドされたか」を証明できなくなる。

## 実践ポイント
- 最小権限（PoLP）を徹底：ランナーに永続的なアクセスキーを置かず、GitHub ActionsならOIDCで短期トークンを使用する。permissionsキーでGITHUB_TOKENの権限を限定。  
- ワークフローのトリガーを安全に：pull_request_targetを安易に使わない。外部コントリビュータ用PRはCI実行前に承認を必須化する。  
- スクリプト保護とレビューポリシー：.github/workflowsやビルドスクリプトの変更にはCode Ownersやセキュリティチームの承認を要求。  
- アクションやツールの固定：uses: actions/checkout@v3 のような参照はSHA固定（フルハッシュ）で使用し、サードパーティActionの改ざんリスクを下げる。  
- ネットワーク分離とEgress制限：自己ホストRunnerはVPC内に置き、外向き通信を許可先に限定。ビルド中の異常な外部通信を監視する。  
- アーティファクトの署名と検証：Sigstore/Cosign等でビルド結果に署名を付与し、デプロイ前に検証する。  
- 可視化と検出：SSPM/SSCSツールで「影のランナー」「過剰なIAMロール」「危険なスクリプト」を検出し、SLSA等の基準に合わせる。  
- ログ監査とシークレットローテーション：ビルドログの外向き通信を監査し、侵害が疑われたらトークンを速やかに無効化・ローテーションする。

短期的にはワークフローと参照スクリプトのレビュー強化、OIDC導入、ActionsのSHA固定、外部PRの承認運用をまず実施してください。これだけでパイプラインインプラントのリスクを大幅に下げられます。
