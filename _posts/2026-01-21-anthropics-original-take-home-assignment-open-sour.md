---
layout: post
title: "Anthropic's original performance take home assignment open sourced - Anthropicの元性能評価テイクホーム課題を公開"
date: 2026-01-21T04:52:02.176Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/anthropics/original_performance_takehome"
source_title: "GitHub - anthropics/original_performance_takehome: Anthropic&#39;s original performance take-home, now open for you to try!"
source_id: 46700594
excerpt: "Anthropicの性能課題を公開、クロック最小化で採用機会も狙える公開リポジトリ"
image: "https://opengraph.githubassets.com/fc82378bf93905162003a0b1a2270748816dd588c71995387170628738635ea6/anthropics/original_performance_takehome"
---

# Anthropic's original performance take home assignment open sourced - Anthropicの元性能評価テイクホーム課題を公開
「AIと‘クロックサイクル勝負’——Anthropicの公開パフォーマンス課題で最適化力を証明する」

## 要約
Anthropicが以前に使っていたパフォーマンステイクホーム課題をGitHubで公開。シミュレートされたマシンの「クロックサイクル」でスコアを競い、特定の閾値を下回る実装で注目される可能性がある（採用の窓口あり）。

## この記事を読むべき理由
日本のエンジニアや学生にとって、アルゴリズム最適化や低レイヤー性能改善のスキルを実践的に磨ける数少ない公開チャレンジ。採用リードや研究採点の指標としても使われた実案件が手元で試せる点は希少価値が高い。

## 詳細解説
- リポジトリ概要  
  - 主要言語はPython（パフォーマンステスト用のシミュレータやスコアリングが含まれる）。ファイル例: perf_takehome.py, problem.py, watch_trace.py, テスト群など。  
  - スコアは「シミュレートされたマシンのクロックサイクル」で計測される。つまり実行の論理的ステップや命令コストに基づいた評価指標で、純粋な壁時計時間とは異なる。  
- ベンチマーク（リポジトリ内の記載）  
  - Claude Opus 4（初期）: $2164$ cycles  
  - Claude Opus 4.5（カジュアル）: $1790$ cycles  
  - Claude Opus 4.5（2時間）: $1579$ cycles  
  - Claude Sonnet 4.5: $1548$ cycles  
  - Claude Opus 4.5（11.5時間）: $1487$ cycles  
  - 改良ハーネスでの最良: $1363$ cycles  
  - 目安: $1487$ 未満で「当時の最高性能を超えた」と見なされ、performance-recruiting@anthropic.com に提出すると採用検討などにつながる可能性あり。  
- 実行方法（リポジトリ記載）  
  - テスト実行: `python tests/submission_tests.py`（Python環境で実行して、どの閾値を満たすか確認）  
- なぜ面白いか（技術的観点）  
  - アルゴリズム選択、データ構造、ループ変換、メモリアクセスパターン、プロファイリング／トレース解析といった、実務に直結する性能改善スキルを問う設計。  
  - AIモデルの性能対比ではなく、低レイヤーな効率改善で「AIを打ち負かす」体験ができる点がユニーク。

## 実践ポイント
- 手順（すぐできる）  
  1. リポジトリをクローン。  
  2. Pythonで `python tests/submission_tests.py` を実行して現状スコアを把握。  
  3. 問題コード（problem.py 等）を読み、トレース（watch_trace.html）でホットスポットを特定。  
  4. アルゴリズム改善→プロファイル→再テストのサイクルを回す。  
- 最適化の着眼点  
  - アルゴリズムの時間計算量の見直し（O(n^2)→O(n log n)等）  
  - 無駄なデータコピー／冗長なループの削減、メモリ局所性改善  
  - Python特性を利用した高速化（組み込み関数、配列操作、可能ならPyPyやC拡張の検討）  
- 提出とキャリア活用  
  - 目標スコアを下回せたら、動作するコードと簡潔な説明、可能なら履歴書を performance-recruiting@anthropic.com に送ると話が進む可能性あり（リポジトリのREADMEに記載）。

短く言うと、これは「アルゴリズムとプロファイリングのトレーニング場」であり、実力を示すための公開された実戦問題。日本でもシステム寄り／インフラ寄りの技術力を示す良い材料になる。
