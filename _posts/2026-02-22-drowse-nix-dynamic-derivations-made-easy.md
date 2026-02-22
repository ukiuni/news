---
layout: post
title: "Drowse: Nix dynamic derivations made easy - Drowse：Nixの動的派生を簡単に"
date: 2026-02-22T15:46:04.778Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/figsoda/drowse"
source_title: "GitHub - figsoda/drowse: Nix dynamic derivations made easy"
source_id: 1324879780
excerpt: "drowseでIFDを使わずcrate2nix連携でNixの評価時間とCIコストを劇的に削減"
image: "https://opengraph.githubassets.com/adabc6021fb233dfd5f92ff577b2d16d7f40f6f2028224085eb2fdde22f4ace5/figsoda/drowse"
---

# Drowse: Nix dynamic derivations made easy - Drowse：Nixの動的派生を簡単に

Nixで「IFDを使わずに細かい依存キャッシュ」を実現するdrowse — crate2nixと組み合わせて評価時間を節約する実践ガイド

## 要約
drowseはNixの実験機能「dynamic derivations」をラップして、IFDやコード生成なしで細粒度キャッシュを実現しつつ、crate2nixなどと連携してmkDerivation風の扱いやすさを提供します。

## この記事を読むべき理由
Nixでの大量依存解決（特にRustのcrate）に悩む日本の開発チームやCI利用者にとって、評価時間短縮とキャッシュ効率向上がそのまま開発速度とCIコスト減に直結します。drowseはその痛点を解消する実用的な選択肢です。

## 詳細解説
- 背景問題
  - crate2nixなどは依存を細かくキャッシュできる利点がある一方で、import-from-derivation（IFD）は評価を逐次化して遅くし、コード生成はGit履歴を汚したり巨大ファイルで再評価を遅くします。
- dynamic derivationsの役割
  - dynamic derivationsは実験的機能で、IFDや生成コードなしにビルド時に派生を動的に生成でき、細粒度キャッシュの利点を維持します。ただしドキュメントが少なく扱いにくい面があります。
- drowseのアプローチ
  - drowseはdynamic derivationsのボイラープレートを削り、以下の主要関数を提供：
    - callPackage: srcの内容をビルド時まで遅延評価し、pkgs.callPackage相当の感覚で使えるラッパー。pname/versionの指定を推奨。
    - crate2nix: crate2nixの応用をIFDなしで行うためのテンプレート／ヘルパー。プロジェクト用テンプレートも提供（nix flake init -t github:figsoda/drowse#crate2nix）。
    - mkDynamicDerivation: より低レイヤで動的派生を作るためのラッパー。
  - 利用には実験フラグが必要：ca-derivations, dynamic-derivations, recursive-nix。
- 実務上の注意
  - dynamic derivationsは実験的で将来の互換性が不確定。CI導入前に小スコープで検証を。
  - srcはfilesetで絞る、もしくはfetchFromGitHubで取得して不要な再評価を避けるのが有効。
  - flakesとの相性が良く、flake入力で簡単に導入できる。

例：flakeでの導入例（最小）
```nix
{
  inputs.drowse.url = "github:figsoda/drowse";
  outputs = { self, drowse, ... }:
    let pkgs = import drowse { }; in
    {
      packages.x86_64-linux.myhello = drowse.lib.x86_64-linux.callPackage {
        pname = "hello";
        version = "2.12.2";
        src = ./hello.nix;
        args.withFoo = true;
      };
    };
}
```

例：crate2nixテンプレート初期化
```bash
nix flake init -t github:figsoda/drowse#crate2nix
```

## 実践ポイント
- まずはローカルで小さなRustプロジェクトにテンプレートを適用して挙動を確認する。
- flakesベースでdrowseをinputsに追加し、ca-derivations/dynamic-derivations/recursive-nixを有効化する。
- srcはfilesetやfetchFromGitHubで絞り、pname/versionを明示して差分追跡を楽にする。
- CIに入れる前にビルド時間・キャッシュヒット率を測定して効果を確認する。
- dynamic derivationsは実験的機能なので、問題が起きたら関連リソース（nix-ninjaやfzakariaのブログ等）で知見を補う。

短くまとめると、drowseはNixでIFDの弊害を避けつつ細粒度キャッシュを活かしたいチームにとって、「試す価値のある」ツールです。
