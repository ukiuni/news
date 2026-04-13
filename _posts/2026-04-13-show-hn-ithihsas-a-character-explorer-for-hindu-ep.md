---
layout: post
title: "Show HN: Ithihāsas – a character explorer for Hindu epics, built in a few hours - Show HN: Ithihāsas — ヒンドゥー叙事詩の登場人物探索ツール（数時間で制作）"
date: 2026-04-13T19:46:13.805Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.ithihasas.in"
source_title: "Ithihasas — Hindu Epics Character Explorer"
source_id: 47756569
excerpt: "数時間で作られた叙事詩可視化ツールで登場人物の系譜と関係を直感探索"
image: "https://www.ithihasas.in/opengraph-image?f20489d4ac7527e4"
---

# Show HN: Ithihāsas – a character explorer for Hindu epics, built in a few hours - Show HN: Ithihāsas — ヒンドゥー叙事詩の登場人物探索ツール（数時間で制作）

魅力的タイトル: 数時間で作られた神話ビジュアライザーが示す「物語をデータで読む」新しい方法

## 要約
Ithihāsas は『ラーマーヤナ』『マハーバーラタ』の登場人物・王朝・関係性をインタラクティブに可視化するウェブツール。力学的グラフ、系図ツリー、コー​​ド図などで相互関係を直感的に探れるのが特徴です。

## この記事を読むべき理由
技術的には短時間プロトタイプでありながら、テキスト資料を構造化して視覚的に解釈させる手法は、日本のデジタル人文学や歴史データ可視化にも応用可能——初心者でも真似できる設計と実装のヒントが詰まっています。

## 詳細解説
- 可視化手法
  - Force Graph（力学的ノード配置）: ノード（人物）とエッジ（関係）を力学モデルで配置して関係性の密度や中心人物を直感的に示す。
  - Dynasty Trees（系図ツリー）: 血縁・世代関係を木構造で表現し、継承や分岐を追いやすくする。
  - Chord Diagrams（コー​​ド図）: 人物間の相互作用や事件のつながりを円環で可視化し、頻度や強さを把握できる。
- データ面
  - 元テキスト（叙事詩）の人物抽出、同名・異表記の正規化、関係性のタイプ分類（親子、敵対、師弟など）が鍵。
  - 軽量ならJSONでノード/エッジを管理、規模が大きければグラフDB（例：Neo4j）やバックエンドAPIを検討。
- 実装の特徴（短時間で作るための設計）
  - フロントエンド中心の実装（静的ホスティング）で素早く公開。
  - 可視化は既存ライブラリ（D3.js、sigma.js、react-force-graph 等）を組み合わせて短期間で機能実装。
  - パフォーマンス対策は、段階的読み込み・サマリー表示・WebGLレンダリングが有効。
- UX・文化的配慮
  - 名称や表記ゆれの扱い、多言語（デーヴァナーガリー／英語）対応、宗教・文化への敬意を保つデザインが重要。

## 実践ポイント
- まずサイトを触って、Force Graph や系図で「中心人物」「関係の密度」を体感する。
- 小さめのコーパスで試す：人物をノード、関係をエッジとするJSONを作り、D3やreact-force-graphで可視化してみる。
- 技術スタック候補：D3.js / react-force-graph / sigma.js / Neo4j（データ管理）／GitHub Pages（公開）。
- 日本向け応用案：『古事記』『日本書紀』や戦国武将系譜の可視化、社史や家系図のデジタル探索ツールに転用可能。
- 小さく始めて、名前正規化とインタラクション（フィルタ・検索）を優先的に整備する。

興味があれば、試作データモデルの作り方や短時間プロトタイプの手順を具体的に示します。どちらを知りたいですか？
