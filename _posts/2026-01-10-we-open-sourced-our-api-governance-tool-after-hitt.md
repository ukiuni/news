---
layout: post
title: "We open-sourced our API governance tool after hitting the \"every service has different error formats\" wall - 「全サービスでエラーフォーマットがバラバラ」壁に当たってOSS化したAPIガバナンスツール"
date: 2026-01-10T16:33:35.160Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/akz4ol/api-governance-skill"
source_title: "GitHub - akz4ol/api-governance-skill: API governance and breaking change detection for OpenAPI specs"
source_id: 467500391
excerpt: "エラー形式バラバラ問題を自動検出し移行計画まで生成するOpenAPI向けOSSガバナンスツール"
image: "https://opengraph.githubassets.com/8c17dd9f2086aa8209416ec893a6635805c02ae4149d090742ee689e0b476fdb/akz4ol/api-governance-skill"
---

# We open-sourced our API governance tool after hitting the "every service has different error formats" wall - 「全サービスでエラーフォーマットがバラバラ」壁に当たってOSS化したAPIガバナンスツール
現場の“エラー地雷”と決別する：OpenAPI向けの自動ガバナンス＆破壊的変更検出ツール

## 要約
OpenAPI 3.0/3.1仕様を対象に、ポリシー駆動でリント（ガバナンスチェック）・破壊的変更検出・レビュー用アーティファクト生成を行うOSSツールです。PRゲートやCIに組み込んで、セキュリティ欠陥や仕様の不整合、非互換変更を自動検出できます。

## この記事を読むべき理由
APIが増えると「エラーレスポンスの形式が各サービスでバラバラ」「後方互換性を壊す変更が流出する」といった運用コストと事故リスクが急増します。日本の開発現場でも、マイクロサービス化／外部連携が進む今、APIの一貫性と安全性を自動化する仕組みは即戦力になります。

## 詳細解説
- 目的：レビューのばらつきや見落とし、ドキュメント未整備を自動化で補強するためのツール。人のレビュープロセスを置き換えるのではなく、効率化・標準化する補助ツールです。
- 主な機能
  - ポリシー駆動リント：セキュリティ（認証の有無、弱いスキーム）、ネーミング、ページング、観測性項目などカテゴリ別ルールを持ち、重大度（BLOCKER/MAJOR/MINOR）で評価。
  - 破壊的変更検出：ベースライン仕様と比較して削除／必須化などの互換性破壊を検出し、DEPRECATION_PLAN.md などの移行プランを生成。
  - アーティファクト生成：API_REVIEW.md（所見）、API_CHANGELOG.md（変更一覧）、DEPRECATION_PLAN.md（移行ガイド）を自動出力。レビューの差し戻し材料やマージ時の説明になる。
  - 拡張性：カスタムルールプラグイン、JSON/SARIF出力（CIやGitHub Code Scanning連携）、VS Code拡張でIDE内リンティング。
- コマンド例（導入は簡単）
```bash
# インストール
pip install api-governor

# 仕様チェック（デフォルトポリシー）
api-governor openapi.yaml

# 破壊的変更検出（baseline指定）
api-governor openapi-v2.yaml --baseline openapi-v1.yaml --strict
```
- Python APIやDockerイメージ、GitHub Actions用のアクションも用意されており、CIへの組み込みが容易です。
- 他ツールとの違い：Spectralは汎用リント、openapi-diffは差分のみ、api-governance-skillは“発見＋レビュー用アーティファクト生成＋ポリシーでの阻止”までカバーする点が特徴。

## 日本市場との関連性
- エンタープライズ系や金融、公共APIではセキュリティ・互換性要件が厳格で、ドキュメント整備やデprecation対応は法令・SLAに直結します。自動生成される移行計画や差分報告は社内レビューや監査対応で有用です。
- 多言語・多チーム環境が一般的な日本の大規模組織でも、ポリシーを中央で定めてCIに組み込めば、サービス間のスタイルドリフトを抑えられます。
- VS Code拡張でIDE内即時フィードバックが得られるため、社内のコード文化に馴染みやすい点もメリットです。

## 実践ポイント
- まずはローカルで1リポジトリ分をポリシー適用して出力を確認する（api-governor openapi.yaml）。
- PRパイプラインに組み込み、BLOCKER発生でマージをブロックするルールを設定する（GitHub Actions連携が簡単）。
```yaml
# .github/workflows/api-governance.yml（例）
name: API Governance
on: [pull_request]
jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: API Governance Check
        uses: akz4ol/api-governance-skill@v1
        with:
          spec-path: openapi.yaml
          policy: strict
          fail-on: blocker
```
- 既存API群にはまず「監査モード」で全OpenAPIを走らせ、主要な違反を洗い出して段階的にポリシーを厳格化する。
- 必要に応じてカスタムルールを作成し、社内独自の命名規約やエラースキーマを自動チェックする。
- SARIF出力を使えば、GitHubのCode ScanningやIDEで結果を可視化できます。

導入コストは低く、レポートと移行プランが自動で出るためチームの合意形成やレビュー効率化に即効性があります。まずは1サービスで試し、CIゲート化→組織横展開の順で進めるのが現場的に現実的です。
