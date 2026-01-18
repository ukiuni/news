---
layout: post
title: "How I Use AI Agents + MCP to Fully Automate My Website’s Content - AIエージェント＋MCPで自分のサイトのコンテンツを完全自動化する方法"
date: 2026-01-18T22:31:27.416Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://dev.to/debs_obrien/how-i-use-ai-agents-mcp-to-fully-automate-my-websites-content-3ekj"
source_title: "How I Use AI Agents + MCP to Fully Automate My Website’s Content - DEV Community"
source_id: 3172385
excerpt: "Goose＋MCP連携でポッドキャスト記事をほぼワンクリック自動作成"
image: "https://media2.dev.to/dynamic/image/width=1000,height=500,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Fv5qdhdw99ou3m6jsj2gz.png"
---

# How I Use AI Agents + MCP to Fully Automate My Website’s Content - AIエージェント＋MCPで自分のサイトのコンテンツを完全自動化する方法
面倒な手作業をAIに任せる——ポッドキャストや記事の追加をワンクリックで完了させる自動化レシピ

## 要約
著者はGoose（エージェント）＋Playwright MCP＋Cloudinary MCP＋GitHub MCPを組み合わせ、ポッドキャスト情報の収集から画像アップロード、Markdown生成、プルリク作成までを完全自動化するワークフローを作った。初期設定は必要だが、一度整えればほぼワンアクションで更新できる。

## この記事を読むべき理由
日本でも個人サイトや技術ブログ、企業の情報ページは数が多く、手作業での更新は工数の無駄になります。今回の手法は「既存のアーキテクチャ（Nuxt Content＋Cloudinaryなど）を壊さずに自動化する」実例で、エンジニア・広報担当・個人ブロガーがすぐに試せる実践的な指針を示しています。

## 詳細解説
- 背景
  - 著者はNuxt ContentでコンテンツをMarkdown（YAML frontmatter付き）で管理。ポッドキャスト回を追加する際、タイトル・日付・ホスト・画像URLなどを手でコピーしていたため手間が発生していた。
- 使われた主要コンポーネント
  - Goose：Block製のデスクトップ/CLIのエージェント。プロンプトを「レシピ」として保存し、パラメータを受け取れる。
  - Playwright MCP：ブラウザ操作を自動化してホストサイトからメタデータ（タイトル、日付、画像）を取得するために利用。
  - Cloudinary MCP：ダウンロードした画像をCloudinaryにAPI経由でアップロードし、最適化済みURLを得る（Cloudinaryを使い続けられる利点を維持）。
  - GitHub MCP：生成したMarkdownをリポジトリにコミットしてプルリクを作成。
- ワークフロー（流れ）
  1. GooseレシピにポッドキャストのURLを渡す。
  2. Playwright MCPが該当ページにアクセスしてメタデータを抽出。
  3. 画像をダウンロードし、Cloudinary MCPで適切なフォルダにアップロード。返却された画像ID／URLを取得。
  4. 取得した情報でNuxt用のMarkdown（YAML frontmatter含む）を生成。
  5. GitHub MCPでブランチを切り、ファイルを追加してプルリクを作成。
  6. （オプション）ローカル開発サーバを立ち上げてPlaywrightで表示確認・スクリーンショット取得。
- メリットと注意点
  - メリット：一度レシピを作れば非エンジニアでも更新可能。Cloudinaryの最適化など既存利点を維持できる。チームで共有して運用可能。
  - 注意点：初期設定（APIキー、MCPの設定、レシピ調整）は手間。エージェントの挙動は完全ではないためPRレビューは必須。APIキーは安全に保管すること。

## 実践ポイント
1. 小さく始める：まずは1ページタイプ（例：ポッドキャスト）のテンプレートMarkdownを作成し、自動化対象を限定する。  
2. 必要なMCPを整理する：Playwright（抽出）、Cloudinary（画像）、GitHub（PR）の順に接続を検証する。  
3. レシピをパラメータ化する：URLや公開日などを引数にできれば複数件のバルク処理が楽になる。  
4. セキュリティ対策：APIキーはエージェント拡張の安全な設定領域かシークレットマネージャで管理。ログに平文を出さない。  
5. CI／レビュー設計：エージェント生成のPRは自動マージせず必ず人がレビューする運用ルールを敷く。  
6. 代替案を用意：Goose以外のエージェントやGitHub Actions＋Playwrightスクリプトでも同様の自動化は可能。まずは概念を掴むことが大事。

日本の個人開発者や中小チームでも、今回のような「日常的な更新」をエージェントに任せることで工数を大きく削減できます。最初の設定は投資ですが、運用が回り始めると確実に効率化のメリットが出ます。興味があれば、小さなページで試してみてください。
