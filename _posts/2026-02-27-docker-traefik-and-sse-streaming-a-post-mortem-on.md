---
layout: post
title: "Docker, Traefik, and SSE streaming: A post-mortem on building a managed hosting platform - Docker、Traefik、SSEストリーミング：マネージドホスティング構築のポストモーテム"
date: 2026-02-27T13:05:52.815Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://clawhosters.com/blog/posts/building-managed-hosting-platform-tech-deep-dive"
source_title: "Docker + Traefik + SSE: Managed AI Hosting Platform | Daniel Samer | ClawHosters"
source_id: 396457782
excerpt: "DockerとTraefikで小規模AIホスティングを運用し、SSEの落とし穴と実践的対策を詳解"
image: "https://clawhosters.com/rails/active_storage/representations/proxy/eyJfcmFpbHMiOnsiZGF0YSI6MjE0LCJwdXIiOiJibG9iX2lkIn19--9643329a93a51bfc7988f99cbec1a5a475651a4a/eyJfcmFpbHMiOnsiZGF0YSI6eyJmb3JtYXQiOiJqcGciLCJyZXNpemVfdG9fZmlsbCI6WzEyMDAsNjMwXX0sInB1ciI6InZhcmlhdGlvbiJ9fQ==--d404be4ee82a9aa01a622bf9bac68be7cce4c6b0/banner.png"
---

# Docker, Traefik, and SSE streaming: A post-mortem on building a managed hosting platform - Docker、Traefik、SSEストリーミング：マネージドホスティング構築のポストモーテム

50ユーザーを支える小さなAIホスティングの裏側──Dockerが救いでもあり地雷でもあった運用ノウハウ

## 要約
Rails＋Dockerで顧客ごとにVPSを分離した小規模マネージドAIホスティングの技術的総括。コンテナ隔離、Traefikによる動的ルーティング、そしてSSEストリーミング周りの落とし穴と対策が中心。

## この記事を読むべき理由
日本でも小規模でAIサービスを運用するチームが増えています。Kubernetesを使わずに低コストで「複数顧客の安全な分離＋ストリーミング対応」をする実践的手法と失敗回避策が学べます。

## 詳細解説
- 全体構成  
  Rails 8 モノリス＋Postgres、Sidekiq、Hetzner上の顧客ごとのVPSにOpenClawをDockerで稼働。フロントはCloudflareワイルドカード→前段Nginx→Traefik(設定はRedis)→VPS内Nginx→OpenClaw、という5レイヤーのルーティング。

- なぜDockerか／代償  
  メモリ制限やプロセス隔離でホスト破壊を防げる一方、pnpmのシンボリックリンク扱いやmDNS、PID 1周りのゾンビプロセス、コンテナ再作成でランタイム状態が消える等、多くの運用障害を生む。顧客がコンテナ内で自由にパッケージを入れるため、Writable layer（OverlayFS）を残す運用を採用し、更新前にdocker commitで書き込み層を保存する方式に落ち着いた。

- Traefik + Redisによる動的ルーティング  
  Rails側でRedisのキーをMULTIで原子書き込みし、TraefikはRedisのキー通知で即時反映。各顧客にbcryptでハッシュしたbasic authミドルウェアを登録する運用。ルール例は概念的に以下のように管理。

- セキュリティとネットワーク  
  Hetznerファイアウォールで公開ポートを限定し、fail2banでSSHを保護。VPSは基本的にプロダクションサーバ経由でしか到達させない。

- SSE（Server-Sent Events）を巡る地獄と対策  
  1) TCPチャンクの断片化に対して、受信チャンクを蓄積→`\n\n`で分割するリフレーミングバッファを実装。  
  2) NginxのバッファリングがSSEを潰す問題は多段構成で顕著。全プロキシ層で以下のような設定が必要（要件はすべて揃えること）。  
  ```nginx
  # nginx
  location /v1/ {
    proxy_pass http://upstream;
    proxy_buffering off;
    proxy_cache off;
    proxy_http_version 1.1;
    chunked_transfer_encoding off;
    proxy_set_header Connection '';
    proxy_set_header X-Accel-Buffering no;
  }
  ```
  Rails側もヘッダでSSEを明示する必要がある：
  ```ruby
  # ruby (Rails controller)
  response.headers['Content-Type'] = 'text/event-stream'
  response.headers['Cache-Control'] = 'no-cache'
  response.headers['X-Accel-Buffering'] = 'no'
  response.headers['Transfer-Encoding'] = 'chunked'
  ```
  3) 請求用トークン情報は多くのプロバイダが最後のSSEチャンクで返すため、レスポンス全体を保持せずに「最後数KBだけを保持するリングバッファ」で使用量JSONを検出・解析する運用が現実的。

- フェイルオーバーと課金の難しさ  
  プロバイダごとにトークン計測方法が異なり、欠損がある場合はプロバイダ固有の係数で推定。観測(概算)と請求(正確)のギャップをどう扱うかは運用ポリシーが必要。

- 自動復旧・監視  
  10分毎のルート同期、5分毎のエンドツーエンドヘルスチェック（正しいHostヘッダを付与）でミスの自動是正やTraefikの再起動を行う。

## 実践ポイント
- Dockerは使う価値あり。ただし「書き込み層を保つ運用（docker commit）」と「コンテナ再作成を最小化するホットリロード」を設計する。  
- 多段プロキシでSSEを扱うなら、すべてのプロキシでproxy_buffering等のSSE向け設定を漏れなく適用する。  
- SSEはTCPチャンク断片化を前提にリフレーミングを実装し、最後数KBだけを保存するリングバッファで課金情報を回収する。  
- Traefikの動的ルーティングはRedisのキー通知＋原子更新で即時反映が可能。デプロイ時の一貫性をRedis MULTIで担保する。  
- 小規模運用でもネットワーク層（ファイアウォール）、ログ、ヘルスチェックを整え、プロバイダ差異による課金ポリシーを明確化する。

短時間で立ち上げて回すには「隔離と柔軟性」を両立する設計と、SSEやプロバイダ差異に耐える運用スクリプトが鍵です。
