---
layout: post
title: "Coding Agent VMs on NixOS with microvm.nix - microvm.nixでNixOS上にコーディングエージェント用VMを構築"
date: 2026-02-01T08:29:02.199Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://michael.stapelberg.ch/posts/2026-02-01-coding-agent-microvm-nix/"
source_title: "Coding Agent VMs on NixOS with microvm.nix"
source_id: 702959097
excerpt: "NixOSで使い捨てMicroVMを即構築しAIエージェントを安全に隔離して実験可能に"
---

# Coding Agent VMs on NixOS with microvm.nix - microvm.nixでNixOS上にコーディングエージェント用VMを構築
使い捨てMicroVMで「エージェントに個人データを触らせない」安全なコーディング環境を素早く作る

## 要約
microvm.nixを使うと、NixOS上で永続性を持たない（ほぼ使い捨ての）MicroVMを簡単に作れ、AIコーディングエージェントをホスト環境から隔離して安全に実行できます。

## この記事を読むべき理由
AIエージェントがコードを触る機会が増える今、個人ファイルや社内資産を守りつつ実験できる「隔離された実行環境」は必須。日本のスタートアップや企業でのプロトタイプ検証、セキュリティ重視の開発フローに直結します。

## 詳細解説
- 背景と目的  
  - コーディングエージェント（例：Claudeなど）は便利だが、勝手にコマンドを実行するとプライバシーやセキュリティが危険になる。microvm.nixは「VMごと廃棄できる」エフェメラル環境を簡単に作るためのNixOSモジュール群です。主な考え方は「ホストと最小限だけ共有し、残りは使い捨てにする」。

- 基本構成（簡潔）  
  1. ネットワーク準備：ホスト側にブリッジ（例：microbr）を作り、microvm用tapインターフェイスをブリッジに接続、NATで外向き通信を許可。  
  2. flake.nix：microvm.nixを入力に追加し、ホストのNixOS設定にmicrovm.nixosModules.hostを有効化。VM群は別ファイル（microvm.nix）で宣言。  
  3. microvm.nix：各VMごとにホスト名・IP・tap ID・MAC・workspace（ホストと共有する作業ディレクトリ）などを定義し、microvm-base.nixをimportして共通設定を注入。  
  4. microvm-base.nix（コア）：
     - systemd-networkd/systemd-resolvedの設定で固定IPやゲートウェイを与える。  
     - 共有はvirtiofs（または適宜）で /nix/store（読み取り）や作業ディレクトリ、SSHホスト鍵などをマウント。  
     - writableStoreOverlayを使い一時的な書き込み可能な /nix/.rw-store を提供（home-managerやnix-daemonのため）。  
     - ハイパーバイザはcloud-hypervisor（QEMUも可）、vCPU/メモリ等のリソース設定。  
     - systemdの /nix/store アンマウント問題へのワークアラウンドを含む。  
  5. home-manager連携（microvm-home.nix）：ユーザー環境（zsh、emacs、claude関連設定）をVM側で再現するために設定を共有。  
  6. 実行：VMの作業ディレクトリに必要なSSHホスト鍵を作り、systemdで microvm@<vmname> を起動。VMにSSHで入り、エージェントを「共有フォルダ上で」実行する。  

- セキュリティモデルの要点  
  - 「プライベートデータをそもそも渡さない」ことでリスクを大きく減らす。VMを破棄すれば状態は消えるため、マルウェアに感染しても影響は限定的。  
  - ただしネットワーク経由の情報漏洩や、共有ディレクトリ経由のデータ漏れは注意が必要（必要最小限の共有に留める）。

- 自動化と拡張  
  - 一度設定を作れば、Claudeのスキル等でVM作成手順を自動化できる（記事ではSkillsを使った自動化の試みを紹介）。  
  - 商用のサンドボックス/VMホスティング（exe.dev、Fly.ioのSpritesなど）も選択肢として挙げられる。

## 実践ポイント
- 必須手順（最短で試す）  
  1. microvm.nixをflakeへ追加し、microvm.nixosModules.hostを有効化。  
  2. 作業ディレクトリとSSHホスト鍵を用意：
```bash
mkdir -p ~/microvm/emacs/ssh-host-keys
ssh-keygen -t ed25519 -N "" -f ~/microvm/emacs/ssh-host-keys/ssh_host_ed25519_key
```
  3. VMを起動：
```bash
sudo systemctl start microvm@emacsvm
ssh 192.168.83.6
```
  4. 共有ワークスペース上でエージェントを実行（ホストのファイルは渡さない）。例：claudeを権限プロンプトなしで動かす。

- 実運用での注意点  
  - 共有するパスは最小限に（/nix/storeの読み取り共有も検討）。  
  - ネットワーク経路・nameserver設定を確認し、社内ポリシーに合わせてファイアウォールやプロキシを調整。  
  - 重要な機密は決して共有フォルダに置かない。必要ならさらに強固なサンドボックス（商用サービスや専用ハードウェア）を検討。

まとめ：NixOSとmicrovm.nixは、再現性の高い設定で「捨てられるVM」を素早く作れる強力なツールです。国内でもプロトタイプ検証やセキュリティ重視の開発に役立つので、Nixに馴染みがある開発者は一度試す価値があります。
