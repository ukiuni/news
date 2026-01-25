---
layout: post
title: "Software patches in NixOS for fun and productivity - NixOSでパッチを楽しむ・生産性を上げる方法"
date: 2026-01-25T16:45:31.278Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://log.pfad.fr/2026/software-patching-in-nixos/"
source_title: "Software patches in NixOS for fun and productivity"
source_id: 1589849465
excerpt: "NixOSでローカルパッチを自動再適用して、PR待ち不要で即座に環境やレトロ機器対応を実現"
---

# Software patches in NixOS for fun and productivity - NixOSでパッチを楽しむ・生産性を上げる方法
NixOSならではの「ローカルパッチ運用術」で、手元の環境を即座に安全にカスタマイズする方法

## 要約
NixOSではパッケージにローカルパッチを組み込み、アップデート時に自動で再適用させられるため、 upstream のリリース待ちに悩まされずに自分の修正を安全に使い続けられる。

## この記事を読むべき理由
日本でも OSS の修正がリリースされるまで時間がかかったり、レトロ機器対応や個人的なカスタムが必要な場面が多い。NixOS の仕組みを使えば、そうした「一時的だが大事な修正」をシステマティックに管理できるからだ。

## 詳細解説
- 基本概念：Nix のパッケージ定義を override して、patch ファイルやビルドフラグを差し込み、結果のビルドを常に自分の設定経由で行う。これによりアップグレード時も patch が再適用される。
- 実例（要点）
  - Lazygit のパッチ適用：PR を待たずに `overrideAttrs` で patches 配列にローカルパッチを入れて即利用。PR が後でマージされると、将来的にパッチが適合しなくなってビルドが失敗するが、そのときに通知を得て取り除けば安全。
  - Strawberry（iPod）の依存復活：パッケージメンテナが libgpod を外したが自分の用途では必要。`overrideAttrs` で `buildInputs` に戻し、`cmakeFlags` を修正してビルド可能にする。
  - 自作ウィンドウマネージャ（niri）の遊びパッチ：小さな Rust パッチを当て、同様に Nix 設定で管理。機能が不適切なら upstream に戻すか削除する。
- メリットと安全性：ビルド失敗は「壊れたシステム」ではなく「パッチ再適用失敗」として検出される。パッチ適用中も新バージョンは取り込め、不要になれば設定から削除するだけで元に戻る。

## 実践ポイント
- パッチ生成：`git format-patch origin/main` か PR の `.patch` URL を保存する。
- Nix 設定例（抜粋）：
```nix
{ pkgs, ... }:
{
  programs.lazygit = let
    patchedPackage = pkgs.lazygit.overrideAttrs (final: prev: {
      patches = [ ./patches/lazygit-4018.patch ];
    });
  in {
    enable = true;
    package = patchedPackage;
  };
}
```
- ワークフロー：
  1. まず upstream に PR を出す（可能な限り）。
  2. 同時にローカルで patch を config リポジトリに置き `overrideAttrs` で適用。
  3. CI でパッケージビルドをチェックして破壊的変更を早期発見。
  4. PR がマージ・リリースされたら設定からパッチを削除して様子を見る。
- ベストプラクティス：パッチは小さく、コメントや PR リンクを残す。長期的な分岐は避け、 upstream 取り込みを目標にする。

この手法は、リリース待ちで作業が止まる日本の現場やレトロハード対応などに即効性のある実用技術になる。
