---
layout: post
title: "A list of fun destinations for telnet - Telnetで遊べる面白スポット集"
date: 2026-01-27T07:08:37.010Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://telnet.org/htm/places.htm"
source_title: "Places to Telnet | telnet.org"
source_id: 46775135
excerpt: "Telnetで世界地図や天文データ、MUD/BBSまで遊び尽くせるレトロ体験案内"
image: "https://telnet.org/sx/telnet-soc.jpg"
---

# A list of fun destinations for telnet - Telnetで遊べる面白スポット集
懐かしさと好奇心を刺激する──テキストだけで遊べる「Telnetの遊び場」案内

## 要約
世界中のTelnetサーバーには、地図描画、宇宙データ、ターミナル版ゲーム、チャット/MUD/BBSまで多彩な遊び場が残っている。初心者でも試せる接続例と注意点を押さえて紹介する。

## この記事を読むべき理由
古いプロトコルだからこそ学べるネットワークの仕組み、レトロ文化としての価値、そしてWebでは味わえないテキスト体験があるため。日本でもレトロコミュニティや教育、プロトコル学習の題材として実用性が高い。

## 詳細解説
- Telnetとは：TCP上で動くテキストベースのリモート接続プロトコル。暗号化されないため現代のリモート管理には推奨されないが、公開サービスに接続してテキスト体験を楽しむ用途で使われる。
- 元記事の注目スポット（抜粋）：
  - mapscii.me（ASCII/Braille地図レンダラ） — 端末で世界地図をテキスト表示。
  - horizons.jpl.nasa.gov（NASA JPL HORIZONS） — 太陽系天体データ照会。
  - telehack.com — 古典的なネット体験を再現する遊べるサービス（Web版あり）。
  - doom.w-graj.net（ポート666） — 端末からDoomをプレイする試み。
  - freechess.org（FICS） — テキストベースのチェスサーバー。
  - ticker.bitcointicker.co — ビットコイン価格のライブ表示。
  - telnet.wiki.gd — Telnet経由のWikipedia風インターフェイス（AIアシスタント付き）。
  - 名作（現在はオフラインのことがある）：towel.blinkenlights.nl（Star Wars ASCIIアニメ）、rainmaker.wunderground.com（天気）、nyancat.dakko.us（ANSIアート）など。
  - MUD/BBS系：Aardwolf、BatMUD、Achaea、Legend of the Red Dragonなど、テキストMMOやBBSへの入口が多数。
- ディレクトリ：telnetbbsguide、vintagebbs、mudconnectなどで他のサーバーを探せる。
- 可用性と注意点：多くは趣味で運用されており、いつでもオフラインになる可能性がある。またTelnetは平文通信のため、認証情報や機密データの送信は避ける。

## 実践ポイント
- 簡単な接続例（ターミナル / コマンドプロンプト）：
```bash
# telnetが有効／インストールされている前提
telnet mapscii.me 23
telnet telehack.com 23
telnet doom.w-graj.net 666
telnet freechess.org 5000
```
- WindowsでTelnetを使うには「Windowsの機能の有効化」からTelnetクライアントをオンにするか、PuTTYなどのクライアントを使う。macOS/Linuxは通常ターミナルにtelnetコマンドがある（ない場合はパッケージで導入）。
- セキュリティ：パスワード入力や個人情報は送らない。公開コンテンツ閲覧や匿名プレイに留める。SSHやHTTPSが使えるならそちらを優先。
- 遊び方のヒント：まずはmapsciiやtelehackのような読み物系／観察系から入り、慣れたらMUDやBBSでチャットやゲームを試すと敷居が低い。
- 日本関連：レトロBBS文化やローカルの趣味コミュニティ（レトロPCイベント、同人サークル）と相性が良く、展示や学習教材としても活用できる。

元記事はTelnetの多彩な楽しみ方を列挙しており、まずは気になるホストに繋いで「手を動かす」ことを推奨する。
