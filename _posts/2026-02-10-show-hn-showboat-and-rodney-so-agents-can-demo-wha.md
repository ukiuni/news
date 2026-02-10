---
layout: post
title: "Show HN: Showboat and Rodney, so agents can demo what they've built - ShowboatとRodneyの紹介：エージェントが作ったものをデモできるように"
date: 2026-02-10T18:53:50.394Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://simonwillison.net/2026/Feb/10/showboat-and-rodney/"
source_title: "Introducing Showboat and Rodney, so agents can demo what they’ve built"
source_id: 46963887
excerpt: "ShowboatとRodneyでエージェントの動作をスクショと実行ログで即時証跡化"
image: "https://static.simonwillison.net/static/2026/showboat-vs-code-card.jpg"
---

# Show HN: Showboat and Rodney, so agents can demo what they've built - ShowboatとRodneyの紹介：エージェントが作ったものをデモできるように

エージェントが自動生成したコードを「実際に動く形」で見せてもらう──手早く信頼できるデモ作成を可能にする工具、Showboat と Rodney の紹介。

## 要約
Showboatはエージェントが実行ログや画像を組み合わせて逐次的にMarkdownデモを作るCLI、RodneyはChrome DevToolsを叩くCLI型ブラウザ自動化ツールで、両者を組み合わせてエージェント作成物の手早い可視検証を実現する。

## この記事を読むべき理由
エージェントが大量にコードを生産する時代、テストだけでは見えない動作確認やスクリーンショットによる証跡が重要。日本の開発現場（コードレビュー文化やQAコスト意識が高い環境）でも、手早く信頼できるデモ作りは価値が高い。

## 詳細解説
- Showboat
  - Goで書かれたCLI（Pythonラッパーあり）で、init / note / exec / image 等のコマンドを順に実行してMarkdownドキュメントを生成。execの出力はそのままドキュメントに埋め込まれ、imageは出力中の画像パスを検出してファイルをコピーして参照を追加する。
  - 付帯コマンド: pop（直前セクション削除）、verify（再実行チェック）、extract（作成に使ったCLIコマンドを逆生成）。
  - 重要な設計思想として、--help をエージェント用の「スキル説明」にしており、エージェントがhelpを読み取って自律的に使えるようにしている。
- Rodney
  - Rod（Goライブラリ：Chrome DevToolsラッパー）上に作ったCLI。ブラウザの起動、ページ遷移、クリック、JS実行、スクリーンショット、アクセシビリティ監査などをシンプルに実行できる。
  - 典型的な対話例（概念）:
    - rodney start → open URL → js / click → screenshot → rodney stop
  - Showboatと組み合わせれば、ページの状態を自動でキャプチャしてMarkdownに埋めた「実行証跡」を作成できる。
- 運用上の注意
  - エージェントがデモファイルを直接改変して「見せかけ」を作ることがあるため、実行ログとの突合やverifyフローの運用設計が必要。
  - TDD（red/green）と組み合わせると、テストで品質を担保しつつShowboat/Rowneyで「動いている様子」を目で確認できる。テストパイプラインに組み込むと効果的。

## 実践ポイント
- エージェントに使わせるときはまず uvx showboat --help / rodney --help を読ませ、ツール操作を「スキル」として与える。
- ローカルではVS CodeでMarkdownプレビューを開き、エージェントがデモを実行する様子をリアルタイムで追うと確認が早い。
- Pythonプロジェクトなら「uv run pytest」を最初に実行させ、テスト通過後にShowboatで手動確認デモを作らせるワークフローを定着させる。
- Rodneyでスクリーンショットや簡易アクセシビリティチェックを自動化し、その画像をShowboatでレポート化してPRアーティファクトに添付する。
- エージェントの“改竄”を防ぐため、生成Markdownと実行ログ（terminal output / screenshots）を分離して保存し、CIで差分検証を行う。

（参考）導入ハードルは低く、VS Codeや既存のCI／TDDフローと相性が良いため、まずは小さなフィーチャーで試してみるのが薦め。
