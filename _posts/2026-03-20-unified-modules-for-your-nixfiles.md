---
layout: post
title: "[Unified Modules For Your Nixfiles] - [Nixfilesのための統一モジュール]"
date: 2026-03-20T14:04:39.556Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://jadarma.github.io/blog/posts/2026/03/unified-modules-for-your-nixfiles/"
source_title: "Unified Modules For Your Nixfiles | Jadarma's Blog"
source_id: 788064385
excerpt: "機能単位モジュールでmacOS/NixOSのdotfilesを一元管理しimport忘れを防ぐ"
image: "https://jadarma.github.io/blog/posts/2026/03/unified-modules-for-your-nixfiles/thumb.webp"
---

# [Unified Modules For Your Nixfiles] - [Nixfilesのための統一モジュール]
Nixで「機能単位」のモジュール設計に変えるだけで、dotfiles管理が驚くほどシンプルに — macOS/NixOS/複数ホストを一元管理する実践メソッド

## 要約
機能（feature）単位でモジュールをまとめ、common/darwin/nixos/homeの役割を分離して自動インポートすることで、Nix/NixOS/nix-darwin/Home Managerを横断するdotfiles管理を堅牢かつ見通し良くする手法の紹介。

## この記事を読むべき理由
- macOSとNixOSを混在させた環境や複数ホストを扱う日本の開発者にとって、従来の「型別（home/nixos/darwin）分割」は管理負担とミスを生む。  
- これを機能単位に整理すると、参照性／再利用性が高まり、チーム共有や将来の拡張が楽になる。

## 詳細解説
問題意識
- よくあるテンプレはモジュールを「home」「nixos」「darwin」で分けるため、同一機能の断片がツリー上で離れてしまい参照や同期が面倒になる。
方針
- 各機能フォルダを feature 単位で作り、最大で4ファイルを置く:
  - common.nix：全プラットフォーム共通のオプション宣言やドキュメント
  - nixos.nix：NixOS専用設定
  - darwin.nix：macOS（nix-darwin）専用設定
  - home.nix：Home Manager 用（全環境で読み込む）
ディレクション
- common.nixでオプションを定義し、home.nixはシステム設定（osConfig）を参照してHMの設定を組み立てる。これにより「どのモジュールが何を有効にするか」を一箇所で把握できる。
自動インポート
- 命名規約を使い、mainモジュールから再帰的に該当ファイルを列挙してインポートすることで、人為的なimport忘れを防ぐ。
例（概念的に短縮）:
```nix
# nix
imports = lib.pipe ./. [
  (lib.filesystem.listFilesRecursive ./.)
  (lib.lists.filter (lib.strings.hasSuffix "nixos.nix"))
  (lib.lists.filter (path: path != ./nixos.nix))
];
```
プラットフォーム差分の扱い
- 小さな差分なら stdenv.hostPlatform を使った条件式（lib.mkIf や if）で分岐。複数差分は小さな onDarwin/onLinux のattrsetを作り lib.mkMerge で統合する。
注意点（重要）
- Nixのモジュールシステムでは「オプション定義」が存在しないとエラーになる場合があるため、システム専用のオプションは system-specific ファイルに分けるのが安全。commonに定義しておいて、プラットフォームで使えないときは assertions で明示的にエラー化する手法が有効。
例（assertion）:
```nix
# nix
config = lib.mkIf config.nixfiles.programs.steam.enable {
  assertions = [ {
    assertion = pkgs.stdenv.hostPlatform.isLinux;
    message = "SteamはLinuxのみ設定されています。";
  } ];
};
```
設計方針のメリット
- リポジトリを機能単位で俯瞰できるため、新規機能追加やリファクタが容易。外部のスクリプトや追加ツールに依存せず、純粋にnixの標準ツールだけで完結するため保守性が高い。

## 実践ポイント
1. リポジトリを機能単位に再編成（modules/<feature>/{common.nix,home.nix,nixos.nix,darwin.nix}）する。  
2. common.nixでオプション宣言を行い、ユーザー名など共通設定は top-level の osConfig で参照する。  
3. 再帰的自動インポートを実装してimport忘れを無くす（lib.filesystem.listFilesRecursive + lib.pipe）。  
4. 小差分は stdenv.hostPlatform で分岐、複雑差分は onDarwin/onLinux を mkMerge で結合。  
5. プラットフォーム専用機能は assertions で誤設定を早期検出する。  
6. まずは1〜2機能（例：git, gpg）で試して、運用ルールをチームで固める。

この手法は、日本でマシンが macOS と NixOS を併用する個人開発者や小規模チームに特に効く実践的な改善策です。
