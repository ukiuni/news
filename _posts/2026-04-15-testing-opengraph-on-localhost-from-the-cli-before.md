---
layout: post
title: "Testing OpenGraph on localhost from the CLI before you go public - 公開前にローカルでOpenGraphをCLIから確認する方法"
date: 2026-04-15T16:33:45.500Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://simonhartcher.com/posts/2026-04-15-testing-opengraph-on-localhost-from-the-cli"
source_title: "Testing OpenGraph on localhost from the CLI before you go public | Simon Hartcher"
source_id: 1566001888
excerpt: "公開前にローカルで数秒確認、og-checkで画像付きOGカードを端末表示"
image: "https://simonhartcher.com/og/2026-04-15-testing-opengraph-on-localhost-from-the-cli.png"
---

# Testing OpenGraph on localhost from the CLI before you go public - 公開前にローカルでOpenGraphをCLIから確認する方法
ローカルでサクッとOpenGraphカードをプレビューして、公開前の微調整を高速化する方法

## 要約
公開URLがなくてもローカルのページからOpenGraph/Twitterカードをターミナル上でプレビューできるツール「og-check」を紹介。画像付きで数秒のフィードバックが得られるため、デプロイやトンネル待ちの手間を省けます。

## この記事を読むべき理由
OG/Twitterカードの表示はSNSでの見え方に直結しますが、FBやTwitterのデバッガーは公開URLやキャッシュ問題で試行錯誤が遅くなりがち。日本のスタートアップや個人開発者でも、ローカルで高速に確認できればリリース品質が上がります。

## 詳細解説
- 問題点：FacebookやTwitterのデバッガー、opengraph.xyzなどは公開URLが必要、さらにFacebookはキャッシュが強く途中版が固定されやすい。
- 解決策：og-check（neutilsの一部）がローカルのURLをフェッチし、metaタグ（og:*, twitter:*, article:* など）を抽出してターミナルにレンダリングします。画像はダウンロードしてKitty graphics protocol のエスケープシーケンスでインライン表示します。
- 実装の要点：
  - 言語/ライブラリ：Zig（std.http.Client, std.json）で実装。
  - Markdown→端末レンダリングは zigdown に委譲。画像描画はzigdown内でKittyプロトコルを出力。
  - 対応端末（Kittyプロトコル対応）：Kitty、Ghostty、WezTerm、Konsole、iTerm2、Warp、wayst、st（パッチあり）、xterm.js（一部）など。未対応端末ではテキストのみ表示。
  - 出力フォーマット：opengraph（デフォルト）、twitter、table（タグ一覧）、json（機械可読）。
  - バリデーション：必須フィールド（og:title, og:type, og:image, og:url）が欠けるとstderrにエラーを書いて非0終了 → CIのスモークテストに有用。

## 実践ポイント
- ローカル開発ループに組み込む：レイアウト修正 → 保存 → og-check http://localhost:PORT を数秒で実行して見た目を確認。
- CI取り込み：必須OGフィールドの有無でビルドを失敗させることで、デプロイ前チェックに使える。
- 端末選び：画像プレビューが欲しいなら Kitty / WezTerm / iTerm2 等を使う（日本ではmacOS+iTerm2やWezTerm利用者が多い）。
- インストール例（簡易）：

```bash
# og-checkの使い方（例）
og-check http://localhost:4343/
og-check -o twitter http://localhost:4343/
og-check -o json http://localhost:4343/ | jq '.og.image'
```

```bash
# ソースからビルド（Zig 0.15+が必要）
git clone https://github.com/deevus/neutils
cd neutils
# インストール先は例: ~/.local/bin
zig build install --release=small --prefix ~/.local
```

- 配布バイナリやmise経由での導入も可能（Linux/macOS/Windows・x86_64/aarch64対応）。

このツールを使えば、公開前の「カード表示チェック」が数分→数秒のサイクルになり、SNSでの初期表示ミスやキャッシュ地獄を避けられます。
