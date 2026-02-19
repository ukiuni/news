---
layout: post
title: "Suffering from BUGS: How I Almost Deleted My Entire Project - バグ地獄：プロジェクトをほぼ削除しかけた話"
date: 2026-02-19T10:44:18.521Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://dev.to/maame-codes/suffering-from-bugs-how-i-almost-deleted-my-entire-project-1eef"
source_title: "Suffering from BUGS: How I Almost Deleted My Entire Project - DEV Community"
source_id: 3266984
excerpt: "**依存未固定と遅延でプロジェクト消失寸前、モデル切替とピン留めで救った実話**"
image: "https://media2.dev.to/dynamic/image/width=1000,height=500,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Fj0ot4q5711pxfrcoqdjr.png"
---

# Suffering from BUGS: How I Almost Deleted My Entire Project - バグ地獄：プロジェクトをほぼ削除しかけた話
デプロイ地獄からの生還術――「動くはず」が動かない時にまずやるべきこと

## 要約
ローカルでは完璧に動いたAIツールが、クラウドで依存関係やレスポンス遅延により動作不能に。原因の切り分けと「速さを優先する」判断で復旧した事例。

## この記事を読むべき理由
開発・デプロイで誰もが遭遇する「Works on my machine」問題、依存管理、モデル選定、コストとレイテンシのトレードオフを初心者にも実践的に学べるから。

## 詳細解説
- 問題の全体像  
  ローカルで動いていたスライド要約ツールをRenderへデプロイしたところ、サーバー側で古いAIライブラリが入っていてModuleNotFoundErrorや500エラーが多発。さらに外部モデル（Google Gemini Pro）の応答が45〜180秒と遅く、UXが致命的になった。

- 技術的要因と原因究明  
  1) 依存関係の未固定：requirements.txtでバージョンを固定していないと、クラウド側が古いパッケージを引いてくる。  
  2) コールドスタート／無料枠の制約：無料プランやサーバレスの初回起動遅延でレスポンスが長くなる。  
  3) モデルの選定ミス：最も高性能なモデル＝最適ではなく、用途によっては低レイテンシなモデルが優先される。

- 解決の方向性  
  - 依存をピン留め（例：pip freeze → requirements.txt）し、本番ライクな環境で早期テスト。  
  - 「遅くて高精度」より「速くて十分な精度」を採用。筆者はGemini→Groq（Llama-3）に切替え、応答時間を大幅短縮。  
  - デプロイログ／エラーメールを冷静に解析し、環境変数やパッケージ問題を優先的に潰す。  
  - この経験は単なるバグ潰しではなく、環境管理・システム設計・コスト最適化の学習になる。

## 実践ポイント
- まずやること：requirements.txtは必ずバージョン固定（pip freeze推奨）。  
- 本番ライクな検証：ローカルだけでなくステージングかコンテナで動作確認。  
- UX重視のモデル選定：要約などのユースケースは「速さ」を優先して検証する（レスポンスタイムをSLAの観点で基準化）。  
- 無料枠対策：コールドスタートを想定した設計か、短いレイテンシを得られるプラットフォーム（Vercel等）を検討。  
- 心理的対処：エラーログを読み切れない時は一度休む・バックアップを取って削除は避ける。

以上。問題に遭遇したら、まず依存固定と本番ライク検証を試してください。
