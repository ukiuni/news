---
  layout: post
  title: "Functors, Applicatives, and Monads: The Scary Words You Already Understand - 「ファンクター、アプリカティブ、モナド：実はあなたが既に使っている怖い言葉」"
  date: 2026-01-05T14:52:15.826Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://cekrem.github.io/posts/functors-applicatives-monads-elm/"
  source_title: "Functors, Applicatives, and Monads: The Scary Words You Already Understand · cekrem.github.io"
  source_id: 470504956
  excerpt: "Elmのmap/map2/andThenでファンクター・アプリカティブ・モナドが分かる"
  image: "https://cekrem.github.io/images/banner.jpg"
---

# Functors, Applicatives, and Monads: The Scary Words You Already Understand - 「ファンクター、アプリカティブ、モナド：実はあなたが既に使っている怖い言葉」
クリックせずにはいられないタイトル: 「怖がる必要ナシ。Elmでわかる Functor / Applicative / Monad の正体」

## 要約
専門用語に怯える必要はない。Functor／Applicative／Monad は「値が箱に入っている」状況を扱うためのパターンで、Elmでは既に日常的に使っている操作（map, map2, andThen）そのものだ。

## この記事を読むべき理由
関数型プログラミングの“恐怖ワード”を実践的な視点で剥がし、ElmやJavaScript、Haskell を横断して「何が同じで何が違うか」を短時間で理解できる。日本のプロダクトやチームで導入検討する際に説明しやすくなる。

## 詳細解説
- 共通のメンタルモデル：すべて「ラップされた値（箱・コンテナ）」の操作
  - Maybe, Result, List, Promise などが箱の例。中身があるかもしれない／複数ある／非同期で来る、という違いがあるだけ。

- Functor（map）
  - 「関数は持っているが値は箱の中」のときに使う。箱を開けずに中の値に関数を適用する。
  - Elm の例:
```elm
elm
Maybe.map String.toUpper (Just "hello")  -- Just "HELLO"
List.map String.toUpper ["hello","world"] -- ["HELLO","WORLD"]
```
  - JavaScript の [1,2,3].map はまさに Functor 的操作。

- Applicative（map2, map3, <*>）
  - 「関数も値も箱の中」に対して箱の中の関数を箱の中の値に適用する。複数の箱を組み合わせる際に便利。
  - Elm では map2/map3 として現れる（デコーダやフォーム結合で多用）。
```elm
elm
Maybe.map2 User maybeName maybeAge
-- どれかが Nothing なら全体が Nothing になる
```

- Monad（andThen / >>=）
  - 「中身に適用する関数自体が箱を返す」場合の連鎖。箱の二重化（Maybe (Maybe a)）を自動でフラット化してくれる。
```elm
elm
parseAge : String -> Maybe Int
parseAge s = String.toInt s |> Maybe.andThen (\n -> if n > 0 then Just n else Nothing)

getUserAge maybeAgeString =
  maybeAgeString |> Maybe.andThen parseAge
```
  - JavaScript の Promise.then はネストした Promise を平坦化する点で同様。

- Elm と Haskell の違い（用語と抽象度）
  - Haskell: Functor / Applicative / Monad が型クラスとして抽象化され、fmap や <*> や >>= といった汎用関数で扱える。
```haskell
haskell
fmap toUpper (Just "hello")  -- Just "HELLO"
Just toUpper <*> Just "hello" -- Just "HELLO"
```
  - Elm: 明示的に Maybe.map, List.map, Result.map といった具体名を使う。抽象化は抑え、可読性と明瞭性を優先する設計判断。

## 実践ポイント
- mental model を持つ：すべてを「箱に入った値」として考えるだけで挙動が予測しやすくなる。
- まずは Elm の map / map2 / andThen を使ってパターンに慣れる。抽象的な名前より具体的操作で理解が進む。
- デコーダ（Json.Decode）やフォーム検証では Applicative（map2/map3）が自然。個々のステップの失敗を短絡できる。
- 逐次的な失敗処理（パース→検査→変換）は Monad（andThen / >>=）でチェーンする。
- JS/TS 実務者は Promise.then や Array.map と対応づけると早く理解できる。
- 深掘りしたければ、視覚的解説（Adit Bhargava のガイド）や Haskell の型クラス解説を参照すると良い。

短くまとめると：用語に怯えるより、map と andThen を手で書いてみること。名前は後からついてくる。
