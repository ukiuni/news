---
layout: post
title: "Invisible Failures: The Python Server Mistake We Made in Production - 見えない失敗：本番でやらかしたPythonサーバの落とし穴"
date: 2026-01-26T18:22:44.825Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://itay-bittan.medium.com/invisible-failures-the-python-server-mistake-we-made-in-production-7d20f144c480?source=friends_link&amp;sk=119beeac5da6d00e2b26ba8327b33d7c"
source_title: "Invisible Failures: The Python Server Mistake We Made in Production"
source_id: 417004963
excerpt: "uWSGIのlisten queueが溢れて5XX大量発生、即確認と対処法"
---

# Invisible Failures: The Python Server Mistake We Made in Production - 見えない失敗：本番でやらかしたPythonサーバの落とし穴

魅力的なタイトル: なぜ「普通の」Pythonサーバが突然5XXを撒き散らすのか？見えない失敗の正体と今すぐできる対策

## 要約
uWSGIの「listen queue」制限でリクエストが捨てられ、本番で大量の5XXが発生していた。同期WSGIから非同期サーバに移すことで、リクエスト損失が解消され、問題が可視化されスケールしやすくなった。

## この記事を読むべき理由
多くの日本のサービスは小さなEC2やコンテナでPython/WGSI構成を使っています。平均負荷は問題なくても、突発的なスパイクで見えない層（uWSGIやカーネル設定）が致命的になることがあり、現場で役立つ対処法と観測ポイントを知る価値があります。

## 詳細解説
- 問題の本質  
  uWSGIは内部ソケットのlisten queue（デフォルト100など）を使う。これが埋まると接続はアプリに届かず、ロードバランサ側では5XXとして観測される（リクエストが「床に落ちる」）。ログには "listen queue ... full" のような警告が出るが、放置されがち。

- 同期WSGI vs 非同期サーバ  
  同期モデル（uWSGI + Flask/Bottle）はI/O待ちでワーカーがブロックすると同時接続処理能力が急激に低下し、listen queueが溢れる。非同期モデル（Tornado / FastAPI + uvicorn等）はブロッキングを回避できるため、ボトルネックがメモリ/CPUに移り、失敗が可視化されて容量増強やスケール対策が取りやすくなる。

- 再現と定量データ（要点のみ）  
  単純なGETで500msスリープする負荷をk6で1,000仮想ユーザで投げた結果：
  - 同期（Flask+uWSGI）：成功約37%、多数の5XX、平均遅延非常に長い  
  - 非同期（FastAPI）：成功ほぼ100%、遅延大幅に改善

- 観測の重要性  
  ロードバランサの5XXメトリクス、uWSGIログ、内部メトリクス（StatsD等）を組み合わせて解析すると原因に辿り着ける。どれか一つだけでは誤判断しやすい。

## 実践ポイント
- まず確認する項目  
  - ALB/NLBなどロードバランサのHTTP 5XX（分単位）を監視する。  
  - uWSGIログに "listen queue ... full" がないかチェックする。  
- 即効性のある対処  
  - uWSGIのlisten queue設定（--listen）やカーネルのsomaxconnを調整する。  
  - Nginxの接続設定（keepalive、backlog）を見直す。  
- 中長期対策  
  - I/O多めの処理は非同期フレームワーク（FastAPI/Tornado/uvicorn）へ移行検討。  
  - スパイク耐性のために水平スケールとオートスケーリング、メトリクスしきい値を整備。  
  - 負荷再現テスト（k6など）でスパイク時の挙動を確認する。  
- 日本の現場向け注意点  
  - 小さなEC2インスタンスやコンテナ環境だとlisten queueやカーネル設定の影響が出やすい。まず設定確認→観測→段階的改修を推奨。

以上を踏まえ、まずはロードバランサとuWSGIログの確認、簡単なスパイク試験を実施して「見えない失敗」が起きていないか確かめましょう。
