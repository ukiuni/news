---
layout: post
title: "Anthropic Cowork feature creates 10GB VM bundle on macOS without warning - AnthropicのCowork機能が警告なく10GBのVMバンドルを生成する件"
date: 2026-03-02T15:42:35.595Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/anthropics/claude-code/issues/22543"
source_title: "Cowork feature creates 10GB VM bundle that severely degrades performance · Issue #22543 · anthropics/claude-code · GitHub"
source_id: 47218288
excerpt: "AnthropicのCoworkが知らぬ間に10GB超のVMを生成しMacを低速化"
image: "https://opengraph.githubassets.com/f57fad01ec47613d63af02bf8e4766301475fab1787df1a440fad267c7bf5451/anthropics/claude-code/issues/22543"
---

# Anthropic Cowork feature creates 10GB VM bundle on macOS without warning - AnthropicのCowork機能が警告なく10GBのVMバンドルを生成する件
注意喚起：Claudeの「Cowork」機能が知らぬ間に10GB超のVMイメージを作り、Mac（特に8GB機）を徐々に遅くする問題

## 要約
AnthropicのClaude DesktopのCowork機能が~/Library/Application Support/Claude/vm_bundles/... に10GB級のrootfs.imgを生成・残し、CPU負荷上昇やスワップ増加で数分〜数時間でパフォーマンスが劣化する報告が上がっている。削除で一時改善するが再発する。

## この記事を読むべき理由
多くの日本の開発者やテック愛好者はMac（MacBook Air/Proで8–16GB）を日常的に使っているため、知らないうちにストレージとRAMが圧迫され作業効率が落ちる可能性が高い。問題の把握と対処法を知っておけば業務停止や遅延を避けられる。

## 詳細解説
- 問題の本質：Cowork機能がローカルにVMバンドル（rootfs.img）を生成し、10GBまで増大して削除しても短時間で再生成される。ファイルは
  ~/Library/Application Support/Claude/vm_bundles/claudevm.bundle/rootfs.img
  に存在する。  
- 性状：生成されたVMイメージ自体が即座に容量を食うだけでなく、長時間の使用でCPUアイドル時でも合計24%→55%へ上昇、レンダラー/メインプロセスとGPUで負荷が分散、スワップインが増加するという観察がある。これはメモリリークか累積作業（バックグラウンドジョブ）の疑いを示す。  
- 環境：報告はmacOS（Darwin 25.2.0）、Claude Desktop最新、8GB RAMで確認。8GB前後のマシンが多い日本のユーザーに影響しやすい。  
- 一時的な改善：該当ディレクトリ（vm_bundles、Cache、Code Cache）を削除すると約75%改善するが、使い続けると再び劣化する。期待される挙動は「Coworkセッション後に不要なVMが自動的にクリーンアップされること」と「継続的に安定したCPU/RAM挙動」。

## 実践ポイント
- 現象確認（容量とプロセス）:
```bash
# ファイルサイズ確認
du -sh "$HOME/Library/Application Support/Claude/vm_bundles/claudevm.bundle/rootfs.img"

# プロセスのCPU/メモリ確認（macOSのtopやActivity Monitorを利用）
top -o cpu
```
- 一時対処（Claudeを終了してから実行）:
```bash
# Claudeを完全終了した上で削除（自己責任で）
rm -rf "$HOME/Library/Application Support/Claude/vm_bundles"
rm -rf "$HOME/Library/Application Support/Claude/Cache"
rm -rf "$HOME/Library/Application Support/Claude/Code Cache"
```
- 実務的な注意点：
  - 削除前に重要データのバックアップを取る。  
  - 再発するので定期的に監視するか、Cowork機能の利用を控える。  
  - 企業利用ならIT管理者に周知し、社内のMacで自動クリーン運用（スクリプトや監視）を検討。  
  - GitHub Issue（元報告）にリアルな環境情報（macOSバージョン、RAM、再現手順）を追加して報告すると対応が早まる可能性がある。

短くまとめると：Coworkは便利だが、現状はローカルに巨大なVMを残して性能悪化を招くリスクがある。Macのストレージ・メモリが限られる環境では利用と監視を慎重に。
