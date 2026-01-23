---
layout: post
title: "remotely unlocking an encrypted hard disk with systemd initrd on Arch - systemd initrdで暗号化ディスクをリモート解除する方法"
date: 2026-01-23T03:01:07.319Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://jyn.dev/remotely-unlocking-an-encrypted-hard-disk/"
source_title: "remotely unlocking an encrypted hard disk"
source_id: 896063680
excerpt: "initramfsにTailscaleとSSHを組み込み暗号化ルートを安全に遠隔解除する手順"
---

# remotely unlocking an encrypted hard disk with systemd initrd on Arch - systemd initrdで暗号化ディスクをリモート解除する方法
外出先からでも「起動→認証→復旧」できる！initramfsにTailscaleとSSHを仕込んで暗号化ルートを安全に解除するハック

## 要約
initramfs（初期RAMファイルシステム）上でTailscaleと軽量SSHを動かし、暗号化されたルートをリモートで解除する手法。Arch + systemd環境での具体手順と安全策を紹介する。

## この記事を読むべき理由
日本でも出張や移動先から自宅の開発マシンにアクセスする場面は多い。停電やIP変化でリモート接続できない事態を、防げる実用的な手法だから。

## 詳細解説
- なぜ可能か：initramfsは「メモリ上で動く小さなOS」で、ArchではsystemdがPID 1として動く。つまりinitramfsにサービス（ネットワーク/Tailscale/SSH）を組み込める。
- 必要な構成要素：
  - ネットワーク（sd-networkフックでEthernet DHCP等を設定）
  - Tailscale（initramfs内で接続し、リモートIPを確保）
  - SSH（initramfs内でdropbearなどを使い、実際のシェルではなくパスワード入力エージェントのみを許可）
- セキュリティ考慮：
  - initramfs内に秘密鍵が平文で置かれる点に注意（Tailscaleキーはデフォルト90日で期限切れ）。
  - 対策例：Tailscale側で tag:initrd を付与しACLで受信のみ許可／キー有効期限を無効化／SSHは実行コマンドを解除用agentに限定。
  - ホストの通常SSH鍵を流用しない（dropbear専用鍵を生成する）。
- 実装ポイント：mkinitcpioフック（sd-network, tailscale, sd-dropbear）を追加してinitramfsを再生成し、起動時にinitramfsがネットワークとTailscale経由で外部から接続可能になる。

## 実践ポイント
- パッケージ例（rootで実行）:
```bash
bash
pacman -S dropbear
yay -S mkinitcpio-systemd-extras mkinitcpio-tailscale
```
- /etc/mkinitcpio.conf の HOOKS に sd-network, tailscale, sd-dropbear を追加（例）:
```bash
bash
# 例: HOOKS=(base systemd ... sd-network tailscale sd-dropbear sd-encrypt filesystems)
```
- Tailscale初期設定（initcpio用デバイス登録）:
```bash
bash
setup-initcpio-tailscale
# Webコンソールで該当デバイスに tag:initrd を付与し、必要に応じてキー期限を無効化
```
- dropbearはinitramfs側でシェルを渡さないよう設定:
```bash
bash
# /etc/mkinitcpio.conf に
SD_DROPBEAR_COMMAND="systemd-tty-ask-password-agent"
```
- dropbear専用鍵生成とauthorized_keysコピー:
```bash
bash
cp ~/.ssh/authorized_keys /root/.ssh/
dropbearkey -t ed25519 -f /etc/dropbear/dropbear_ed25519_host_key
```
- Ethernet用の早期ネットワーク設定（/etc/systemd/network-initramfs/10-wired.network）:
```bash
bash
# [Match]
# Type=ether
# [Network]
# DHCP=yes
# SD_NETWORK_CONFIG=/etc/systemd/network-initramfs を mkinitcpio.conf に設定
```
- systemdがパスワード待ちで無期限待機する例（ブートローダのoptionsに追加）:
```bash
bash
# rootflags=subvol=/@,x-systemd.device-timeout=0
```
- initramfs再生成:
```bash
bash
mkinitcpio -P
```

補足：Wi‑Fiでの早期接続は複雑なので有線推奨。Tailscale ACLやタグでアクセス制御を厳しくし、不用意な外部アクセスを防ぐこと。

以上を踏まえれば、外出先から安全に暗号化ルートを解除して自宅マシンを復旧できる仕組みが作れる。
