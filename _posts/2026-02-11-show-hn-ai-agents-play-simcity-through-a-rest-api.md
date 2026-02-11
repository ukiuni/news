---
layout: post
title: "Show HN: AI agents play SimCity through a REST API - 「AIエージェントがREST APIでSimCityを操る」"
date: 2026-02-11T13:22:29.614Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://hallucinatingsplines.com"
source_title: "Hallucinating Splines | The city simulator where AI agents are the mayors"
source_id: 46946593
excerpt: "REST APIでAIがSimCity風都市を自動構築し競う実験プラットフォーム"
---

# Show HN: AI agents play SimCity through a REST API - 「AIエージェントがREST APIでSimCityを操る」
街づくりをAIに任せる未来 — あなたの次のハッカソンで試したくなるWebベースのシミュレーター

## 要約
AIエージェントがREST API経由でオープンソースの都市シミュレーター（Micropolis/micropolisJS）を操作し、複数の「市長」が自動で街を作り競うプラットフォームです。

## この記事を読むべき理由
APIで操作できる都市シミュレーションは、自治体向けプロトタイピング、マルチエージェント学習、ゲームAIの実験など日本の開発者・研究者にとって手軽な実践場になります。敷居が低く、アイデアを短期間で検証できます。

## 詳細解説
- 基盤: Micropolis（オープンソースのSimCityクローン）をmicropolisJSでブラウザ/サーバーに移植している点が肝。ライセンスはGPL v3。
- 操作方法: ゲームの操作やイベント（交通、発電、犯罪、モンスター出現など）はREST APIで外部からコマンド送信でき、AIエージェントが“市長”として振る舞う仕組み。
- メトリクス: 各都市の人口、スコア、需要（住宅など）、インフラ状態が集計され、リーダーボードや可視化で比較・分析が可能。
- 応用性: 強化学習やルールベース、チェーンオブソート（複数エージェント協調）など、さまざまなAI手法のテストベッドになる。CIや自動評価にも組み込みやすい。

## 実践ポイント
- まずはサイト（hallucinatingsplines.com）とDocs/GitHubを確認。ローカルでmicropolisJSを動かすと実験が速い。
- REST APIはHTTPクライアントから簡単に叩ける。例えば（プレースホルダ）:
```bash
# bash
curl -X POST 'https://hallucinatingsplines.com/api/agents' \
  -H 'Content-Type: application/json' \
  -d '{"name":"MyMayor","strategy":"greedy_build"}'
```
- 実験アイデア: 交通政策だけを変えるエージェント群、災害発生時の復興戦略比較、市民満足度最適化の学習など。
- ライセンスに注意（micropolisJSはGPL v3）：商用利用や再配布時は条件を確認すること。

この手軽さは、学生の演習やハッカソン、自治体・民間の都市実験プロジェクトにすぐ応用できます。興味があればDocsを読み、まずはAPIを叩いて「市長」になってみてください。
