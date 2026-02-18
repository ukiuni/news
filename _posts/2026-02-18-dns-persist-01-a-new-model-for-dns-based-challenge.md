---
layout: post
title: "DNS-Persist-01: A New Model for DNS-Based Challenge Validation - DNS‑PERSIST‑01：DNSベース認証検証の新モデル"
date: 2026-02-18T19:13:47.767Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://letsencrypt.org/2026/02/18/dns-persist-01.html"
source_title: "DNS-PERSIST-01: A New Model for DNS-based Challenge Validation -  Let&#39;s Encrypt"
source_id: 47064047
excerpt: "DNSに一度置くだけで証明書更新が自動化、IoTやマルチテナント運用を劇的に簡素化する新方式"
image: "https://letsencrypt.org/images/LetsEncrypt-SocialShare.png"
---

# DNS-Persist-01: A New Model for DNS-Based Challenge Validation - DNS‑PERSIST‑01：DNSベース認証検証の新モデル
更新の手間をゼロに近づける？Let's Encryptの「DNS‑PERSIST‑01」が切り拓く証明書発行の新常識

## 要約
DNS‑PERSIST‑01は、DNSに「一度だけ設置する永続的な承認レコード」を置くことで、以降の証明書発行や更新で何度もDNSを書き換える必要をなくす新しいACMEチャレンジ方式です。

## この記事を読むべき理由
IoTやマルチテナント環境、DNS資格情報を発行パスに置きたくない運用—こうした日本の現場で直面する課題に対する現実的な解決策だからです。運用負荷・セキュリティのトレードオフを理解し、導入準備ができます。

## 詳細解説
- 背景：従来のDNS‑01は毎回ワンタイムのトークンをTXTに書き込み、検証後にまた別のトークンで…というフローでDNS更新が発行ごとに発生。これがプロパゲーション遅延やDNS API資格情報の頻繁な配布を招く。
- 新モデルの本質：DNS‑PERSIST‑01は1つの永続TXTレコードで「このCA＋このACMEアカウントに発行を許可する」ことを宣言する。以降の発行や更新で同じレコードを再利用でき、DNS変更は初期セットアップに限定される。
- レコードの中身（概念例）：
  - ラベル：_validation-persist.example.com
  - TXTに含める主な要素：CA識別子（issuer）、accounturi（ACMEアカウントURI）、オプションで policy=wildcard や persistUntil（有効期限）など
- スコープ制御：
  - デフォルト：当該FQDNのみ有効、無期限
  - policy=wildcard を追加するとワイルドカード（*.example.com）なども許可可能
  - persistUntil（UNIX秒）で有効期限を設定して期間限定にできる（更新忘れに注意）
- セキュリティ上のトレードオフ：
  - DNS‑01：敏感な資産は「DNS書き込み権限」。発行経路に資格情報を広めがち。
  - DNS‑PERSIST‑01：敏感なのは「ACMEアカウントキー」。DNSは初期設定後は厳格に管理できる一方、アカウントキーの保護がより重要に。
- 運用面：
  - 複数CAを許可するには同ラベルに複数のTXTレコードを配置。各CAは自分のissuer名に合致するレコードだけを参照。
  - 実装状況：IETFドラフト化済、Pebble（Boulderのミニ実装）で試験的サポート、lego-cli等のクライアント対応進行中。ステージングは2026年Q1末、製品化はQ2予定（記事時点）。

## 実践ポイント
- 導入検討チェックリスト：
  1. 発行フローからDNS書き込みを排除したいか（IoT/マルチテナントで有効）。
  2. ACMEアカウントキーの保護体制（HSM/シークレット管理）を整備する。
  3. policy=wildcard や persistUntil をどう使うか方針決定する。
  4. 最初はPebbleやlegoで検証環境を構築して動作確認する。
  5. persistUntilを使う場合は監視／更新リマインダーを設定する（期限切れ防止）。
- 日本の現場での活用例：
  - ネットワークに直接公開できないエッジIoT機器や閉域環境での一括発行
  - マルチテナントPaaSでテナントごとにDNS資格情報を配らずに証明書発行を委任
  - 大量発行・更新が頻繁な環境での運用負荷軽減

まずはステージング実装で既存の発行フローとセキュリティ要件を比較検証し、ACMEアカウント管理の体制を固めることを推奨します。
