---
layout: post
title: "Show HN: Crazierl – An Erlang Operating System - Crazierl — Erlangで動くオペレーティングシステム"
date: 2026-03-29T22:13:27.861Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://crazierl.org/demo/"
source_title: "Crazierl: an Erlang Operating System"
source_id: 47567049
excerpt: "ブラウザでErlang分散OSをURL共有で体験、即チャットやプロトタイプ可能だが要注意"
---

# Show HN: Crazierl – An Erlang Operating System - Crazierl — Erlangで動くオペレーティングシステム
ブラウザ上でErlangの分散OSを体験できるデモ — 友達と“dist”でつながる新感覚エミュレーション

## 要約
ブラウザ上のx86エミュレータ（v86）上で動く「Crazierl」は、Erlangプロセス間の標準的な分散機能（dist）をURLのハッシュで共有して複数ノードをつなげるデモ。実運用には致命的なセキュリティ注意事項があるが、学習やプロトタイピングに強力。

## この記事を読むべき理由
Erlang/BEAMはメッセージングや耐障害性の高いシステムで日本企業でも採用実績が多く、ブラウザで分散環境を即体験できるこのデモは、学習・プロトタイプ作成・社内デモに最適。実際の分散挙動やセキュリティ課題を手早く確認できる。

## 詳細解説
- 実行基盤：Crazierlはv86によりブラウザ内でx86環境をエミュレートし、その上でErlangベースのOSを動かす。端末UIはxterm.jsが利用される。  
- 分散接続（dist）：URLのハッシュを共有して同じハッシュに接続し、端末下のチェックボックスでdistを有効にすると、gen_tcp_distを用いたErlang分散が動作する。chat:start()などでノード間チャットが可能。  
- ネットワーキング：デモはwss://relay.widgetry.orgを使ったリレー経由や、gen_tcp_dist（平文）で通信する。つまり通信は暗号化・認証が十分ではない。  
- セキュリティ警告：ノード間に認証・隔離がないため、信頼できる相手同士でのみ使うべき。もし悪意あるノードと接続されれば、Erlangノードの制御や、万が一v86の脆弱性があればブラウザが乗っ取られるリスクがある。個人情報や資格情報は絶対に入力しない。  
- 法規・準拠：デモは地域法（例：California Digital Age Assurance Act）対応がされていない旨が明示されている点にも注意。

## 実践ポイント
- 試す際はローカルまたは信頼できる内部ネットワークで行う。公開ネットワークや不特定多数と接続しない。  
- 実験はサンドボックス化したブラウザプロファイルで、機密情報は扱わない。  
- 学習用途：Erlangのdistの挙動、gen_tcp_distの動作、ノード間メッセージングの挙動を手早く確認する教材として有効。chat:start()で簡単に動作確認できる。  
- 開発応用：社内プロトタイプや教育用デモの実装アイデアとして活用可能。セキュリティ設計（認証・暗号化）を付与してから本番化を検討する。

元デモ（v86 / xterm.js利用）をまずはローカルで触ってみると、分散Erlangの実態が直感的に掴める。
