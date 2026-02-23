---
layout: post
title: "Tracking NixOS option values and dependencies - NixOSのオプション値と依存関係の追跡"
date: 2026-02-23T21:37:24.641Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://oddlama.org/blog/tracking-options-in-nixos/"
source_title: "Tracking NixOS option values and dependencies | oddlama's blog"
source_id: 1378817081
excerpt: "Nix評価を追跡しNixOS設定の依存と影響範囲を可視化、更新前に壊れる箇所を特定"
---

# Tracking NixOS option values and dependencies - NixOSのオプション値と依存関係の追跡
「どの設定が本当に効いているか？」NixOS設定の“影響範囲”を可視化して安全に更新する方法

## 要約
Nixの評価器にアクセス追跡を入れて、NixOSモジュール評価時にどのオプションがどれに依存しているかを記録できるようにした話。これにより設定レベルでの差分比較や「system.stateVersionを上げると何が壊れるか」の可視化が可能になる。

## この記事を読むべき理由
NixOSはオプションが膨大で、見た目の少数の設定が実は多数に波及することがある。日本でも自己管理サーバーやCIでNixを使う場面が増えており、アップデートやマイグレーションの安全確認に直結する実用的な技術だから。

## 詳細解説
- 問題点：NixOSはモジュール経由のfixpoint評価で最終設定を作るため、実際にどのオプションが最終結果に寄与しているかがわかりにくい。nix-diffは派生物やビルド差分を見せてくれるが、設定レベルの「意味的」な差分は別の話。
- 解法（要点）：
  - Nix評価器に小さな追跡プリミティブを追加し、「どの文脈で（どのサンクが）」評価されたかを記録するようにした。評価の振る舞い自体は変えず観測のみ行う。
  - NixOSモジュールシステムにフックを入れ、lib.nixosSystemで trackDependencies = true を渡すだけで追跡を有効化できる（ただし追跡対応のパッチ入りnix/nixpkgsが必要）。
  - 評価で使われた値の一覧と依存エッジを tracking-deps.json / tracking.json / tracking-explicit.json として出力し、これを解析するユーティリティ nixos-config（TUI）で探索・差分表示ができる。
- 効果：
  - あるオプションがシステムのどこに使われているか（逆方向依存）を即座に確認可能。
  - 2つの構成を比較して「設定レベルで何が変わったか」を分かりやすく表示（デフォルト値を除外する explicit モードもあり）。
- 実装上の工夫：全操作を丸追跡すると爆発的に遅くなるため、どこを観測するかを絞り、評価性能への影響を抑える工夫が入っている。過去に試した全評価トレースは遅すぎて実用にならなかった。

例：lib.nixosSystemにフラグを渡す（flake内の簡易例）
```nix
{
  nixosConfigurations.host1 = nixpkgs.lib.nixosSystem {
    system = "x86_64-linux";
    trackDependencies = true;
    modules = [ ./configuration.nix ];
  };
}
```

## 実践ポイント
- 試す手順（概要）
  1. oddlamaのフォークからパッチ入りnixとnixpkgsを使うシェルを起動（nix shell github:oddlama/nix/... github:oddlama/nixpkgs/...#nixos-config）。
  2. lib.nixosSystemで trackDependencies = true を設定し、追跡付きと同様に toplevel をビルド（少し評価時間が増える）。
  3. 出力された toplevel のパスに対して nixos-config show / diff / text-diff を実行して依存グラフや差分を確認。
- 使いどころ：system.stateVersionの影響確認、サービス追加で何が有効化されるかの事前解析、アップデート前の安全性チェック。
- 注意点：現時点はパッチ入りのnix/nixpkgsが必要。追跡は評価対象に限定されるため「参照されなかったオプション」はレポートに出ない（＝実害のない未使用設定は無視される）。

元記事の実装・リポジトリ（nixos-config / thunk-origins）を参照すると、より詳細な導入手順やグラフ出力の例が得られます。
