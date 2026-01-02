---
  layout: post
  title: "FreeBSD: Home NAS, part 1 – configuring ZFS mirror (RAID1) - FreeBSDで作る自宅NAS（前編）：ZFSミラー（RAID1）の設定"
  date: 2026-01-02T08:06:01.050Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://rtfm.co.ua/en/freebsd-home-nas-part-1-configuring-zfs-mirror-raid1/"
  source_title: "FreeBSD: Home NAS, part 1 – configuring ZFS mirror (RAID1)"
  source_id: 931729766
  excerpt: "NVMeをOS、SATA二台をZFSミラー化して作る静音・高信頼な自作NAS構築手順"
  image: "https://rtfm.co.ua/wp-content/uploads/2025/11/freebsd_logo1.jpg"
---

# FreeBSD: Home NAS, part 1 – configuring ZFS mirror (RAID1) - FreeBSDで作る自宅NAS（前編）：ZFSミラー（RAID1）の設定
魅力タイトル: 自作静音NAS入門 — FreeBSDでNVMeをOS、SATAをZFSミラーにして安全かつ高速な家庭用ストレージを作る方法

## 要約
FreeBSD 14.3を使い、NVMeにシステム（UFS）、SATA SSD 2台でZFSミラー（RAID1）を構成する手順をVMで検証。LiveCD経由でSSHインストールし、gpart→zpoolで簡潔にミラーを作る流れを解説します。

## この記事を読むべき理由
家庭で静かで信頼できるNASを安価に作りたい日本のエンジニア／DIY好き向け。TrueNASも選択肢だが、素のFreeBSDで手動構築すると挙動や障害対応が理解でき、メンテ性と学習効果が高い点が日本の自宅運用に合います。

## 詳細解説
- 全体構成の方針  
  - マシン例：Lenovo ThinkCentre M720s SFF（NVMe + 2x SATA）を想定。  
  - 役割分離：NVMe = OS（UFS, 将来的にZFS化も可）、SATA×2 = ZFSプール（mirror/RAID1）。冗長性と耐障害性を確保。

- インストール手順（要点）  
  1. LiveCDでブートし、SSHで作業する（bsdinstallを使う）。ネットワークは ifconfig / dhclient で設定。  
  2. Live環境はISO上で /etc が読み取り専用のため、tmpfsを使った一時上書きでSSHのrootログイン許可やパスワード設定を行う（下記コマンド参照）。  
  3. bsdinstallで手動パーティション。システムディスクはGPT、freebsd-boot（仮想環境は512K）、freebsd-swap（2GB推奨）、freebsd-ufs（例:14GB）を作成。  
  4. ZFS用のディスク（ada1, ada2）にGPT作成→freebsd-zfsパーティションを追加。  
  5. zpoolでミラーを作成：zpool create tank mirror ada1p1 ada2p1。作成直後に /tank がマウントされる。  
  6. zfs set mountpoint=/data tank 等でマウントポイント変更、zfs set compression=lz4 tank で圧縮有効化。  
  7. UFSルートの場合は /boot/loader.conf に zfs_load="YES" を追加し、/etc/rc.conf に zfs_enable="YES" を設定して再起動し自動マウントを有効化。

- LiveCD上での小ワザ（重要）  
  - /etc が読み取り専用なので一時的に tmpfs を重ねて編集可能にする：
```bash
# bash
mount -t tmpfs tmpfs /mnt
cp -a /etc/* /mnt/
mount -t tmpfs tmpfs /etc
cp -a /mnt/* /etc/
passwd
service sshd onestart
echo "PermitRootLogin yes" >> /etc/ssh/sshd_config
service sshd onerestart
```
  - rootでのSSHログインを許可してから bsdinstall をリモートで続行。

- 主要コマンド（ダイジェスト）
```bash
# bash
gpart create -s gpt ada1
gpart add -t freebsd-zfs ada1
gpart create -s gpt ada2
gpart add -t freebsd-zfs ada2
zpool create tank mirror ada1p1 ada2p1
zfs set mountpoint=/data tank
zfs set compression=lz4 tank
sysrc -f /boot/loader.conf zfs_load="YES"
sysrc zfs_enable="YES"
```

## 実践ポイント
- テストは必ずVMで：まずVirtualBox/VMware上で手順確認。実機導入前に障害時の挙動やリカバリ手順を検証。  
- システムディスクをZFSにするかUFSにするかは要検討：ZFSは機能豊富だがRAM消費やブート周りの設定が増える。小メモリ環境ならUFSから開始。  
- ZFSの利点を活かす：lz4圧縮、スナップショット、dataset分離でデータ管理・バックアップを整備。  
- 自動マウント設定を忘れずに：UFSルート運用なら loader.conf と rc.conf にZFS関連を追加。  
- 監視・UI：運用時は zpool status / zfs list を定期確認。GUIが欲しければ Seafile や FileBrowser 等を検討。  
- バックアップ方針：ミラーはディスク故障から守るが誤削除やランサムウェアは防げない。別媒体/クラウドへの定期バックアップを設定する。

