---
layout: post
title: "SOLID in FP: Liskov Substitution, or The Principle That Was Never About Inheritance - FPにおけるSOLID：リスコフの置換原則──継承の話ではなかった原則"
date: 2026-03-02T13:20:29.953Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://cekrem.github.io/posts/solid-in-fp-liskov-substitution/"
source_title: "SOLID in FP: Liskov Substitution, or The Principle That Was Never About Inheritance · cekrem.github.io"
source_id: 392744423
excerpt: "型で不正値を封じ、FP（Elm例）でLSP違反を防ぐ具体手法を示す"
image: "https://cekrem.github.io/images/banner.jpg"
---

# SOLID in FP: Liskov Substitution, or The Principle That Was Never About Inheritance - FPにおけるSOLID：リスコフの置換原則──継承の話ではなかった原則
「継承じゃない、型の約束だ」——FP視点で読み解くLSPの本質

## 要約
Liskov Substitution Principle（LSP）は「継承」の話ではなく「サブタイプの振る舞い」に関する原則で、関数型言語（この記事ではElm）では多くの違反が言語機能で防止でき、あとは意味的契約を型で表現すれば安全性が大きく向上する、という主張です。

## この記事を読むべき理由
日本でも可用性や信頼性が求められる開発（金融、組込み、業務系）で、誤った実装が呼び起こすバグを減らすには「言語や型で意味を表現する」アプローチが有効です。本記事はその実践法をFPの具体例で示します。

## 詳細解説
- LSPの本質：Uncle Bobの言葉を解釈すると「あるインターフェースを使うコードが、そのインターフェースの実装によって混乱してはならない」ということ。継承という機構自体が問題なのではなく、呼び手が期待する振る舞い（意味）を実装が裏切ることが問題。
- FPの利点（Elmの例）：Mutationや例外、nullなどLSP違反を生みやすい要因を言語が持たないため、多くの典型的違反は構造的に不可能になる。つまり「compiler prevents many LSP violations」。
- 残る課題＝意味的契約：型が示すのは「形（shape）」だけで、値の意味（例えば割引が0〜1であること）は表現できないときがある。これがLSP違反を引き起こす余地を残す。
- 解決策：不正な値を表現不能にする。Elmなら不透明型とスマートコンストラクタで、意味的制約を型レベルに移せる。例：DiscountをFloatの別型として定義し、不正なFloatが作れないようにすることで、期待する契約をコンパイラに担保させる。

例（Elm風のスマートコンストラクタ）：
```elm
module Discount exposing (Discount, fromFloat, toFloat)

type Discount = Discount Float

fromFloat : Float -> Maybe Discount
fromFloat value =
    if value >= 0 && value <= 1 then
        Just (Discount value)
    else
        Nothing

toFloat : Discount -> Float
toFloat (Discount v) = v
```

この設計だと、-0.2のような不正値はそもそもDiscountを構築できず、呼び側で明示的に扱う必要が出るためLSP違反が防げます。

## 実践ポイント
- ドメインの不変条件は型で表現する（不透明型＋スマートコンストラクタ）。  
- 副作用・例外・nullが原因のクラスの違反はFPで大幅に減る。  
- Elmが無理なら、TypeScriptのブランド型やRustの新型、Kotlinのvalue classで同じ発想を適用する。  
- テストは依然重要だが、まずは「不正値を作れない」設計でバグの表面積を減らす。
