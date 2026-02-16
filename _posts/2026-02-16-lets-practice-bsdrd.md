---
layout: post
title: "Let's practice! (bsd.rd) - bsd.rd を分解して学ぶ"
date: 2026-02-16T22:41:45.757Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://openbsdjumpstart.org/bsd.rd/"
source_title: "OpenBSD Jumpstart | bsd.rd"
source_id: 930304861
excerpt: "再起動不要でbsd.rdを分解・改変し社内署名付きインストーラを作る手順を15分で解説"
---

# Let's practice! (bsd.rd) - bsd.rd を分解して学ぶ
bsd.rdの中身を15分で丸裸にする — 再起動不要でインストーラをカスタマイズする方法

## 要約
OpenBSDのブートイメージbsd.rdは、gzip→ELF（カーネル）→埋め込みRAMディスク（miniroot）という多層構造になっており、稼働中のシステム上で再起動せずに中身を取り出して調べたり書き換えたりできます。

## この記事を読むべき理由
日本の現場でも、ネットワークインストール、自動化（autoinstall）、カスタムインストーラ作成や検証が必要になる場面が増えています。bsd.rdを理解すれば、オフラインでのリカバリメディア作成や、社内用に署名・設定済みのインストーラを配布することが現実的になります。

## 詳細解説
手順は大きく分けて以下の流れです（manページ群 rd(4) → rdsetroot(8) → vnconfig(8) → vnd(4) を辿るのが近道）。

1. bsd.rdはgzip圧縮ファイルなのでコピーして拡張子を変え、gunzipで展開するとELF形式のカーネルになります。readelfでヘッダを見れば通常のカーネルと同様に扱えます。

2. rdsetroot -s で埋め込みRAMディスクのサイズ（バイト）を確認できます。カーネルはRAMDISKオプションであらかじめ領域を確保しており、rdドライバがブロックデバイスとして起動時に割り当てます。

3. rdsetroot -x で埋め込みのdisk.fs（miniroot）を抽出すると、FFSファイルシステムのイメージファイルになります。vnconfigでvndデバイスに割り当て、disklabelでパーティションを確認してマウントすれば中身を覗けます。

主なコマンド例:
```bash
# 作業ディレクトリ作成・コピー
mkdir -p /tmp/lab && cd /tmp/lab
cp /bsd.rd bsd.rd.gz
file bsd.rd.gz
gunzip bsd.rd.gz
readelf -h bsd.rd

# 埋め込みRAMディスク情報取得・抽出
rdsetroot -s bsd.rd
rdsetroot -x bsd.rd miniroot.fs
file miniroot.fs

# vnd に割当ててマウント
vnconfig vnd0 miniroot.fs
disklabel vnd0
mount -r /dev/vnd0a /mnt
ls -l /mnt
```

minirootの中身は非常に最小限で、install.sub（インストール/アップグレード/自動インストールを司るkshスクリプト）、最小限のbin/sbin、signify公開鍵やCA証明書があり、信頼チェーンとインストールに必要なツールだけが揃っています。

変更を加えて再組み込みする手順（安全に行うならVMで検証すること）:
```bash
vnconfig vnd0 miniroot.fs
mount /dev/vnd0a /mnt       # read-writeで編集
# 変更を加える（例）
echo "custom" > /mnt/custom.txt
umount /mnt
vnconfig -u vnd0
rdsetroot bsd.rd miniroot.fs
gzip -c9n bsd.rd > bsd.rd.new
```

最後に必ず umount /mnt と vnconfig -u vnd0 でクリーンアップします。

## 実践ポイント
- 作業は必ずrootで／一時ディレクトリで行い、元のbsd.rdはバックアップしておく。  
- 編集後は仮想環境で起動テストしてから実機へ適用する。  
- autoinstallやPXEで使う設定や日本ローカルのミラーURL、ロケールをminirootに組み込み、社内用カスタムイメージを作ると運用が楽になる。  
- signify公開鍵とssl/CAがminiroot内にあるので、配布するイメージの取得先と署名ポリシーを明確にして信頼を確保する。  
- manページ（rd(4), rdsetroot(8), vnconfig(8), vnd(4), disklabel(8), elf(5)）を順に読むと理解が深まる。

以上を踏まえれば、bsd.rdは「壊れたシステムの救出」だけでなく「自分仕様のインストーラ作成」や「セキュアな導入ワークフロー構築」に強力に役立ちます。
