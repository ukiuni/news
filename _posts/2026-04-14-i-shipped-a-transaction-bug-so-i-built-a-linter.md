---
layout: post
title: "I shipped a transaction bug, so I built a linter - トランザクションバグを出荷したので、linter を作った"
date: 2026-04-14T05:02:29.649Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://leonh.fr/posts/go-transaction-linter/"
source_title: "I shipped a transaction bug, so I built a linter &#183; léon h"
source_id: 47715389
excerpt: "本番で起きるトランザクション漏れをGoの静的解析で検出するカスタムlinterを作った話"
---

# I shipped a transaction bug, so I built a linter - トランザクションバグを出荷したので、linter を作った
本番で静かに起きる「トランザクションの漏れ」をコンパイル時に捕まえるために、Go の静的解析フレームワークでカスタム linter を作った話

## 要約
本番でデータ不整合を招いた「callback 型トランザクションで外側の repo を誤って使う」バグを防ぐため、Go の go/analysis を使ってトランザクション境界を越えるアクセスを検出する linter を実装した。AST と型情報を組み合わせ、コールバック引数（tx）を追跡して違反を報告する。

## この記事を読むべき理由
トランザクション漏れはコンパイルもテストも通ることが多く、日本のサービス（FinTech、EC、物流など）でも沈黙するデータ破壊を招きやすい問題です。自動化して早期に防げれば本番障害と調査コストを大幅に削減できます。

## 詳細解説
- 問題の型  
  コールバックで受け取った transaction-scoped なリポジトリ（例：tx）を使うべきところで、コンポーネントのフィールド（例：s.repo）を誤って使うと、その DB 操作はトランザクション外で動いてしまう。テストでは再現しにくく、本番高負荷時にのみ露呈する。

- 技術基盤：go/analysis  
  go/analysis フレームワークを使うと、パーサ／型情報の取り回しを気にせず Analyzer を書ける。Analyzer は Parsed AST、TypesInfo、Reportf を経由して診断を出す。

- 実装の要点  
  1. AST を絞って CallExpr を巡回し、Transaction メソッド呼び出しを検出。  
  2. Transaction のコールバック引数（tx）の型/オブジェクトを取得して「この引数がトランザクションパラメータである」ことを型の Object 比較で判定（名前照合は不可）。  
  3. コールバック内を再帰的に走査して、メソッド呼び出しの受け手がリポジトリ型かつ tx でない場合を検出して報告。  
  4. 引数で外側の repo を渡すケース（helper に非 tx repo を渡してしまう）も同様に検出。  
  5. helper のチェーンでは、トランザクションパラメータが引数として伝播する箇所で再帰的に解析し、各関数を一度だけ解析することで無限ループを防止。  

- テストと実行  
  analysistest を使えば、// want コメントで期待される診断を記述するテストが書ける。CLI は singlechecker で簡単に公開でき、golangci-lint に組み込む運用も可能。

- 注意点  
  リポジトリ型や Transaction の識別はプロジェクト固有なので、一般化には限界がある。まずは自分のコードベースに合わせたルールで導入するのが現実的。

## 実践ポイント
- まずは小さな Analyzer を作る：go/analysis のテンプレートから CallExpr をフィルタするところまで実装してみる。  
- tx を型の Object で比較する実装を採用し、変数シャドーイングにも強くする。  
- helper 呼び出しの伝播を追う再帰解析を入れて、チェーン中の末端での誤使用も捕まえる。  
- analysistest で期待診断（// want）を用意して回帰テストを整備する。  
- CI（例えば golangci-lint や repo のビルドパイプライン）に組み込み、本番リスクを事前に低減する。  
- 日本の現場では GORM 等の ORM やリポジトリパターンを使うケースが多いので、プロジェクト固有の型名／パッケージ名をルール化しておくと効果的。

参考実装の核心（例：誤った呼び出し）：
```go
// go
// バグ例: s.repo を使っている（tx を使うべき）
return s.repo.Transaction(ctx, func(tx models.Repo) error {
    user, err := s.repo.GetUser(ctx, userID) // ← ここがトランザクション外
    if err != nil { return err }
    return tx.SaveUser(ctx, user)
})
```

このアプローチは「構造的なミス」をソースコードレベルで捕まえる有効な手段です。まずは自分のリポジトリ構造に合わせた小さな linter を作って CI に流し、本番事故を未然に防ぎましょう。
