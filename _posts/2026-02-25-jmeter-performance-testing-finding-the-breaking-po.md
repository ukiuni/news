---
layout: post
title: "JMeter Performance Testing: Finding the Breaking Point with Data-Driven Scenarios - JMeterパフォーマンステスト：データ駆動型シナリオで限界を見極める"
date: 2026-02-25T10:48:34.213Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://medium.com/ai-in-quality-assurance/jmeter-performance-testing-part-3-finding-the-breaking-point-with-data-driven-scenarios-0d7b7924b5a3?source=friends_link&amp;sk=d6a7ae1199bf01b9ad6b51c8710124ee"
source_title: "JMeter Performance Testing: Finding the Breaking Point with Data-Driven Scenarios"
source_id: 398156379
excerpt: "CSVで本番近似負荷を再現し千同時で発生する40%エラーとDB/CPUの限界を暴く"
---

# JMeter Performance Testing: Finding the Breaking Point with Data-Driven Scenarios - JMeterパフォーマンステスト：データ駆動型シナリオで限界を見極める
クリックせずにはいられない！「本番に近い負荷」を再現してサーバの限界点を見つける方法

## 要約
JMeterでCSVベースのデータ駆動テストを作り、現実に近い複数ユーザーの振る舞いで100ユーザーと1,000ユーザーを比較。100では安定する一方、1,000では約40%のエラーと極端な遅延が発生し、CPUとDBコネクションがボトルネックになった。

## この記事を読むべき理由
単一アカウントで何度も繰り返す「疑似負荷」は誤った安心を生む。日本のSaaSやECの現場でも、実運用に近いデータ駆動テストで本当の耐久性を把握することは必須であり、対応策（DBチューニング／水平スケール／接続プール設計）を優先的に検討する判断材料になる。

## 詳細解説
- テストデータの準備：Python等で5,000件のユニークなユーザ行（email,password,product_id）をCSV生成。単一ユーザの再利用はキャッシュ効果で誤測定を招く。  
- JMeter側の組み込み機能：CSV Data Set Configを使いファイルを1行ずつ読み込み、変数（${email}, ${password}, ${product_id}）に割り当ててパラメータ化する。これにより各仮想ユーザが固有のセッションを再現。  
- 動的処理の安定化：前工程（Part 2）で行うべきはRegexやHTTP Cookie Managerでトークンやクッキーを正しく扱うこと。これがないと並列実行で認証やセッションが破綻する。  
- 負荷実験（比較結果）：  
  - 100同時ユーザ：エラー率0%、平均応答239ms — ローカル環境は余裕あり。  
  - 1,000同時ユーザ：エラー率≈40%、平均応答4.6s、最大応答約54.6s、主なエラーは504やConnection Refused。監視でCPU100%・MySQLの接続プール枯渇を確認。  
- 原因分析：アプリロジック自体は正しいが、ローカルハード/コンテナのリソース制限とDB設計（同時接続・書き込み負荷）がスケールの天井となる。

## 実践ポイント
- テストデータは必ずユニークに（CSV + CSV Data Set Config）。同一ユーザ連投はNG。  
- テスト前に認証フロー（Regex／Cookie）を自動化して並列実行に耐えるスクリプトを作る。  
- 境界値テスト：段階的に負荷を上げて（例：100→300→500→1,000）どこで劣化するか把握する。  
- 監視を同時に実行：CPU, メモリ, DBコネクションプール, ネットワーク待ちを可視化（Prometheus/Grafanaなど）。  
- 改善候補：DB接続プール調整・クエリ最適化・インデックス追加・キャッシュ導入・水平スケール（複数DB/アプリノード）・クラウドの負荷生成で本番近似環境を用意。  
- 本番適用前に必ず専用の負荷テスト環境を用意し、ローカル環境の「見かけ上の性能」に騙されない。

元記事（Burak Karakoyunlu / Medium）を参考に、まずは小さく段階的に実施して「測定→原因特定→対策」のサイクルを回してください。
