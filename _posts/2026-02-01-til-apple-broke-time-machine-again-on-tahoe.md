---
layout: post
title: "TIL: Apple Broke Time Machine Again On Tahoe - TIL: AppleがTahoeでTime Machineを再び壊した"
date: 2026-02-01T20:45:14.729Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://taoofmac.com/space/til/2026/02/01/1630"
source_title: "TIL: Apple Broke Time Machine Again On Tahoe - Tao of Mac"
source_id: 46848699
excerpt: "macOS TahoeでTime MachineがSMB仕様変更で停止、即効復旧手順と回避策を解説"
image: "https://taoofmac.com/media/til/2026/02/01/1630/fY_oAYhU-aPe6gdiXpboLe7GTwI=/image.png"
---

# TIL: Apple Broke Time Machine Again On Tahoe - TIL: AppleがTahoeでTime Machineを再び壊した
Appleがまたやらかした？Time MachineがTahoeで動かなくなったときの速攻対処法

## 要約
macOS TahoeでAppleがSMBの既定設定を変更したため、SynologyなどのNASに対するTime Machineバックアップが動作しなくなる問題が報告されています。対処法としてMac側でのnsmb.conf調整、NASのSMB設定変更、あるいは自前のDockerベースTime Machineターゲットへ移行する選択肢があります。

## この記事を読むべき理由
Time Machineは多くの開発者やユーザーにとって重要な復元手段。日本でもSynologyやNAS運用が一般的なため、同様のトラブルに直面する可能性が高く、短時間で復旧できる実務的な手順が役立ちます。

## 詳細解説
- 原因：macOS TahoeでSMBの既定値（例：署名の扱い）が厳格化され、NAS側の緩めのSMB実装と噛み合わなくなっています。結果として.sparsebundleを用いたTime Machineのマウント／復元が失敗するケースが発生。
- Mac側の対処：/etc/nsmb.conf を編集してSMB動作を緩和または互換性を持たせる手法が有効。サンプル内容は次のとおり（要管理者権限）。
```ini
# /etc/nsmb.conf
[default]
signing_required = yes
streams = yes
soft = yes
dir_cache_max_cnt = 0
protocol_vers_map = 6
mc_prefer_wired = yes
```
- Synology側の設定例（DSMのUI版により名称が多少異なる）：Maximum SMB protocol=SMB3、Opportunistic Locking=有効、SMB2 Lease=有効、SMB Durable Handles=有効、Server signing=NoまたはAuto、Transport encryption=無効。これらを調整すると互換性が改善することがあります。
- ネーミング注意点：.sparsebundle名に非ASCII文字が含まれると問題を引き起こすことがあるため、ASCIIのみの名前にしておくと安全。
- より堅牢な代替：Proxmox＋ZFS上にDockerでTime Machine用Sambaを立てる（mbentley/timemachine等）。NASベンダー実装に依存せず細かく設定可能です。Compose例：
```yaml
services:
  timemachine:
    image: mbentley/timemachine:smb
    container_name: timemachine
    restart: always
    network_mode: host
    environment:
      - TM_USERNAME=timemachine
      - TM_GROUPNAME=timemachine
      - PASSWORD=timemachine
      - TM_UID=65534
      - TM_GID=65534
      - SET_PERMISSIONS=false
      - VOLUME_SIZE_LIMIT=0
    volumes:
      - /mnt/shares/timemachine:/opt/timemachine
    tmpfs:
      - /run/samba
```

## 実践ポイント
- まずはMacでの一時的対処として /etc/nsmb.conf を編集して復旧を試みる。編集はsudo権限で行うこと。
- Synology等のNASはSMB設定を見直す（SMB3有効、署名設定など）。設定変更前に構成のスクリーンショットを撮っておく。
- .sparsebundleの名前に非ASCIIがあれば英数字だけに変更して再試行する。
- 長期的にはベンダー実装に依存しないDocker/Sambaベースのターゲットに移行すると安定性が向上する可能性が高い。
