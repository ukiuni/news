---
layout: post
title: "Writing Load Balancer From Scratch In 250 Line of Code in Golang - 250行で作るGoのロードバランサ"
date: 2026-01-01T04:38:28.310Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://sushantdhiman.substack.com/p/writing-load-balancer-from-scratch"
source_title: "Writing Load Balancer From Scratch In 250 Line of Code in Golang"
source_id: 473951351
excerpt: "250行のGo実装でRound Robinを実演、負荷分散の実践ノウハウ解説"
---

# Writing Load Balancer From Scratch In 250 Line of Code in Golang - 250行で作るGoのロードバランサ
ローカルで試せる！Goで「本当に動く」ロードバランサを250行で作って学ぶ負荷分散の基礎

## 要約
元記事はGoで動作するシンプルなロードバランサを約250行で実装し、Round Robin方式でリクエストをバックエンドに順番に転送する仕組みを解説する。

## この記事を読むべき理由
ロードバランサはスケール設計の基礎。小さくても「動く」実装を読むことで、プロダクションで使うリバースプロキシやKubernetes Ingressの挙動をローレベルで理解できる。日本のスタートアップや社内サービスで負荷分散を一から学びたいエンジニアに有用。

## 詳細解説
- ロードバランサの役割  
  クライアントからのリクエストを複数のアプリケーションインスタンスに均等に振り分け、単一インスタンスの負荷を下げ可用性を高める。例えばリクエスト総数が毎秒1,000,000でインスタンスが5台なら、理想的には1台当たり
  $1{,}000{,}000/5=200{,}000$
  件を処理することになる。

- 実装方針（元記事の構成）  
  1) Server型：ID、Name、Protocol、Host、Port、URL、IsHealthy、LastHealthCheckといったメタ情報を保持。  
  2) ServerPool：複数バックエンドの管理。サーバ追加や一覧取得を提供。  
  3) Strategyインタフェース：GetNextServer()を定義し、Round Robin等の戦略を差し替え可能にする。  
  4) Round Robin：ミューテックスでインデックスを保護し、次のサーバを循環的に選択。並行アクセスでの競合回避がポイント。  
  5) LoadBalancer.Serve：受け取ったHTTPリクエストを選ばれたバックエンドへプロキシ。ヘッダ転送、X-Forwarded-For追加、タイムアウト設定（例: 30秒）、レスポンスヘッダとボディをクライアントに返す。

- コアロジック（Round Robinの要点）  
  複数ゴルーチンから同時にGetNextServerが呼ばれても安全にインデックスを更新する必要がある。擬似コード：
  ```go
  package main

  import "sync"

  type Server struct { URL string }
  type Pool struct { servers []*Server }

  type RoundRobin struct {
    pool *Pool
    mu   sync.Mutex
    idx  int
  }

  func (r *RoundRobin) GetNextServer() (*Server, error) {
    servers := r.pool.servers
    if len(servers) == 0 { return nil, errors.New("no servers") }
    r.mu.Lock(); defer r.mu.Unlock()
    r.idx = (r.idx + 1) % len(servers)
    return servers[r.idx], nil
  }
  ```
- 欠点と拡張案  
  元実装はヘルスチェック未実装。実運用ではヘルスチェック、重み付け、セッション固着（IPハッシュ）、TLS終端、接続プール、タイムアウト制御、リトライ/サーキットブレイカー、メトリクス収集が必要。

## 実践ポイント
- ローカルで試す手順
  1) 簡易バックエンドを3つ（例えば http.ListenAndServe(":3001", ...) など）で起動。  
  2) ロードバランサをポート3000で起動して、/ に来たリクエストを順に転送させる。  
  3) curl -v http://localhost:3000 を複数回実行してRound Robinの挙動を確認。  
- 今すぐ改善できる点（優先度順）
  1) 定期的なヘルスチェックで IsHealthy を更新し、死活不良ノードを除外。  
  2) タイムアウトとリトライの調整で遅いバックエンドからの影響を低減。  
  3) Prometheusメトリクス（リクエスト数、レイテンシ、バックエンド状態）を追加。  
- 日本の現場での応用例
  - 小規模サービスの自作LB学習やオンプレ環境での簡易フロントに最適。  
  - KubernetesやクラウドLB導入前に挙動確認をしたい時のローカル検証用。

## 引用元
- タイトル: Writing Load Balancer From Scratch In 250 Line of Code in Golang  
- URL: https://sushantdhiman.substack.com/p/writing-load-balancer-from-scratch
