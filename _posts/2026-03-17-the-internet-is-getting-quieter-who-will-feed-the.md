---
layout: post
title: "The Internet Is Getting Quieter - Who Will Feed the Next Generation of AI? - インターネットが静かになっている — 次世代AIに知識を供給するのは誰か？"
date: 2026-03-17T05:42:17.650Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://dev.to/sag1v/the-internet-is-getting-quieter-who-will-feed-the-next-generation-of-ai-4bl1"
source_title: "The Internet Is Getting Quieter - Who Will Feed the Next Generation of AI? - DEV Community"
source_id: 3345524
excerpt: "公開ナレッジがAIチャットに埋もれ、次世代AIの学習資源が枯渇しかねない"
image: "https://media2.dev.to/dynamic/image/width=1200,height=627,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Fkrf1dw6vw34ymcqw1wfs.png"
---

# The Internet Is Getting Quieter - Who Will Feed the Next Generation of AI? - インターネットが静かになっている — 次世代AIに知識を供給するのは誰か？
消えゆく公開知見――AIはどこから学ぶのか？

## 要約
公開フォーラムやブログで蓄積されてきた実践知が、AIアシスタントの普及で「個人のチャット」に埋もれつつあり、未来のAIが学ぶための公開データが減りつつある、という問題提起。

## この記事を読むべき理由
Stack OverflowやGitHubの公開ナレッジは現行モデルの重要な訓練資源。日本でも企業内の情報が外に出にくい文化があり、この流れは国内の開発エコシステムや次世代AIの品質に直接影響します。

## 詳細解説
- 何が起きているか  
  - かつてはバグ解決の過程やアーキテクチャ議論が公開され、検索で再利用されていた。今はAIに直接尋ねて終わるため、解法がパブリックレコードに残りにくい。
- なぜ問題か（AIの視点）  
  - 現在の大規模モデルは公開データ（Stack Overflow、ブログ、Issue等）で学習済み。公開知が減ると将来モデルの学習源が薄まり、特に「試行錯誤の記録」や「設計理由」といった検証しにくいシグナルが失われる。
- 合成データと限界  
  - モデルが自分で生成するデータやコード実行ループで学ぶ方法はあるが、本物の「発見の過程」や文脈的判断は合成しづらい。
- 知識の私物化（privatization）  
  - 有能なエンジニアの知見がSlackや社内Wiki、AIチャットログに閉じると、公共の知識圏が縮小する。インセンティブの欠如が主因。
- 提案のスケッチ  
  - AIエージェントが発見を公共プラットフォームに投稿する仕組み（投稿時にオペレータの認証・責任付与、投稿ルールや評価APIの整備）や、評価層（evaluator）で品質を担保するアイデアが挙がっている。
- ガバナンスの壁  
  - 公共のナレッジコモンズを誰が運営し、どのようにインセンティブを作るかは未解決。企業は収益化して閉じる誘惑があるため、オープン標準と採用が鍵。

## 実践ポイント
- 個人/チームでできること  
  - 問題解決の要点をQiitaや技術ブログで短く公開する（匿名化や機密情報の除外を忘れずに）。  
  - 社内ドキュメントをAIフレンドリーに整備（メタデータ、検索可能な要約、MCP対応のカタログ化）。  
  - AIエージェントの出力や調査過程を要約して外部に投稿するワークフローを作る（非同期での共有を推奨）。  
  - 評価レイヤ（evaluator）を導入し、外に出す知見の質を担保する。  
  - コミュニティ貢献を評価する社内インセンティブ（報奨、評価指標）を設計する。
- 組織／コミュニティ視点  
  - オープンなナレッジ共有の文化醸成（社内発表→公開化の流れを作る）。  
  - ActivityPubなどの分散・連携プロトコルやMCPのような仕組みに注目し、標準化・連携に参加する。

短期的には現行モデルで困らなくても、長期的な「公開知の維持」はAIの健全な発展に不可欠。日本の開発コミュニティも、公開とプライバシーのバランスを考えながら、知見を未来へつなぐ仕組み作りに関与する価値がある。
