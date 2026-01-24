---
layout: post
title: "Writing a generic JSON.stringify that serializes any C struct? An experiment on making it possible via reflection - 任意のC構造体をJSON化する実験：Reflectionで実現する試み"
date: 2026-01-24T18:32:41.407Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/lcsmuller/reflect-c"
source_title: "GitHub - lcsmuller/reflect-c: Code-generates ANSI C helpers that give your structs reflection-style access to field names, types, and values."
source_id: 418536254
excerpt: "Reflect‑Cで任意C構造体をゼロランタイムで自動JSON化する手法と実装手順を紹介"
image: "https://opengraph.githubassets.com/f47d905f1d566bfe3e15c4311187478874cba3cb0c71fc32ce5b72b5a172e868/lcsmuller/reflect-c"
---

# Writing a generic JSON.stringify that serializes any C struct? An experiment on making it possible via reflection - 任意のC構造体をJSON化する実験：Reflectionで実現する試み
Cでも「反射（reflection）」的にstructの名前・型・値を扱えるようにするツール、Reflect‑Cの紹介

## 要約
Reflect‑Cはコンパイル時にメタデータを自動生成して、ANSI Cで構造体/共用体/列挙をランタイムに「反射的」に扱えるようにするツールチェーンです。これにより任意のC構造体を汎用コードで列挙・シリアライズ（例：JSON）できます。

## この記事を読むべき理由
Cは組み込みやレガシー系で今も主力。手書きのシリアライザや大量のボイラープレートに悩む日本のエンジニアにとって、ビルド時生成＋ゼロランタイムコストで反射風APIを得られる点は即戦力になります。

## 詳細解説
- アプローチ：ユーザは「recipe」と呼ぶ薄いヘッダー（.recipe.h）で型をマクロDSLで記述。ビルド時にreflect-cがそのレシピを複数回展開して（定義／列挙表／メタデータ／コンストラクタ）生成ソースを吐き出します。生成はビルド時のみでランタイムでの解析は不要（＝ゼロコストメタデータ）。
- カバー範囲：struct/union/enumの入れ子、ポインタ深度、配列、const/volatile等の修飾子まで扱えます。JSONのラウンドトリップ例や単体テストで検証済み。
- ランタイムAPI（主だったもの）
  - reflectc_from_<type>(ptr, reuse)：インスタンスのメタデータツリーを構築
  - REFLECTC_LOOKUP(struct, type, field, root)：コンパイル時インデックス
  - reflectc_get_member / reflectc_deref：メンバのポインタ解決と取得
  - reflectc_set / reflectc_memcpy / reflectc_string：安全な書き込み
  - reflectc_array：配列長の操作
  - オプショナルなレジストリAPIでラッパーのキャッシュ管理も可能
- 開発ワークフロー：git clone → make gen でジェネレータと生成ソースを作成。VS Code向けにはreflect-c_intellisense.hをforcedIncludeすることでIntelliSenseがrecipeのマクロを理解します。
- カスタマイズ：REFLECTC_PREFIX/REFLECTC_PREFIX_UPPERで名前空間を変更可能。tupleヘルパーは必要に応じて再生成できます。

例（簡単なrecipeと使用例）
```c
/* C */
PUBLIC(struct, person, 3, ((_,_,char,*,name,_),( _,_,int,_,age,_),( _,_,bool,_,active,_)))
```

```c
/* C */
struct person p = { "Yuki", 29, true };
struct reflectc *r = reflectc_from_person(&p, NULL);
size_t pos = REFLECTC_LOOKUP(struct, person, name, r);
const char *name = reflectc_get_member(r, pos);
free(r);
```

## 実践ポイント
- まず試す：git clone https://github.com/lcsmuller/reflect-c && make gen、付属のapi/レシピをビルドしてテストを実行（make -C test ./test/test）。
- VS Codeでrecipe編集するなら reflect-c_intellisense.h を forcedInclude して作業性を上げる。
- 既存プロジェクトに埋め込む際は REFLECTC_PREFIX を上書きして名前衝突を回避。
- 組み込み/IoTやレガシーCコードのテレメトリ/設定シリアライズに特に有用。JSON化や汎用ツール作成の初手として試す価値あり。
