---
layout: post
title: "Runtime validation in type annotations - 型注釈でのランタイム検証"
date: 2026-02-16T07:39:19.864Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://blog.natfu.be/validation-in-type-annotations/"
source_title: "Runtime validation in type annotations | Gribouillis"
source_id: 1164264382
excerpt: "typing.Annotatedで検証を宣言し、dataclass初期化で検証とエラー集約を自動化"
---

# Runtime validation in type annotations - 型注釈でのランタイム検証
魅力的タイトル: 型注釈でバリデーションを“宣言”する—PythonのAnnotatedで実務に効く入力検証パターン

## 要約
typing.Annotatedを使って型注釈に「実行時検証ロジック」を埋め込み、dataclassの初期化時にそのメタデータを走らせることで、宣言的に入力検証を行う手法を紹介します。

## この記事を読むべき理由
FastAPIやpydanticのようなライブラリで見かける「型から検証を実行する」パターンを自分のプロジェクトに取り入れれば、API入力や設定値の安全性を型注釈ベースで担保でき、日本のWeb/バックエンド開発でもコードの可読性と信頼性が上がります。

## 詳細解説
- 基本アイデア
  - typing.Annotated[type, metadata] に検証用オブジェクト／関数を入れる。
  - get_type_hints(..., include_extras=True) でメタデータを取り出し、初期化時に実行する。
- 実装の要点
  - dataclassをベースにして __post_init__ 内で各フィールドの注釈を取得する。
  - 注釈の __metadata__ から callable な要素だけ取り出し、フィールド値に対して順に適用する。
  - frozen dataclass の場合は object.__setattr__ を使って検証後の値を書き戻す（不変性を維持しつつ初期化補正を可能にするため）。
- パラメタ付き検証
  - 単なる関数では引数を注釈に書けないため、Callableクラス（callableな dataclass）を作ると便利。例：Number(gt=0, lt=100) のようにインスタンス化して注釈に入れる。
- 複数エラーの集約
  - 3.11以降の ExceptionGroup を使えば、全フィールドの検証を走らせて得られた複数の ValueError をまとめて報告できる。各例外に add_note で属性名や値の文脈を付与するとデバッグが楽になる。
- 代替アプローチ（関数クロージャ）
  - functools.partial やクロージャを使って境界値を遅延バインドする方法もあり、クラスより軽量に再利用可能な検証関数を作れる（ただし Placeholder は3.14以降）。

簡単な骨組み（要点のみ）:
```python
from dataclasses import dataclass
import typing as t

@dataclass(frozen=True)
class Base:
    def __post_init__(self):
        annotations = t.get_type_hints(type(self), include_extras=True)
        excs: list[Exception] = []
        for k, annot in annotations.items():
            callables = [m for m in getattr(annot, "__metadata__", []) if callable(m)]
            for f in callables:
                try:
                    val = getattr(self, k)
                    object.__setattr__(self, k, f(val))
                except ValueError as e:
                    e.add_note(f"Error for attribute '{k}': {val}")
                    excs.append(e)
        if excs:
            raise ExceptionGroup("Validation Errors", excs)
```

検証クラス例（Numberで範囲チェック）:
```python
from dataclasses import dataclass
import typing as t

@dataclass(frozen=True)
class Number:
    gt: t.Optional[float] = None
    lt: t.Optional[float] = None
    def __call__(self, value: float) -> float:
        if self.gt is not None and value <= self.gt:
            raise ValueError(f"{value} must be > {self.gt}")
        if self.lt is not None and value >= self.lt:
            raise ValueError(f"{value} must be < {self.lt}")
        return value

@dataclass(frozen=True)
class A(Base):
    x: t.Annotated[int, Number(gt=0, lt=100)]
```

## 実践ポイント
- 必要なPythonバージョン：ExceptionGroupを使うなら3.11以上、Placeholderを使う手法は3.14以降を確認。
- get_type_hints(..., include_extras=True) を忘れずに。通常の get_type_hints は Annotated のメタデータを返しません。
- 例外はValueErrorで統一すると扱いやすい（用途に応じて拡張可）。複数エラーは ExceptionGroup でまとめて出すとUXが良い。
- validatorは不変（frozen）で設計すると副作用を避けられる。初期化後の補正は object.__setattr__ を使う。
- FastAPIや設定読み込みコードに適用すれば、型注釈ベースの明示的な入力検証が得られ、テストや自動生成ドキュメントと相性が良い。

この記事をヒントに、小さなユーティリティとして検証フレームワークを社内ライブラリ化すると再利用性が高まります。
