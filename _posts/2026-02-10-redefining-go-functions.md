---
layout: post
title: "Redefining Go Functions - Go関数を書き換える"
date: 2026-02-10T20:07:11.857Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://pboyd.io/posts/redefining-go-functions/"
source_title: "Redefining Go Functions | pboyd.io"
source_id: 1023824482
excerpt: "Goの実行中に関数先頭命令を書き換え、time.Nowを固定化する危険な技術と回避策を解説"
---

# Redefining Go Functions - Go関数を書き換える
Goで「関数を書き換える」技術――time.Nowを常に「5時」にする魔法と、その危険

## 要約
Goで実行時に関数の先頭命令を書き換え、別の関数へジャンプさせることで挙動を差し替えられる。reflect/unsafeでポインタを取り、mprotectでメモリ保護を外してJMP命令を埋める手法だが、多くの制約と重大な危険がある。

## この記事を読むべき理由
Goは日本のサーバー/クラウドサービスや組み込み分野でも広く使われており、ランタイム改変の「魔法」が何を可能にし、どのような落とし穴を生むかを知っておくことは、安全な設計とデバッグの観点で重要。

## 詳細解説
手順の概略
- 関数ポインタの取得: reflect.ValueOf(fn).Pointer() で関数エントリのアドレスを得る。
- 命令の読み取り: unsafe.Slice((*byte)(unsafe.Pointer(addr)), n) で先頭バイトを参照。
- 差し替え: x86では先頭にE9 + 相対オフセット（JMP）を埋める。ジャンプ先は置き換えたい関数のエントリ。
- メモリ保護の変更: mmap/mprotect（Unix）や VirtualProtect（Windows）でページの書き込みを許可。
- ARM64や他アーキテクチャでは命令セットやキャッシュクリアが必要。

短い例（概念のみ）:
```go
package main

import (
  "encoding/binary"
  "reflect"
  "unsafe"
)

// src := reflect.ValueOf(orig).Pointer()
// dst := reflect.ValueOf(repl).Pointer()
// buf := unsafe.Slice((*byte)(unsafe.Pointer(src)), 8)
// mprotect(src, len(buf), PROT_READ|PROT_WRITE|PROT_EXEC)
// buf[0] = 0xE9 // x86 JMP
// binary.LittleEndian.PutUint32(buf[1:], uint32(int32(dst-(src+5))))
// mprotect(src, len(buf), PROT_READ|PROT_EXEC)
```

主な制約と危険
- インライン化: コンパイラが関数呼び出しをインラインすると、呼び出し先のエントリを差し替えても意味がない（呼び出し元に直接命令が埋め込まれる）。
- ジェネリクス/特殊化: コンパイル時に生成される別インスタンスが存在し、期待通り動かない。
- メソッドのレシーバ不整合: 置き換えるメソッドが別構造体向けにコンパイルされていると、メモリレイアウトの違いで巨大な数値やメモリ破壊を引き起こす（例: 高32ビットを書き換える等）。
- 権限・安全性: 実行中のコード書換えはセキュリティ・保守性・トレース性を破壊する。プロダクションではほぼタブー。
- プラットフォーム依存: 実装はアーキテクチャ（AMD64 vs ARM64）やOS（mprotect vs VirtualProtect）に依存する。

補足: 著者はtime.Nowを常に固定時刻にする例で動作を示し、ARM64版やWindows向けの対応についても言及しているが、動作・副作用は環境依存。

## 実践ポイント
- 基本方針: ランタイム書換えは最終手段。代替としてインターフェース、依存性注入、テスト用フック（build tagや設計で差し替え可能な関数）を採用する。
- デバッグ用途に限定: ローカル実験や検証用でのみ試し、CI/本番には持ち込まない。
- アーキ・プラットフォーム固定: 実験時は対象CPU/OSを固定し、命令セット・キャッシュ挙動を理解する。
- 安全対策: 置き換える関数と置換先のシグネチャ・レイアウトを厳密に一致させる（メソッドのレシーバは同一レイアウトでなければならない）。
- 参考実装: 著者はLinux/AMD64向けのパッケージを公開している。試すならソースを読み、リスクを受け入れること。

この手法は「できる」けれど「してはいけない」ことが多い――設計で代替できる場合はそちらを選ぶのが安全。
