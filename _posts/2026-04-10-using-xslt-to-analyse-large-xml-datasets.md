---
layout: post
title: "Using XSLT to analyse large XML datasets - 大規模XMLデータをXSLTで解析する"
date: 2026-04-10T21:29:11.074Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://xn--mbius-jua.band/blog/nmapview/"
source_title: "Using XSLT to analyse large XML datasets"
source_id: 365019243
excerpt: "XSLTでNmapのXMLを1ファイルHTMLに変換し数百ホストを即トリアージ"
---

# Using XSLT to analyse large XML datasets - 大規模XMLデータをXSLTで解析する
Nmapの「ノイズ」を瞬時に可視化する：XSLTで生成する1ファイルHTMLレポートで速攻トリアージ

## 要約
NmapのXML出力をXSLT（xsltproc）で単一のインタラクティブHTMLに変換し、ブラウザ側でフィルタ・集約・可視化してスキャンのトリアージを劇的に速める手法を紹介します。

## この記事を読むべき理由
大量ホストのスキャン結果は“何が開いているか”よりも“どこを先に見るか”が重要。日本のSOCやペンテスト現場で環境構築なしに素早く共有・解析できる現実的なワークフローです。

## 詳細解説
- なぜXSLTか：NmapはXMLを出力するため変換ツールが不要、xsltprocは軽量で広く利用可能。XSLTでHTMLの骨格を作り、動的部分（ソート・グルーピング・プロット）はブラウザのJavaScriptに委ねる設計。
- パイプライン：1) Nmapでscan.xmlを出力 2) xsltproc + NmapView.xsl → report.html 3) ブラウザでフィルタ／プロット／エクスポート
- 主要機能：
  - Host Overview：状態・ベンダ・OS推定・ポート数・ローカルな「Rarity（希少度）」で異常ホストを浮かび上がらせる。
  - Open Services：ポート・サービス・バージョン・NSE出力を1行にまとめ、クリックでHTTPを開けるなど素早い追跡が可能。
  - Service Summary：サービス→製品→バージョンでグルーピングし、バージョン分散（version drift）を視覚化。
  - 可視化：サービス分布、ホスト×ポートマトリクス、その他プロットでパターン検出。
  - エクスポート：表示中の結果をCSV/Excel/JSONで書き出し、別ツール（httpx/nuclei/testssl.sh等）へ引き継ぎ可能。
- 制約：CDN依存（デフォルトで完全オフラインではない）、scanの検出品質に依存、ブラウザ処理なので数百ホスト規模が実用上の目安。

## 実践ポイント
- まずは試す（bash）
```bash
# bash
curl -fsSL -o NmapView.xsl \
  https://github.com/dreizehnutters/NmapView/releases/latest/download/NmapView.xsl
xsltproc -o report.html NmapView.xsl scan.xml
# ブラウザで report.html を開く
```
- スキャン時のコツ：-sV と NSE を適切に使い、サービス検出精度を上げる（グルーピング精度が向上）。
- トリアージの流れ：Host Overview（Rarityで絞る）→ Open Services（異常ポート／証明書情報確認）→ Service Summary（バージョン差分把握）。
- 共有運用：クライアントやチームへは単一HTMLを渡すだけでOK。完全オフラインが必要なら前述のフロントライブラリをローカルに置く。
- 大規模運用： ~500ホストが目安。それ以上は分割スキャンかサーバ処理に切替えを検討。

参考：GitHub repo — dreizehnutters/NmapView、ライブデモあり。
