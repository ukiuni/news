---
  layout: post
  title: "Native Amiga Filesystems on macOS / Linux / Windows with FUSE - macOS/Linux/WindowsでネイティブにAmigaファイルシステムを読む方法"
  date: 2026-01-07T20:43:30.765Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://github.com/reinauer/amifuse"
  source_title: "GitHub - reinauer/amifuse: Native AMIGA filesystems on macOS / Linux / Windows with FUSE"
  source_id: 46473726
  excerpt: "実機用AmigaドライバでHDF/ADFを各OS上で忠実にマウント"
  image: "https://opengraph.githubassets.com/26b588a2a60e1ba32402b28965a158d3b9251beb1cbe3bb186e08202f06c700a/reinauer/amifuse"
---

# Native Amiga Filesystems on macOS / Linux / Windows with FUSE - macOS/Linux/WindowsでネイティブにAmigaファイルシステムを読む方法
魅せるレトロ復元：実機のファイルシステムドライバでAmigaディスクイメージをそのままマウントして中身を覗く

## 要約
amifuseは、実際のAmiga用ファイルシステムドライバ（例：PFS3）をm68kエミュレーション上で動かし、HDF/ADFなどのAmigaディスクイメージをmacOS / Linux / Windows上でネイティブにマウントできるツールです。逆解析実装に頼らず正確に中身を参照できるのが最大の特徴です。

## この記事を読むべき理由
- レトロコンピューティングやデジタルアーカイブに関心がある開発者／保存担当者は、実機互換の方法でディスクイメージから安全にデータを抽出できるため、ツールチェインに加える価値が高いです。  
- 日本でもAmigaのソフト資産やデモシーン資料の復元需要があり、実際のファイルシステム実装を使うamifuseは信頼性と精度で有利です。

## 詳細解説
- 基本概念  
  amifuseはFUSE（macFUSE / FUSE / WinFSP）をバックエンドに、Amiga用のファイルシステムハンドラ（バイナリ）をm68k CPUエミュレータ上で実行します。つまり、PFS3やSFSなど「実機用のドライバ」をそのまま利用してファイルアクセスを提供するため、reverse-engineered な実装より互換性が高く、細かな動作も再現されます。

- 対応環境と要件
  - OS: macOS（macFUSE）、Linux（FUSE）、Windows（WinFSP）  
  - Python 3.9+、7z（イメージ展開用）、および少なくとも1つのファイルシステムハンドラ（例：pfs3aio）  
  - 開発リポジトリはGitHubにあり、サブモジュールを含めてクローンして利用します。

- 主要コマンドと用途
  - amifuse inspect <image> : RDB（Rigid Disk Block）のパーティション/埋め込みドライバ情報を表示  
  - amifuse mount <image> : 指定イメージをFUSE経由でマウント（macOSなら/Volumes、Linuxは明示的なマウントポイントが必要）  
  - rdb-inspect : RDB情報の詳細表示・JSON出力・埋め込みドライバの抽出  
  - driver-info : ファイルシステムハンドラの解析（再配置可能か等の確認）

- イメージ/ファイルシステム対応
  - サポートイメージ: HDF/RDB（RDBにドライバ埋め込み可能）、Emu68風MBR内RDB、ADF（フロッピー・要明示ドライバ）  
  - テスト済みFS: PFS3（pfs3aio）、SFS、FFS/OFS（L:FastFileSystem）、BFFS など。その他のハンドラも動く可能性あり。

- 注意点
  - デフォルトは読み取り専用。書き込みは --write で実験的に有効化（注意して使用）。  
  - マウントはフォアグラウンド動作（Ctrl+Cでアンマウント）。macOSではFinderのインデックスを無効化してパフォーマンス最適化。  
  - macOS限定でAmigaの.infoアイコンをネイティブアイコンに変換する --icons 機能がある（実験的）。

## 実践ポイント
- すぐ試す最短手順（macOS/Linux共通の例）
```bash
# リポジトリをサブモジュールごと取得
git clone --recursive https://github.com/reinauer/amifuse.git
cd amifuse

# 推奨: 仮想環境を作成して依存をインストール
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e ' ./amitools[vamos] '
pip install -e .

# テスト用PFS3イメージとハンドラを取得
make download
make unpack   # pfs.hdf と pfs3aio を用意

# マウント（macOSは /Volumes/<name> に自動マウント）
amifuse mount pfs.hdf

# RDB情報を確認するだけなら
amifuse inspect pfs.hdf
```

- OS固有の注意
  - macOS: macFUSE が必要（Homebrewで brew install --cask macfuse）。セキュリティ許可や再起動が必要な場合あり。--icons はmacOS限定機能。  
  - Linux: fuse と libfuse-dev をパッケージ管理で導入（Debian/Ubuntu: sudo apt install fuse libfuse-dev）。マウントポイントを明示する点に注意。  
  - Windows: WinFSP を事前にインストール。

- 実用的なワークフロー例
  - 保存・検証: rdb-inspect でイメージのRDBと埋め込みドライバを確認→ amifuseで読み取り→必要ファイルを抽出して現代のファイル形式で保存。  
  - エミュレータ連携: エミュレータで使うドライブイメージの中身を直接編集・確認（※書き込みは実験的でリスクあり）。  
  - 展示/アーカイブ: 博物館やコミュニティイベントで、オリジナルのファイル構造を忠実に示す展示資料を作成。

以上を踏まえると、amifuseは「Amiga資産を正しく・安全に読み出す」ための実務的で強力なツールです。レトロ保存やデータ復旧、エミュレータ開発の現場で即戦力になります。興味があればまずは公式リポジトリのREADMEに従って実際にマウントしてみてください。
