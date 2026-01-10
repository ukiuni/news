---
layout: post
title: "Show HN: Hosting 100 Linux dev environments on one VM using LXC - 1台のVMで100のLinux開発環境をホストする（LXC利用）"
date: 2026-01-10T15:26:50.202Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/FootprintAI/Containarium"
source_title: "GitHub - FootprintAI/Containarium: Hundred of containers living together with LXC container for saving resources and make the configuration easier"
source_id: 46566100
excerpt: "1台の安価なVMで100のフル機能Linux開発環境をLXCで高速に配布し、運用コストを大幅削減"
image: "https://opengraph.githubassets.com/4526a57d082224b78b3d43e0b9758d83ba6493c82be944480bcbebcba7daed48/FootprintAI/Containarium"
---

# Show HN: Hosting 100 Linux dev environments on one VM using LXC - 1台のVMで100のLinux開発環境をホストする（LXC利用）
魅力的な日本語タイトル: 1台の安いVMで「自分専用のLinux」を何十個も動かす──Containariumが狙う現実的なコスト革命

## 要約
ContainariumはLXC（Incus）とZFS、SSH ProxyJumpを組み合わせ、1台のクラウドVM上で多数のフル機能な開発環境（システムコンテナ）を高速に作成・管理するOSSプラットフォーム。従来の「1ユーザー＝1VM」を置き換え、インフラコストと運用工数を大幅に削減することを目指す。

## この記事を読むべき理由
日本の開発チームや教育現場では、まだ「個人VM」や重い仮想化に頼るケースが多い。ContainariumはSSHベースのワークフローを壊さずに低コスト・高速に環境を配布でき、特にコスト意識が高いスタートアップやブートキャンプ、社内ハンズオンに刺さる実用案である。

## 詳細解説
- 基本コンセプト  
  - 1台のクラウドVM（Jump Server）上に複数のLXCシステムコンテナを配置。各コンテナは「軽量なVM」的に振る舞い、ユーザーごとにSSHでログイン可能。KubernetesやAppコンテナ（Docker）ではなく、システムコンテナ（LXC）を採用している点が特徴。

- 主な技術要素  
  - LXC / Incus: フルLinuxユーザー空間を提供するシステムコンテナ。SSHやユーザーアカウント管理、サービスの常駐に向く。  
  - ZFS: 永続ストレージ。コンテナボリュームをZFSで管理することで、スナップショット、圧縮、クォータ、スポットインスタンスの復旧に強い。  
  - SSH ProxyJump: ジャンプサーバ経由で各コンテナへ透過的に接続。ジャンプ側はプロキシ専用アカウントにし、直接のシェルは与えない設計でセキュリティを確保。  
  - 管理プレーン: Go製のCLI（gRPCオプション）＋Terraformでインフラ構築を自動化。コマンド例: containarium create alice --ssh-key ~/.ssh/alice.pub

- 運用設計の肝  
  - 永続性: コンテナとデータはVM再起動やスポットプリエンプションをまたいで保持。  
  - セキュリティ: 各ユーザーはコンテナ内の自分のアカウントのみが操作可能。ジャンプサーバはプロキシ専用で管理者のみが直接操作。AppArmorやリソース制限でサンドボックス化。  
  - スケーラビリティ: 単一サーバで20〜50ユーザー、水平拡張で複数ジャンプサーバに分散し100〜250ユーザーに対応。  

- コスト感（リポジトリにある例）  
  - 50コンテナを1台のn2-standard-8相当に載せた例: 約$98/月（約$2/ユーザー）。水平展開で150ユーザーだと約$312/月。従来の1VM/1ユーザーに比べ最大で90%のインフラコスト削減をうたう。

- 何を意図しているか（差別化点）  
  - 「K8sではなくLXC」を選ぶ理由は、SSHベースで常駐する開発環境に自然にフィットするため。GUIブラウザIDEやアプリコンテナとは用途が明確に異なる。

## 実践ポイント
- 今すぐ試す手順（概略）  
  1) Terraformでジャンプサーバ（VM）と永続ディスクを用意  
  2) Containarium CLIをインストールし、最初のコンテナを作成  
  3) ローカルの~/.ssh/configにProxyJump設定を追加して接続確認

- 便利なコマンド例
```bash
# Containariumでコンテナを作る例
containarium create alice --ssh-key ~/.ssh/alice.pub
```

```bash
# ~/.ssh/config に書くProxyJump設定の例
Host containarium-jump
  HostName <jump-server-ip>
  User alice
  IdentityFile ~/.ssh/containarium

Host my-dev
  HostName 10.0.3.100
  User alice
  ProxyJump containarium-jump
```

- 日本市場での活用シーン  
  - 社内の開発演習、コードリビュー用の再現環境、機械学習の小規模実験用サンドボックス、オンサイト研修やオンライン講座の短期環境。クラウドコストが高めの日本法人や教育機関で即効性がある。国内リージョンのVMとブロックストレージ（GCP/AWS/Azure）で同様に構成可能。

- 注意点（導入前に確認すべきこと）  
  - 現行の認証・監査要件（ログ保存や鍵管理）が満たせるか。  
  - コンテナあたりのディスク・メモリ割当とZFSのチューニング。  
  - セキュリティポリシー（外部ネットワーク接続制限やイメージの管理）。  

Containariumは「既存のSSHワークフローを壊さず、運用コストと配布時間を劇的に下げる」現実的な打ち手だ。まずは小規模でPoCを回して、接続性・復旧・監査の要件を満たすかを確認してみることを勧める。
