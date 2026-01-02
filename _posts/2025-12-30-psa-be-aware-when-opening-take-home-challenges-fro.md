---
layout: post
title: "PSA: Be aware when opening \"take home challenges\" from untrusted recruiters - 注意喚起: 信頼できないリクルーターからの「持ち帰り課題」を開くときは要注意"
date: 2025-12-30T22:37:54.609Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://bitbucket.org/brain0xlab/challenge/src/master/"
source_title: "PSA: Be aware when opening \"take home challenges\" from untrusted recruiters"
source_id: 434201801
excerpt: "リクルーター経由の持ち帰り課題はマルウェアや資格情報窃取の罠かも、隔離環境で必ず検査を"
---

# PSA: Be aware when opening "take home challenges" from untrusted recruiters - 注意喚起: 信頼できないリクルーターからの「持ち帰り課題」を開くときは要注意
面接用の「持ち帰り課題」が実は罠？リンク先が404やCAPTCHAでも油断禁物、まずは安全確認を。

## 要約
リクルーター経由のリポジトリや課題ファイルを無検査で開くと、マルウェアや情報漏えいのリスクがある。404やCAPTCHAの表示も安全とは限らないため、まずはローカルで実行せずに検査・サンドボックス実行を行うべき、という注意喚起。

## この記事を読むべき理由
日本でもオンライン面接やリモート採用が増え、外部から送られる「持ち帰り課題」を扱う機会が増えています。採用熱の中で軽率にファイルを実行すると、開発マシンや社内ネットワークが攻撃される可能性があるため、現場で役立つ実践的な対処法を知っておく必要があります。

## 詳細解説
元情報はBitbucketのリポジトリURLが404を返している例です。一見「存在しないだけ」に見えますが、攻撃者は以下のような手口で候補者を誘導することがあります。

- リポジトリに含まれるスクリプト（install.sh、setup.py、package.jsonのpostinstall等）に後処理を仕込み、実行時に外部サーバへ接続して悪意あるペイロードを取得する。
- DockerfileやCI設定（.travis.yml、bitbucket-pipelines.yml、azure-pipelines.yml）にコマンドを書き込み、テスト実行時にネットワーク経由で悪性コードを投入する。
- アーカイブ内にバイナリや実行ファイルを含め、ユーザーが「テストを実行」した瞬間に権限昇格や情報抜き取りを行う。
- .gitmodulesやサブモジュールで外部リポジトリを参照させ、クローン時に攻撃を組み込む。
- 404やCAPTCHAは「消した／非公開にした」行為の後処理で、痕跡を消すために用いられることもある。つまり一度ダウンロードやアクセスした痕跡が残らないようにするための挙動である可能性がある。

技術的に危険なのは「信頼できないソースから入手したコードを、そのまま自分の開発マシンで実行する」ことです。特にローカル環境でテストを走らせると、環境変数やSSHエージェント、資格情報がアクセスされる危険があります。

## 実践ポイント
- 実行は絶対にしない：まずREADMEやpackage.jsonなどを「読む」だけにする。
- ネットワーク遮断のサンドボックスで動かす：例えば隔離されたVMや一時的コンテナで、かつ--network=none等でネットワークを切って実行する。
  - 例（確認用）:
    ```bash
    # ダウンロードして中身を調べる
    curl -I https://bitbucket.org/brain0xlab/challenge/src/master/

    # 安全に確認するための例: ネットワーク無効でコンテナ内を使う
    docker run --rm -it --network none -v "$(pwd):/workspace:ro" ubuntu:24.04 bash
    ```
- スクリプトの自動実行に注意：npm/yarnのpostinstall、pipのsetup.py、Makefile、CI設定を最初に開いて確認する。
- 固有ファイルを検索：Dockerfile、*.sh、package.json、setup.py、.travis.yml、bitbucket-pipelines.yml、.gitmodules などをチェックする。
- ファイル実行は最小権限で：必要なら専用のQEMU/VM/クラウドの使い捨て環境を使い、ホストの資格情報やマウントを避ける。
- 静的解析を活用：bandit（Python）、npm audit、cargo-auditなどでまずスキャンする。
- 身元確認：送付元のリクルーターや企業の公式ドメイン、LinkedIn等での確認、求人の正式な掲示と照合する。
- 疑わしければ断る／企業に確認：正規の採用プロセスであれば別の渡し方（スクリーン共有、オンラインIDE、公式レポジトリ）を提案してくれるはずです。

