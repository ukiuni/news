---
layout: post
title: "Python Type Checker Comparison: Empty Container Inference - 空のコンテナ推論の比較"
date: 2026-03-01T18:56:31.743Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://pyrefly.org/blog/container-inference-comparison/"
source_title: "Python Type Checker Comparison: Empty Container Inference | Pyrefly"
source_id: 47151367
excerpt: "空のコンテナ推論3戦略の比較でバグ検出と誤報の最適解を提示、事例と設定指南付き"
image: "https://pyrefly.org/assets/images/empty-container-blog-cef98862cb6b53726eb97df7ee6f2d14.png"
---

# Python Type Checker Comparison: Empty Container Inference - 空のコンテナ推論の比較
「[] = 何のリスト？」空のコンテナでバグを見逃すな — 型チェッカーの3つの戦略

## 要約
空のリストや辞書（[] / {}）の型をどう推論するかで、型チェックの検出力や誤検出の傾向が大きく変わる。この記事は3つの主要戦略（Any推論／全使用箇所から推論／最初の使用から推論）を比較し、それぞれの利点・欠点と実務での使いどころを解説する。

## この記事を読むべき理由
空のコンテナは初学者からプロまで日常的に使うパターンで、推論戦略次第で本番クラッシュを見逃したり、ノイズの多いエラーに悩まされたりする。日本のチームが型チェッカーを選ぶ・設定する際の判断材料になる。

## 詳細解説
1. Strategy 1 — 要素を Any と推論する（Pyright, Ty, Pyre系）
   - 実装が簡単で誤検出が少ないが、型安全性を放棄するため潜在的なバグを見逃す。
   - 例: x = [] → x: list[Any]。後で間違った型を入れても警告が出ない。

2. Strategy 2 — 全ての使用箇所から要素型を集約する（Pytype）
   - 実際の実行時挙動に近い（複数箇所で異なる型を入れたら union にする）ため、取り出し時の問題を検出しやすい。
   - 欠点は、利用箇所が離れていると原因特定が難しくなり、複雑なunionがエラーメッセージを読みにくくする点。
   - 例:  
```python
# python
x = []
x.append(1)       # int
x.append("foo")   # str
# 推論: list[int | str]
```

3. Strategy 3 — 最初の使用だけで型を決める（Mypy, Pyreflyのデフォルト）
   - 最初に現れる操作を「意図」と見なして型を決めるため、エラーが起きた箇所が修正箇所に近く、アクショナブルな警告になりやすい。
   - 誤推論の可能性はあるが、意図と異なる場合は明示注釈で上書き可能（例: lines: list[str | list[str]] = []）。
   - 実例（バグ）：  
```python
# python
from dataclasses import dataclass

@dataclass
class MenuItem:
    title: str | None
    details: list[str]

def first_three_lines(menu_item: MenuItem) -> list[str]:
    lines = []                      # 最初の使用で list[str] と推論されることを期待
    if menu_item.title is not None:
        lines.append(menu_item.title)
    lines.append(menu_item.details)  # 意図は extend だが append してしまい型不整合
    return lines[:2]
```

まとめの比較
- Any推論：誤検出は少ないがバグを見逃す。
- 全使用箇所推論：実行時挙動に近いが原因追跡が難しくなる場合あり。
- 最初の使用推論：原因に近い警告を出すが、意図と違えば注釈が必要。

## 実践ポイント
- チーム方針を決める：寛容さ（Any）を優先するか、早期発見（最初の使用）を優先するかで型チェッカーと設定を選ぶ。
- 明示注釈を活用：空のコンテナを作るときに意図が明確なら注釈を書く（例: items: list[int] = []）。
- エラーメッセージの読み方を統一：全使用推論では発生箇所と原因が離れることを理解しておく。
- ツール設定：Pyreflyはデフォルトで最初の使用推論だが、設定で無効にできる。CIポリシーに合わせて設定を固定する。
- テストで補完：型推論だけでは足りないケースがあるので、ユニットテストで実行時の不整合を捕まえる。

以上を踏まえ、まずはチームの「検出したいバグの優先度」と「誤検出に耐えられるか」を議論し、型チェッカーと設定を決めることをおすすめする。
