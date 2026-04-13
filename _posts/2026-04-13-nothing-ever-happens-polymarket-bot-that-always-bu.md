---
layout: post
title: "Nothing Ever Happens: Polymarket bot that always buys No on non-sports markets - 「何も起きない」：スポーツ以外の市場で常に“No”を買うPolymarketボット"
date: 2026-04-13T16:44:11.028Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/sterlingcrispin/nothing-ever-happens"
source_title: "GitHub - sterlingcrispin/nothing-ever-happens · GitHub"
source_id: 47753472
excerpt: "Polymarket非スポーツ市場で常にNoを買うPythonボット実装とHeroku運用解説"
image: "https://opengraph.githubassets.com/54b95712640bceb4e424ee7a649f50f1763fdf936647e45735c95c88901e4d98/sterlingcrispin/nothing-ever-happens"
---

# Nothing Ever Happens: Polymarket bot that always buys No on non-sports markets - 「何も起きない」：スポーツ以外の市場で常に“No”を買うPolymarketボット
「ありえない未来に賭け続けるボット」の中身を覗いてみませんか？

## 要約
Polymarketのスタンドアロン（非スポーツ）のyes/no市場に対して常に「No」を買うことを目的にした非同期Pythonボット。教育・エンタメ目的でコードは公開され、ローカル実行からHerokuデプロイまで想定されています。

## この記事を読むべき理由
- 予測市場やマーケットメイキングの自動化の仕組みを実例で学べる。  
- 非同期Python、ダッシュボード、環境変数ベースの安全設定、Heroku運用など実務に直結する要素が詰まっている。  
- 日本でも学習用や研究用に同様の仕組みを作るニーズが増えているため、実践的な知見が得られる。

## 詳細解説
- コア機能：リポジトリの runtime（nothing_happens）はスタンドアロンのyes/no市場をスキャンし、設定した価格上限を下回る"No"注文を見つけると買いを入れ、ポジション管理・ダッシュボード表示・状態の永続化を行います。  
- 安全モデル：実際の注文送信（ライブ取引）を行うには3つの環境変数が必須（BOT_MODE=live、LIVE_TRADING_ENABLED=true、DRY_RUN=false）。これらが無い場合はPaperExchangeClient（ペーパートレード）にフォールバックします。さらに実稼働時は秘密鍵やファンダーアドレス、DATABASE_URL、POLYGON_RPC_URLなどの追加設定が必要です。  
- 設定と起動：config.example.jsonと.env.exampleを元にローカルでconfig.json/.envを作成。pipで依存を入れ、python -m bot.mainで起動。ダッシュボードは$PORTかDASHBOARD_PORTを参照します。  
- デプロイと運用：Heroku向けのスクリプトが用意され、環境変数をHeroku configにセットしてgit pushでデプロイ可能。ワーカーは不意起動を防ぐ設計です。ログ整形やDBエクスポートなどの運用スクリプトも揃っています。  
- テストと品質：pytestベースのユニット/回帰テストが含まれ、ローカル検査用スクリプトもありリポジトリは動作検証を重視した構成です。  
- ライセンス/注意：CC0ライセンスで公開されていますが、READMEに明確な免責（エンタメ用途、自己責任）と安全警告がある点に注意。

## 実践ポイント
- まずはDRY_RUN=trueで動かし、PaperExchangeClientで挙動を確認する。  
- config.example.jsonと.env.exampleを読み替えて自分の環境に合わせる。秘密鍵等は絶対に公開リポジトリに置かない。  
- Herokuで試す場合は専用アプリ名と環境変数を設定してワンデプロイで動作を検証。  
- 学習用途ならコードの非同期処理、オーダー管理、ダッシュボード連携部分を重点的に読むと実務スキルが身につく。  
- 日本で実運用を考えるなら法的・規制面（金融商品性やプラットフォーム規約）を事前に確認すること。

元リポジトリ（学習・参考向け）: https://github.com/sterlingcrispin/nothing-ever-happens
