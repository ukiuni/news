---
layout: post
title: "typenix: Full typing for Nix based on TypeScript - typenix: TypeScriptベースでNixに完全な型付け"
date: 2026-03-17T02:28:04.115Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/ryanrasti/typenix"
source_title: "GitHub - ryanrasti/typenix: Full typing for Nix based on TypeScript · GitHub"
source_id: 1264273229
excerpt: "TypeNixで.nixにTypeScript型を導入し補完・型検査・定義移動を実現"
image: "https://opengraph.githubassets.com/c8d073ec7bc8ccca8e8422efeec508c50e09bc76ff0d56e373da84e11b8d3581/ryanrasti/typenix"
---

# typenix: Full typing for Nix based on TypeScript - typenix: TypeScriptベースでNixに完全な型付け
Nixの世界をTypeScriptの型システムで“型付け”してエディタ体験を劇的に向上させるTypeNix

## 要約
TypeNixは、.nixファイルをTree‑sitterで解析してTypeScriptのASTに変換し、TypeScriptのバインダー／チェッカー／LSPを流用してNixにフル型付け（補完・型エラー・ホバー・定義へ移動）を提供する実証プロジェクトです。

## この記事を読むべき理由
Nixは依存管理と再現可能性で注目される一方、言語ツールの不足が普及の障壁になっています。TypeNixはエディタ体験を改善して学習コストを下げ、日本の開発チームがNix採用を検討する際の導入障壁を下げます。

## 詳細解説
- アーキテクチャ：.nix → tree-sitter-nixでパース → TypeScriptのASTノードに変換 → TSのbinder/checker/LSPを利用。つまり「同じ型システム、同じパイプライン」をNixに適用します。  
- 特殊対応：固定点（fixed-point）やoverrideの自己参照パターンをTypeScriptのクラスに変換して自己参照型を実現。既存のlib型注釈（nixpkgsの型情報）も読み取り利用可能。  
- 提供機能：補完・ホバーでの型表示、型エラー検出、go-to-definition、.nixからの参照追跡。VSCode拡張、Neovim用LSP設定、CLI（nix run）あり。  
- 型注釈：ファイル内で `# @ts:` コメントを使いTypeScript風の型を付与可能（例：LibやStdenv等が使える）。  
- パフォーマンス実績：nixpkgs約42kファイルを13秒で解析・型チェックした実績あり（proof‑of‑conceptとして）。  
- 現状の制約：まだPoC段階で多くをanyで扱う箇所がある（noImplicitAny: falseで一部抑制）。細かいパッケージ型や自動生成エントリは更なる明示的注釈が必要。貢献歓迎。

簡単な型注釈例：
```nix
# @ts: { lib: Lib; stdenv: Stdenv; [key: string]: any }
{ lib, stdenv }:
let
  version = lib.concatStringsSep "." [ "1" "0" "0" ];
  isLinux = stdenv.hostPlatform.isLinux;
in stdenv.mkDerivation { inherit version; src = ./.; }
```

## 日本市場との関連
- 日本のSRE／インフラチームでNixを採用する際、エディタの型支援はオンボーディングの差を生みます。TypeNixは社内テンプレやflake運用の安全性向上、レビュー効率化に寄与します。  
- VSCode／Neovim利用者が多い日本でも導入しやすく、既存ワークフローへの適合が比較的容易です。

## 実践ポイント
- とりあえず試す：プロジェクトルートに簡易tsconfigを置き、CLIで型チェックを試す。
```bash
echo '{"include": ["**/*.nix"]}' > tsconfig.json
nix run github:ryanrasti/typenix -- --noEmit
```
- エディタ導入：VSCode拡張やNeovimのLSP設定を使って補完／ホバーを有効化する。  
- まずは重要なモジュールに `# @ts:` で型注釈を追加して、型の恩恵を少しずつ得る。  
- 貢献：型を増やすPRや、pkgs/by-nameの細かい型付けはプロジェクトに貢献しやすい領域。

興味があれば公式リポジトリ（GitHub: ryanrasti/typenix）のexamples/starterを起点に試すのが最速です。
