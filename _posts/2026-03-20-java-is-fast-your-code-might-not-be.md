---
layout: post
title: "Java Is Fast. Your Code Might Not Be - Javaは速い。あなたのコードはそうとは限らない"
date: 2026-03-20T15:03:25.681Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://jvogel.me/posts/2026/java-is-fast-your-code-might-not-be/"
source_title: "Java Is Fast. Your Code Might Not Be. | Jonathan Vogel"
source_id: 47454384
excerpt: "同じJavaで1,198ms→239ms、スループット5倍にした8つの実践的最適化術"
image: "https://jvogel.me/_astro/string_concat_in_loop.9aeLgUH_.jpg"
---

# Java Is Fast. Your Code Might Not Be - Javaは速い。あなたのコードはそうとは限らない
Javaは速い。本当に重要なのは「コードの書き方」—同じアプリが1,198ms→239ms、スループット5倍になった現場の最適化術

## 要約
JVMやJDK自体は高速でも、ちょっとしたコーディング・アンチパターンが性能を大幅に悪化させる。プロファイリングで見つかる典型的な8つの問題を直すだけで劇的に改善する。

## この記事を読むべき理由
日本のサービスでも「同じJDKでも実行環境は複数台」「トラフィック増で微差が倍増の差になる」ため、簡単に見落としがちなホットパスの最適化は即効性が高い。中規模〜大規模システムの運用・開発者に直接役立つ。

## 詳細解説
以下は実際にプロファイリングで見つかった典型的な8つのアンチパターンとその改善要点。各例は「見た目は正しいがコストが高い」点を意識する。

1) ループ内の文字列連結（O(n²)のコピー）
- NG例:
```java
String report = "";
for (String line : logLines) {
  report = report + line + "\n";
}
```
- 問題: Stringは不変。毎回コピーされるため文字数が二次的に増える。
- 対策:
```java
StringBuilder sb = new StringBuilder();
for (String line : logLines) {
  sb.append(line).append("\n");
}
String report = sb.toString();
```

2) ループ内での.stream()（隠れたO(n²)）
- NG例: 各要素ごとに全リストをストリームして集計。
- 対策: 単一パスで集計（mergeやCollectors.groupingByを活用）。
```java
for (Order o : orders) {
  int hour = o.timestamp().atZone(...).getHour();
  ordersByHour.merge(hour, 1L, Long::sum);
}
```

3) ホットパスでのString.format()
- 問題: フォーマット文字列の解析コストが高い。
- 対策: 文字列連結やStringBuilderで組み立て、必要なら数値のみformatする。

4) ホットループでのオートボクシング
- NG例:
```java
Long sum = 0L;
for (Long v : values) { sum += v; }
```
- 問題: 毎回ボクシング/アンボクシングで多数のオブジェクトを生成。
- 対策:
```java
long sum = 0L;
for (long v : values) { sum += v; }
```

5) 例外による制御フロー（例: parse例外を日常的に使う）
- 問題: 例外生成はfillInStackTraceで高コスト。頻発するなら致命的。
- 対策: 事前バリデーションやisParsable系ユーティリティで例外を避ける。

6) 広範囲な同期（synchronizedがボトルネック化）
- NG例: メソッド単位でsynchronizedすると競合で遅くなる。
- 対策: ConcurrentHashMap + LongAdder等、細粒度で競合を緩和。
```java
private final ConcurrentHashMap<String, LongAdder> counts = new ConcurrentHashMap<>();
public void increment(String key) {
  counts.computeIfAbsent(key, k -> new LongAdder()).increment();
}
```

7) 再利用可能なオブジェクトを毎回生成（ObjectMapper等）
- 問題: 構築時の初期化コストが毎回発生する。
- 対策: スレッドセーフならstatic finalで使い回す。
```java
private static final ObjectMapper MAPPER = new ObjectMapper();
```

8) 仮想スレッドのピンニング（JDK21–23）
- 問題: synchronized内でブロッキングIOするとキャリアスレッドがpinされる（仮想スレッドのスケーラビリティを壊す）。
- 対策: ReentrantLockなどで同期を置き換える、またはJDK24以降の改善を確認。

補足: これらは単独では小さく見えても、アプリ全体では複合して大きな性能差を生む。プロファイラ（JFR/flame graph）でホットスポットを特定し、優先度順に対処する。

## 実践ポイント
- まずプロファイル：Java Flight Recorderで実際のホットパスを把握する。  
- ルールチェック：
  - ループ内で+を使っていないか（StringBuilderにする）
  - ループ内で.stream()を呼んでいないか
  - ホットメソッドでString.formatや例外生成をしていないか
  - 算術累積はプリミティブ型で行う
  - 再利用可能な重いオブジェクトはstatic/fieldで共有
  - 同期はConcurrentHashMap/LongAdderや細粒度ロックへ
- 仮想スレッドを使う場合はJDKバージョン依存のリスクを確認（21–23はpinningに注意、24で改善）。
- 小さな修正でもクラスター全体のスループット/コストに直結するため、負荷テスト→プロファイル→修正→再テストのループを回す。

以上。この記事は実際の改善事例（同一アプリで5倍スループット・87%ヒープ削減）に基づく実務的なチェックリストです。
