---
layout: post
title: "The Compose key is magic - Composeキーは魔法"
date: 2026-03-14T15:27:16.160Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://crescentro.se/posts/compose-key/"
source_title: "The Compose key is magic // crescentro.se"
source_id: 895210990
excerpt: "Composeキーで一発入力：覚えやすいキー列で記号・絵文字を高速に使いこなす方法"
image: "https://crescentro.se/posts/compose-key/preview.png"
---

# The Compose key is magic - Composeキーは魔法
たった一手で特殊文字も絵文字も出る！LinuxでComposeキーを即戦力にする方法

## 要約
Composeキーを割り当てると、Compose → e → = で €、Compose → < → 3 で ♥、Compose → - → > で → のように、覚えやすいキー列で特殊文字や絵文字を入力できる。カスタム定義はホームの .XCompose に追加可能。

## この記事を読むべき理由
特殊文字や矢印、記号、絵文字を毎回検索・コピペしている人は時間を大幅に節約できる。日本語環境でも記号入力やドキュメント作成、チャットでの表現が格段に効率化される。

## 詳細解説
- Composeキーの役割  
  Compose（Multi_key）は「続けて押す普通のキー列」を特殊文字に変換する物理的なキー扱い。標準キーボードに専用キーは少ないが、既存キーをComposeにマップできる。

- 代表的な組み合わせ（覚えやすい）  
  - Compose, e, = → €  
  - Compose, 1, 4 → ¼  
  - Compose, o, e → œ  
  - Compose, <, 3 → ♥  
  - Compose, -, > → →

- 設定の流れ（概念）  
  1. 既存キーをComposeに割り当て（例：右Win/Alt/Option）。  
  2. Wayland + GTK4環境ではIMEが必要（IBus等）。  
  3. ~/.XCompose にカスタム定義を追加して拡張。

- xkbオプション例（構成ファイルに追加）  
```nix
# nix系設定例（言語はnix）
input.keyboard.xkb.layout = "nl(mac)";
input.keyboard.xkb.options = "compose:rwin"; # 右WinをComposeに
```

- Wayland/GTK4でのIME（例：NixOS）  
```nix
# nix系設定例（言語はnix）
i18n.inputMethod = { enable = true; type = "ibus"; };
```

- .XCompose の最小例（ホームに .XCompose を置く）  
```text
# include the global configuration
include "%L"

# 基本的なカスタム例
<Multi_key> <less> <3> : "♥"
<Multi_key> <minus> <greater> : "→"
<Multi_key> <e> <equals> : "€"
```

## 実践ポイント
- まずは右Win/右Altなど使っていないキーを compose:rwin / compose:menu / compose:caps などで割り当てる。  
- Wayland環境なら IBus 等の IME を有効化する（DEなら多くはデフォルトで用意）。  
- ~/.XCompose に include "%L" を入れ、頻出シンボルを数行定義して試す。  
- よく使う矢印・ダッシュ・ハート・絵文字を登録すると入力が劇的に速くなる。
