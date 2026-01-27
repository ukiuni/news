---
layout: post
title: "4 Pyrefly Type Narrowing Patterns that make Python Type Checking more Intuitive - Pyreflyが示す「直感的な」型絞り込み4パターン"
date: 2026-01-27T18:39:23.623Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://pyrefly.org/blog/type-narrowing/"
source_title: "4 Pyrefly Type Narrowing Patterns that make Type Checking more Intuitive | Pyrefly"
source_id: 416031210
excerpt: "Pyreflyで型絞り込みが直感的に学べ、現場で安全性を素早く向上できる方法を4例で解説"
image: "https://pyrefly.org/assets/images/type-narrowing-blog-688b8aae77abd588a29ddb9d5bab231f.png"
---

# 4 Pyrefly Type Narrowing Patterns that make Python Type Checking more Intuitive - Pyreflyが示す「直感的な」型絞り込み4パターン
Pyreflyで型チェックがぐっと扱いやすくなる—面倒な型キャストを減らす実践テクニック

## 要約
Pyreflyは、hasattr/getattr、タグ付き（識別フィールド）ユニオン、タプル長による絞り込み、変数に保存した条件の追跡といったパターンを理解して、静的型検査をより直感的にします。

## この記事を読むべき理由
日本でもDjango/Flask/FastAPIの現場やデータサイエンスのコードベースでは動的な属性追加や混合型が頻出します。Pyreflyの絞り込み理解は、既存コードを大きく変えずに型安全性を高める実務的メリットがあります。

## 詳細解説
- hasattr / getattr
  - 動的に属性を追加するコードや、コンストラクタで初期化されないフィールドを扱う際、Pyreflyは `hasattr(x, "f")` や `getattr(x, "f")` のチェックを見て属性の存在や真偽を絞り込みます。  
  - 例:
  ```python
  python
  def func(x: object) -> None:
      if hasattr(x, "value"):
          val = x.value  # Pyreflyはここでエラーを出さない
  ```

- タグ付きユニオン（識別フィールド）
  - Pythonの非明示的なユニオンでも、各メンバーに共通の「タグ」フィールドを持たせれば、その値で絞り込めます（TypedDictやクラスで有効）。  
  - 例:
  ```python
  python
  from typing import TypedDict, Literal
  class Ok(TypedDict):
      result: Literal["ok"]
      payload: bytes
  class Err(TypedDict):
      result: Literal["error"]
      message: str
  Response = Ok | Err

  def read(res: Response) -> bytes:
      if res["result"] == "ok":
          return res["payload"]
      else:
          raise Exception(res["message"])
  ```

- タプル長による絞り込み
  - `len(x) == n` のようなリテラル長チェックで、異なる長さのタプル型を持つユニオンを分離できます。  
  - 例:
  ```python
  python
  from typing import Tuple
  XY = tuple[float, float]   # 2要素
  RGB = tuple[int, int, int] # 3要素
  Vec = XY | RGB
  def describe(v: Vec) -> None:
      if len(v) == 2:
          x, y = v  # 2要素として扱える
      else:
          r, g, b = v
  ```

- 変数に保存した条件の追跡
  - `isinstance` 等の結果をローカル変数に保存して再利用するパターンをPyreflyは追跡します。ただし、その後の変化（変数の再代入など）で条件が無効化されると正しく警告します。  
  - 例:
  ```python
  python
  def f(x: int | str, y: int, z: int | str):
      x_is_int = isinstance(x, int)
      if x_is_int:
          y += x  # 安全
      x = z
      if x_is_int:
          y += x  # ここは安全ではないと判断される
  ```

## 実践ポイント
- 既存コードに大きなリファクタ不要で型の恩恵を受けたいなら、まずPyreflyを試す（CIに導入して挙動を確認）。  
- 動的属性は `hasattr`/`getattr` を守備的に使うと型推論が利く。  
- 識別可能なユニオンには明示的なタグフィールドを追加すると安全性が向上。APIレスポンスやメッセージ列挙で有効。  
- 条件を変数に保存する場合は、その後の変数変更で無効化される点に注意する。  

必要なら、上の例コードをローカルで試すための最小セットや、Pyrefly導入手順も用意しますか？
