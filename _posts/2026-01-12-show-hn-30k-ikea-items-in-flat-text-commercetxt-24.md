---
layout: post
title: "Show HN: 30k IKEA items in flat text (CommerceTXT). 24% smaller than JSON - CommerceTXTで表現した30,000件のIKEA商品（JSONより24%小さい）"
date: 2026-01-12T14:00:18.018Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://huggingface.co/datasets/tsazan/ikea-us-commercetxt"
source_title: "tsazan/ikea-us-commercetxt · Datasets at Hugging Face"
source_id: 46526809
excerpt: "IKEA約3万点をAI向けテキスト化、JSON比トークン24%削減で検索に最適。"
image: "https://cdn-thumbnails.huggingface.co/social-thumbnails/datasets/tsazan/ikea-us-commercetxt.png"
---

# Show HN: 30k IKEA items in flat text (CommerceTXT). 24% smaller than JSON - CommerceTXTで表現した30,000件のIKEA商品（JSONより24%小さい）

驚くほどシンプルでトークン節約に効く「CommerceTXT」で、IKEA商品カタログを丸ごとAIフレンドリーなフラットテキストに変えた話

## 要約
Hugging Faceに公開された「ikea-us-commercetxt」は、IKEA米国の約30,511商品のカタログを人間可読なテキスト形式（CommerceTXT）で公開。JSONと比べて入力トークンを$24\%$節約でき、RAGや検索、AIショッピングアシスタント用途に最適化されている。

## この記事を読むべき理由
- 日本でもLLMを使ったプロダクト検索やチャット型販売支援が広がっており、トークン効率と可読性を両立するデータ設計は実務で即役立つから。
- データ構造・使い方が具体的に示されており、既存のJSONカタログを置き換える際の実践的ヒントになるから。

## 詳細解説
- 何が公開されているか  
  - 総商品数: $30{,}511$、カテゴリ: 632、データ日付: 2025-07-15。形式は CommerceTXT v1.0.1（ルートに @CATALOG、カテゴリごとにファイル、商品ごとに .txt）。データは研究/教育目的のスナップショットで、IKEA公式ではない点に注意。

- CommerceTXT の特徴（技術的ポイント）  
  - テキスト指向で冗長なJSONシンタックス（中括弧や引用、フィールド名のオーバーヘッド）を削り、LLMへの入力トークン数を削減。  
  - 人間が読めるディレクティブ（例: `# @PRODUCT`, `# @OFFER`, `# @SPECS`, `# @IMAGES`, `# @CATALOG`）で構造化。パーサーで容易にキー/値を取り出せる。  
  - カタログ自体（カテゴリ一覧＋各カテゴリのインデックス）を含めても、全体でJSON比でトークン$24\%$削減（総トークン節約 $3.6\mathrm{M}$）。個別商品レベルでは平均約$31\%$の削減。  
  - 実用的な利点: デバッグやバージョン管理がしやすく、RAGワークフローでそのままテキストをベクトル化→検索→LLMへ投入しやすい。

- ファイル構成（読みやすく）  
  - commerce.txt（@CATALOG）  
  - products/<カテゴリ名>/*.txt（各商品）  
  - categories/<カテゴリ名>.txt（カテゴリのインデックス）

- 使い方（抜粋）  
  - Hugging Faceの datasets ライブラリで読み込み可。公式のparserがあり、Pythonから `parse_file` で簡単に構造化データを得られる。

Example（Pythonでの読み込みとパース）:
```python
# python
from datasets import load_dataset
from commercetxt import parse_file

dataset = load_dataset("tsazan/ikea-us-commercetxt")
root = dataset['train'][0]['commerce.txt']
product_list = dataset['train'][0]['products']  # paths or content depending on load

# ローカルで product ファイルをパースする例
result = parse_file("products/frames/00263858.txt")
product = result.directives.get('PRODUCT', {})
offer = result.directives.get('OFFER', {})
print(f"Name: {product.get('Name')}, Price: {offer.get('Price')}")
```

- なぜトークン節約が重要か  
  - LLMへの入力コストはトークン数に比例するため、特に大量の商品カタログをRAGや対話に渡す場合、$24\%$の削減は運用コストに直結（記事では例としてGPT-4o換算での月間節約見積りを提示）。

## 実践ポイント
- まず試す（初心者向け手順）  
  1. Hugging Faceから該当データセットを読み込む。  
  2. いくつかの商品の .txt を parse_file で解析して中身（Name, Price, Specs）を確認する。  
  3. ベクトルDB（FAISS, Milvusなど）にテキストを格納して、RAGクエリを試す（例: 「黒いフレームで安いもの」）。  

- 既存JSON→CommerceTXT移行のヒント  
  - 自動変換で不要なメタ（長いフィールド名、過剰なネスティング）を削るだけで効果が出る。  
  - カタログ（カテゴリ索引）を別ファイルに分けると検索の柔軟性が上がるが、カタログ分のオーバーヘッドも評価する。  

- 日本市場での応用アイデア  
  - 日本語商品説明や価格表記を取り込み、CommerceTXTルールに従って同様に整形すれば、国内ECデータでもトークン節約と可読性の恩恵を受けられる。  
  - 店舗在庫やプライシングの頻繁な更新がある場合、テキスト差分（gitでの差分管理）が効きやすく変更追跡が楽になる。

- 注意点（リーガル＆実運用）  
  - 元データは非公式スナップショット。商用利用や公開UIでそのまま使う場合は権利関係の確認が必要。  
  - スナップショット日付（2025-07-15）以降の更新や価格差に注意。

短くまとめると、CommerceTXTは「人間に優しく、LLMに優しい」中間フォーマットで、日本の開発チームがRAG/検索/対話型ECを設計する際にすぐ試せる実用的なアプローチです。興味があるならまずは数百件で変換→ベクトル化→クエリを試し、コストと精度の改善を測ってみてください。
