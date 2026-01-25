---
layout: post
title: "Show HN: VM-curator – a TUI alternative to libvirt and virt-manager - Show HN: VM-curator — libvirt/virt-managerの代替となるTUI"
date: 2026-01-25T05:13:18.793Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/mroboff/vm-curator"
source_title: "GitHub - mroboff/vm-curator: vm-curator is a fast and friendly TUI to build and manage QEMU/KVM virtual machines in Linux. It does not rely on libvirt, which means 3D acceleration (para-virtualized, not pass-through) works for NVIDIA GPUs."
source_id: 46750437
excerpt: "libvirt不要でRTX対応の3D加速が動くRust製TUIでVM作成・管理を高速化"
image: "https://opengraph.githubassets.com/31342703885a4da53b9d4dee0dbdcebecb09752bbf60ea4e1ed6dedc427eb4c4/mroboff/vm-curator"
---

# Show HN: VM-curator – a TUI alternative to libvirt and virt-manager - Show HN: VM-curator — libvirt/virt-managerの代替となるTUI
libvirt不要でNVIDIAの3D加速が使える？Rust製TUI「vm-curator」が描くシンプルで高速なVM管理体験

## 要約
Rustで書かれたターミナルUIツール「vm-curator」は、libvirtに依存せずQEMU/KVM仮想マシンを発見・作成・起動・管理できる。NVIDIA向けのパラバーチャライズド3D加速（virtio-vga-gl）が動作する点が大きな特徴。

## この記事を読むべき理由
日本の開発者やインフラ担当は、手軽に高性能なGPU対応VMやレガシーOS検証環境を作りたい場面が多い。libvirtの複雑さや制約を回避して直接QEMUを扱えるツールは、ローカル検証やテストベッド構築の時間短縮に直結する。

## 詳細解説
- アーキテクチャ：Rust製のTUIアプリ。VMライブラリ（デフォルト ~/vm-space）内のlaunch.shを解析して構成を抽出する。GUIではなく端末中心の操作性（vim風のキー操作など）。
- libvirt非依存：libvirtを介さないため、NVIDIAの「パラバーチャライズド」3Dアクセラレーションが動作する（開発者がRTX-4090＋特定ドライバで動作確認済み）。ただし完全なGPUパススルー（フルパススルー）とは異なる。
- 主要機能：
  - 自動VM検出とOSごとの階層整理
  - 5ステップの作成ウィザード（50以上のOSプロファイル）
  - launch.shの編集・再解析、スナップショット管理（qcow2 + qemu-img）
  - USBデバイス列挙と永続的なパススルー設定（libudev利用）
  - OVMF/UEFIパスの自動検出（複数ディストリで対応）
- 依存とビルド：Rust 1.70+、QEMU（qemu-system-*）、libudev（開発パッケージ）。cargo build --releaseでビルド可能。
- CLI補助：TUIのほか list/launch/info/snapshot 等のCLIサブコマンドを提供。

## 日本市場との関連性
- ローカルでのマルチOS検証（組み込み・レガシーサポート、教育用環境構築）や、GPUを必要とする機械学習・グラフィックス検証を手元でやりたい開発者に有益。  
- 企業の閉域ネットワークやオンプレのラボ環境で、libvirtを導入せず軽量に運用したいケースにも適合。  
- 日本で広く使われるディストリ（Debian/Ubuntu/Arch/Fedora/NixOS）でのUEFI検出を考慮しており、環境移植性が高い。

## 実践ポイント
- まずはテスト環境で検証：重要なVMはバックアップ（qcow2のスナップショット運用推奨）。
- 必須パッケージ：qemu-system-* と libudev-dev を整備してからビルドする。
- GPU利用時：ホストのNVIDIAドライバやゲスト側のQEMU 3D対応（virtio-vga-gl, gl=on）を確認する。フルパススルーが必要なら別手段を検討。
- カスタマイズ：OSメタデータやASCIIアート、QEMUプロファイルを ~/.config/vm-curator/ 以下で上書き可能。
- 貢献や改善：TUIゆえの見た目改善（ASCIIアート等）やプロファイル追加は歓迎されているため、興味があればPRを検討する。

元リポジトリ（ソース・README・インストール手順）は GitHub: https://github.com/mroboff/vm-curator を参照。
