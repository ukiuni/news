---
layout: post
title: "ajail: a basic jail for programs you don't completely trust - ajail：完全には信用しないプログラム向けのシンプルなサンドボックス"
date: 2026-02-21T14:14:57.819Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/jtolio/ajail"
source_title: "GitHub - jtolio/ajail: a basic jail for programs you don&#39;t completely trust"
source_id: 936688989
excerpt: "300行で作れる読み取り専用ルートと一時オーバーレイで未検証コードを安全に試せる軽量サンドボックス"
image: "https://opengraph.githubassets.com/9005030cddddf31ab0f2f8d9df8107ef107d396ad92f22f30ab32230b977092f/jtolio/ajail"
---

# ajail: a basic jail for programs you don't completely trust - ajail：完全には信用しないプログラム向けのシンプルなサンドボックス
ローカルで安全に「試す・壊す・リセット」できる――300行ほどのシンプルなサンドボックス、ajailの魅力と使いどころ

## 要約
ajailはbubblewrapをラップした軽量な「chroot＋名前空間」ベースのサンドボックス。読み取り専用のルートFS＋一時的なオーバーレイで、パッケージやホームの変更をセッション単位で消せます。

## この記事を読むべき理由
ローカルで外部コード（例：未検証のAIエージェント、サードパーティスクリプト）を安全に実験したい日本の開発者や研究者にとって、手早く監査できて導入コストの低い選択肢だからです。

## 詳細解説
- アーキテクチャ：ajailはbubblewrapで囲ったchroot環境。Immutableなルートファイルシステムを ~/.ajail/fs/<name> に置き、ルートは読み取り専用でマウント、必要に応じて一時的な書き込みオーバーレイを重ねる。
- UID/GIDマッピング：外からのUIDをコンテナ内でrootとして見せる（ユーザー名前空間ではなくUIDだけマップ）。内部はrootに見えるが、実際の権限はホストのUIDに従います。
- 永続化と一時化：
  - --fs-edit：ルートFSへの変更を永続化
  - --home-edit：jail内の /root（＝外からの $HOME 相当）変更を永続化
  - --ro / --rw：現在ディレクトリやサブディレクトリを一時化または永続化してマウント
  - --hide：指定ディレクトリを空に見せる（例：.git を隠す）
  - --clone：カレントがGitリポジトリならクローンを作ってマウント（複数エージェント並行実行に便利）
- ネットワーク：--no-net でネットワークを無効化可能。リモート接続は範囲外だが、singleuser-sshdをjail内で動かしTailnet等を使う運用は可能。
- 環境変数：AJAIL_ARGSでデフォルト引数、AJAIL_ENV_*でjail内に持ち込みたい環境変数を指定可能（direnvと相性良し）。
- 付属ツール：mkfs/* スクリプトで Alpine・Arch・Debian・Ubuntu・Nix・Void・Wolfi 等のrootfsを作成。例：sudo ./mkfs/debian.sh -u $(whoami) ~/.ajail/fs/deb -p vim,build-essential
- 要件：Linuxカーネル >= 6.2（overlayfs in user namespaces）、Python >= 3.9、bubblewrap >= 0.11、debootstrap（Debian/Ubuntu 用 mkfs）。

## 実践ポイント
- まずは環境準備：bubblewrap をインストール、mkfs で好みの rootfs を作成。
  - 例: sudo ./mkfs/wolfi.sh -u $(whoami) ~/.ajail/fs/default -p build-base,go,python3
- 試す：カレントを書き込み可でシェル起動
  - ajail sh
- 一時化したいとき：.git を外に残したくない場合
  - ajail --ro=.git sh
- 永続化したいパッケージや設定は --fs-edit / --home-edit を使う
  - ajail --fs-edit apt install vim
- LLMやCIで複数インスタンスを走らせるなら --clone を検討（並列で別々の作業ツリーを渡せる）
- デフォルト動作をディレクトリ単位で変えたいときは AJAIL_ARGS を direnv 等で運用

短くまとめると、ajailは「小さくて目で追える」サンドボックス。初学者でも挙動を理解しやすく、ローカルで安全に実験するワークフローにすぐ組み込めます。
