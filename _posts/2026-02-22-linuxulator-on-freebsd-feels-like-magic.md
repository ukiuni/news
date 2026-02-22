---
layout: post
title: "Linuxulator on FreeBSD Feels Like Magic - FreeBSD上のLinuxulatorは魔法のようだ"
date: 2026-02-22T19:30:50.434Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://hayzam.com/blog/02-linuxulator-is-awesome/"
source_title: "Linuxulator on FreeBSD Feels Like Magic | Hayzam"
source_id: 47113527
excerpt: "FreeBSDでLinuxulatorを使いVSCode Remoteをローカル並みに高速化する手順"
image: "https://hayzam.com/open-graph.jpg"
---

# Linuxulator on FreeBSD Feels Like Magic - FreeBSD上のLinuxulatorは魔法のようだ
FreeBSDで動くVS Codeリモート開発が「本当に使える」理由 — Linux互換レイヤでローカル開発並みの快適さを手に入れる

## 要約
FreeBSDのLinux互換レイヤ（Linuxulator）を使うと、VS CodeのRemote SSHがほぼそのまま動作し、NFS/SSHFSよりはるかに快適なリモート開発環境が構築できる。

## この記事を読むべき理由
多ファイル・大型プロジェクトや組込み機器（OpenWRTなど）を扱う日本の開発者にとって、遅いファイルマウントを回避して本体上で開発ツールを動かす手法は即効性のある生産性向上策だから。

## 詳細解説
著者はVS CodeのRemote SSHをFreeBSDで動かそうとし、公式サポート外にもかかわらずLinuxulator経由でLinuxバイナリを動かす手順で成功。ポイントは以下。

- FreeBSDのLinuxulatorを有効化し、Linuxベースシステムを導入する：
```bash
service linux enable
service linux start
pkg install linux_base-rl9
```
- VS Codeが接続した際にLinux互換パスを使わせるため、ログインシェル用に専用の環境ファイルを作成（例：~/.bash_linux）：
```bash
# ~/.bash_linux
PATH="/compat/linux/usr/local/sbin:/compat/linux/usr/local/bin:/compat/linux/usr/sbin:/compat/linux/usr/bin:/compat/linux/sbin:/compat/linux/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
```
- sshdがクライアントからBASH_ENVを受け取るように設定し、クライアント側で送信する：
```bash
# サーバ（FreeBSD）
sysrc sshd_flags="-o AcceptEnv=BASH_ENV"

# クライアント（~/.ssh/config）
Host sylve-code
  Hostname 192.168.72.172
  User root
  Port 22
  IdentityFile ~/.ssh/id_ed25519
  SetEnv BASH_ENV=".bash_linux"
  RemoteCommand /compat/linux/bin/bash
```
この構成でRemote SSHがLinuxバイナリ上で起動し、LSPや拡張機能がほとんど問題なく動作。唯一のハマりどころとしてRollupのネイティブバイナリが利用できなかったが、WASM版に切り替えるnpm overridesで回避できた：
```json
{
  "overrides": {
    "rollup": "npm:@rollup/wasm-node@^4.30.1"
  }
}
```

著者はOpenWRT（muslベース）でも同様に動作した例を挙げ、Linux ABIの安定性とFreeBSDの実装の良さを強調している。

## 実践ポイント
- まずは非本番マシンでLinuxulatorを有効化して試す（rootログインは避け、必要ならユーザー環境を整える）。
- 大きなリポジトリや多数のLSPでNFS/SSHFSが遅いなら、この方法は即効性が高い。
- ネイティブバイナリが無ければWASMやnpmのoverridesで代替を検討する。
- セキュリティ面は要注意（SSH設定・ユーザー権限・パッケージ管理を適切に）。

FreeBSDを「使い倒したい」開発者にとって、LinuxulatorでVS Codeリモートが手軽に動くことは大きな発見です。導入コストは低いので、まずは試して違いを体感してみてください。
