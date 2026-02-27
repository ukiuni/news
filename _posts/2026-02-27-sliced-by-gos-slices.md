---
layout: post
title: "Sliced by Go’s Slices - Go のスライスにスライスされた話"
date: 2026-02-27T13:00:47.440Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://ohadravid.github.io/posts/2026-02-go-sliced/"
source_title: "Sliced by Go&rsquo;s Slices"
source_id: 1066971201
excerpt: "Goのs...展開で裏側配列が共有され、呼び出し元が意図せず変更される危険"
image: "https://ohadravid.github.io/2026-02-go-sliced/gopherNoMouthWide.webp"
---

# Sliced by Go’s Slices - Go のスライスにスライスされた話
思わず「えっ？」となるGoの振る舞い：スライスを variadic 展開すると呼び出し先と裏側の配列が共有される

## 要約
Goでスライスを variadic 展開（s...）して受け取ると、呼び出し元と呼び出し先で同じ裏側配列を参照するため、要素を代入すると元のスライスが変わります。Pythonの *args / **kwargs とは挙動が違います。

## この記事を読むべき理由
Goを使う日本のエンジニアや学習者は、関数呼び出しで意図せずスライスの中身を変更してバグを生むことがあります。特にPythonや他言語から移行している人は驚きやすいので、実務での安全対策を知るべきです。

## 詳細解説
元記事の例（要点を抜粋）：

```go
package main

import "fmt"

func main() {
    nums := []int{1, 2, 3}
    PrintSquares(nums...) // variadic expansion
    fmt.Printf("2 %v\n", nums)
}

func PrintSquares(nums ...int) {
    for i, n := range nums {
        nums[i] = n * n
    }
    fmt.Printf("1 %v\n", nums)
}
```

出力:
1 [1 4 9]
2 [1 4 9]

解説ポイント
- Goのスライスは内部的に (ptr, len, cap) の小さな構造体で、コピーで渡されても ptr が指す「裏側配列」は共有されます。variadic 展開（s...）で渡すと、関数側はその配列を指すスライスヘッダのコピーを受け取るため、要素の書き換えは呼び出し元に反映されます。
- ただし、スライス変数自体を再代入（例: nums = append(nums, 16)）すると新しい配列を作る場合があり、これは呼び出し元には影響しません（容量不足で再割当が起きた場合）。
- 比較でいうと、Python の *args はタプルになり不変なので、関数内で args[i]=... はできません。**kwargs も呼び出し先に新しい dict が渡されるため、呼び出し元の辞書は変更されません。

## 実践ポイント
- 呼び出し先で元スライスを変更させたくないときはコピーして渡す：
```go
// 安全なコピーして渡す
numsCopy := append([]int(nil), nums...)
PrintSquares(numsCopy...)
```
または
```go
numsCopy := make([]int, len(nums))
copy(numsCopy, nums)
PrintSquares(numsCopy...)
```
- 関数設計で副作用を明確化する（ドキュメントや関数名で「in-place」や「mutating」を明示）。
- 大きなスライスを頻繁にコピーするとコストが上がるので、パフォーマンスと安全性のトレードオフを意識する。

Goのスライスの「参照共有」は便利な一方で落とし穴になりやすいので、渡し方と関数の副作用を意図的に設計しましょう。
