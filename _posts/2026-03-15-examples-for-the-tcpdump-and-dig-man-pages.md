---
layout: post
title: "Examples for the tcpdump and dig man pages - tcpdump と dig の man ページ向け例"
date: 2026-03-15T12:38:23.176Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://jvns.ca/blog/2026/03/10/examples-for-the-tcpdump-and-dig-man-pages/"
source_title: "Examples for the tcpdump and dig man pages"
source_id: 47334668
excerpt: "tcpdumpとdigのmanに初心者向け実例を追加、現場で役立つ使い方と制作裏話を紹介"
---

# Examples for the tcpdump and dig man pages - tcpdump と dig の man ページ向け例
マンページが変わる！tcpdump と dig の「はじめの一歩」例集

## 要約
tcpdump と dig の公式 man ページに、初心者や使用頻度が低い人向けの「最も基本的な例」を追加・改善した取り組みの紹介とその気づき。

## この記事を読むべき理由
公式ドキュメントを見直すことで、実務で何度も役立つ小さなコツ（例えば tcpdump の -w と一緒に -v を使うと進捗が見える等）を確実に得られる。日本の現場でもトラブルシューティングや教育で直接役立つ内容。

## 詳細解説
- 目的：man ページに「初心者・たまに使う人向け」の最小限の実例を載せ、コマンドを思い出しやすくする。  
- tcpdump の発見：パケットをファイルに保存する際（-w out.pcap）、-v を併用するとキャプチャ件数のサマリが表示されて便利。こうした小さな運用ノウハウはメンテナ／レビューで明らかになる。  
- dig の例：クエリの基本（A レコード照会、特定 DNS サーバ指定、簡潔表示など）を示すことで DNS 調査の敷居を下げる。  
- 実装の工夫：tcpdump の man は roff（歴史あるフォーマット）で書かれており面倒なので、Markdown→roff の簡易変換スクリプトを作って編集性を高めた。mandoc や roff の歴史的背景にも触れつつ、ドキュメント整備の生産性向上を目指している。  
- 文化的観察：BSD 系と Linux 系でドキュメント運用の流儀に差があり、レビュープロセスを通した「正確さ」と「読みやすさ」の両立が重要。

## 実践ポイント
- すぐ使える tcpdump の基本例：
```bash
bash
# インターフェイス eth0 をキャプチャして画面に表示
tcpdump -i eth0

# ポート80のTCPのみをキャプチャしてファイルに保存（進捗を見るため -v を併用）
tcpdump -i eth0 tcp port 80 -w out.pcap -v
```
- すぐ使える dig の基本例：
```bash
bash
# シンプルに A レコードを表示
dig example.com A +short

# 特定の DNS サーバを指定して MX を調べる
dig @8.8.8.8 example.com MX
```
- ドキュメント改善に参加する価値：小さな「使い方例」の追加が、現場での誤用を減らし新人教育を楽にする。ローカルでのテスト・提案→レビューの流れに乗ると効果的。  
- 学んだことを共有する：会社のナレッジや社内訳注として man ページの「使い方例」を翻訳・追加しておくと、日本の現場で役立つ。

簡潔に言えば、公式 man ページに「最低限の例」があるだけでツールの壁がぐっと下がる。まずは上のコマンドを試し、気づいた小ネタをドキュメントに還元してみてほしい。
