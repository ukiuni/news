---
layout: post
title: "4x faster network file sync with rclone (vs rsync) (2025) - rcloneでネットワーク同期が4倍速に（rsync比）"
date: 2026-02-02T15:50:02.084Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.jeffgeerling.com/blog/2025/4x-faster-network-file-sync-rclone-vs-rsync/"
source_title: "4x faster network file sync with rclone (vs rsync) - Jeff Geerling"
source_id: 46820142
excerpt: "rcloneの並列ストリームで10ギガ回線を活用、rsync比約4倍で大容量同期を劇的に短縮"
---

# 4x faster network file sync with rclone (vs rsync) (2025) - rcloneでネットワーク同期が4倍速に（rsync比）
ローカルLANで10GbEをフル活用！rsyncを超えるrcloneの並列転送で大容量プロジェクトが一気に終わる

## 要約
rsyncがシングルスレッドでファイルを逐次コピーする一方、rcloneの並列ストリーム機能（--multi-thread-streams）を使うと、同じディレクトリコピーが約8分→約2分に短縮され、実測でネットワーク帯域（10Gbps）をほぼ飽和させられた。

## この記事を読むべき理由
日本でも映像制作や大容量データを扱うチームは増えており、社内NASやThunderbolt/NVMeストレージ間の同期速度は作業効率に直結します。手元の環境で簡単に試せる手法なので、時間短縮と帯域活用の改善に即効性があります。

## 詳細解説
- 問題点（rsync）
  - rsyncは多くの設定で「1ファイルずつ直列コピー」するため、並列転送ができずネットワーク/ストレージのピーク性能を引き出せないことがある。
  - 実例では大容量ファイルでもrsyncが約350MB/s付近で頭打ちし、合計で約59GiBのコピーに8分超を要した。

- rcloneの強み
  - rcloneはクラウド向けツールとして有名だが、ローカルLANやNAS間でも使える。重要なのは --multi-thread-streams オプションで、ファイル内の転送を複数ストリームで並列化できる点。
  - 例：筆者は32ストリームに設定して実行。結果、ネットワークが約1GB/s（=10Gbps回線）をほぼフルに使い、同じ作業を約2分で完了した。
  - ディレクトリスキャン（メタデータ比較）はrsyncと同程度の時間なので、差が出るのは実データ転送フェーズ。

- 実行時の注意
  - rcloneでrsyncの -a 相当を再現するフラグや、Final Cut Proのようなソフトが作る特殊なキャッシュ（.fcpcache等）の除外を設定しておく必要あり。
  - NASのCPU（特に省電力なARMコア）は圧縮や暗号化でボトルネックになるため、不要な圧縮は逆効果になる可能性がある。
  - サイズ表記（GiB vs GB）や除外パターンで転送量表示が異なる場合がある。

- 実行例（簡略）
```bash
# rsync（例）
rsync -au --progress --stats /Volumes/mercury/* /Volumes/Shuttle/Video_Projects
```
```bash
# rclone（並列ストリームで高速化）
rclone sync /Volumes/mercury/ /Volumes/Shuttle/Video_Projects \
  --exclude='**/._*' --exclude='.fcpcache/**' \
  --multi-thread-streams=32 -P -L --metadata
```

## 実践ポイント
- まず小さなディレクトリでrcloneの並列数（--multi-thread-streams）を段階的に増やして挙動を確認する。
- NASやルーターのCPU/PCIe帯域がボトルネックにならないか監視する（iostat, iftop, NASの管理画面）。
- 元のrsync設定で残したい属性がある場合は、rcloneの --metadata / --links 等で明示的に再現する。
- 定期バックアップならば差分転送はrsyncが有利なケースもあるので、用途に応じて使い分ける。
- 大容量メディアワークフロー（映像編集など）では、まずrcloneでフル同期してから差分はrsync／rcloneで運用するハイブリッドが有効。

短時間で効果が出る手元チューニングなので、10GbEやNVMe/NASを使う現場はまず一度試してみてください。
