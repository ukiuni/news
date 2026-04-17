---
layout: post
title: "Show HN: Smol machines – subsecond coldstart, portable virtual machines - Smol machines：サブセカンド起動のポータブル仮想マシン"
date: 2026-04-17T19:30:21.107Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/smol-machines/smolvm"
source_title: "GitHub - smol-machines/smolvm: Tool to build &amp; run portable, lightweight, self-contained virtual machines. · GitHub"
source_id: 47808268
excerpt: "サブ200msで起動、単一ファイル配布可能な軽量隔離VMでローカル開発やCIを即改善"
image: "https://opengraph.githubassets.com/eca4b80f3e27e1d1c1a76063824eeaf127d3a33f6442cd38ca64fe9571b047f4/smol-machines/smolvm"
---

# Show HN: Smol machines – subsecond coldstart, portable virtual machines - Smol machines：サブセカンド起動のポータブル仮想マシン

魅力的な日本語タイトル: 「起動200ms以下で配布可能な“自己完結型VM”——SmolVMがローカル開発とサンドボックスを変える」

## 要約
SmolVMはサブセカンド級のコールドスタート、ポータブルな単一ファイル（.smolmachine）、macOS（Hypervisor.framework）とLinux（KVM）で動く軽量なハードウェア隔離VMツールです。

## この記事を読むべき理由
ローカル開発・CI・安全な実行環境を手早く作りたい日本の開発者やSREにとって、依存を持ち運べて高速に起動する自己完結型VMはワークフローとセキュリティ運用を大きく簡素化します。Apple Siliconの普及や社内ポリシーでのサンドボックス需要とも親和性があります。

## 詳細解説
- アーキテクチャ: 各ワークロードはゲストカーネルを持つ“実際のVM”。macOSはHypervisor.framework、LinuxはKVMを利用。VMMはlibkrun（libkrunfw）をベースに実装。
- 起動性能とリソース: デフォルトは4 vCPU／8 GiB、メモリはvirtio balloonで「弾力的」に割当て（実際に使う分だけホストがコミット）。vCPUはアイドル時にハイパーバイザ側でスリープするため過剰配分のコストが小さい。
- 可搬性: smolvm packでイメージを単一バイナリ(.smolmachine)に焼ける。ホスト側のアーキテクチャが合えば依存不要で再現可能。
- セキュリティとサンドボックス用途: ネットワークはデフォルト無効。--netでオンにし、--allow-hostで許可先を制限可能。ホストSSHエージェントのフォワードにより秘密鍵をゲストに渡さずgit操作が可能（SSH_AUTH_SOCK必須）。
- 開発運用: 永続マシン作成・停止・再起動が可能で、インストール済パッケージは持ち越し。Smolfile（TOML）で環境を宣言して再現性を担保。
- 制約・注意点: macOSではバイナリ署名とHypervisorの権限が必要、ネットワークはTCP/UDPのみ（ICMP不可）、マウントはディレクトリ単位。ホストが対応アーキテクチャであることが前提。

## 実践ポイント
- インストール（macOS/Linux）:
```bash
# bash
curl -sSL https://smolmachines.com/install.sh | bash
```
- 一時的なコマンド実行（エフェメラルVM）:
```bash
# bash
smolvm machine run --net --image alpine -- sh -c "echo 'Hello from smolvm' && uname -a"
```
- .smolmachine にパッケージ化:
```bash
# bash
smolvm pack create --image python:3.12-alpine -o ./python312 ./python312 run -- python3 --version
```
- 永続マシン作成とSSHエージェント利用:
```bash
# bash
smolvm machine create --net myvm
smolvm machine start --name myvm
smolvm machine exec --name myvm -- git clone git@github.com:org/private-repo.git
```
- 日本向けの運用提案: 開発チームでSmolfileを共有してローカルの再現性を確保、CIでのテストサンドボックス化、社内での検証環境配布に.smolmachineを活用。macOSで配布する場合は署名とエンタイトルメント要件を事前に確認。

簡潔に言えば、SmolVMは「持ち運べる・速い・隔離された」開発・実行環境を求める日本の現場で即戦力になり得るツールです。
