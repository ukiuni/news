---
layout: post
title: "A Builder's Guide to Not Leaking Credentials - 資格情報（シークレット）を漏らさない開発者ガイド"
date: 2026-02-25T05:38:13.965Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.eliranturgeman.com/2026/02/20/secrets-leaked/"
source_title: "A Builder&#39;s Guide to Not Leaking Credentials"
source_id: 398328601
excerpt: "Gitに残したキーが数分で悪用される理由と今すぐできる防止策を具体的に解説"
---

# A Builder's Guide to Not Leaking Credentials - 資格情報（シークレット）を漏らさない開発者ガイド
秘匿情報をGitに置かない：一度のミスが数分で被害につながる現実と、今すぐできる対策

## 要約
公開・非公開問わずGitにシークレットを置くのは危険。自動化されたスキャナーが数分で発見して悪用するため、発見→ローテーション→CI強制が必須。

## この記事を読むべき理由
日本のスタートアップや小規模チームでも「ちょっとテストで貼った」をきっかけにAWSキーやDBパスワードが流出しやすく、事業継続や顧客信頼に直結するため今すぐ対策すべきだから。

## 詳細解説
- なぜ漏れると速攻で悪用されるか  
  GitHubのイベントやスキャナーがpushを自動巡回し、差分を解析して既知フォーマット（AWS/Stripe/DB接続文字列など）と突合。検出→プロバイダAPIで有効確認→悪用の流れが自動化され、数分で被害が出ることがある。

- Gitが持つ構造上の問題点  
  Gitは分散・永続で履歴を完全複製する。つまり一度コミットしたシークレットはクローンやフォークに残り、.gitignoreであとから無効化しても履歴は消えない（履歴書き換えは可能だが既存クローンには効かない）。

- よくあるミス  
  - 一時コミット（「テスト用に貼った」）をそのままプッシュ  
  - .envを誤ってコミット（.gitignore追加後でも履歴には残る）  
  - 本番キーをローカルで使う（履歴・シェル履歴・ツール保存など大量にコピーされる）  
  - Slack/メール/LLMプロンプトに貼る（保存・監査外で回収不能）  

- 検出ツールと運用  
  - gitleaks：オフラインで正規表現ベースの高速スキャン。ローカルとCIで有効。  
  - truffleHog：プロバイダAPIで検証して誤検知を減らす。  
  - スキャンは作業ディレクトリだけでなく必ず全履歴を走らせる（過去コミットが対象になるため）。

- 漏れが見つかったら（優先順）  
  1. 速やかに該当キーをローテーション（新規発行）  
  2. 古いキーを無効化（自動無効化されないサービスは明示的に）  
  3. プロバイダのアクセスログを調査（AWS CloudTrail等）  
  4. 必要なら履歴書き換え（git filter-repo等）—ただし「履歴消し」よりまずローテーション

- 正しい扱い方（推奨設計）  
  - 実行時に環境変数や注入ファイルから読み込む（コードにハードコードしない）  
  - 環境ごとに別の資格情報を用意（dev/staging/prod分離）  
  - 小規模ならgitignoredな.env＋pre-commitフック＋CIスキャンで十分な場合あり  
  - サービス増・チーム拡大時はSecrets Manager/Vault/Doppler等で集中管理、監査とローテーションを自動化  
  - さらに可能なら短命トークン（IAMロール／OIDC／セッションユーザ）で被害範囲を小さくする

## 実践ポイント
- ローカルでまず全履歴をスキャン：
```bash
# bash
gitleaks dir .
gitleaks git --log-opts="--all" .
```
- CIで検出を必須化（例：GitHub Actionsでgitleaksを実行）：
```yaml
# yaml
name: Secret Scan
on: [push, pull_request]
jobs:
  gitleaks:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run gitleaks
        run: gitleaks git --log-opts="--all" .
```
- 漏れが見つかったら即ルール：1)キーを発行→2)古いキーを無効化→3)アクセスログ確認。履歴消去は二次対応。
- .gitignore・pre-commit（コミット阻止）・CIスキャンの3点セットを導入。既存履歴はgitleaksのignore指紋機能で段階的に対応。
- 日本の現場ではSlackや社内ドキュメント、LLMプロンプトに貼らない運用ルールを明文化し、クラウド監査ログ（CloudTrail/GCP Auditログ/Azure Monitor）を定期確認すること。

チェックリスト（最低限）
- [ ] gitleaksでワーキングツリーと全履歴をスキャン  
- [ ] 漏れがあれば即ローテーション＆無効化  
- [ ] シークレット管理をCIに組み込み（ブロック）  
- [ ] .gitignore / pre-commit を整備し運用ルールを社内共有

以上。
