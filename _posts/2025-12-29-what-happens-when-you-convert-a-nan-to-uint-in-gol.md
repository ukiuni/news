---
layout: post
title: What Happens when you convert a NAN to uint in Golang - GolangでNaNをuintに変換すると何が起こるか
date: 2025-12-29T14:30:19.699Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://sakshamar.in/posts/what-happens-when-you-convert-a-nan-to-uint-golang/"
source_title: "| What Happens when you convert a NAN to uint in Golang"
source_id: 435370434
excerpt: "GoでNaN→uintの暗黙変換がCPU依存で異常値を生む実例と対策"
---

# What Happens when you convert a NAN to uint in Golang - GolangでNaNをuintに変換すると何が起こるか

## 要約
Goで浮動小数点の$NaN$をuintに変換すると、CPUアーキテクチャ（x86 vs ARM64）によって異なる整数値が出力される。無防備なキャストは環境依存のバグを生む可能性がある。

## この記事を読むべき理由
最近は開発環境と本番環境でCPUアーキテクチャが異なる（例：ローカルはx86、クラウドはAWS Graviton/ARM、開発MacはM1/M2）ことが多い。浮動小数点の扱いがプラットフォーム依存だと、検出が難しい原因不明の不具合やセキュリティリスクにつながるため、事前に対策を知っておくべき。

## 詳細解説
問題の本質は「$NaN$を整数にキャストするとき、Goランタイム自体がチェックしていない（ハードウェア命令をそのまま利用している）ため、CPUの実装差に依存した結果になる」こと。

単純な例（概念的）：
```go
package main

import "fmt"

func main() {
    a := 0.0
    b := 0.0
    fmt.Printf("result: %d\n", uint64(a/b))
}
```
ここで `a/b` は $NaN$ になるが、`uint64($NaN$)` の結果はマシンによって異なることがある。これは、浮動小数点→整数変換に使われる命令（x86系の cvtt* 系、ARM64 の相当命令など）が $NaN$ に対して定めた振る舞いがアーキテクチャ依存だからで、Go言語が変換時に明示的な $NaN$ チェックを入れていないために起きる。

他言語の挙動も試すと、C++やGoはプラットフォーム差が出ることがあり、Rustは手元の例では両方で同じ結果になった（言語／実装に依存するため一概には言えないが、実運用で差が出る可能性は常にある）。

## 日本市場との関連性
- クラウド移行：AWSのGraviton（ARM）やAzureのARM VMを採用するケースが増えている。x86でしか検証していないコードが本番で挙動を変える危険性がある。
- 開発環境の多様化：M1/M2搭載MacやRaspberry Pi等のARMボードで動作検証が必要なプロダクト（IoT、エッジ）では特に重要。
- CI/CD：GitHub Actionsや自社CIランナーが混在するチームでは、アーキテクチャ差を考慮したテストが必須。

## 実践ポイント
- 明示的にチェックする：変換前に math.IsNaN を使って $NaN$ を検出し、適切なフォールバックを用意する。
- 安全な変換関数を作る：暗黙のキャストを避け、エラーや既定値を返すユーティリティを使う。
- テストを多様なアーキテクチャで回す：x86とARMでユニットテスト／統合テストを実行し、差異を早期に検出する。
- 内部表現で検査する：必要なら math.Float64bits でビットパターンを確認して $NaN$ や符号付きの特殊値を扱う。
- 例（安全な変換のサンプル）：
```go
package main

import (
    "fmt"
    "math"
)

func safeFloatToUint64(f float64) (uint64, error) {
    if math.IsNaN(f) {
        return 0, fmt.Errorf("cannot convert NaN to uint64")
    }
    if f < 0 {
        return 0, fmt.Errorf("negative float cannot convert to uint64")
    }
    return uint64(f), nil
}

func main() {
    f := math.NaN()
    if v, err := safeFloatToUint64(f); err != nil {
        fmt.Println("error:", err)
    } else {
        fmt.Println("value:", v)
    }
}
```
- コードレビューで「暗黙のfloat→intキャスト」をチェックするルールを追加する。

短く言えば、$NaN$ のまま暗黙にキャストするとアーキテクチャ依存の不可解な動作を招く可能性がある。特に多様な環境で動くサービスやCIを運用しているチームは、早めに防御策を導入しておこう。
