---
layout: post
title: "FreeBSD Home NAS, part 8: Backing up NFS and Samba data with restic - FreeBSDホームNAS（第8回）：resticでNFS／Sambaデータをバックアップする"
date: 2026-01-08T12:32:14.247Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://rtfm.co.ua/en/freebsd-home-nas-part-8-nfs-and-samba-data-backups-using-restic/"
source_title: "FreeBSD: Home NAS, part 8 – NFS and Samba data backups using restic"
source_id: 1251322017
excerpt: "FreeBSD NASのNFS/Sambaをresticで暗号化しS3へ安全にバックアップ"
image: "https://rtfm.co.ua/wp-content/uploads/2025/11/freebsd_logo1.jpg"
---

# FreeBSD Home NAS, part 8: Backing up NFS and Samba data with restic - FreeBSDホームNAS（第8回）：resticでNFS／Sambaデータをバックアップする
魅力的タイトル: 家のNASをクラウドに守る―FreeBSD/NFS/Sambaをresticで安全にバック備する方法

## 要約
FreeBSD上のNFSとSamba共有を、ローカルでスナップショット管理するZFSに加え、resticで暗号化しながらクラウド（AWS S3を本命、Google Driveを冗長）へバックアップする手順と考え方を紹介する。

## この記事を読むべき理由
ローカルRAIDやZFSスナップショットだけでは災害や機器紛失に対応しきれません。特に日本の家庭や小規模オフィスで、写真・仕事データ・設定ファイルを確実に守る実践的な方法が学べます。FreeBSD環境での実践例は少ないため、導入ハードルを下げる参考になります。

## 詳細解説
- なぜresticか  
  resticはGo製のCLIツールで、暗号化・差分（ブロック単位の重複排除）・多様なストレージバックエンド対応が特徴。NFSやSamba経由のデータ、Linux/FreeBSD/Windows混在環境でも同じクライアントで扱える点が強みです。S3はネイティブ対応、Google Driveはrclone経由で接続できます。

- リポジトリとスナップショットの仕組み（簡潔）  
  resticはリポジトリ内に暗号化されたブロック（blob）を保存し、各バックアップは「スナップショット」として記録されます。変更がなければ新しいスナップショットによる容量増は最小化されます。復元にはresticクライアントだけあれば良く、ファイルシステム依存が少ない点も利点です。

- 暗号と鍵管理のポイント  
  各リポジトリにマスターキーがあり、ユーザーパスワードはKDF（scrypt）で派生キーに変換されてマスターキーを復号します。複数のアクセス用キーを発行でき、パスワード変更や運用時の自動化（RESTIC_PASSWORD 環境変数、--password-file）に対応します。

- FreeBSD上での配置例（構成）  
  例：LinuxノートPC群 -> NFSマウントされたFreeBSD上の /nas/nfs/backups に定期バックアップ -> FreeBSDからAWS S3（primary）とGoogle Drive（rclone経由、secondary）へコピー。Sambaは /nas/smb/media と /nas/smb/private を保管対象に含めます。FreeBSD本体の設定（/etc、/usr/local/etc、/var/db 等）も別途スナップショット対象に。

- 運用上の注意点  
  - バックアップ対象／除外はリストファイルで明示できる（--files-from、--exclude-file）。  
  - 自動化はcronやFreeBSDのperiodic/rcスクリプトで。パスワードはファイルか環境変数で安全に渡す。  
  - 保持ポリシーは restic forget と prune で管理する（スナップショット肥大化対策）。  
  - 定期的に restic check や復元試験を行い、実際に復旧できることを確認する。

## 実践ポイント
- インストール（FreeBSD / Arch Linux例）
```bash
# FreeBSD
pkg install restic

# Arch Linux
sudo pacman -S restic
```

- リポジトリ初期化と簡単なバックアップ例
```bash
restic init --repo /path/to/repo
# バックアップ（例: NFSマウントされた共有）
restic backup /mnt/nfs/share --repo /path/to/repo
# スナップショット一覧
restic snapshots --repo /path/to/repo
```

- パスワード自動化の一例（ファイル経由）
```bash
mkdir -m700 ~/.config/restic
pwgen 32 1 > ~/.config/restic/repo-pass
chmod 600 ~/.config/restic/repo-pass
restic backup /mnt/nfs/share --repo /path/to/repo --password-file ~/.config/restic/repo-pass
```

- Google Driveを追加の保存先にする（概念）  
  1) rcloneでGoogle Driveを設定し、remote名を作る。  
  2) resticは rclone を介したバックエンドをサポートするので、S3を本体、rclone remote を予備コピー先として restic copy や別ジョブで同期する。

- 運用ルール（推奨）  
  - 本番（S3）と二次（Google Drive）を分ける：S3へ直接バックアップ、別ジョブで restic copy を使いGoogle Driveへ複製。  
  - 毎週・毎月の保持ポリシーを設定して forget/prune を運用。  
  - 復元手順をドキュメント化して半年に一度は完全復元テストを実施する。

FreeBSD＋ZFSのスナップショットとresticの暗号化クラウド保存を組み合わせれば、ローカル障害と地域災害の両方に強いバックアップ戦略になります。興味があれば、実際のcrontab例やrclone設定ファイルの書き方も続編で紹介します。
