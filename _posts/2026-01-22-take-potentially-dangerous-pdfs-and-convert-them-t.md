---
layout: post
title: "Take potentially dangerous PDFs, and convert them to safe PDFs - 潜在的に危険なPDFを安全なPDFに変換する"
date: 2026-01-22T00:19:17.680Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/freedomofpress/dangerzone"
source_title: "GitHub - freedomofpress/dangerzone: Take potentially dangerous PDFs, office documents, or images and convert them to safe PDFs"
source_id: 46712815
excerpt: "疑わしいPDFをサンドボックスで画素化し埋め込み悪用を除去、即運用可"
image: "https://opengraph.githubassets.com/6546ebec1ca2079d5676d585e0719c942caa808d488e36ed3636024f35b29f2c/freedomofpress/dangerzone"
---

# Take potentially dangerous PDFs, and convert them to safe PDFs - 潜在的に危険なPDFを安全なPDFに変換する
添付ファイルが怖くなくなる—危険PDFを“画素化”して完全に無害化するDangerzone入門

## 要約
Dangerzoneは、疑わしいPDF／Office文書／画像を安全なPDFに変換するオープンソースツールで、サンドボックス内で文書をラスタ化（各ページをRGBピクセル列に変換）してから外側で再構築することで埋め込みコードや悪意ある機能を排除します。

## この記事を読むべき理由
メール添付やダウンロード文書からの攻撃は日本の企業・個人にも頻発。手軽に導入できる安全化ワークフローとして、社内運用や調査業務で即戦力になるため。

## 詳細解説
- 基本処理フロー：入力（PDF／docx／xlsx／pptx／odt／hwp 等や画像）→ サンドボックス内でPDF化（必要なら）→ PDFをページごとの生のピクセル（RGB）に変換 → サンドボックス外でピクセルから新しいPDFを生成。これにより埋め込みスクリプト、悪意あるフォント、リンク、埋め込みファイルなどを除去できる。  
- サンドボックス実装：コンテナベース（macOS/WindowsはDocker/埋め込みPodman、Linuxはpodman）。gVisorを使いシステムコールを制限し、ネットワークアクセスも無効化できるため、サンドボックスが破られても外部と通信用の経路がない。  
- 追加機能：変換後にOCRでテキストレイヤを再付与、ファイルサイズ圧縮、変換後のPDFを好みのビューアで自動的に開く設定。  
- サポート環境とライセンス：macOS/Windows/主要Linux/Qubes/Tails対応。AGPLv3で公開。  
- セキュリティ評価：Include Securityによる監査で高リスクは指摘されず、低リスク・情報レベルの所見あり。エアギャップ利用や更新手順のドキュメントあり。

## 実践ポイント
- 導入：公式ページ／GitHubからバイナリを取得してインストール。社内の受信メールルールでDangerzone経由で開く運用を検討する。  
- 既存運用との統合：既定のPDFビューア設定をDangerzone経由に変えると誤開封を防げる。  
- OCRの有無：検索やコピペが必要ならOCRを有効に。機密保持ならOCRをオフにして画像のみで管理。  
- エアギャップと更新：オフライン環境でも動作可。コンテナイメージ更新手順を確認して安全にパッチを適用する。  
- テスト運用：社内で代表的な文書形式をテスト変換し、見え方（レイアウト／文字化け）と業務影響を確認してから全社展開する。  

関連リンク：公式リポジトリ（GitHub: freedomofpress/dangerzone）
