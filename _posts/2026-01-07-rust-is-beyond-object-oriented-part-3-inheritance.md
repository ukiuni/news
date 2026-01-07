---
  layout: post
  title: "Rust Is Beyond Object-Oriented, Part 3: Inheritance (2023) - Rustはオブジェクト指向を超える（その3）：継承"
  date: 2026-01-07T08:14:53.183Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://www.thecodedmessage.com/posts/oop-3-inheritance/"
  source_title: "Rust Is Beyond Object-Oriented, Part 3: Inheritance :: The Coded Message"
  source_id: 46476915
  excerpt: "継承の落とし穴を解明し、Rust流の安全で具体的な置換手法を例付きで解説。"
  image: "https://www.thecodedmessage.com/img/favicon/green.png"
---

# Rust Is Beyond Object-Oriented, Part 3: Inheritance (2023) - Rustはオブジェクト指向を超える（その3）：継承
「継承」を捨てたRust — 継承の罠と実務で使える置き換え術

## 要約
継承はレコード（状態）・モジュール（実装）・インタフェース（仮想メソッド）を同名で結びつけることで便利に見えるが、多くの設計上の問題を生む。Rustはこれらを明確に分離し、継承に頼らない設計（コンポジション＋トレイト）で同等以上の表現力と安全性を提供する。

## この記事を読むべき理由
Java/C++で継承設計に慣れた開発者がRustへ移行・設計置換をする際、継承の何がまずいのか、Rustでどう置き換えるかを具体的に理解できる。日本のプロダクトでもレガシーOOPコードが残る場面で実務に直結する知見となる。

## 詳細解説
- 継承が抱える根本問題
  - 継承は「is-a」関係をコード上で表すが、実際には親クラスのフィールドを子に無名で埋め込む（implicit field）という「has-a」の糖衣に過ぎない。この不透明さが状態と振る舞いの結合、意図しないオーバーライドや副作用を生む。
  - 仮想メソッド（virtual methods）があると、クラスは「状態（record）」「実装（module）」「仮想インタフェース（interface）」という3つを同一名で兼務し、インタフェース実装が暗黙の状態依存になる。結果としてプロキシ化や別表現（DB/ネットワーク/計算）での実装が困難になる。

- Rustのアプローチ
  - Rustはstruct（レコード）／impl（実装）／trait（インタフェース）を明確に分離する。traitにはフィールドがない（状態を要求しない）ため、「traitを実装するためにこのフィールドを持て」というような暗黙ルールが存在しない。
  - 継承が必要に見える設計は、概ね「共通状態＋共通振る舞い」の組合せだが、Rustではそれを明示的なフィールド（コンポジション）とtrait（振る舞い）へ分解する。必要ならデリゲーションを使って明示的に振る舞いを委譲する。

- 動的／静的多相について
  - 継承で得られた動的ディスパッチは、Rustでは Box<dyn Trait> のようなtraitオブジェクトで表現し、静的な多相はジェネリクス（trait境界）で表現する。どちらを使うかは性能と設計のトレードオフで明確化される。
  - 「implicit virtualで驚かされる」ことがなく、仮想化は明示的に選ぶものになるため、性能や安全性の予測がしやすい。

- 簡単なコード変換イメージ
  - 継承でよく見るパターン（擬似C++）
```cpp
class Base { public: Color color; virtual void draw() = 0; };
class Square : public Base { int size; void draw() override { /*...*/ } };
```
  - Rustでは状態と振る舞いを分ける：
```rust
struct BaseState { color: Color }
trait Drawable { fn draw(&self, state: &BaseState); }

struct Square { state: BaseState, size: u32 }

impl Drawable for Square {
    fn draw(&self, state: &BaseState) {
        // state と size を使って描画
    }
}
```
  - 動的に扱いたければ Box<dyn Drawable> を使い、静的に高速化したければジェネリクスを使う。

## 実践ポイント
- 継承に頼った設計を見つけたら、まず「状態」と「振る舞い」を分離する（struct + trait）。状態は明示的なフィールドにする。
- 動的振る舞いが必要なら Box<dyn Trait>、パフォーマンスを重視するならジェネリクス（T: Trait）を選ぶ。
- デリゲーションが多くて冗長なら macros/crates（例: delegate）で補助するが、まずは手動で明示的に委譲を書くことで設計の意図を明確にする。
- 「継承でしか実現できない」と思えるケースは概してまやかし：プロキシ、ストレージ分離、別表現の実装はtraitとコンポジションで表現可能。
- 移行時は小さな単位（モジュール／型）で分解してテストを回し、traitの境界を決めることで安全にリファクタリングする。

以上を踏まえると、Rustが継承を持たないのは欠点ではなく、複雑さを隠さず設計を明示化することで長期的な保守性と安全性を得るための言語設計だと理解できます。日本の現場でも、レガシーOOPからの移行や新規設計で役立つ実践的な指針になります。
