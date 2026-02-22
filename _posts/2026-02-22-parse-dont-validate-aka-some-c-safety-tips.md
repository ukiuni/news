---
layout: post
title: "Parse, Don’t Validate AKA Some C Safety Tips - 「検証するな、解析せよ」〜Cで学ぶ安全設計のコツ"
date: 2026-02-22T15:45:29.532Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.lelanthran.com/chap13/content.html"
source_title: "Parse, Don’t Validate AKA Some C Safety Tips"
source_id: 1437274599
excerpt: "境界で文字列を解析してopaque型に変換し、Cで引数取り違えやバッファ脆弱性をコンパイル時に防ぐ手法"
---

# Parse, Don’t Validate AKA Some C Safety Tips - 「検証するな、解析せよ」〜Cで学ぶ安全設計のコツ
バグや脆弱性をコンパイルで防ぐ――Cで実践する「Parse, Don’t Validate」の短く実用的な解説

## 要約
入力は境界で一度だけ「解析（parse）」して型化し、内部では生文字列を扱わない。Cでもopaque型を使えばコンパイル時に多くのミスを防げる、という考え方。

## この記事を読むべき理由
日本の組込み・業務系コードやレガシーCプロジェクトは今も多く、文字列の誤用やバッファ誤操作が致命的な脆弱性を招きやすい。本手法は低コストで安全性と可読性を改善する実践策になる。

## 詳細解説
- 問題点：受け取った生の文字列をシステム中でそのまま渡すと、各所で別々に検証が行われたり、誤った使い方（emailとnameを取り違える等）が発生する。
- 考え方：境界（ネットワーク、CLI、ファイル等）で入力を解析して専用の型に変換する（email_t, name_tなど）。以降の関数はその型しか受け取らない。
- Cでの実装要点：
  - ヘッダでopaque型を宣言し、実体は実装ファイルに隠す。
  - parse関数は入力文字列から構造化されたオブジェクトを返す（失敗時はNULL）。
  - del（デストラクタ）はポインタへのポインタを受け取り、解放後に呼び出し元のポインタをNULLにする（ダブルフリー防止）。
  - 結果：email_tとname_tは同じ内部構造でもコンパイラが型混在を検出するため、引数取り違えなどがコンパイルエラーになる。

短縮したコード例（概念説明用）：

```c
// callee.h
typedef struct email_t email_t;
typedef struct name_t name_t;

email_t *email_parse(const char *untrusted);
name_t  *name_parse(const char *untrusted);

void email_del(email_t **e);
void name_del(name_t  **n);
```

```c
// caller.c
void store_old(char *email, char *name);      // 生文字列版
void store_new(email_t *email, name_t *name); // 型安全版

bool rx(char *in_name, char *in_email) {
    email_t *e = email_parse(in_email);
    name_t  *n = name_parse(in_name);
    if (!e || !n) { email_del(&e); name_del(&n); return false; }

    // store_old(in_name, in_email); // 間違えて引数を入れ替えると実行时のバグ
    // store_new(n, e); // 型が合わずコンパイルエラーになる
    store_new(e, n);
    return true;
}
```

## 実践ポイント
- 境界で必ずparseして専用型を生成する（char*は境界だけに限定）。
- ヘッダでは型をopaqueにして内部実装を隠す。
- 破棄関数はポインタのアドレスを受け取りNULL設定する習慣をつける。
- コンパイラ警告を有効化（-Wall -Wextra）、静的解析ツールを導入して型ミスを早期発見。
- まずはemail/nameなどミスしやすいデータから段階的に置き換えると導入コストが小さい。

この手法は「検証（validate）を各所で繰り返す」よりも安全で手入れしやすく、特に長期運用されるCコードベースでの品質改善に有効である。
