---
layout: post
title: "Hammerspoon - ハンマースプーン"
date: 2026-03-13T19:21:10.071Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/Hammerspoon/hammerspoon"
source_title: "GitHub - Hammerspoon/hammerspoon: Staggeringly powerful macOS desktop automation with Lua · GitHub"
source_id: 47367932
excerpt: "*LuaでmacOSを自在に自動化、ウィンドウやIME操作をコード化して生産性を劇的に向上させる*"
image: "https://opengraph.githubassets.com/254f30e6f026af4cbbea48f31081a7a2e9742e708575d53618efd55b9e2982e6/Hammerspoon/hammerspoon"
---

# Hammerspoon - ハンマースプーン
驚くほど強力なmacOS自動化をLuaで手に入れる方法

## 要約
HammerspoonはmacOSの深い操作をLuaスクリプトで自在に自動化するツールで、ウィンドウ操作やホットキー、ファイル監視などを拡張経由で利用できます。軽量かつ拡張性が高く、手元のMacで生産性を劇的に上げられます。

## この記事を読むべき理由
macOSを使う日本の開発者・テック愛好者にとって、日常的な繰り返し作業やウィンドウ管理、キーボードカスタムをコードで再現できるのは大きな時間短縮になります。特に複数ディスプレイ／日本語入力の癖がある環境で効果が出ます。

## 詳細解説
- 仕組み：HammerspoonはLua実行環境とmacOSの機能をつなぐブリッジ。Objective‑C/Cで書かれた「Extensions（Spoons）」がシステムAPIを公開し、Luaから呼び出します。  
- 主な機能：グローバルホットキー、ウィンドウ管理、アプリ監視、ファイルシステム監視、メニューバー操作、通知など。  
- 開発・配布：GitHubで活発に開発（多数のスターとリリース）、MITライセンス。元はMjolnirのフォークで、より統合された体験を目指しています。  
- エコシステム：ユーザー提供のサンプル設定やAPIドキュメント、Discord/IRCコミュニティが充実。Karabiner‑ElementsやAlfred、BetterTouchToolと組み合わせる運用が一般的です。  
- 技術ポイント：設定は ~/.hammerspoon/init.lua にLuaコードを置くだけ。Luaに馴染みがなくても、既存のサンプルを組み替えることで素早く効果を得られます。

## 実践ポイント
1. インストール（Homebrew推奨）
   - brew install hammerspoon --cask
2. 最小の初期設定：~/.hammerspoon/init.lua を作成し、設定変更後に再読み込みするホットキーと簡単なウィンドウ操作を試す。

```lua
-- lua
hs.hotkey.bind({"cmd","alt","ctrl"},"R",function()
  hs.reload()
  hs.alert.show("Hammerspoon reloaded")
end)

hs.hotkey.bind({"cmd","alt"}, "H", function()
  local win = hs.window.frontmostWindow()
  if win then
    win:moveToUnit(hs.layout.left50)
  end
end)
```

3. 次のステップ：APIドキュメント、サンプル設定集、Spoonsを覗き、必要な自動化を1つずつコード化する。  
4. 日本での活用例：日本語入力切替やIME周りの自動化、複数ディスプレイでのウィンドウ配置、定型操作の自動化に特に有効。

元リポジトリ（参照）：https://github.com/Hammerspoon/hammerspoon
