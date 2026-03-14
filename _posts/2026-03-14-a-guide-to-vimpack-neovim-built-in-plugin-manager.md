---
layout: post
title: "A Guide to vim.pack (Neovim built-in plugin manager) - vim.packガイド（Neovim組み込みプラグインマネージャ）"
date: 2026-03-14T14:22:55.460Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://echasnovski.com/blog/2026-03-13-a-guide-to-vim-pack"
source_title: "A Guide to vim.pack (Neovim built-in plugin manager) – Evgeni Chasnovski"
source_id: 927463096
excerpt: "Neovim 0.12のvim.packで設定だけでプラグイン管理を自動化"
image: "https://echasnovski.com/assets/EC2-social.png"
---

# A Guide to vim.pack (Neovim built-in plugin manager) - vim.packガイド（Neovim組み込みプラグインマネージャ）

Neovim 0.12で使える新しい標準機能を、初心者にもわかりやすく：vim.packでプラグイン管理を「設定ファイルで完結」させる方法

## 要約
Neovim 0.12で導入される組み込みプラグインマネージャvim.packは、Luaで書かれた関数群でプラグインのインストール・読み込み・更新・ロックを一元管理し、設定ファイル（init.lua）をプラグインの「設計図」にします。

## この記事を読むべき理由
日本でもNeovimは開発環境の中心になるケースが増えています。会社PC⇄自宅PC⇄WSLのように複数環境で同じ設定を使う場面で、vim.packはプラグインの初回導入や再現性（bootstrap）を非常に楽にしてくれます。

## 詳細解説
- 基本設計：vim.packはLuaモジュールで、主に vim.pack.add() を使ってプラグインを「宣言的に」追加します。add()は足りないものを自動インストールし、そのセッションで即ロードします。
- ランタイムとpack構成：Neovimは runtimepath を検索して lua/, plugin/, ftplugin/ 等を読み込みます。プラグインは pack/<package>/{start,opt} 構造で配置され、startは起動時自動読み込み、optは :packadd で遅延読み込みされます。vim.packはインストール時にcoreパッケージのoptに置く運用を前提とします（設定ファイルでオンオフを管理するため）。
- 仕様（Specification）：プラグイン指定は文字列（ソースURL）かテーブルで可能。テーブルで name, version, data 等を指定できます。versionには semver 系の指定が使え、vim.version.range() が利用可能です。
- ロックファイル：nvim-pack-lock.json がユーザーの設定ディレクトリに作られ、各プラグインの確定状態（バージョン等）を記録します。これをバージョン管理すると、別マシンでのブートストラップや更新のロールバックが容易になります。
- フックとイベント：プラグイン状態変更時に PackChangedPre / PackChanged イベントが発火します。ビルドやパーサ更新などの後処理はこれらのautocmdで実装します。
- 運用上の注意：vim.packはGitリポジトリ単位で管理します。手動でvim.pack管理下のディレクトリを編集するとロックと同期の齟齬が起きるので、ローカル開発は別パッケージ（~/.local/share/nvim/site/pack/mine/opt 等）に置くのが安全です。直接編集した場合は、vim.pack.update(..., { offline = true }) で復帰するなど自己責任の手順が必要です。
- 遅延ロードの柔軟性：load オプションに関数を渡して「登録だけして読み込まない」「特別な読み込み手順を実行する」といった制御が可能です。これがvim.packの「設定で完結する」強みです。

コード例（基本）:
```lua
-- lua
vim.pack.add({
  'https://github.com/nvim-treesitter/nvim-treesitter',
  'https://github.com/neovim/nvim-lspconfig',
})
```

コード例（詳細指定とカスタムロード）:
```lua
-- lua
local function selective_load(plug)
  if (plug.spec.data or {}).skip_load then return end
  vim.cmd.packadd(plug.spec.name)
end

vim.pack.add({
  { src = 'https://github.com/nvim-mini/mini.nvim', version = 'stable' },
  { src = 'https://github.com/neovim/nvim-lspconfig', name = 'lspconfig', data = { skip_load = true } },
}, { load = selective_load })
```

## 実践ポイント
- Neovim 0.12 へ更新してまずは vim.pack.add() にプラグイン一覧を移す（init.lua に集約）。
- nvim-pack-lock.json をコミットして環境再現性を確保する。
- ローカル開発中のプラグインは別pack（pack/mine/opt）に置き、packaddで使う。
- 遅延ロードは load 関数で細かく制御し、起動速度と機能性を両立する。
- PackChanged イベントでビルドやparser更新を自動化する（CIや初回セットアップが楽になる）。

以上を踏まえれば、vim.packは単なるパッケージ管理ではなく「設定ファイルを中心に据えたプラグイン運用」を実現するツールになります。
