---
layout: post
title: "TIL: Docker log rotation - Dockerログのローテーションについて学んだこと"
date: 2026-02-16T18:36:12.764Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://ntietz.com/blog/til-docker-log-rotation/"
source_title: "TIL: Docker log rotation | nicole@web"
source_id: 980814815
excerpt: "Dockerの無制限ログでVPSが死亡、即デーモン設定と既存コンテナ再作成で復旧"
---

# TIL: Docker log rotation - Dockerログのローテーションについて学んだこと
知らないと痛い目に遭う！Dockerコンテナのログがディスクを無限に食いつぶす原因と、今すぐできる対処法

## 要約
Dockerは既存コンテナのログを自動でローテーションしないため、放置すると数GB〜10GB単位でログが肥大化してディスクを使い尽くす。デーモン設定でログローテーションを有効にし、既存コンテナは再作成するのが対処の基本。

## この記事を読むべき理由
国内の低容量VPS（例：さくらのVPS、ConoHa、Lightsail等）を使っていると、ログ肥大がすぐ致命的になる。運用コストやダウンタイムを避けるため、基本対策は必須です。

## 詳細解説
- まず原因確認
  - ディスク使用状況確認: `du -h -d 1 /` 等で /var/lib/docker が大きいか見る。
  - Dockerコンテナのログは通常 `/var/lib/docker/containers/<id>/<id>-json.log` に溜まる。
  - コンテナごとのログ設定確認:
```bash
docker inspect --format='{{.HostConfig.LogConfig}}' <コンテナ名またはID>
```
  - 未設定だと `{json-file map []}` のように表示され、デフォルトの json-file ドライバで無制限に増える。

- ログローテーション設定（デーモンレベル）
  - /etc/docker/daemon.json を作成・編集してログドライバ設定を追加する例:
```json
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "100m",
    "max-file": "3"
  }
}
```
  - 設定変更後は Docker デーモンを再起動:
```bash
sudo systemctl restart docker
```
  - 注意: この設定は再起動後に作成される新しいコンテナにのみ適用される。既存コンテナには反映されないため、対象コンテナは停止→削除→再作成する必要がある。

- 既存ログの扱い
  - 一時的にディスクを確保するなら（安全を確認して）コンテナ停止後にログファイルを削除または切り詰めする：
```bash
sudo systemctl stop docker
sudo truncate -s 0 /var/lib/docker/containers/<id>/*-json.log
sudo systemctl start docker
```
  - より安全にはコンテナを再作成してローテーション設定を反映させる。

## 実践ポイント
- まずディスク使用量をチェックして `/var/lib/docker/containers` のログサイズを確認する。
- /etc/docker/daemon.json に log-opts を設定して、`max-size` と `max-file` を環境に合わせて決める（例: 100m / 3 は一般的）。
- 既存コンテナは再作成するか、停止してログを切り詰めすることで即時対処。
- ログを長期保存したい場合は、fluentd/Elasticsearch/Syslog 等へ集中ログ収集する運用を検討する。
- 低容量VPSでは定期チェック（cronでディスク使用量通知）を仕込むと安心。

以上を実行すれば、Dockerログによる「知らぬ間のディスク枯渇」を防げます。
