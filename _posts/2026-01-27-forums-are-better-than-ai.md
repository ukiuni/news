---
layout: post
title: "Forums are better than AI - フォーラムはAIより優れている"
date: 2026-01-27T12:10:35.291Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.kaggle.com/discussions/general/240644"
source_title: "Uploading Images to RMarkdown in Kaggle | Kaggle"
source_id: 416317597
excerpt: "Kaggleの環境に合わせたRMarkdown画像表示の実践手順とトラブル解決法"
image: "https://www.kaggle.com/static/images/logos/kaggle-logo-opengraph.png"
---

# Forums are better than AI - フォーラムはAIより優れている
フォーラムの知恵でKaggleのRMarkdownに画像を確実に表示する方法

## 要約
KaggleでRMarkdownに画像を貼るときは、環境（ファイルパス、データセットの配置、knitrの使い方）に正確に合わせる必要がある。汎用AIより、フォーラムの実例と環境依存のノウハウが効く場面が多い。

## この記事を読むべき理由
Kaggle特有のファイル配置（/kaggle/input、/kaggle/workingなど）やRMarkdown側の書き方を知らないと画像が表示されない。日本の初心者にも再現性のある実務的な手順を示します。

## 詳細解説
- 問題の本質：RMarkdownはファイルパスに依存するため、画像がNotebookカーネルで参照可能な場所にないと表示されない。AIの一般的な回答は概念的だが、Kaggle固有のパスや「データとして画像を追加する」「Notebookにファイルを置く」などの手順はフォーラムの実例の方が具体的で役立つ。
- よく使う配置とパス
  - データセットとして追加した場合: /kaggle/input/<dataset-name>/...
  - ノートブック実行中にアップロードしたファイルや作業結果: /kaggle/working/...
- RMarkdownでの画像挿入方法（代表例）
  - Markdown記法:
```markdown
![](/kaggle/input/my-dataset/image.png)
```
  - knitr経由（推奨、出力サイズ調整可能）:
```r
# r
knitr::include_graphics("/kaggle/input/my-dataset/image.png")
```
- トラブル対策
  - ファイルがカーネルに存在するかを先に確認する（e.g. list.files("/kaggle/input/my-dataset")）。
  - 相対パスを使う場合は作業ディレクトリを確認・固定する（setwd()やknitr::opts_knit$set(root.dir=...)）。
  - 再現性を重視するなら、画像はNotebookの付随データ（Dataset）としてコミットする。

## 実践ポイント
- まず右ペインのFilesやDatasetsで画像の実際のパスを確認する。
- 小さな検証セルでlist.files()を実行して存在確認をする。
- 再現性のために「画像はDatasetとして添付」→ Markdownかknitrで参照する運用を習慣化する。
- 分からない時はフォーラムで同じKaggle環境の投稿（同じカーネルやデータ名）がないか検索する。環境依存の解決はフォーラムの具体例が最短経路。
