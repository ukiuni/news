---
layout: post
title: "I Cannot SSH Into My Server Anymore (And That’s Fine) - もうサーバーにSSHしなくなった（それで大丈夫）"
date: 2026-01-09T15:47:51.846Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://soap.coffee/~lthms/posts/i-cannot-ssh-into-my-server-anymore.html"
source_title: "I Cannot SSH Into My Server Anymore (And That’s Fine) · Thomas Letan’s website"
source_id: 1349300458
excerpt: "K8s不要で低コスト、SSH不要なPodman自動更新型セルフホスティング術"
image: "https://soap.coffee/~lthms/img/thinking.png"
---

# I Cannot SSH Into My Server Anymore (And That’s Fine) - もうサーバーにSSHしなくなった（それで大丈夫）
サーバーにSSHしなくても回る「手放せる」セルフホスティング術 — 手間もコストも減らすコンテナ中心の不変インフラ

## 要約
筆者は Fedora CoreOS + Ignition + Podman（Quadlets）＋Terraform を組み合わせ、SSH不要で自動的にコンテナを配備・更新する小さなセルフホスト環境「tinkerbell」を構築した。イミュータブル（破壊的再作成）な考え方と Podman の自動更新で、デプロイは「イメージをプッシュするだけ」に帰着する。

## この記事を読むべき理由
小規模サイトや個人サービスを安価かつ低運用で動かしたい日本のエンジニア／趣味の開発者にとって、複雑な K8s を使わずに「安全で自動化された」運用を実現する現実的な選択肢が学べるから。運用時間を減らしたい人、クラウドコストを下げたい人に特に有益。

## 詳細解説
- 基本コンセプト  
  - イミュータブルなVM：Ignition（初回起動時にだけ実行されるプロビジョニング）でVMを「一度だけ」セットアップし、変更は「破棄して再作成」する。これにより Ansible 的な状態遷移の複雑さを避ける。  
  - コンテナ中心：アプリケーションはすべてコンテナで配布。CoreOS 系 OS（Fedora CoreOS）を使えばコンテナ実行が主役になる。  
  - 宣言的設定：Butane で書いた設定から Ignition を生成し、Terraform で VPS（例：Vultr）を作る流れ。  

- 主要技術と役割  
  - Fedora CoreOS：軽量でコンテナ向けに設計されたOS。Ignition と相性が良い。  
  - Ignition / Butane：Ignition は JSON（.ign）で初回プロビジョンを実行。Butane は人間向けの YAML を Ignition に変換するツール。  
  - Podman + Quadlets：systemd 連携でコンテナを宣言的に起動。quadlet を使うと .container/.pod ファイルを定義して systemd と同様の管理が可能。Pod を使えばネットワーク名前空間を共有して localhost 経由で通信できる。  
  - Podman auto-update：コンテナイメージをレジストリで監視して自動で更新を当てる。ラベル io.containers.autoupdate=registry を付けるだけで、podman-auto-update タイマーが新しいイメージを取り込んで再起動する。  
  - Terraform：VPS の作成や Ignition の注入を自動化。再現性のあるインフラ構築に役立つ。

- 実践上の注意点  
  - Ignition は一度しか動かない：設定変更は VM を再生成するワークフローを前提にする設計思想。  
  - Pod 内のコンテナ再起動は副作用あり：1つのコンテナ再起動で pod 内の他コンテナも再起動されるケースがあるため注意。  
  - 可観測性（観測基盤）は別途必要：SSH をなくすと内部がブラックボックス化するため、メトリクス・ログ収集や外部監視の整備を検討する。  
  - TLS/証明書管理：Caddy の自動取得は便利だが、発行制限や永続化の方針（ブロックストレージに置くかなど）を検討する。

- 実際の流れ（概略）  
  1. Butane でユーザーや Quadlet 定義を含む Ignition を作る。  
  2. Terraform で VPS を作成し user_data に .ign を渡す。  
  3. Quadlet の .container/.pod ファイルでコンテナを宣言。  
  4. コンテナに自動更新ラベルを付け、podman-auto-update を有効化。  
  5. 新バージョンのイメージをレジストリに push すると自動で更新される（SSH 不要）。

例：quadlet の .container（簡略）
```ini
[Container]
ContainerName=soap.coffee
Image=ams.vultrcr.com/lthms/www/soap.coffee:live

[Service]
Restart=always

[Install]
WantedBy=multi-user.target
```

例：Terraform での Vultr インスタンス指定（簡略）
```hcl
resource "vultr_instance" "tinkerbell" {
  region   = "cdg"
  plan     = "vc2-1c-1gb"
  os_id    = "391"
  label    = "tinkerbell"
  hostname = "tinkerbell"
  user_data = file("main.ign")
}
```

## 実践ポイント
- 最初は小さく始める：Nginx/Caddy + 1アプリのような単純構成で試し、動作を確認してから拡張する。  
- Butane → Ignition → Terraform の流れをローカルで繰り返しテストする（terraform apply → destroy を使って反復）。  
- Podman 自動更新を有効にする：コンテナにラベル io.containers.autoupdate=registry を付け、podman-auto-update タイマーを有効化（デフォルトは日次、必要なら短くする）。  
- 監視とログを早めに用意する：Prometheus / Loki や外部監視を入れて、SSHなし運用時の可視化を確保する。  
- TLS の永続化を検討する：Let’s Encrypt の発行制限や再発行の手間を考え、必要ならボリュームやオブジェクトストレージに保存する。  
- 緊急用の脱出口を用意：SSH を無くすのは便利だが、コンソールアクセスやリカバリ手順（プロバイダのシリアルコンソール、スナップショットからの復旧など）は確保しておく。

このやり方は「完全無人運用」を目指す小規模サービスに向く実用的な選択肢です。日本のローカルVPS（さくらのVPS、ConoHa、あるいは安価な国外VPS）でも同様の構成は可能なので、まずは小さな実験環境を作って「イメージをプッシュするだけで更新される」体験を試してみてください。
