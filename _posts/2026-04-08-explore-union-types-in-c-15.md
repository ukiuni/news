---
layout: post
title: "Explore union types in C# 15 - C# 15 のユニオン型を探る"
date: 2026-04-08T13:07:56.458Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://devblogs.microsoft.com/dotnet/csharp-15-union-types/"
source_title: "Explore union types in C# 15 - .NET Blog"
source_id: 47645717
excerpt: "C# 15のunionで戻り値や引数の型選択を安全に表現し、網羅的パターンマッチでバグを防ぐ方法"
image: "https://devblogs.microsoft.com/dotnet/wp-content/uploads/sites/10/2026/03/csharp-15-union-types.webp"
---

# Explore union types in C# 15 - C# 15 のユニオン型を探る
魅力的タイトル: C# 15で「型の選択肢」を安全に扱う新機能：ユニオン型でコードがぐっとシンプルに

## 要約
C# 15で導入された union キーワードは、変数が取ることができる型を限定する「閉じた集合」をコンパイラが保証するユニオン型を提供し、網羅的なパターンマッチングを可能にします。

## この記事を読むべき理由
複数候補の戻り値や引数を扱う設計が増える中で、例外やobject型の乱用を避け、コンパイル時に漏れを検出できる型設計は日本の開発現場でも即戦力になります。

## 詳細解説
- 何が変わるか：unionは「この変数はAかBかCのどれか」という閉じた集合を宣言でき、switch式などでコンパイラが全ケース網羅を保証します。従来のobject/マーカーインターフェイス/抽象基底クラスは完全閉鎖にならないため、抜け漏れ検出が難しかった問題を解決します。
- 基本構文（例）：

```csharp
// csharp
public record class Cat(string Name);
public record class Dog(string Name);
public record class Bird(string Name);
public union Pet(Cat, Dog, Bird);
```

- 使い方：各ケース型から暗黙変換され、switch式は全ケース（およびnullableを含む場合はnull）を扱う必要があります。

```csharp
// csharp
Pet pet = new Dog("Rex");
string name = pet switch {
    Dog d => d.Name,
    Cat c => c.Name,
    Bird b => b.Name,
};
```

- null扱い：unionのValueは既定で nullable になり得るため、nullableなケースが含まれるか既定値があり得る文脈では null ケースを考慮する必要があります。
- ユニオン本体にメソッドを持たせることも可能（ボディ付きユニオン）：

```csharp
// csharp
public union OneOrMore<T>(T, IEnumerable<T>) {
  public IEnumerable<T> AsEnumerable() => Value switch {
    T single => new[] { single },
    IEnumerable<T> multiple => multiple,
    null => Array.Empty<T>()
  };
}
```

- 実行時サポート（Preview注意）：.NET 11 Preview 2では UnionAttribute と IUnion がランタイムに未導入なためプロジェクトにポリフィルを追加して試せます。カスタム実装や非ボクシング（TryGetValue/HasValue）パターンもサポートされ、ライブラリは独自ストレージ戦略を維持可能です。
- 関連機能：closed hierarchies（閉じた継承）、closed enums と合わせてC#の「網羅性」設計が強化されます。

## 実践ポイント
- すぐ試す手順：.NET 11 Preview SDK をインストール → ターゲットを net11.0 に設定 → <LangVersion>preview</LangVersion> を csproj に追加。
- 小さな導入例：APIの戻り値が単一値かコレクションか、成功/失敗の戻り値（Resultパターン）などにOneOrMoreや独自のユニオンを当てると、呼び出し側の防御コードが減り可読性が上がります。
- 本番導入の注意：現時点はプレビュー。ランタイムやIDEサポート（Visual Studio Insiders/C# DevKit Insiders）を確認し、ポリフィルや将来の仕様変更に備えておくこと。
