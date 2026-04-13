---
layout: post
title: "How to make Firefox builds 17% faster - Firefoxのビルドを17%速くする方法"
date: 2026-04-13T19:47:17.822Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://blog.farre.se/posts/2026/04/10/caching-webidl-codegen/"
source_title: "How to make Firefox builds1 17% faster2 | farre’s blog"
source_id: 47756321
excerpt: "WebIDLのPython生成をbuildcacheでキャッシュし、Firefoxビルドを約17%高速化"
---

# How to make Firefox builds 17% faster - Firefoxのビルドを17%速くする方法
Firefoxビルドの「Pythonコード生成」をキャッシュして開発サイクルをぐっと短くする方法

## 要約
MozillaのbuildcacheのLuaプラグインで、WebIDLから生成されるC++バインディングコードの出力をキャッシュできるようになり、クローン→ビルド（clobber）後の再ビルドが大幅に高速化します。

## この記事を読むべき理由
毎回のビルド時間は開発生産性に直結します。特に大規模なネイティブ／ブラウザ開発では、Pythonで行うコード生成など「コンパイラ以外の確定的処理」もキャッシュできれば、編集→ビルド→テストのサイクルが速くなり、日本の開発現場でも即効性のある改善になります。

## 詳細解説
- 問題点  
  Firefoxビルドでは早い段階で `python3 -m mozbuild.action.webidl` を実行し、数百の .webidl から大量のヘッダ／cpp等を出力します。処理自体は決定的（同じ入力で同じ出力）が前提ですが、従来のコンパイラキャッシュはこのPythonコード生成に介入していませんでした。

- 変更内容（Makefile 側）  
  dom/bindings/Makefile.in 側で、buildcache を使っている場合に py_action にコマンドラッパーを渡すようにしました。要点は py_action に $(CCACHE) を渡すことで、実行が
  buildcache python3 -m mozbuild.action.webidl …
  のようになり、buildcache が介入できるようになることです。

  ```makefile
  WEBIDL_CCACHE = 
  ifdef MOZ_USING_BUILDCACHE
  WEBIDL_CCACHE = $(CCACHE)
  endif

  webidl.stub : $(codegen_dependencies)
  	$(call py_action,webidl $(relativesrcdir),$(srcdir),,$(WEBIDL_CCACHE))
  	@$(TOUCH) $@
  ```

- Luaラッパーの仕組み  
  buildcache の Lua プラグイン（webidl.lua）がコマンドを判別し、入力ファイル群（.webidl と Pythonスクリプト等）を file-lists.json と codegen.json から取得、出力ファイル群も file-lists.json から特定します。direct_mode を使って実ファイルをハッシュ化し、キャッシュにヒットすれば生成済み出力を再配置、なければ実行して結果を保存します。

- 実測値（記事より）  
  ./mach build のクローン→ビルドでの比較（代表値）：buildcache の warm ビルドが 1m27s、webidl.lua を有効にするとさらに短く 1m12s まで改善。単一マシンの例ではありますが、編集→再ビルドサイクルでの恩恵は明確です。

- 設定方法（要点）  
  buildcache を既に使っているなら、ビルド環境を最新にして buildcache-wrappers をクローンし、 ~/.buildcache/config.json に lua_paths を追加するか、環境変数 BUILDCACHE_LUA_PATH を設定します。大きなキャッシュエントリ（例：Rust生成物）に備え max_local_entry_size を大きめに設定します。

  ```json
  {
    "lua_paths": [ "/path/to/buildcache-wrappers/mozilla" ],
    "max_cache_size": 10737418240,
    "max_local_entry_size": 2684354560
  }
  ```

## 実践ポイント
- リポジトリを最新の central に更新して Makefile の変更を取り込む。  
- buildcache-wrappers をクローンし、~/.buildcache/config.json の lua_paths か MOZ の mozconfig に BUILDCACHE_LUA_PATH を設定する。  
- max_local_entry_size を 2.5GB 程度に設定して巨大なキャッシュを許容する。  
- 他の deterministic なコード生成ステップ（Python や独自ツール）も同様にラップできるか調べ、同手法を横展開する。  
- まずは clobber → warm 再ビルドで時間差を測り、CI／ローカルの恩恵を確認する。
