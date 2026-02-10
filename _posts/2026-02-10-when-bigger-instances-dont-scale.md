---
layout: post
title: "When Bigger Instances Don’t Scale - 大きなインスタンスがスケールしないとき"
date: 2026-02-10T14:16:44.775Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.scylladb.com/2026/02/10/when-bigger-instances-dont-scale/"
source_title: "When Bigger Instances Don&#039;t Scale - ScyllaDB"
source_id: 446417050
excerpt: "クラウドで大型インスタンスがI/Oで伸びない原因と即効対策を実務視点で解明"
image: "https://www.scylladb.com/wp-content/uploads/1200x625-when-bigger-instances-dont-scale-1.jpg"
---

# When Bigger Instances Don’t Scale - 大きなインスタンスがスケールしないとき
「大きい＝速い」の神話を覆す、クラウドI/Oの落とし穴と実務で使える対策

## 要約
ScyllaDBがAWSのi7i系インスタンスで遭遇した「インスタンスを大きくしてもI/Oが伸びない」問題を追跡し、IOTuneの誤測定、IO Schedulerのトークン制御、キュー利用といった複合要因を突き止めた調査報告（シリーズ1/3）。

## この記事を読むべき理由
日本のクラウド運用者・DBエンジニアも同様の「スケールしない」現象に遭遇しやすく、原因の切り分け方法や現場で使える検証手順がそのまま役立つため。

## 詳細解説
- 問題の症状  
  - IOTuneでの測定がインスタンスタイプ拡大で頭打ち（帯域が約8.5GB/sで飽和）し、fioでは大きなインスタンスで40GB/s近く出るという乖離が発生。IOPSもインスタンス増加に対して期待値より低かった。  
- 測定ツールの役割  
  - IOTune（Seastar付属）→ io-properties.yaml（read/write IOPS, BW）を生成し、Seastar IO Schedulerがディスクモデルを構築してスロットリング制御に使う。io_testerは詳細実験向け。  
- IO Schedulerのモデル（簡略）  
  $$\frac{\text{read\_bw}}{\text{read\_bw\_max}}+\frac{\text{write\_bw}}{\text{write\_bw\_max}}+\frac{\text{read\_iops}}{\text{read\_iops\_max}}+\frac{\text{write\_iops}}{\text{write\_iops\_max}}\le 1$$  
  これに基づく公平キューとトークンバケットでスロットリングされる。  
- 主な原因と発見  
  1. ブロックサイズ誤検出：sysfsからの自動検出失敗で512Bになり、IOPSが低下。4KB指定で改善したが真の根本は別に存在。  
  2. IO Scheduler側のトークン再充填ロジックやフェアキューの算術ミスで、リクエストのディスパッチ遅延（例：期待1μsが83μsに）→ 実効帯域が頭打ちに。  
  3. ハッカソンで作った「スロットリング抑制」パッチを適用すると帯域が期待値近く（約9.7GB/s → 期待9.6GB/s）に回復。fioもディスクをフルに使えていたことから、実機ディスクではなくスケジューラ側の制約がボトルネックだった。  
- 実験のポイント  
  - リクエストサイズと並列数の組合せでディスクキュー深度を観察。大きなリクエスト（約1–4MB）は少ない並列性でキューを埋められる。io_testerの --io-latency-goal を変えてスプリッティングやスケジューラ挙動を確認。

## 実践ポイント
- 測定は複数ツールで突き合わせる（IOTune, fio, io_tester）。差が出たらツール側とスケジューラ双方を疑う。  
- IOTuneでブロックサイズが誤検出されることがある → 明示的に読み/書きのブロックサイズを指定して再測定する。  
- テスト時はリクエストサイズを変えて（128KB→1MB→4MB）並列性と帯域の関係を確認。ディスクを「本当に」飽和させるには大きめのリクエストが必要な場合がある。  
- Seastar/ScyllaのIO Schedulerのバージョン差やパッチ適用履歴を確認し、トークンバケットやフェアキューのメトリクス（ディスパッチ遅延）を収集する。  
- 日本の本番環境でも、単にインスタンスを上げるだけで性能が出るとは限らないため、インスタンスタイプ選定前にプロファイリングを実施し、io-properties.yamlの値と実ワークロードの差を検証する。

（本記事はScyllaDBの調査記事を要約・解説したシリーズ第1回の内容を元にしています。続編では書き込み特有の劣化要因や一般的な落とし穴がまとめられます。）
