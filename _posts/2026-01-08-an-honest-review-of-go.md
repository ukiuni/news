---
layout: post
title: "An Honest Review of Go - Go言語の率直なレビュー"
date: 2026-01-08T16:18:15.352Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://benraz.dev/blog/golang_review.html"
source_title: "An Honest Review of Go - Ben Raz Blog"
source_id: 46542253
excerpt: "Goの並行処理は強力だが、enumや不変性、エラー設計の欠点をツールと設計で補う実践術を解説"
---

# An Honest Review of Go - Go言語の率直なレビュー
Goは本当に仕事で使える？ 並行処理の強みと設計上の“困りごと”を正直に解説

## 要約
Goは並行処理の扱いやすさとシンプルな型システムが強みだが、列挙型（enum）や不変性、エラー表現など設計上の欠点が開発者の生産性に影響することがある、という率直な評価。

## この記事を読むべき理由
日本のサーバー／クラウド開発現場ではGo導入が進んでおり（マイクロサービス、Kubernetes周りなど）、Goの長所と短所を現実的に把握することは採用判断や既存コードの改善に直結するため必読。

## 詳細解説
- 並行処理（長所）
  - Goroutineとchannelが言語レベルで用意されているため、軽量スレッド＋メッセージパッシングで並行処理を書きやすい。selectによる待ち合わせも自然で、よく設計すれば競合やデッドロックを抑えやすい。
- 型システム（長所）
  - 継承はなく、struct埋め込み（embedding）でメソッドを再利用する設計。インターフェイスは暗黙的に充足され、テストダブルや抽象化がシンプルにできる。
  - 例（埋め込み）:
  
```go
type Animal struct{}
func (a Animal) DoSomething() {}

type Dog struct{ Animal }

func main() {
    Dog{}.DoSomething() // DogはAnimalのメソッドを継承的に使える
}
```

- 文法・エルゴノミクス（長所）
  - 宣言が簡潔で可視性は大文字小文字で制御。冗長なアクセス修飾子が不要な点は書きやすい。

- 列挙型の欠如（短所）
  - 明示的なenumがなく、iotaで整数定数群を作るのが一般的だが「閉じた集合」を型システムが保証しないため、予期しない値が混入するリスクがある。

```go
type State int
const (
    Off State = iota
    On
    Error
)
```

- 不変性（短所）
  - constはコンパイル時定数に限定され、構造体やマップなどを真に不変にできない。公開変数をやむなくvarで持つと外部から改変されるリスクがあるため、ゲッターで隠蔽する等の工夫が必要。

- エラー設計（短所）
  - errorは単一メソッド Error() string を持つインターフェイスで、元の具体型の情報を失いがち。errors.Is / errors.Asなどでラッピングや型アサーションはできるものの、列挙型や合成型（sum type）が持つ「意味のあるエラー値」には劣る、という指摘がある。
  - Goは複数戻り値を使うが、タプル型が言語レベルで存在しないため、(T, error)を値として扱う柔軟性は限定される。

## 実践ポイント
- 並行処理を活かす：goroutine＋channelで設計し、context.Contextでキャンセル/タイムアウトを統一する。sync.WaitGroupやselectで整然と制御する。
- enumの代替：iotaを使うなら必ずvalidation関数を用意し、String()実装＋go:generateで列挙値チェックを自動化する（linters とテストで補完）。
- 不変性の確保：公開データはコピーを返すか、公開は読み取り専用の関数（getter）経由にしてミューテーションを防ぐ。
- エラー設計：カスタム型を定義して errors.Is / errors.As を利用する、あるいはエラーに追加情報を持たせたラップ（%w）を使って扱いやすくする。ライブラリ設計時はエラーの型設計に特に注意する。
- ツールを活用：go vet, golangci-lint, go test を導入し、enumや不変性に関するルールをCIで自動検出する。

この記事のポイントを採用すれば、Goの「並行処理の強み」を生かしつつ、言語設計の弱点をツールと設計ルールで補うことができる。
