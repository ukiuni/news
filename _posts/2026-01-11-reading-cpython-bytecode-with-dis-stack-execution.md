---
layout: post
title: "Reading CPython bytecode with dis: stack execution walkthrough - disで読むCPythonバイトコード：スタック実行ウォークスルー"
date: 2026-01-11T11:18:24.342Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://youtu.be/LH2Y15OkG64?si=inerlenGM8r8DfH6"
source_title: "Is Your Python Code Slow? Read the Bytecode (dis + Stack) - Visually explained - YouTube"
source_id: 465569804
excerpt: "disでCPythonバイトコードを追い、3分で無駄なスタック操作と性能改善点を発見する方法"
image: "https://i.ytimg.com/vi/LH2Y15OkG64/maxresdefault.jpg"
---

# Reading CPython bytecode with dis: stack execution walkthrough - disで読むCPythonバイトコード：スタック実行ウォークスルー
3分でわかる、なぜそのPythonコードが遅いかを「バイトコード視点」で発見する方法

## 要約
disモジュールでCPythonのバイトコードを可視化し、スタック上で命令がどう実行されるか追うことで、無駄な操作やパフォーマンスのヒントを短時間で得られる、という内容。

## この記事を読むべき理由
Pythonは高生産性だが、「どこで時間を食っているか」が見えにくい。企業システムやWebサービス、データ処理でPythonを本番運用している日本のエンジニア／運用担当にとって、バイトコードの読み方は低コストで性能改善の糸口になる。

## 詳細解説
- CPythonはソース→バイトコード（.pyc）→スタックベースの仮想マシンで命令を実行する。高レベルの式は一連のLOAD/STOREや演算命令に分解される。
- disモジュールを使うと関数やコードオブジェクトの命令列を確認できる。命令はスタックのpush/popで振る舞いが決まるため、実行時のスタック深度やデータ移動が見える化される。

簡単な例：
```python
# python
def add(a, b):
    return a + b

import dis
dis.dis(add)
```
出力（概略）:
- LOAD_FAST a
- LOAD_FAST b
- BINARY_ADD
- RETURN_VALUE

解釈：LOAD_FASTでローカル変数をスタックに積み、BINARY_ADDが2つを取り出して加算し結果を積み、RETURN_VALUEで返す。

注目すべきパターンと示唆
- グローバル/属性参照は命令数が増え、遅くなりがち（LOAD_GLOBAL / LOAD_ATTR）。ループ内で何度も参照するならローカル変数に束縛しておくと命令が減る。
- 不要なオブジェクト生成（タプル・リスト作成）や一時変数のSTORE/LOADはコストになる。
- 関数呼び出しはCALL_*命令でコストが目に見える。頻繁に呼ぶ処理はインライン化やキャッシュを検討する。
- CPythonのバージョン差に注意（3.11以降は最適化が進み、命令セットが変化）。

## 実践ポイント
- dis.dis()をまず使う：ホットスポットの関数だけを分解して命令数と種類を確認する。
- ループ最適化：ループ内で使う定数/関数/属性はループ外に束縛してLOAD回数を減らす。
- ローカル優先：可能な限りローカル変数を使う（LOAD_FASTは速い）。
- バージョン確認：最適化効果はCPythonのバージョン依存。3.11以降のバイトコードを確認する際は差分を意識する。
- プロファイラと併用：まずプロファイラで熱い関数を特定し、disで命令を読み解き、必要ならリファクタリングする。

日本の現場では、短時間でパフォーマンス改善できる手法が歓迎される。disで「何が実際に動いているか」を見る習慣をつけると、無駄な最適化や誤った推測を減らせる。
