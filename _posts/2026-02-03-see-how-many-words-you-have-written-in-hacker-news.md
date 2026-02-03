---
layout: post
title: "See how many words you have written in Hacker News comments - Hacker Newsコメントで自分が書いた単語数を確認する"
date: 2026-02-03T05:36:24.311Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://serjaimelannister.github.io/hn-words/"
source_title: "HN Word Oracle"
source_id: 46829029
excerpt: "HNコメントをClickHouseで集計し、総単語数・順位と本換算を表示するランキング"
---

# See how many words you have written in Hacker News comments - Hacker Newsコメントで自分が書いた単語数を確認する
HNでの“語彙量”をランキング化！あなたのコメントはどれだけ書かれている？

## 要約
Hacker Newsのコメントを集計して、ユーザーごとの総単語数・順位・パーセンタイルや「何冊分の本か」換算などを表示するツール（ClickHouseを利用したプロジェクト）です。

## この記事を読むべき理由
日々の議論やアウトプット量を数値で把握できるため、コミュニティでの存在感評価やデータ分析の練習素材として日本のエンジニアにも価値があります。ClickHouseを使った高速集計の実例として学べます。

## 詳細解説
- 何をしているか：HN（Hacker News）のコメントコーパスを集計し、ユーザーごとの単語数を算出。上位1000のリーダーボードや全体に対するパーセンタイル、任意の換算（例：1冊 = 300,000語、Game of Thrones換算）を表示します。
- 技術要素：大規模テキスト集計にClickHouseのような列指向DBを使うことで、膨大なコメントを短時間で集計可能。UIはプレイフルな見せ方（リーダーボード、変換表示）でユーザー体験を高めています。実装はClickHouseクラスタへのクエリ実行が中心で、play.clickhouse.comのAPIを活用する例も見られます。
- 集計のポイント：コメントテキストを空白や正規表現でトークン化して単語数を取得し、作者ごとにSUM→ORDER BYで上位表示。データの前処理（HTMLエスケープ除去、ボット除外など）が精度に直結します。

簡単なClickHouseクエリ例（参考）：
```sql
SELECT author,
       sum(arraySize(splitByRegexp('\\s+', comment_text))) AS words
FROM hn_comments
GROUP BY author
ORDER BY words DESC
LIMIT 1000;
```

## 実践ポイント
- まずはツールのページを開いて自分のHNアカウントを確認してみる（URLを参照）。
- 同じ手法を日本サービス（Qiita、Zenn、はてな）に適用して、コミュニティ内の発言量を可視化してみる。
- ローカルで試すならClickHouseを立て、HNのコメントダンプ（または自サービスのログ）を投入して上のようなクエリを実行する。
- 倫理面：公開コメントのみを対象にし、個人情報や意図しない利用にならないよう配慮する。

元記事を実際に試して、ランキングや換算の遊び心をデータ分析の練習に活かしてみてください。
