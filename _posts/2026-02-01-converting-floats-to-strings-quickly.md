---
layout: post
title: "Converting floats to strings quickly - 浮動小数点を文字列へ高速変換"
date: 2026-02-01T18:30:50.523Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://lemire.me/blog/2026/02/01/converting-floats-to-strings-quickly/"
source_title: "Converting floats to strings quickly &#8211; Daniel Lemire&#039;s blog"
source_id: 909289103
excerpt: "Dragonbox/Schubfachで浮動小数点→文字列を高速化、帯域I/O削減の最適化指針"
image: "https://lemire.me/blog/wp-content/uploads/2026/02/Capture-decran-le-2026-02-01-a-10.32.13.png"
---

# Converting floats to strings quickly - 浮動小数点を文字列へ高速変換
魅惑の「0.00011」が遅い理由――高速・短縮化された浮動小数点→文字列変換の今

## 要約
浮動小数点を最短かつ高速に文字列化するアルゴリズムを比較した実験レビュー。Dragon系から最新のRyū／Schubfach／Dragonboxまで、処理コストと出力長のトレードオフを明らかにしている。

## この記事を読むべき理由
JSONやCSVシリアライズ、ログ、高速通信で大量の数値を扱う日本のサービス開発者・組込みエンジニアは、変換速度と文字列長が帯域・I/O・コストに直結するため、本稿の知見は即効性のある最適化指針になる。

## 詳細解説
- 背景：CPUやライブラリ実装の高速化で、数値→文字列変換の「文字列生成部分」が全体の約20〜35%を占め、重要度が増している。  
- 変換は大きく2段階：1) 数値から有効数字（significand）と10乗（power of 10）を計算、2) その情報で小数点位置や指数表記を整えて実際の文字列を生成。たとえば π はまず 31415927 と −7 を求めてから "3.1415927" を作る。  
- 主なアルゴリズム：Steele & White の Dragon（1990）が最初。以降、Grisu3、Ryū、Schubfach、Dragonbox、Grisu-Exact など高速化が進んだ実装が登場。実験では Jeon の Dragonbox と Giulietti の Schubfach が総合的に優秀、Adams の Ryū もほぼ同等。従来の Dragon4 と比べて約10倍の高速化を達成。  
- パフォーマンス概観：効率的な実装は1文字列当たり約200〜350命令（instructions）。一方、Linux上の標準関数 std::to_chars は過剰な命令を使っており、場合によってはほぼ2倍の命令数を消費する。  
- 最短文字列の問題：どの実装も常に「最短の文字列表現」を出すわけではない。例として 0.00011 を std::to_chars は "0.00011"（7文字）で出すが、理論上は "1.1e-4"（6文字）が短い。ただし慣例で指数部を2桁にパディングすると "1.1e-04"（7文字）になり同等になるなど、表示ルール次第で最短性は変わる。  
- 参考と再現性：測定用ベンチマークとデータは公開（fastfloat/float_serialization_benchmark, fastfloat/float-data）。

成長率の目安：
$$ (1+r)^{30}=10 \Rightarrow r\approx 7.96\% $$
約30年で10倍は年率約8%の改善に相当（実装・アルゴリズム改善効果）。

## 実践ポイント
- 大量シリアライズがボトルネックなら Dragonbox／Schubfach 実装を検証する（ベンチは https://github.com/fastfloat を参照）。  
- C++では std::to_chars の実装差が性能に効くため、標準実装だけに頼らずベンチを取る。fmt もやや劣る傾向。  
- ネットワーク帯域やログ容量を削減したければ「出力形式（通常表記 vs 指数表記）」の方針を定め、最短化ルールをプロダクト仕様に組み込む。  
- 高速化目標がある場合はプロファイルして、変換が占める割合（≒20〜35%）を確認のうえ、アルゴリズム差での改善効果を定量評価する。

出典：Daniel Lemire, "Converting floats to strings quickly"（2026）および関連ベンチマーク（fastfloatプロジェクト）。
