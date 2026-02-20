---
layout: post
title: "SOLID in FP: Open-Closed, or Why I Love When Code Won't Compile - SOLIDをFPで考える：開放-閉鎖原則と「コンパイルしないコード」が好きな理由"
date: 2026-02-20T12:32:08.024Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://cekrem.github.io/posts/solid-in-fp-open-closed/"
source_title: "SOLID in FP: Open-Closed, or Why I Love When Code Won't Compile · cekrem.github.io"
source_id: 437084070
excerpt: "型とパターンマッチで拡張漏れをコンパイラが教える、Elm流OCPの実践法"
image: "https://cekrem.github.io/images/banner.jpg"
---

# SOLID in FP: Open-Closed, or Why I Love When Code Won't Compile - SOLIDをFPで考える：開放-閉鎖原則と「コンパイルしないコード」が好きな理由
「コンパイルエラーが味方になる」——型とパターンマッチで守る、もっと安全な拡張戦略

## 要約
FP（関数型プログラミング）の直和型（union types）とパターンマッチは、Open‑Closed Principle（OCP）を「コンパイラが拡張の忘れを教えてくれる」形で実現する。Elmの例で、新しいケース追加時に即座に欠落箇所を検出できることが示される。

## この記事を読むべき理由
日本でもフロントエンドやドメインロジックで状態分岐が増えがちです。ミスが本番で出る前にコンパイラで潰せる設計知識は、品質と開発速度の両方を改善します。React中心の開発現場でも、アイデアはTypeScriptの識別共用体などに応用可能です。

## 詳細解説
- OCPの定義：ソフトウェア要素は拡張に対して開かれ、修正に対して閉じているべき、という原則。OOPでは継承やラップ（composition）で「外から拡張する」設計が奨められるが、チーム運用に依存する面がある。  
- Elm（FP）のアプローチ：データ（型）と操作（関数）が明確に分離され、直和型（union type）を使うと「型に新しいバリアントを追加」した瞬間に、パターンマッチしているすべての箇所で未処理ケースがコンパイルエラーとして通知される。つまり「閉じている」側はコンパイラが担保する。

Elmの例（要点）
```elm
elm
type Notification = Success String | Warning String | Error String

view : Notification -> Html msg
view notification =
  case notification of
    Success msg -> div [ class "success" ] [ text msg ]
    Warning msg -> div [ class "warning" ] [ text msg ]
    Error msg   -> div [ class "error" ] [ text msg ]
```
ここに `Info String` を足すと、未対応の箇所がコンパイルエラーで全部列挙される。

- 「開く」側：既存の型に対して新しい関数（アイコン表示、ログレベル変換など）を自由に追加できる。型をいじらずに操作を増やせる。  
- トレードオフ（表現問題）：FPでは「新しい操作は楽、バリアント追加はうるさい（＝安全）」、OOPでは逆。どちらが良いかは用途次第だが、UIやアプリケーションロジックでは操作追加の方が多い傾向があり、FPのスタイルは現場で有利なことが多い。

React（OOP/コンポーネント）例（比較）
```javascript
javascript
const NotificationBase = ({ message, className }) =>
  <div className={`notification ${className}`}>{message}</div>;

const SuccessNotification = (props) => <NotificationBase {...props} className="success" />;
const InfoNotification    = (props) => <NotificationBase {...props} className="info" />;
```
コンポーネント拡張は静かだが、アイコンや解析ロジックの更新漏れをコンパイラが教えてくれない。

## 実践ポイント
- ElmやOCaml、Reason、F#など直和型を持つ言語を使える部分は採用検討する（小さなコンポーネントや状態機械から試す）。  
- TypeScriptなら「識別共用体（discriminated unions）」で似た効果を得られる（厳格な --strict をオンに）。  
- 既存のReactコードベースでも、状態を型で表現し、パターンマッチ的（switch＋neverチェック）に扱う習慣を付けると安全性が上がる。  
- 新しいバリアントを追加したら、コンパイラ／型チェッカーが出す未処理ケースを必ず潰す。これが本質的な「閉鎖」維持の鍵。

以上。次回は「Liskov Substitution」のFP的再解釈がテーマです。
