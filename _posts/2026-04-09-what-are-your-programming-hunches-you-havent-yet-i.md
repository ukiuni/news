---
layout: post
title: "What are your programming \"hunches\" you haven't yet investigated? - まだ調べていないプログラミングの「勘」は何か？"
date: 2026-04-09T12:11:31.399Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://lobste.rs/s/gns27z"
source_title: "What are your programming &quot;hunches&quot; you haven&#39;t yet investigated? | Lobsters"
source_id: 1241101591
excerpt: "クラウドや図、UIを性質で宣言する革新的手法と実践案を紹介し、最適構成自動探索の可能性を示す"
image: "https://lobste.rs/story_image/gns27z.png"
---

# What are your programming "hunches" you haven't yet investigated? - まだ調べていないプログラミングの「勘」は何か？
クラウドも図もUIも、「宣言」から「性質（プロパティ）で定義する」発想に変えたら何が起きるか？

## 要約
Lobsters上の議論から、インフラや図作成、UI設計に関する「未検証の勘」を集めた話。特に注目は「プロパティベースのインフラ（IaC）」と「コードで書ける図にWYSIWYGを組み合わせる」アイデア。

## この記事を読むべき理由
- 日本でもKubernetesやクラウドの利用が急速に進み、運用の複雑化が課題になっている。  
- ドキュメントや図の再現性・保守性は開発現場で困りごとが多い。  
これらの勘は運用自動化やチーム生産性に直結するため、今のうちに知っておく価値がある。

## 詳細解説
- プロパティベースのインフラ（Property-based Infrastructure）  
  - 概念: TerraformやCloudFormationのように「こう作る」ではなく、アプリが満たすべき性質（例: データは2ノード以上に存在、サービス応答はNms未満、ドメインで公開される、TLSが必須等）を宣言する。  
  - 利点: 要件志向で適応的な構成探索が可能になれば、最適解に近いリソース配置や構成を自動生成できる。  
  - 課題: クラウド資源は状態を持ち副作用があり探索空間が巨大。解探索には制約解決器や最適化アルゴリズム、そして分散システムのコストモデルが必要。  
  - 参考例: FPGAの配置問題やk8sのスケジューリングで使われるアルゴリズムは類似点があり、応用のヒントになる。PrologやMiniKanrenのような論理言語を使うアイデアも提示されている。

- 図作成用の「Pikchr＋WYSIWYG」  
  - 現状のトレードオフ: Graphviz/Mermaid（コードで再現可だが微調整がしづらい） vs Drawio/Excalidraw（直感的だがコード化しにくい）。  
  - 勘: Pikchr等のテキストベース図記法にWYSIWYG編集を付ければ、再現性と編集性の両立ができる。UIと内部の座標・抽象をうまくマッピングできれば実装は現実的。

- Web UIライブラリの再考  
  - 多くのライブラリはアクセシビリティ不足や過剰複雑、コンポーネント欠如が問題。Web Components＋テーマでの互換性あるコンポーネント群が解になる可能性。

## 実践ポイント
- 小さく試す: 既存インフラの重要要件（可用性、レイテンシ、公開可否等）を「性質」として列挙してみる。まずは検証的にルールセットを作る。  
- ツール探索: MiniKanrenやProlog系の小さな制約解決ライブラリを触って、単純な配置問題を解かせてみる。  
- 図のワークフロー改善: 現在使っている図（Mermaid, Drawio等）を洗い出し、どの手順が一番手間か（微調整？テンプレ化？）を可視化してPikchrの導入可能性を検討する。  
- 日本の現場への応用: 金融・製造など可用性/コンプライアンス重視の業界では「性質ベース」の自動検証は特に有益—PoCを限定環境で行うと説得しやすい。

短い時間で試せる領域が多く、アイデア自体は現場での改善に直結します。興味があれば、まずは「性質リスト」を1件作って検証してみてください。
