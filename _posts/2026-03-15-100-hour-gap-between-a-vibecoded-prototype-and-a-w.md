---
layout: post
title: "100 hour gap between a vibecoded prototype and a working product - vibecodedプロトタイプと実運用の間の100時間ギャップ"
date: 2026-03-15T13:33:15.539Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://kanfa.macbudkowski.com/vibecoding-cryptosaurus"
source_title: "The 100 hour gap between a vibecoded prototype and a working product"
source_id: 47386636
excerpt: "vibecodingで1時間の原型が公開品質になるまで約100時間の現実的工数と対策を解説"
image: "https://paragraph.com/api/og?title=The+100+hour+gap+between+a+vibecoded+prototype+and+a+working+product&amp;blogName=kanfa+%5Bby+Mac+Budkowski%5D&amp;coverPhotoUrl=https%3A%2F%2Fstorage.googleapis.com%2Fpapyrus_images%2F0c0ba73a08751599a6b7ecd02e72a87a08c89b74f4b5a3b130d04856bd1cbbf0.jpg&amp;blogImageUrl=https%3A%2F%2Fstorage.googleapis.com%2Fpapyrus_images%2F9c0f5716df4987236239bc96f39b432e.jpg&amp;publishedDate=1772813254067"
---

# 100 hour gap between a vibecoded prototype and a working product - vibecodedプロトタイプと実運用の間の100時間ギャップ
「AIで“30分でアプリ”は幻想か？vibecodingで本当に公開できるプロダクトを作るまでのリアルな100時間」

## 要約
AI（vibecoding）で「1時間で動くプロトタイプ」は作れても、ユーザーに出せる品質で公開するには約100時間かかった、という実体験レポート。UI/UX、画像生成のエッジケース、インフラ、スマートコントラクト運用などで時間を費やした。

## この記事を読むべき理由
AI支援開発が普及する中で、「早く作れる」ことと「使えるものを作る」ことの差を知っておくのは、日本のスタートアップやPM、エンジニアにとって重要。期待値調整と実務で必要な工数・リスク対策が分かる。

## 詳細解説
- プロジェクト概要  
  - シンプルなSLC（Small Lovable Complete）として「Cryptosaurus」：ユーザーのプロフィール画像（pfp）を元に恐竜イラストを生成してNFT化するミニアプリ。
- ツールチェーン（生成系と開発環境）  
  - LLM／画像モデル：ChatGPT → Opus → Gemini / Claude / Codex（複数モデルの併用で役割分担）  
  - 開発・公開：ローカル→Vercel、ドメインはCloudflare。インフラは学習目的でAWS（S3、Lambda、CLI）を採用。
- プロトタイプと現場のギャップ  
  - 1時間で動く原型は作れたが、デザインの微調整・レイアウト崩れ・モバイル対応・不要アウトラインなどの細かい修正を繰り返し数十時間。Figmaを使えばUI作業は遥かに高速化できる場面が多数。  
  - 画像生成では多種のpfpで200回以上のプロンプト試行。出力のフレーミング崩れ、背景に説明テキストが残る、装飾が欠けるなどのエッジケース対策が膨大。
- インフラと運用での時間コスト  
  - .envやキー共有、S3の公開設定ミス、LLMが勝手にバケットを作る等のトラブルシュート。Farcaster向けのミニアプリ化で通知やマニフェスト、検証アカウントなど追加作業。  
  - スマートコントラクトはonlyMinterやSafe（多署名）での権限分離を実装し、CLIによる不正実行対策を追加。
- スケーラビリティと同時実行の落とし穴  
  - 同時ユーザー発生時のnonce（非同期性・排他）を見落とし、決済は通るが生成処理が競合してリクエストが失われる不具合が発生。返金対応と被害者抽出スクリプトで対応。
- 学びと結論  
  - AIは「最初の90%」を速く出すが、残りの10%（品質・UX・堅牢性・運用）は手間が掛かる。経験あるエンジニアや設計上の配慮が効く場面が多い。

## 実践ポイント
- スコープを分ける：プロトタイプ（1時間）／公開版（品質・運用）を明確に分離する。  
- UIはFigmaで先に固める：LLM任せは反復コストが高い。  
- プロンプトとテンプレート化：エッジケース対応をコード化して再現性を担保（例：prompt.tsに多数のガードを実装）。  
- 同時実行対策：idempotency、nonce管理、キュー化で競合を防ぐ。  
- 秘密鍵・権限設計：onlyMinter・Safeのように権限分離を行い、運用時のリスクを下げる。  
- 事前の負荷試験と監視：APIのレート制限やスパイクを想定した設計とログ/アラートを用意。  
- 小規模プレ公開で学ぶ：招待ベースの事前利用で重大な不具合を検出し、透明な返金フローを準備する。  
- 日本市場向けの注意点：決済やNFT関連は法規制・税務・ユーザーサポートが重要。モバイルUX重視でローカルでの表示崩れに注意。

短い結論：vibecodingは強力な加速剤だが、「公開できる良品」を作るにはAIが生む初速の後に人の手で詰める工程が必須。
