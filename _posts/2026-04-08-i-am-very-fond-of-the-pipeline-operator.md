---
layout: post
title: "I Am Very Fond of the Pipeline Operator - パイプライン演算子が大好きです"
date: 2026-04-08T18:09:05.156Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://functiondispatch.substack.com/p/i-am-very-fond-of-the-pipeline-operator"
source_title: "I Am Very Fond of the Pipeline Operator - by Jack Smith"
source_id: 366989184
excerpt: "小さな関数を繋ぐパイプ演算子で読みやすくテストしやすいコードを実現する方法を学ぶ"
image: "https://substackcdn.com/image/fetch/$s_!vNwG!,w_1200,h_675,c_fill,f_jpg,q_auto:good,fl_progressive:steep,g_auto/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0dd23a92-1a90-4eea-a8e7-998626206361_1920x1080.png"
---

# I Am Very Fond of the Pipeline Operator - パイプライン演算子が大好きです
シンプルなのに魔法級。現場で役立つ「パイプ演算子」の魅力

## 要約
出力をそのまま次へ渡す「パイプ演算子」は古くはUnixの哲学に根ざし、関数合成を読みやすく・再利用しやすくする。小さな構文がチームの可読性と生産性を大きく向上させる。

## この記事を読むべき理由
日本の現場でもシェルスクリプト、ログ処理、CIやデータパイプラインが増えており、「小さな接着剤」であるパイプの考え方を知ることでコードの整理・運用負荷の削減に直結します。

## 詳細解説
- 起源：Unixの`|`は、あるプログラムの標準出力を別のプログラムの標準入力に繋ぐ単純かつ強力な仕組み。例えば外部APIのJSONを取得して整形する一連処理は次のように書けます。

```bash
curl -s 'https://cataas.com/api/cats' | jq '.'
```

- 合成性（composability）：各コマンド/関数は互いを知らずに連結可能。これは疎結合で拡張しやすい設計を促進する重要な性質です。
- プログラミング言語への展開：関数型言語（Elixir、OCaml等）はこの考えを言語レベルで取り入れている。Elixirの`|>`は値を次の関数に渡す直感的な構文を提供します。

```elixir
my_string = "A wizard is never late."
result = my_string |> String.upcase() |> String.reverse()
```

- オブジェクト指向的手法との比較：JSのメソッドチェーンでも似た表現は可能ですが、チェーンは中間状態の扱いや非純粋な副作用で読みづらくなることがある。最近のJS提案ではパイプ演算子も登場しています。

```javascript
const result = "A wizard is never late."
  |> (s) => s.toUpperCase()
  |> (s) => s.split('').reverse().join('');
```

- 実務的意義：パイプは小さな関数の組み合わせで複雑な処理を作ることを促し、ユニットテストや部分的なリファクタリングを容易にする。

## 実践ポイント
- シェル／CIでのログ変換やフォーマット処理にはまず`|`を意識する：小さいツールを繋いで一行ずつ処理する癖をつける。
- 新規プロジェクトやツール選定で、関数合成やパイプをサポートする言語（Elixir、OCaml、または将来のJSパイプ提案）を検討する。可読性・テスト容易性が向上する場面が多い。
- チーム規約として「短く単機能な関数を作り、パイプで繋ぐ」スタイルを導入すると、レビューと運用が楽になる。

興味があれば、まずはシェルで`curl | jq`のような小さなパイプの利用を増やしてみてください。
