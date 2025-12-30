---
layout: "post"
title: "Tachyon: High frequency statistical sampling profiler - Tachyon：高頻度統計サンプリングプロファイラ"
date: "2025-12-26 07:10:14.679000+00:00"
categories:
- tech
- world-news
tags:
- tech-news
- japan
source_url: "https://docs.python.org/3.15/library/profiling.sampling.html"
source_title: "profiling.sampling â\x80\x94 Statistical profiler — Python 3.15.0a3\ \ documentation"
source_id: "46353257"
excerpt: "本番で低オーバーヘッドに高頻度サンプリングし即ボトルネック可視化するPy3.15プロファイラ"
---
# Tachyon: High frequency statistical sampling profiler - Tachyon：高頻度統計サンプリングプロファイラ

## 要約
Python 3.15で導入された profiling.sampling（Tachyon）は、外部から定期的にスタックをスナップショットして“統計的に”ホットスポットを特定する軽量プロファイラ。ほぼゼロに近いオーバーヘッドで本番計測が可能になる。

## この記事を読むべき理由
日本のサービス開発では、本番環境での性能解析を止められない制約や低レイテンシ要件が多い。Tachyonはコード改修不要で稼働中プロセスにアタッチでき、短時間でボトルネックの所在を把握できるため、運用中の性能改善サイクルを大幅に短縮する。

## 詳細解説
- 統計サンプリングの仕組み  
  Tachyonはプロセス外部から定期的にコールスタックを取得することで、どの関数が頻繁に現れるかをカウントします。各関数の時間はサンプル比から推定され、例えば関数が全サンプルの5%に現れれば総計測時間の約5%を消費したと見なします。

  $$t_{est} = \frac{s_f}{S} \cdot T$$

  ここで $s_f$ は関数のサンプル数、$S$ は総サンプル数、$T$ は計測時間。

- 長所と短所  
  長所：オーバーヘッドが極めて小さいため、本番環境で長時間稼働させても安全。アタッチやサブプロセス追跡、リアルタイム統計、フレームグラフ出力など豊富な機能を備える。  
  短所：サンプリングは「統計的推定」なので、短時間実行や呼び出し回数の厳密なカウントが必要なケース（マイクロベンチや1〜2%の差の検出）には不向き。そうした場合は profiling.tracing や timeit を使うべき。

- モードと出力  
  Wall-clock / CPU / GIL / Exceptionなどモードがあり、用途に応じて切替可能。出力は pstats、collapsed stacks、flamegraph、Gecko、heatmap、バイナリなど多様で、既存の可視化ツールとの親和性が高い。

- 使い方の概要（例）  
  アプリに変更を入れずに実行中のプロセスにアタッチでき、あとで再生（replay）やフレームグラフ生成を行える。短い例：

  ```bash
  python -m profiling.sampling run my_app.py --rate 10000 --duration 10 -o flame.svg
  ```

## 日本市場との関連性
- 本番稼働中のSaaS、FinTech、ゲームバックエンドなどで「停止できない」サービスが多い日本市場では、低オーバーヘッドで実行可能なTachyonは即戦力。  
- コンテナ/クラウド環境、マイクロサービス構成でもプロセスにアタッチして分析できるため、既存の運用フローに組み込みやすい。  
- Xdebugや既存のAPMでは見えにくいPython固有のコールスタックやasyncタスクのホットスポット把握に有効。

## 実践ポイント
- 長めに（数秒〜数十秒）計測してサンプル数を稼ぐ。サンプル数が多いほど誤差は小さくなる。  
- 短時間ジョブでは profiling.tracing を使うか、ループで実行時間を延ばしてからTachyonで計測する。  
- マイクロベンチ（1〜2%差の判定）には timeit やトレースベースのプロファイラを併用する。  
- 出力はまずフレームグラフで全体像を掴み、気になる関数を pstats 等で掘る。  
- 本番で使う場合は最初に非本番で動作検証（attach/record/replayフロー、出力フォーマット確認）を済ませておく。

