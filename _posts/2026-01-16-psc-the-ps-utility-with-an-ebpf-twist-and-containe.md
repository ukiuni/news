---
layout: post
title: "psc: The ps utility, with an eBPF twist and container context - psc: eBPFとコンテナ文脈を加えたpsユーティリティ"
date: 2026-01-16T15:41:35.540Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/loresuso/psc"
source_title: "GitHub - loresuso/psc: the ps utility, with an eBPF twist and container context"
source_id: 46646091
excerpt: "eBPFで/procを迂回し、コンテナやソケット情報まで可視化する新しいpsツール"
image: "https://opengraph.githubassets.com/afc95e5dae61d5a4cddb4eaadd4542656ec0ef40a19148e2227b938f3ac106a9/loresuso/psc"
---

# psc: The ps utility, with an eBPF twist and container context - psc: eBPFとコンテナ文脈を加えたpsユーティリティ
カーネル直視で「隠れたプロセス」まで見つける――コンテナとネットワーク文脈を一度に辿れる新しいps

## 要約
eBPFイテレータで/procを迂回し、Google CELで柔軟に絞り込める「psc」は、コンテナ情報やソケット/ファイル記述子を絡めてプロセス状態を精密に可視化するツールです。root権限でカーネル直読みするため、ユーザー空間ルートキットによる隠蔽を回避できます。

## この記事を読むべき理由
日本のSRE／セキュリティ担当やクラウドネイティブ開発者にとって、コンテナ大量運用下でのトラブルシュートや侵害検知は重要課題です。pscは「どのコンテナで何が開いているか」「どのプロセスが外向き接続を張っているか」を短い式で答えてくれるため、調査速度と正確性が大きく向上します。

## 詳細解説
- 仕組み（要点）
  - eBPFイテレータを使いカーネル内部のプロセス／FD／ソケット構造体を直接走査するため、/procやreaddir/openをフックするLD_PRELOAD型ルートキットで見えなくされているものも検出できます。
  - 検索条件はGoogle CEL（Common Expression Language）。文字列操作や論理式、数値比較が可能で、複雑な条件を1行で書けます。
- 主な機能
  - コンテナ文脈：container.id / name / image / runtime（docker/containerd/crio/podman）でフィルタ可能。ホスト側から任意のコンテナのプロセスやソケットを調査できます。
  - ソケット／ファイルフィルタ：socket.state, socket.srcPort/dstPort, socket.family, file.path などで「なぜそのプロセスが存在するか」を探れます。
  - カスタム出力：-o オプションで表示カラムを指定。プリセット（sockets/files/containers/network）も用意。
- 動作環境・ビルド要件
  - Linux カーネル >= 5.8（eBPFイテレータ導入）
  - Go 1.25+, clang/llvm, libbpf 開発ヘッダ、カーネルヘッダ、bpftool（vmlinux.h生成のため）
  - root 権限で eBPF をロードする必要あり（実行時に権限が必要）
- 代表的な使い方（CEL例）
  - nginx を root で実行しているプロセス
    - psc 'process.name == "nginx" && process.user == "root"'
  - 443番ポートに確立済み接続を持つプロセス
    - psc 'socket.state == established && socket.dstPort == uint(443)'
  - コンテナ実行中のプロセスのみ表示
    - psc 'container.id != ""' --tree

## 実践ポイント
- 導入前チェック
  - カーネルバージョン確認:
```bash
uname -r
```
  - bpftool と libbpf のインストール（Debian/Ubuntu例）:
```bash
sudo apt-get install clang llvm libbpf-dev linux-headers-$(uname -r) linux-tools-$(uname -r) bpftool
```
- ビルド手順（概要）
```bash
# vmlinux.h を生成（カーネルごとに一度）
make vmlinux

# ビルド
make build
sudo make install
```
- 運用上の注意
  - root 権限が必要：本番で使う前に非本番環境で動作確認を推奨。
  - eBPFロードはカーネルに影響する可能性があるため監査・ポリシー対応を確認する。
- 実践的な活用案（日本の現場向け）
  - コンテナ大量運用環境で「どのコンテナが外向きに異常な接続を持っているか」を即座に発見し、フォレンジックの初動を短縮。
  - SREがサービス停止原因調査で、/procに頼らず真のプロセス状態を確認。
  - セキュリティ部門がLD_PRELOAD系の隠蔽を疑う際のクロスチェックツールとして併用。
- まず試すコマンド（おすすめ）
```bash
# 全プロセス表示
psc

# リッスンしているTCPソケットを持つプロセス
psc 'socket.type == tcp && socket.state == listen' -o sockets

# Dockerコンテナ内でroot実行しているプロセス
psc 'container.runtime == docker && process.user == "root"' -o process.pid,process.name,container.name
```

ライセンスはMIT。リポジトリでREADMEとビルド手順を確認してから導入すること。
