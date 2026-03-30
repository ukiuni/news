---
layout: post
title: "I use excalidraw to manage my diagrams for my blog - ブログの図をExcalidrawで管理する方法"
date: 2026-03-30T07:59:27.042Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://blog.lysk.tech/excalidraw-frame-export/"
source_title: "How I manage Images for my Blog | Martin Lysk"
source_id: 47571376
excerpt: "VSCodeで保存するだけでExcalidraw図を両テーマSVGに即書き出し、編集が高速化"
image: "https://blog.lysk.tech/assets/images/export.light.exp-9ea347e12c4c7c5d619086eb6016a934.svg"
---

# I use excalidraw to manage my diagrams for my blog - ブログの図をExcalidrawで管理する方法
VSCodeでExcalidrawを編集すると自動でLight/Dark SVGを出力してローカルで即プレビューできるワークフロー

## 要約
Excalidrawの図をフレームで切って名前にexport_プレフィックスを付けると、VSCode拡張が自動でLight/DarkのSVGを生成し、ローカルで即プレビューできるようにした話。

## この記事を読むべき理由
ブログや技術ドキュメントで画像と文章を何度も調整する開発者/技術ライターは、画像の再出力→コミット→プレビューの遅延で生産性が落ちる。本手法はその痛みを解消し、特にARM Macを使う日本の開発者に有用。

## 詳細解説
- 背景：著者はまずGitHub Actions＋excalirenderで、変更された .excalidraw ファイルからフレームを抽出してlight/dark両方のSVGを生成する仕組みを作成。処理はjqでフレーム名を取ってexcalirenderで出力し、生成物をコミットするワークフローだった。
- 問題点：excalirenderの描画バグやx86ベースのコンテナがARM Macで動かないなどの制約で、ローカルで即座に画像確認できない。結果として「編集→プッシュ→CI待ち→プル」という遅いループが残る。
- 新アイデア：VSCode上のExcalidraw拡張（著者のフォーク）に自動エクスポート機能を追加。動作は単純で、開いている *.excalidraw を監視し、フレーム名が export_<名前> のものを検出して、同ディレクトリに
  - <名前>.light.exp.svg
  - <名前>.dark.exp.svg
 という形で出力する。これにより編集すると即座にローカルにSVGが更新され、エディタ内のプレビューやオートコンプリートで反映される。
- 実装要素：フレームで要素を囲む、フレームのnameフィールドに export_ を付与、拡張がフレーム名をパースしてSVGを2種生成して保存。GitHub Action版はgit diffで変更ファイル検出→jqでフレーム列挙→excalirenderで出力→コミット、という流れ。

## 実践ポイント
- すぐ使う手順：
  1. Excalidrawで図をフレームで囲む。フレーム名を export_<画像名> にする。  
  2. 著者のVSCode拡張（フォーク／リリースアーティファクト）をインストールするか、既存ワークフローにGH Actionを組み込む。  
  3. 保存すると同ディレクトリに <画像名>.light.exp.svg / <画像名>.dark.exp.svg が生成されるので、Markdownから参照して即プレビュー。
- 利点：ローカルで即時プレビュー、Light/Dark対応の自動生成、ブログや社内ドキュメントの編集速度向上。
- 注意点：拡張はフォーク版の提供に依存するため、導入前に互換性と信頼性を確認する。既存CI方式は環境差（ARM/x86）に注意。

以上を採り入れれば、図版の微調整と記事執筆を同時に高速化でき、特にローカルレビュー重視のワークフローに大きな恩恵があります。
