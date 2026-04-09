---
layout: post
title: "Flatpak: Complete Sandbox Escape - Flatpak: サンドボックス完全脱出"
date: 2026-04-09T04:48:29.720Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/flatpak/flatpak/security/advisories/GHSA-cc2q-qc34-jprg"
source_title: "CVE-2026-34078: Complete sandbox escape leading to host file access and code execution in the host context · Advisory · flatpak/flatpak · GitHub"
source_id: 1359749612
excerpt: "Flatpakの脆弱性でサンドボックスが破られ、ホストが乗っ取られる危険—今すぐ1.16.4へ更新"
image: "https://opengraph.githubassets.com/1c00b6cca3d2857be4fe2933bec8883831fd065592a9613fb26884da0902e5b4/flatpak/flatpak/security/advisories/GHSA-cc2q-qc34-jprg"
---

# Flatpak: Complete Sandbox Escape - Flatpak: サンドボックス完全脱出
Flatpakで“脱出”されると、アプリがホストのファイルを覗き見・改変しホスト上で任意コードを実行できる—今すぐ対処を。

## 要約
Flatpakのポータル機能の不備により、サンドボックス内アプリがホストの任意ファイルにアクセスし、最悪ホスト上でコード実行できるクリティカルな脆弱性（CVE-2026-34078）が見つかりました。影響はFlatpak < 1.16.4で、1.16.4で修正済みです。

## この記事を読むべき理由
Flatpak/Flathubは開発者やデスクトップLinuxで広く使われており、脆弱性が悪用されると個人のホームディレクトリや業務端末が直接危険に晒されます。日本の開発現場や社内PCでも被害につながるため、迅速な対応が必要です。

## 詳細解説
- 問題の本質：Flatpakポータルが受け付ける「sandbox-expose」オプションにアプリ側で制御できるシンボリックリンクを渡せてしまい、そのリンクが指す実際のホストパスをマウントしてしまう。  
- 結果：サンドボックス外のホストファイルが読み書き可能になり、そこからホストコンテキストでのコード実行（例えば置換したバイナリや設定を使った実行）に発展し得る。  
- 影響範囲：Flatpakのバージョンが1.16.4未満のすべてのインストール。パッチは1.16.4で適用済み（次期1.18.0でも修正予定）。  
- 攻撃ベクター理解のポイント（初級者向け）：
  - 通常、Flatpakはアプリを隔離するが、ポータル経由でホストリソースを限定共有する仕組みがある。
  - その共有指定を悪用されると「隔離の穴」ができるとイメージすれば分かりやすい。

## 実践ポイント
- 最優先：Flatpakを1.16.4以上にアップデートする（配布元のパッケージ更新を適用）。
  - Debian/Ubuntu系例:
    ```bash
    # bash
    sudo apt update && sudo apt install --only-upgrade flatpak
    ```
  - Fedora系例:
    ```bash
    # bash
    sudo dnf upgrade flatpak
    ```
- 臨時の緩和策（アプリ互換性が落ちる可能性あり）：
  ```bash
  # bash
  sudo systemctl --global mask flatpak-portal.service && systemctl --user stop flatpak-portal.service
  ```
  - 注意：ポータル無効化で一部Flatpakアプリが正常に動かなくなる可能性がある。
- 現場運用のチェックリスト：
  - イントラや開発マシンでFlatpak利用状況を把握（どのマシンに誰のアプリがあるか）。
  - 信頼できないソースからのFlatpakアプリを削除または審査する。
  - 組織のエンドポイント保護ログで不審なファイルアクセス／プロセス起動を監視。
- 情報源：CVE-2026-34078、Flatpakリポジトリのセキュリティアドバイザリ（修正は1.16.4）。

短時間でできる最優先対応は「配布元の更新を当てる」→「状況に応じてポータルを一時無効化」→「Flatpakアプリの精査」です。
