---
layout: post
title: "Personal infrastructure setup 2026 - 2026年の個人インフラ構成"
date: 2026-01-20T01:21:14.863Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://linderud.dev/blog/personal-infrastructure-setup-2026/"
source_title: "Personal infrastructure setup 2026"
source_id: 1265116927
excerpt: "Incus＋OpenTofuで宣言管理、WireGuard＋小VPSでCGNAT越え運用"
---

# Personal infrastructure setup 2026 - 2026年の個人インフラ構成
NAT越えでも安心。自宅で「ほったらかし」運用できるパーソナルインフラの作り方

## 要約
著者は長年の自宅サーバ運用を整理して、Incus（旧LXD）＋OpenTofuで宣言的に管理しつつ、WireGuardと小さなVPSを利用してインターネット公開を安定化させる構成に落ち着いた。NASはデータ保管、NGINX＋nginx-acmeでTLSを自動化、静的サイトはSyncthingで配布という実用的な組み合わせ。

## この記事を読むべき理由
- 日本の家庭用回線はCGNATや動的IPが多く、外部公開が難しいケースがある。この記事が示す「小さなVPSを中継にする＋WireGuardの逆接続」は実務的な解決策になる。
- ローカルで信頼できるサービス群（写真管理、RSS、メールなど）をシンプルに運用したい個人・小規模チームに有益な具体例が得られる。

## 詳細解説
- インフラの核：Incus（旧LXD）
  - Incusをコンテナ／軽量VMランタイムとして利用。OCIイメージ対応により、DockerイメージをそのままIncusに取り込めるため既存のDockerベースサービスが容易に移行可能。
  - 複数ホスト（古いNASやNUC群）でクラスタを組み、サービスごとにプロジェクトを分けることで権限やネットワークを整理している。
  - 例: Incusクラスタ確認の一例
```bash
λ ~ » incus cluster list -c nuas
+------------+---------------------------+--------------+--------+
| NAME       | URL                       | ARCHITECTURE | STATUS |
+------------+---------------------------+--------------+--------+
| amd        | https://10.100.100.3:8443 | x86_64       | ONLINE |
| byggmester | https://10.100.100.2:8443 | x86_64       | ONLINE |
+------------+---------------------------+--------------+--------+
```

- ネットワーク設計（シンプルで実務的）
  - ローカルはフラットなブリッジ（br0）で管理し、systemd-networkdで固定IPを振る構成。将来的にVLANで分離する予定だが、まずは安定させることを優先。
```ini
# /etc/systemd/network/50-br0.network
[Match]
Name=br0

[Network]
Address=192.168.1.2/24
Gateway=192.168.1.1
DNS=192.168.1.1
```

- 宣言的管理：OpenTofu（Terraform互換のツール）
  - Incus用プロバイダを使い、コンテナ／インスタンス定義をコード化。dockerイメージをincus_imageで参照してincus_instanceとして起動できるため、手作業を最小化。
```hcl
resource "incus_image" "valkey" {
  project = incus_project.immich.name
  alias { name = "valkey" }
  source_image = { remote = "docker", name = "valkey/valkey:8-bookworm" }
}
resource "incus_instance" "valkey" {
  name   = "valkey"
  image  = incus_image.valkey.fingerprint
  target = "byggmester"
  config = { "boot.autorestart" = true }
}
```

- インターネット公開：WireGuard + 中継VPS + nginx
  - 家庭用ISPのNATと動的IPを回避するため、静的IPを持つ小さなVPSを用意し、そのVPSとWireGuardでポイント・トゥ・サイトトンネルを張る。VPSが外部のフロントになり、VPS上のnginxが内部のサービスへリバースプロキシする。
  - TLSはnginx-acmeで自動化。内部DNSを使ってnginx側で内部ホスト名を解決し、設定の追従を簡単にしている。
```nginx
server {
  listen 443 ssl;
  server_name bilder.linderud.dev;
  include snippets/acme.conf;   # nginx-acmeで取得した証明書を使用
  location / {
    set $immich immich.local;
    proxy_pass http://$immich:2283;
    proxy_set_header Host $http_host;
    proxy_set_header X-Real-IP $remote_addr;
  }
}
```

- 静的サイト配信：Syncthing を使ったローカル同期
  - ブログなどの静的ファイルをローカルでビルドして /srv に出力し、Syncthingで配信先（公開サーバ）と同期。CIや外部サービスを使わず、手軽に公開できる。

## 実践ポイント
1. まずは小さく始める
   - 1台のNUCや古いPCにIncusを入れてコンテナ1つを立て、サービスの動作確認をする。
2. 宣言的管理を導入する
   - OpenTofu/terraformでリソースをコード化すれば、再現性とロールバックが容易。
3. ISPの制限対策
   - 家庭用回線がCGNATや動的IPなら、小さなVPS（国内or東京リージョン）を中継点にしてWireGuardで接続するのが現実的。
4. 証明書とプロキシの自動化
   - nginx-acmeやLet's EncryptでTLSを自動化し、内部DNSと組み合わせると設定管理が楽になる。
5. データはNASへ
   - コンテナは一時的に扱い、写真やDB・バックアップなどの永続データはNASへ置く。スナップショットや定期バックアップを忘れずに。
6. 日本向けの注意点
   - 日本のISPはCGNAT率が高い。プロバイダ規約やポート制限を確認すること。国内VPSを使えば遅延や法的懸念（国内利用の方が安心）も抑えられる。

この構成は「手間を減らしつつローカルで信頼できる環境を持ちたい」人に向いている。まずは「1コンテナ＋ローカルブリッジ＋小VPS」の最小構成から試して、運用ルールを増やしていくのが現実的。
