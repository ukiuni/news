---
layout: post
title: "Upgraded embed experience and new embed types in DEV posts - DEV投稿の埋め込み機能強化と新しい埋め込みタイプ"
date: 2026-03-01T15:22:18.346Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://dev.to/devteam/upgraded-embed-experience-and-new-embed-types-in-dev-posts-1kho"
source_title: "Upgraded embed experience and new embed types in DEV posts - DEV Community"
source_id: 3289627
excerpt: "URLを貼るだけでHuggingFaceやWarp等のAIデモが即埋め込み可—DEVの新機能を試そう"
image: "https://media2.dev.to/dynamic/image/width=1000,height=500,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Fimpdnw3z9qppff9cvjtc.png"
---

# Upgraded embed experience and new embed types in DEV posts - DEV投稿の埋め込み機能強化と新しい埋め込みタイプ
貼るだけで埋め込み完成！DEVが5種のAIツール表示と「ペーストで埋め込み」UXを導入

## 要約
DEV（Forem）が投稿エディタに「ペーストで埋め込み」ポップオーバーを追加し、Lovable、Bolt.new、Warpブロック、HuggingFace Spaces／Dataset Viewerなど5種類の新しい埋め込みを公式にサポートしました。

## この記事を読むべき理由
ブログや技術記事で外部デモやインタラクティブなAIツールを手早く埋め込みたい日本のエンジニア／技術ライターにとって、投稿体験が格段に簡単かつ信頼性の高いものになったため。

## 詳細解説
- 新UX：本文にURLを貼るとカーソル付近にポップオーバーが出現し、ワンクリックでそのURLをLiquid埋め込みタグ（{% raw %}{% embed <url> %}{% endraw %}）に変換。5秒で自動消去、キー入力でも閉じる。任意のURLで動作する（5サービス限定ではない）。
- 新たに公式サポートされた埋め込み種：
  - Lovable（*.lovable.app） — iframe
  - Bolt.new（bolt.new / *.bolt.host） — iframe
  - Warp ブロック（app.warp.dev/block/* → /block/embed/ に変換） — iframe
  - HuggingFace Spaces（*.hf.space / huggingface.co/spaces/*） — iframe
  - HuggingFace Dataset Viewer（huggingface.co/datasets/*） — iframe
 （既存の Cloud Run 埋め込みも引き続き利用可能）
- アーキテクチャ：すべて UnifiedEmbed を通じて登録。各埋め込みクラスは正規表現（REGISTRY_REGEXP）でURLマッチ、parse_inputでURL正規化、UnifiedEmbed.registerで登録、共通のパーシャルでレンダリング。
- 検討したが未採用のサービス：Claudebin（非公開パラメータ必要）、Streamlit（SameSiteクッキーによるiframeリダイレクト問題）、ChatGPT/Amp/Cursor（埋め込み可能な共有URLがないかCSPでブロック）。
- テスト：Ruby／JavaScriptのテスト群が整備され、主要ケースがパス済み。

例（投稿内で使うタグ)
{% raw %}
```liquid
{% embed https://huggingface.co/spaces/KittenML/KittenTTS-Demo %}
{% embed https://iconstack.lovable.app/ %}
{% embed https://app.warp.dev/block/JjdoVfeKebVSw8wiykuDag %}
```
{% endraw %}

## 実践ポイント
  - 書き方：記事本文に埋め込みたいURLを貼り、表示された「Embed」ボタンをクリックするだけで {% raw %}{% embed <url> %}{% endraw %} に変換される。プレビュー／公開でiframeとして動作を確認。
- 日本での活用例：HuggingFaceの日本語モデルデモやデータセット、Warpのターミナル共有、Boltで作ったダッシュボード、Lovableのアイコンプレビューなどを記事内で手早く紹介可能。技術ブログやハンズオン記事の説得力が増す。
- 注意点：サポート外のサービスはCSPやSameSiteの制約で埋め込めないことがあるため、埋め込みに失敗したら通常リンクやスクリーンショットの併用を検討する。改善要望はDEVのコメントで提案可能。

以上。利用シーンを想定してまずは手持ちのデモURLを貼って「Embed」を試してみてください。
