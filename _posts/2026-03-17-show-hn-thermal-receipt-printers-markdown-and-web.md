---
layout: post
title: "Show HN: Thermal Receipt Printers – Markdown and Web UI - サーマルレシートプリンターをMarkdownとWeb UIで活用する"
date: 2026-03-17T00:17:09.148Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/sadreck/ThermalMarky"
source_title: "GitHub - sadreck/ThermalMarky · GitHub"
source_id: 47366766
excerpt: "Markdownで作って即印刷、QRや中央寄せ対応の小型レシート活用法"
image: "https://opengraph.githubassets.com/eda28103914a673e6ba051ed61feae5b7fb7a8bf5a269117e114b96102b4da7f/sadreck/ThermalMarky"
---

# Show HN: Thermal Receipt Printers – Markdown and Web UI - サーマルレシートプリンターをMarkdownとWeb UIで活用する

眠っているレシートプリンターを再活用！Markdownで書いてそのまま印刷、QRコードやセンタリングもOKなシンプル手法

## 要約
サーマルレシートプリンターをMarkdown入力で手軽に印刷できるオープンソースツール「ThermalMarky」。Web UI／CLI／Docker対応で、テック初心者でも試しやすい構成です。

## この記事を読むべき理由
日本の小規模店舗、IoTハッカ―、イベント運営者などで既存の安価なサーマルプリンターを実用的に再利用できるから。ラベルや簡易レシート、QR付き案内の自動化に便利です。

## 詳細解説
- 機能概観：Markdownの見出し・太字・下線・リストをサポートし、独自タグでテキストの左右／中央寄せ、水平線、QRコード生成が可能。Webベースのエディタ（ショートカット付き）とCLIの両方を備えます。
- 入出力手段：USB接続またはネットワーク経由でプリンターに送り、ESC/POS系ライブラリ（python-escpos）を利用。プロジェクトはPythonで実装され、HTMLベースのUIを提供します。
- 設定：.env.example を .env にリネームして設定。USB時はベンダー／プロダクトID（lsusbで確認）を、ネットワーク接続ならIPとポートを指定。行幅（MARKY_LINE_WIDTH）や最大出力行数（MARKY_MAX_LINES）でレイアウト制御できます。
- 動作環境：Docker推奨（USB権限や依存関係対策が容易）。ローカル実行時は Python 3.12+ と libusb 等のネイティブライブラリが必要。開発者は自己署名証明書でHTTPSを提供しているためブラウザ警告が出ます。
- テスト済み機種：MUNBYN ITPP047UE（リポジトリではこの機種で確認）。プリンターの互換性は機種ごとに差があるため事前確認が重要。

## 実践ポイント
- プリンター確認（USB例）
```bash
# USB接続でベンダー/プロダクトID確認
lsusb
```
- 簡単セットアップ（Docker推奨）
```bash
# ビルド＆起動
docker compose up --build
# UIにアクセス
# https://localhost:8000（自己署名証明書の警告あり）
```
- ローカル実行の要点
  - Python仮想環境を作ってrequirementsを入れる
  - 必要なネイティブライブラリ（libusb 等）を事前インストール
- 印刷例（CLI）
```bash
# Markdownファイルを印刷
python print.py my_receipt.md
# パイプから直接送る
echo "# Hello" | python print.py
```
- カスタムタグ活用例：`[align=center]`で中央寄せ、`[qr=https://...]`でQR生成、`[effect=line--]`で罫線。
- 日本市場での応用案：店頭の簡易レシート、イベントの案内チケット、倉庫ラベル、ワークショップでのハンズオン素材作成。

興味があればリポジトリ（sadreck/ThermalMarky）をフォークして、使用プリンターに合わせた調整から始めると実用化が早いです。
