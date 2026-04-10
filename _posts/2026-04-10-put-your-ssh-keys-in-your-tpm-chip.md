---
layout: post
title: "Put your SSH keys in your TPM chip - SSH鍵をTPMチップに格納する"
date: 2026-04-10T19:08:38.217Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://raymii.org/s/tutorials/Put_your_SSH_keys_in_your_TPM_chip.html"
source_title: "Put your SSH keys in your TPM chip! - Raymii.org"
source_id: 1247449977
excerpt: "物理トークン不要でTPMにSSH鍵を安全保存する具体手順と復元対策"
---

# Put your SSH keys in your TPM chip - SSH鍵をTPMチップに格納する
もうローカルの秘密鍵ファイルは怖くない。PC内蔵のTPMでSSH鍵を安全に保管する実践ガイド

## 要約
TPM（Trusted Platform Module）にSSH秘密鍵を保存すると、ファイルやメモリ上に鍵を置くより安全になり、物理トークンなしで鍵をハードウェア保護できる。手順はTPMの準備→PKCS#11トークン作成→鍵のインポート→SSH設定の4ステップ。

## この記事を読むべき理由
Windows 11普及でTPM搭載機が増え、専用HSMやYubiKeyを持たない日本の開発者や企業でも手元のPCでハードウェア保護を手軽に導入できる。初級者でも実用できる具体手順を示す。

## 詳細解説
- TPMとHSMの違い  
  - HSM（YubiKey等）は持ち運べる外部デバイスで物理プレゼンスが必要なことが多い。  
  - TPMはマシンに内蔵され常時接続されているため利便性は高いが、デバイス依存（例：BIOS更新でTPMが初期化されるリスク）がある。  
- 方針の決定理由  
  - TPMに「既存のSSH秘密鍵をインポート」する方式を推奨。TPMで鍵を生成することも可能だが、BIOS更新や移行時の復元性を考え、オフラインで生成しバックアップした鍵をTPMに入れるほうが安全かつ実用的。  
- 必要なソフトウェア（Debian/Ubuntu例）と事前作業  
  - tpm2-tools、tpm2-pkcs11、tpm2-abrmd、opensc等をインストールし、tssグループにユーザーを追加する。WSLでは動作しない点に注意。  
- トークンと鍵の取り扱い  
  - tpm2_ptoolでPKCS#11トークン（永続ストア）を作成し、SO PINとUser PINを設定。実際の秘密鍵はTPM内に直接保存されず、暗号化されたファイルとしてトークンディレクトリに置かれ、利用時にTPMが読み込む方式。  
- SSH連携方法  
  - PKCS#11プロバイダのライブラリパスを環境変数で指定し（例：/usr/lib/pkcs11/libtpm2_pkcs11.so）、~/.ssh/configにPKCS11Providerを追加するとsshがTPM鍵を使える。ssh-add -s を使えばエージェントに登録してPINの入力を一回に抑えられる。

## 実践ポイント
- 必要コマンド（例）
```bash
# Debian/Ubuntu の例
sudo apt install tpm2-tools libtpm2-pkcs11-tools libtpm2-pkcs11-1 opensc tpm2-abrmd
sudo usermod -a -G tss "$USER"   # ログアウト/再ログイン要
```
```bash
# トークン初期化
mkdir -p ~/.tpm2_pkcs11
tpm2_ptool init
# sopin.txt と userpin.txt に改行なしでパスワードを保存してから
tpm2_ptool addtoken --pid 1 --label sshtoken --sopin $(cat sopin.txt) --userpin $(cat userpin.txt)
```
```bash
# 既存鍵をPEM化してインポート（鍵は事前にオフラインで作成してバックアップ）
ssh-keygen -f tpm_key -mPEM -e
tpm2_ptool import --label sshtoken --key-label sshkey1 --userpin $(cat userpin.txt) --privkey tpm_key --algorithm rsa
rm tpm_key
```
```bash
# SSH設定
export TPM2_PKCS11_SO=/usr/lib/pkcs11/libtpm2_pkcs11.so
# ~/.ssh/config に追加:
# PKCS11Provider /usr/lib/pkcs11/libtpm2_pkcs11.so
# エージェントに追加:
ssh-add -s $TPM2_PKCS11_SO
```
- 注意点（必ず守る）  
  - 鍵はオフラインで生成し安全にバックアップを保持する（TPMが初期化される可能性に備える）。  
  - BIOS更新やマザーボード交換でTPM内容が消えることがあるため、復旧手順を用意する。  
  - WSL環境では動作しないケースがあるので、ネイティブLinuxや実機で動作確認する。

以上を踏まえ、まずは非重要な鍵で試してから本番鍵を移行することを推奨する。
