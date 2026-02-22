---
layout: post
title: "Oop design pattern - OOPデザインパターン"
date: 2026-02-22T11:26:03.154Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://youtu.be/7xzI_ReANN4?si=9iyMNtTPMa3YgqY2"
source_title: "OOP Strategy Design Pattern - YouTube"
source_id: 399518420
excerpt: "Strategyパターンで条件分岐を差し替え可能にして決済や認可などの拡張を安全に行う方法"
image: "https://i.ytimg.com/vi/7xzI_ReANN4/hqdefault.jpg"
---

# Oop design pattern - OOPデザインパターン
戦略（Strategy）パターンで「差分だけ」を差し替え、拡張に強い設計に変える方法

## 要約
Strategyパターンはアルゴリズム（振る舞い）を切り替え可能なオブジェクトとして分離するデザインパターンで、継承ではなくコンポジションで柔軟性とテスト性を高めます。

## この記事を読むべき理由
日本の現場ではレガシーな条件分岐や肥大化したクラスが課題です。Strategyを使えば運用ルールや決済・認可・出力形式など、変化する要素を安全に置き換えられます。

## 詳細解説
- 構成要素
  - Strategy（戦略）インターフェース：共通の操作を定義
  - ConcreteStrategy：具体的なアルゴリズム実装
  - Context：Strategyを保持し、呼び出す役割（依存は抽象に向ける）
- 目的
  - 振る舞いをクラスから切り離し、実行時に差し替え可能にする
  - 単一責任の促進、Open/Closed原則（拡張に対して閉じた修正を最小化）
- 利点
  - テストしやすい（個別にモック可能）
  - 新しい戦略を追加して既存コードを壊さない
- 注意点
  - 小さなプロジェクトで過剰設計になりやすい
  - 戦略数が多すぎると管理コストが増す

簡単なPython例（支払い戦略の切替）：

```python
# python
from abc import ABC, abstractmethod

class PaymentStrategy(ABC):
    @abstractmethod
    def pay(self, amount: int) -> str:
        pass

class CreditCard(PaymentStrategy):
    def pay(self, amount: int) -> str:
        return f"Paid {amount} with credit card"

class PayPal(PaymentStrategy):
    def pay(self, amount: int) -> str:
        return f"Paid {amount} via PayPal"

class Order:
    def __init__(self, strategy: PaymentStrategy):
        self.strategy = strategy

    def checkout(self, amount: int) -> str:
        return self.strategy.pay(amount)

# 使い方
order = Order(CreditCard())
print(order.checkout(5000))  # 支払い手段を実行時に差し替え可能
order.strategy = PayPal()
print(order.checkout(3000))
```

## 実践ポイント
- 条件分岐（if/else）がビジネスロジックで増えてきたらStrategyを検討する。
- 決済・ロギング・認可・フォーマット変換など「交換可能な振る舞い」に適用する。
- DI（依存注入）やファクトリで戦略の生成を管理すると切り替えが容易。
- 単体テストは各ConcreteStrategyに集中させ、Contextはインターフェースの動作確認に留める。
- 日本の現場では、複雑な要件やレガシー置換、A/Bテスト対応に特に有益。
