---
layout: post
title: "Nix security advisory: Privilege escalation via symlink following during FOD output registration - Nix セキュリティ勧告：FOD（固定出力導出）出力登録時のシンボリックリンク追従による権限昇格"
date: 2026-04-08T00:27:40.211Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://discourse.nixos.org/t/nix-security-advisory-privilege-escalation-via-symlink-following-during-fod-output-registration/76900"
source_title: "Nix security advisory: Privilege escalation via symlink following during FOD output registration - Security - NixOS Discourse"
source_id: 1090020188
excerpt: "NixのFOD登録でシンボリックリンク追従によりroot奪取可能、即時対策を"
image: "https://discourse.nixos.org/uploads/default/original/3X/a/5/a5e0d7873e3d34aecf874c577c91a1c06490f436.svg"
---

# Nix security advisory: Privilege escalation via symlink following during FOD output registration - Nix セキュリティ勧告：FOD（固定出力導出）出力登録時のシンボリックリンク追従による権限昇格
Nixでroot権限による任意ファイル上書きが可能に——まず確認して直すべき安全対策

## 要約
Nixデーモンにある脆弱性（CVE-2026-39860）により、ビルドを送信できるユーザーがデーモン権限（NixOSやマルチユーザ環境ではroot）で任意ファイルを書き換え、権限昇格できる可能性があります。影響するバージョンとパッチが公表されています。

## この記事を読むべき理由
Nix/NixOSをCIや社内ビルドで使っていると、悪用されればビルド環境やビルドサーバ（例：Hydra）をroot権限で乗っ取られる危険があります。日本でもNixを採用するプロジェクト・サービスが増えており、速やかな対応が必要です。

## 詳細解説
- 何が起きるか：Nixの「固定出力導出（FOD）」の出力を登録する際、漏れたファイル記述子（FD）やシンボリックリンクの扱いを突くことで、登録済みのストアパスを書き換えられる（結果として任意ファイル上書き）。この操作はデーモン権限で行われるためroot権限取得につながる。
- 影響範囲：Nix 2.21以降（特定の古いパッチ版を含む）で、該当の修正が当たっていないバージョンが影響。サンドボックス化されたLinux構成が対象で、サンドボックス化されたmacOSは影響を受けないと報告されています。Lixは別の対処経路を取っていたため影響外。
- 原因の背景：以前のCVE（CVE-2024-27297）対策の実装差分で生じた副作用に起因。固定出力導出同士の間でファイル記述子やUNIXドメインソケットを介した通信が可能になり、それが攻撃に使われた。
- 修正方針：出力を登録する前にコピーする（漏れたFDを含まない安全なコピーを登録する）等の対策が導入され、2.34.5, 2.33.4, 2.32.7, 2.31.4, 2.30.4, 2.29.3, 2.28.6などで修正済み。nixpkgs側にもパッチが組み込まれています。

## 実践ポイント
- まずバージョン確認：Nixのバージョンを確認し、上記修正済みバージョンへ速やかにアップデートする。  
- 対応が難しい場合：allowed-users を厳格化し、信頼できないユーザーにビルド受付を許可しない。CIでの外部プルリクのビルド方針を見直す。  
- CI/Hydra環境：公開ビルドサービスやHydraビルダーを使用している場合は、当該ホストのアップデートまたは一時的に別実装（例：Lix）に切り替える検討を。  
- 監査と対応：ビルドログ／ストアの不審な変更や新規登録パスの差分を確認し、必要ならば秘密情報や鍵のローテーションも。  
- 情報ソースの追跡：nixpkgsのPRやNixOSディスコースでパッチ状況を確認し、適用状況を追う。

短時間で対応可能なものは「Nixのアップデート」→「allowed-users の見直し」です。まずバージョン確認を。
