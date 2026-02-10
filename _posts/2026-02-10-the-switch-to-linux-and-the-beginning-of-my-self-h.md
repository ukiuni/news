---
layout: post
title: "The Switch to Linux and The Beginning Of My Self-Hosting Journey - Linuxへの移行とセルフホスティングの始まり"
date: 2026-02-10T20:06:24.894Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://hazemkrimi.tech/blog/linux-self-hosting-journey/"
source_title: "The Switch To Linux And The Beginning Of My Self-Hosting Journey | Hazem Krimi"
source_id: 46964159
excerpt: "Linux移行でラズパイから始める低コストなセルフホスティングでプライバシーと運用スキル獲得"
image: "https://hazemkrimi.tech/images/big-face.webp"
---

# The Switch to Linux and The Beginning Of My Self-Hosting Journey - Linuxへの移行とセルフホスティングの始まり
自分のPCとサーバーを取り戻す──Linuxで始める「個人クラウド」入門

## 要約
筆者は2023年にWindowsからLinuxへ完全移行し、VPSと自宅サーバーでセルフホスティングを始めた。低コストでプライバシーと運用スキルを手に入れた体験談と学びを共有する。

## この記事を読むべき理由
日本でもクラウド依存やデータ収集への不安が高まる中、安価に始められ、実務スキルも身につくセルフホスティングは現実的な選択肢。初心者がつまづきやすいポイントと実用的なツールが分かる。

## 詳細解説
- なぜLinuxか：所有権・カスタマイズ性・軽量性が主目的。筆者はDebian 11から始め、ゲームはQEMU/KVMのGPUパススルーでWindows VMを動かして対処。Wine/Protonで互換性も向上中。
- ウェブサイト移行：Next.js→Hugoに移して静的化し、VercelからVPSへ。VPS運用でNginx、Certbot、systemd、SSH/ファイアウォール、GitHub Actions、Crowdsecなどの運用ツールを学んだ。
- VPS・自宅サーバー構成例：筆者のVPSはEPYC/32GB/400GB NVMe（ホスティング契約）。自宅は当初Raspberry Pi 4(8GB)+外付けSSDでSyncthing（同期）とPi-hole（広告ブロック）を稼働。後に余ったデスクトップをProxmox VE化してLXC/VMへ移行、WireGuardでリモートアクセス、ddclientで動的IP対策（DDNS）を実装。
- ストレージと可用性：UPS接続で停電対策、GPUのPCIeパススルーでVMに性能割当て。SearXNGなどのセルフ検索も導入。
- 学び：サーバー運用でシステム管理力が上がり、OSSへの貢献意欲が湧く一方、設定や保守には根気が必要。

## 実践ポイント
- まずは小さく始める：Raspberry Pi + SSDでSyncthingとPi-holeを動かすのが入門に最適。
- ウェブは静的ジェネレータ（Hugo）で軽量運用、VPSは最小構成からスケール。
- リモート接続はWireGuard、DDNSはddclientやプロバイダのサービスを利用。
- セキュリティ運用：Nginx+CertbotでHTTPS、SSH鍵認証、Crowdsecで不要トラフィックをブロック。
- 学習ロードマップ：Linux基礎 → systemd / Nginx → コンテナ/LXC/Proxmox → バックアップとUPS運用。
- 日本向け補足：国内VPSやレンタルサーバー（さくらのVPS、ConoHa、さくらのクラウド等）を利用すれば通信遅延やサポート面で安心。

以上を参考に、まずは1台で「自分のクラウド」を作ってみると良い。
