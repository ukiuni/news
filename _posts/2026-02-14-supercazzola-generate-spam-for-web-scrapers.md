---
layout: post
title: "Supercazzola - Generate spam for web scrapers - Supercazzola：Webスクレイパー向けスパムを生成するツール"
date: 2026-02-14T02:29:22.163Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://dacav.org/projects/supercazzola/"
source_title: "Supercazzola"
source_id: 1259669082
excerpt: "マルコフ連鎖で無限ダミー頁を生成し、悪質スクレイパーを資源浪費に誘導する実践的対策ツール紹介"
---

# Supercazzola - Generate spam for web scrapers - Supercazzola：Webスクレイパー向けスパムを生成するツール
クローラーをハマらせる「ダミー迷路」――Supercazzolaで賢くスクレイピング対策

## 要約
Supercazzolaは、マルコフ連鎖で動的に無限のダミーページを生成し、robots.txtを無視する貪欲なクローラ／AIボットを時間とリソースの無駄に誘導するためのツール群です（mchain, spamgen, spamd）。

## この記事を読むべき理由
日本でもニュースサイトやECのスクレイピング被害、無断データ収集は増加しています。Supercazzolaは「攻撃」ではなく「騙しの防御策」として使える一つの実践的アプローチで、運用と法的配慮を踏まえた対策案を学べます。

## 詳細解説
- 仕組み：入力テキストからmchainでマルコフ連鎖データを作成し、spamdがその連鎖を使ってランダムなHTMLページ（spam endpoint）と統計情報（info endpoint）を生成します。spamgenは単体で文を生成するツール。
- コンポーネント：
  - mchain：複数テキストからマルコフ連鎖（.markov）を生成。
  - spamgen：生成済みマルコフ連鎖からランダム文を出力。
  - spamd：HTTPデーモンとしてダミーページを配信、訪問者情報を記録。
- 依存関係：cmake、pkg-config、libevent >= 2。動作確認はGNU/Linux・FreeBSDで報告。
- 運用ポイント：
  - 逆プロキシ経由でspamエンドポイントへリクエストを転送し、X-Forwarded-Forに対応して統計を取れる。
  - URIプレフィックスを切り取る設定（uri_prefix）でプロキシ環境にも柔軟対応。
  - robots.txtにspam用のパスを明示して「正当なボット」は避けられるようにする想定。
- 主な設定項目（抜粋）：daemon.foreground, daemon.uid/gid, spam_ep.bind, spam_ep.mkvchain, spam_ep.n_paragraphs, spam_ep.n_sentences, spam_ep.n_references, spam_ep.max_sentence_len。

簡単なインストール手順例（FreeBSDベースの抜粋）：
```bash
# 依存導入
pkg install -y devel/pkgconf devel/libevent devel/cmake-core

# ビルド
tar -xzf supercazzola-*.tar.gz
cmake -S ./supercazzola-*/ -B ./build
cmake --build ./build
cmake --install ./build

# マルコフ連鎖作成（例：Gutenbergのテキスト）
mchain ./84.txt.utf-8 /usr/local/share/spamd/default.markov

# 動作確認
spamd -f      # フォアグラウンドで起動（ログ確認用）
spamd         # デーモン起動（設定ファイル経由）
```

## 実践ポイント
- まずローカルでマルコフ連鎖を作成してspamgenで出力を確認する（品質・語調を把握）。
- spamdを逆プロキシの特定パス（例 /spam/ ）に割り当て、プロキシのログで挙動を観察する。
- robots.txtにspamエンドポイントを明記して「正当なクローラ」を保護する（例：User-agent: * Disallow: /spam/）。
- 運用時は法令・利用規約を確認し、商用サイトや第三者データを故意に毀損・混乱させない運用方針を定める。
- 需要があれば設定（n_paragraphs や mkvchain など）を調整してトラフィックのコストを増やす／解析を困難にする。

元プロジェクトはBSD 3-Clauseライセンスで配布されています。導入前にライセンスと利用目的を確認してください。
