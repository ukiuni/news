---
layout: post
title: "Show HN: difi – A Git diff TUI with Neovim integration (written in Go) - difi — Neovim連携のGit差分TUI（Go製）"
date: 2026-02-03T15:18:49.571Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/oug-t/difi"
source_title: "GitHub - oug-t/difi: Review and refine Git diffs before you push"
source_id: 46870917
excerpt: "Neovim連携で差分を即編集、キーボードで高速確認できるGit差分TUI"
image: "https://opengraph.githubassets.com/f8b0d9ba8ac7de816cf2f411d18633e8df5016063cb7a900ba9ea21b0387b21c/oug-t/difi"
---

# Show HN: difi – A Git diff TUI with Neovim integration (written in Go) - difi — Neovim連携のGit差分TUI（Go製）

プッシュ前に差分を最速で「見て直す」――Neovimと直結する軽量Git差分TUI

## 要約
Goで書かれた軽量なターミナルUIツール「difi」は、ファイルツリー＋フォーカスされた差分表示で素早く差分を確認し、eキーでNeovim/Vimの該当行へジャンプして即修正できます。

## この記事を読むべき理由
日本でもNeovim/Vimを使うエンジニアは多く、プッシュ前の差分確認を軽量かつキーボード中心に行えるツールは日々の開発効率やレビュー品質向上に直結します。CI前の最終チェックやローカルでの素早い修正に最適です。

## 詳細解説
- 実装・特徴
  - Go製で起動が速くデーモンやインデックス不要。軽量で即時表示。
  - 左にファイルツリー、右に差分を並べて表示する「構造化された」UIで視認性が高い。
  - 完全キーボード操作（h/j/k/lなど）を想定。マウス不要。
- エディタ連携
  - e / Enterで選択行をエディタで開き、Neovim/Vimへ正確にジャンプ。
  - 専用プラグイン difi.nvim を使うと、CLIからNeovimへ自動ジャンプ、差分のインライン表示（GitHub風の色分け）、差分を対話的に復元／破棄できる機能が使える。
- ワークフロー
  - デフォルトでカレントブランチと main を比較。リポジトリ内で difi を実行するだけで開始。
  - インストールは Homebrew / go install / バイナリのいずれか。
- 開発状況
  - MITライセンス、OSSで活発に改良中。Windows対応やUI改善などコントリビュート歓迎。

## 実践ポイント
- インストール例（macOS/Linux）
  - brew tap oug-t/difi && brew install difi
  - あるいは: go install github.com/oug-t/difi/cmd/difi@latest
- すぐ使う
  - cd your-repo && difi
  - hjklで移動、eでNeovimへジャンプして修正、qで終了。
- 効果的な運用
  - pre-pushフックやローカルチェックリストに difi を組み込み、プッシュ前レビューの習慣化。
  - Neovimユーザーは difi.nvim を導入してCLI ⇄ エディタをシームレスに連携させるとさらに効率化。

元リポジトリ: https://github.com/oug-t/difi
