---
layout: post
title: "Why I love NixOS - なぜ私はNixOSを愛するのか"
date: 2026-03-22T17:54:46.633Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.birkey.co/2026-03-22-why-i-love-nixos.html"
source_title: "Why I love NixOS"
source_id: 47479751
excerpt: "NixOSで宣言的に再現可能な環境を作り、設定汚染とオンボーディングを劇的に削減"
---

# Why I love NixOS - なぜ私はNixOSを愛するのか
Nixで「再現可能なOS」を作る――面倒な手作業から解放される宣言型ワークフロー

## 要約
NixOSはLinuxディストリビューションというより、Nixパッケージマネージャーが実現する「決定論的で再現可能な宣言型システム」の具現であり、設定の一元管理・安全な実験・容易なロールバックを提供する。

## この記事を読むべき理由
開発環境やCI、デプロイの再現性が重要な日本のエンジニアにとって、Nix/NixOSは環境構築の手間・「環境汚染」を劇的に減らし、マシンの乗り換えやLLM時代の急速なツール変化にも強い解を与えるから。

## 詳細解説
- コアはNix（関数型パッケージマネージャ）：パッケージと設定を宣言的に記述し、Nixが決定論的にビルド・配置する。状態の「塊」を信頼する従来のOS運用と異なり、設定ファイルが唯一の真実（single source of truth）になる。
- 宣言的なOS構築：OS全体（インストールするパッケージ、デスクトップ設定、キーマップ等）を一箇所で定義し、ビルド→再現→ロールバックができるため、長期間の「システムドリフト」が起きにくい。
- 安全な実験と隔離：nix shell / nix developでツールを一時的に取り込み、ベースシステムを汚さずに実験可能。LLMベースのコーディングエージェントとも親和性が高い（必要なツールを宣言して隔離環境で実行）。
- マルチプラットフォーム利点：NixはmacOSやLinux（コミュニティでFreeBSDも）で使えるため、開発ツールセットを横断的に統一できる。
- デプロイとCI：dockerToolsやflakeを使えば決定論的なイメージやビルドを作成でき、ローカルとCI/本番の差を小さくする。
- 安定性と運用性：長年の実装と半年ごとのリリース、安定/unstableチャネルの使い分けで安定運用と実験を両立できる。

短いNix例（設定の雰囲気）:
```nix
# nix
environment.systemPackages = with pkgs; [
  gnomeExtensions.dash-to-dock gnomeExtensions.unite libappindicator
];
services.keyd.enable = true;
```

## 実践ポイント
- まずはローカルでNixを試す：nix run / nix shell / nix developで既存プロジェクトに導入してみる。
- 設定を宣言化：自分の dotfiles や環境設定を段階的にNixに移す（まずはパッケージ一覧→次にサービス）。
- Flakesを使って再現性を高める：flake.nixで依存を固定し、nix flake checkでビルド確認。
- CI/デプロイへの適用：dockerToolsやnixpkgsで決定論的イメージを作り、ビルドの差分を減らす。
- 日本のチームではオンボーディング短縮に有効：新しい開発者は宣言ファイルをcheckoutして同じ環境を即再現可能。

以上。Nix/NixOSは「設定を忘れても再現できる」ことを重視する開発者にとって強力な選択肢である。
