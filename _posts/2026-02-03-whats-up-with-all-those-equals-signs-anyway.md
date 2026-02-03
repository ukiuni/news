---
layout: post
title: "What's up with all those equals signs anyway? - 末尾に「=」だらけのメールはなぜ起きるのか"
date: 2026-02-03T09:47:44.223Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://lars.ingebrigtsen.no/2026/02/02/whats-up-with-all-those-equals-signs-anyway/"
source_title: "What&#8217;s up with all those equals signs anyway? &#8211; Random Thoughts"
source_id: 46868759
excerpt: "行末の「=」はQuoted-printableのソフト改行が改行変換で壊れ文字化けを招く"
image: "https://lars.ingebrigtsen.no/wp-content/uploads/2026/02/2026-02-02.jpeg"
---

# What's up with all those equals signs anyway? - 末尾に「=」だらけのメールはなぜ起きるのか
メール本文が“=”だらけに見える理由はこれだ！Quoted-printableと改行変換ミスで文字が消える現場レポート

## 要約
古いメールの断片で見かける「=」は暗号でもOCRの跡でもなく、Quoted-printableというメールエンコーディングの“ソフト改行”表現（=CRLF）が誤処理された結果です。改行コード変換や手抜きデコーダで文字化けや一文字欠落が発生します。

## この記事を読むべき理由
日本でもレガシーメールの移行、アーカイブ公開、スクレイピングやSNSで過去メールが話題になる場面は多く、原因を知っておくと誤情報の拡散を防ぎ、データ復旧やログ解析で役立ちます。

## 詳細解説
- Quoted-printableは、長い行や非ASCII文字を安全に送るために使われるMIMEエンコーディング。行末に等号「=」を置いて改行（=CRLF）を示し、表示上は行をつなげる（soft line break）。
- しかしメール処理でCRLFをLFに変換すると、元の3バイト (=CRLF) が =LF のようになり、正規デコーダが期待するシーケンスと合わなくなる。
- さらに単純な実装（末尾の"="を探して文字数を削る、あるいは"=C2"等を単純置換）だと、UTF-8の多バイト列（例: =C2=A0 のノーブレークスペース）を壊したり、直前の文字が消える（例: "cloven" の "c" が消える）といった破壊的な結果になる。
- 結果として「=」が残ったり =C2 =A0 のような断片がそのまま表示され、「何これ？」となる。

## 実践ポイント
- 正しい対処：Quoted-printableを扱う際は改行をCRLFのまま扱うか、信頼できるライブラリでデコードする（手作業の正規表現置換は避ける）。
- ライブラリ例（簡易）:
```python
python
import quopri, email
raw = b'...'  # RFC822準拠のバイト列（CRLFを保持）
decoded = quopri.decodestring(raw)
# もしくは email パッケージでMIMEを正しくパース
```
- 移行時のチェックリスト：CRLFを破壊しない、quoted-printableデコードを通す、UTF-8やISO-2022-JPなどの文字コードを意識する、怪しい箇所は元データと比較して検証する。
- 既に「=」だらけになったテキストを救うなら、まず元の行結合（末尾の'='で行を接続）を復元してからQuoted-printableデコードを試す。

小さなエンコーディング処理ミスが目に見える奇妙なゴミを生みます。古いメールやスクレイプ結果を扱うときは、まずQuoted-printableと改行コードを疑ってください。
