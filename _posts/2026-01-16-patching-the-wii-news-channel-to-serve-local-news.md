---
layout: post
title: "Patching the Wii News Channel to serve local news - Wiiニュースチャンネルをパッチしてローカルニュースを配信する"
date: 2026-01-16T13:27:35.613Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://raulnegron.me/2025/wii-news-pr/"
source_title: "Patching the Wii News Channel to serve local news in 2025"
source_id: 1123103819
excerpt: "Wiiニュースチャンネルを改変し自家サーバで地域速報を配信する手法を実装解説"
---

# Patching the Wii News Channel to serve local news - Wiiニュースチャンネルをパッチしてローカルニュースを配信する
魅力的なタイトル: 「今でも動くWiiで地元ニュースを読む方法 — レトロ機器を“情報端末”に変える技術実験」

## 要約
2007年のWiiニュースチャンネルを解析・改変して、公式配信先を自前サーバに差し替え、現地（例：プエルトリコ）の最新ニュースをWii上で表示するまでの研究と実装を解説します。

## この記事を読むべき理由
レトロハードの“生きた”オンライン機能復元は単なる趣味に留まらず、組み込み向けHTTP観察、バイナリパッチ、圧縮・署名付きバイナリ生成、サーバ自動化といった実務で役立つ技術が凝縮されています。日本のレトロゲーム愛好家やエンジニアが学ぶ価値が高い内容です。

## 詳細解説
- 背景：WiiのNews Channelは2007年開始、2013年に公式配信終了。しかしコミュニティ（WiiLink等）が非公式サーバを立てて機能を復元しています。本プロジェクトは「公式URLの差し替え」と「ニュース用バイナリの生成」を両方実現します。
- 取得方法の解析：Wiiは起動時にnews.bin.00〜news.bin.23のようなファイルをHTTPで取得します。mitmproxyなどを使うと実際のHTTP要求を観察可能で、URL構造には言語コード（例: 1＝English）と国コード（例: 049＝US）が含まれることが分かります。
- パッチの方針：WiiLinkのパッチはNews Channel内のハードコードされたURLを書き換えています。WAD（Wiiのパッケージ）から対象の.app（例: 0000000b.app）を抽出し、パッチ差分（xdelta/vcdiff/bsdiffなど）を適用してnews.dolを得る流れです。バイナリ内の文字列（元URL）を新URLに置換するだけで動作するケースが多いです。
- ツールと実装例：
  - wadlib（Go）でWADの展開/更新を行い、xdeltaでパッチ適用、Hexエディタで差分確認。
  - ニュース生成はWiiLinkのNewsChannel（Go）をベースに、記事収集→バッファ組立→LZ10圧縮→RSA署名→ファイル出力のパイプラインで行います。
  - 自動化はAWS Lambda + EventBridgeで1時間ごとにnews.binを再生成・配置する構成が紹介されています。
- 技術的なポイント：
  - URLはprintf形式（%d/%03d）で時間スロットを作るため、news.bin.00〜.23が要求される。
  - LZ10はNintendo系のLZ77変種。圧縮実装（Goのlzxなど）で整合性を取る必要があります。
  - 生成ファイルは署名されているので、正しくRSAで署名しないとクライアントが拒否する場合あり。
  - 言語・国コードに注意（Wii設定に依存）。

（参考として、WAD内のURLを置換するGoの抜粋）
```go
// go
// 簡略化例：バイナリ内の文字列を差し替えてWADを更新
original := []byte("http://news.wapp.wii.com/v2/%d/%03d/news.bin")
replacement := []byte("http://your.server/news/%d/%03d/news.bin")
content, _ := wad.GetContent(1)
off := bytes.Index(content, original)
copy(content[off:off+len(original)], pad(replacement, len(original)))
wad.UpdateContent(1, content)
```

## 実践ポイント
- 安全対策：元のWADは必ずバックアップ。実機への書き込みは自己責任で。コミュニティのガイド（WiiLink等）を参照してください。
- 初心者向けハードルを下げる：
  - まずmitmproxyでWiiのHTTP挙動を観察して「どのファイルを取っているか」を確認する。
  - 次にWiiLinkの既存ツールやリポジトリを読む（NewsChannel/NewsGenerator系）ことでバイナリ生成の流れを理解する。
- 日本市場との関連：
  - 日本国内にもWiiを持つレトロ層は根強く、地域ニュース（ローカル紙や自治体情報）を表示するサービスはローカライズのネタになります。
  - 技術的にはHTTPプロキシ、バイナリ解析、圧縮/署名、サーバレス自動化といったクラウド/組み込みスキルが学べ、社内のレガシー解析や組み込みプロトタイピングに応用できます。
- すぐに試せる行動：
  1. Wii本体のプロキシ設定を使ってmitmproxyで通信を観察する（法とルールを守って）。
  2. WiiLinkのNewsChannelリポジトリをcloneして、ローカルでnews.bin生成フローを追う。
  3. wadlibやxdelta等でWADの展開・差分適用を試し、バイナリ内のURL置換を小さく検証する。

興味があれば、実装リポジトリ（WiiNewsPR / WiiNewsPR-Patcher）やWiiLinkのソースを参照して、具体的なコードや自動化設定を学んでください。
