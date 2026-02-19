---
layout: post
title: "-fbounds-safety: Enforcing bounds safety for C - C の境界安全性を強制する -fbounds-safety"
date: 2026-02-19T15:12:22.707Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://clang.llvm.org/docs/BoundsSafety.html"
source_title: "-fbounds-safety: Enforcing bounds safety for C &#8212; Clang 23.0.0git documentation"
source_id: 47035088
excerpt: "既存Cコードをほぼ無改変で境界チェック化し、実行時トラップで脆弱性を確実に排除"
---

# -fbounds-safety: Enforcing bounds safety for C - C の境界安全性を強制する -fbounds-safety
Cのポインタ境界エラーを「確実にトラップ」する──現場で使える安全化アプローチ

## 要約
-fbounds-safetyはCに拡張を入れ、ポインタに境界情報を付与して実行時／コンパイル時に範囲外アクセスを検出・トラップする仕組みです。ABI互換性を保ちつつ段階的導入できる点が特徴です。

## この記事を読むべき理由
Cは日本の組み込み・OS・レガシーコードで今も幅広く使われており、境界外メモリアクセスは深刻な脆弱性源です。-fbounds-safetyは既存コードへ最小限の負担で安全性を高める現実的な実装方針を示しています。

## 詳細解説
- 目的：ポインタのOOB（out-of-bounds）アクセスを決定的なトラップに変えることでセキュリティ欠陥を減らす。  
- 基本モデル：すべてのポインタは明示／暗黙の「bounds（範囲）」属性を持ち、参照時にチェックされる。チェック失敗はトラップ（例外的終了）を生む。  
- 外部アノテーション（ABI影響なし）  
  - __counted_by(N)：要素数 N を表す（例：関数パラメータと長さが別にある典型的なAPI）  
  - __sized_by(N)：バイトサイズで指定（void*や不完全型向け）  
  - __ended_by(P)：ポインタの終端を別ポインタで指定（イテレータ風）  
  - *_or_null バリアントで NULL 許容を明示（NULLチェックが必要になる）  
- 単一オブジェクト注釈  
  - __single：単一オブジェクト（またはNULL）。ポインタ演算や添え字はコンパイルエラーにして不正利用を阻止。ABI可視（関数パラメータ等）にはデフォルト。  
- 内部（wide/fat）ポインタ（ABI破壊）  
  - __indexable / __bidi_indexable：ポインタを「wide pointer（ptr + 上限 + 〔下限〕）」として保持。ローカル変数で暗黙的にwide化することで注釈負荷を減らすが、ABIの境界では使わない設計。  
- ABIとの調整：ローカル変数は暗黙的にwideにできる一方、関数の公開シグネチャなどABI可視部分は単一ポインタ（__single）をデフォルトにして互換性を保つ。これにより段階的導入が可能。  
- 安全性維持：境界情報の更新や引き渡しに対してコンパイル時制約や実行時チェックを設け、アノテーション不整合から生じる危険を検出する。  
- 注意点：元記事は設計文書で、実装状況・利用可能性や詳細仕様は更新中。導入時は対応するコンパイラ／ツールチェーンが必要。

例（概念的）:
```c
// c
void fill_array_with_indices(int * __counted_by(count) p, unsigned count) {
  for (unsigned i = 0; i <= count; ++i) { // off-by-one をチェックしてトラップ
    p[i] = i;
  }
}
```

## 実践ポイント
- まずは公開APIの関数パラメータに __counted_by / __sized_by を付けて外部境界を明示する。  
- NULL許容のケースには __*_or_null を使う（追加のNULLチェックが入る）。  
- 関数インターフェースは __single をデフォルトと考え、意図的な配列操作には明示注釈を付ける。  
- 段階導入を目指す：まずヘッダに注釈マクロ（未対応ツール向けに空定義）を置き、対応clangで徐々にビルドを通す。  
- 実運用前にツールチェーンの対応状況（-fbounds-safety 実装の有無）を確認すること。  

以上を踏まえると、-fbounds-safetyは既存のC資産を大きく書き換えずにメモリ安全性を強化する現実的な選択肢になり得ます。
