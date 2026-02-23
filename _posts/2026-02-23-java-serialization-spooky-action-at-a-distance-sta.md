---
layout: post
title: "Java Serialization: Spooky Action at a Distance - Java シリアライズ：遠隔で起こる不気味な副作用"
date: 2026-02-23T16:05:35.076Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://youtu.be/2sxK-z84Oi4?si=HeHzWAFYsO0MBauT"
source_title: "Java Serialization: Spooky Action at a Distance - YouTube"
source_id: 398568909
excerpt: "Java標準シリアライズが遠隔で任意処理を誘発する危険と実践的対策を分かりやすく解説"
image: "https://i.ytimg.com/vi/2sxK-z84Oi4/maxresdefault.jpg"
---

# Java Serialization: Spooky Action at a Distance - Java シリアライズ：遠隔で起こる不気味な副作用
信頼できないシリアライズデータがあなたのアプリを裏側から動かす――Javaの“見えない攻撃”をやさしく解説

## 要約
Javaの標準シリアライズは、受け取ったバイト列を復元するときに任意のクラスの処理（readObject や readResolve など）を実行するため、不注意に使うとリモートで不正な振る舞いを誘発される危険がある。対策は「信頼できないデータはシリアライズしない／復元しない」「クラスのホワイトリスト化とフィルタリング」「安全な代替フォーマットの採用」。

## この記事を読むべき理由
日本の企業でもJavaは基幹系やWebサービスで広く使われており、古いライブラリや社内APIで標準シリアライズをそのまま使っているケースが多い。攻撃者は意図した場所とは別のクラスの副作用を利用してコード実行や情報漏えいを引き起こせるため、エンジニアは仕組みと対策を知っておく必要があります。

## 詳細解説
- 基本仕組み：Javaの標準シリアライズはSerializableインタフェースをもつオブジェクトをバイト列化し、ObjectInputStreamで復元する。復元時にクラスのカスタム読み込みメソッド（readObject、readResolve、readObjectNoData など）が実行される。
- なぜ「怖い」のか：受信したデータがそのまま復元処理をトリガーするため、攻撃者が巧妙に作ったオブジェクトグラフ（gadget chain）を送れば、ターゲット環境に元からあるクラス群の副作用を連鎖させて任意の動作を起こせる。要するに「データを復元しただけで遠くのコードが動く」——これがタイトルの“Spooky Action at a Distance”。
- 代表的リスク要因：古いライブラリ（commons-collections など）に存在する便利なメソッドを悪用するパターン、シリアライズを受け付ける公開API（HTTP、RMI、メッセージキュー）など。
- JDK側の緩和策：最近のJDKではObjectInputFilter等のシリアライズフィルタ機能が導入され、クラス許可/拒否やサイズ制限で危険な入力をブロックできる。さらにライブラリ更新や脆弱性修正も重要。
- 設計上の対策：そもそも外部入力をJavaネイティブシリアライズで受け渡さない（JSON/Protobufなどの明示的フォーマットを採用）、最小権限設計、依存ライブラリの把握。

## 実践ポイント
- 外部/未検証の入力をObjectInputStreamで復元しない。
- どうしても使う場合はObjectInputFilterでクラスのホワイトリストを設定し、オブジェクト数・深さ・サイズを制限する。
- 古いライブラリは最新に更新し、既知のgadgetを含む依存を避ける（脆弱性情報をチェック）。
- RESTやメッセージング間はJSONやProtobufなど明示的で安全性の高いシリアライズ方式に切り替える。
- テスト/監査：シリアライズを使う箇所をコードレビューで洗い出し、静的解析ツールや動的検査で復元コードの実行パスを確認する。

短く言えば、「見えない副作用」を防ぐには、信頼できないデータをそのまま復元しないことと、JDKのフィルタ機能や設計の見直しで攻撃面を減らすことが最も実践的です。
