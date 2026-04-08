---
layout: post
title: "Building a Rust runtime for Typescript - TypeScriptのためのRustランタイムを構築する"
date: 2026-04-08T18:14:47.573Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://encore.dev/blog/rust-runtime"
source_title: "What We Learned Building a Rust Runtime for TypeScript – Encore Blog"
source_id: 366812826
excerpt: "Node.jsを止めずTypeScriptを高速化するRustランタイムの設計と実装ノウハウ"
image: "https://encore.dev/assets/blog/card/rust-runtime-card.png"
---

# Building a Rust runtime for Typescript - TypeScriptのためのRustランタイムを構築する

TypeScriptのビジネスロジックはそのままに、低レイヤーをRustで再設計してNode.jsと同一プロセスで高性能・多言語対応を実現した挑戦。

## 読者を引き込む魅力的な日本語のタイトル
Node.jsを止めずに速くする — TypeScriptランタイムをRustで作った理由と実践的な学び

## 要約
EncoreチームはTypeScript向けにランタイムをGoでもTypeScriptでもなくRustで一から実装し、Node.jsプロセス内でマルチスレッドなインフラ層（HTTPライフサイクル、DBプール、pub/sub、トレーシング等）を動かす設計で大きな性能・運用上の利点を得た。

## この記事を読むべき理由
- Node.jsの単一スレッド制約やサイドカーIPCの遅延に悩む開発者に具体的な代替アーキテクチャを示す。  
- マルチ言語対応のコア設計や、JS↔︎Rustの非自明な実装課題（Promise扱い、呼び出しの返り値、キャンセル）について実装レベルの知見が得られる。

## 詳細解説
- なぜRustか：1) 将来の多言語サポートを一つの安全なコアで実現できる（Prisma等の先例）、2) tokioでインフラ層をマルチスレッドにし、Node.jsのイベントループをブロックしない性能を得られるため。  
- サイドカー（Goランタイムを別プロセス）を試したが、IPCでクエリやイベントが何度も往復して2–4msのレイテンシが積み重なり、運用面でもプロセス数が増える欠点があった。  
- 同プロセス化の実現：napi-rsを使いネイティブモジュールとしてRustをロード。ネイティブ→JSは比較的簡単だが、Rust→JSで返り値やPromiseを扱うのが難しいため、ThreadSafeFunctionをフォークしてJSの返り値（Promise含む）をRust側で捕まえ、tokioチャネルで解決する仕組みを実装した。  
- キャンセル問題：Cloud Run等でRustのFutureが途中で破棄されても、JSハンドラはNode側で動き続けるためトレースが閉じられない。これを CancellationGuard で検出し、破棄時にバックグラウンドでJSハンドラを待つ処理を行い整合性を保った。  
- APIゲートウェイを組み込み：外部プロキシを別プロセスにする代わりにCloudflareのPingoraをライブラリとして組み込み、認証やルーティング結果をメモリ共有で直接ハンドラに渡せるようにした（結果、Windows対応を追加してOSSへ貢献）。  
- クラウド抽象化：NSQ（ローカル）、GCP Pub/Sub、AWS SNS/SQSを型エクスポージャで吸収するため、ジェネリクス地獄を避けて trait オブジェクト（Arc<dyn Trait>）で実装を切り替える設計に。各プロバイダ固有の初期化/要件（OnceCellやpublisher-id等）は内部に閉じる。  
- トレーシングやオブジェクトストレージも同様にRust側で扱い、TypeScriptは純粋にビジネスロジックに集中できる構成になっている。

短いコード例（ランタイムの manager 構造のイメージ）:

```rust
// rust
pub struct Runtime {
    api: api::Manager,
    sqldb: sqldb::Manager,
    pubsub: pubsub::Manager,
    objects: objects::Manager,
    metrics: metrics::Manager,
    secrets: secrets::Manager,
}
```

## 実践ポイント
- サイドカー通信のオーバーヘッドを測ってから選択する（小さな遅延でも多数往復で累積する）。  
- Node↔Rustの双方向呼び出しではPromiseと返り値を扱える仕組み（ThreadSafeFunctionの拡張やチャネル）を用意する。  
- 外部プロキシを統合する場合は、認証コンテキスト等をプロセス内で共有できるか検討すると効率化できる。  
- 複数クラウドを抽象化するなら、ジェネリクスより trait オブジェクトと動的ディスパッチで実装差分を隠すとコードが追いやすい。  
- ローカル開発（Windows含む）も考慮してOSS依存の互換性を確認・必要なら貢献する。

元記事の実装は「TypeScriptはビジネスロジックに専念させ、インフラは高速で安全なRustに任せる」現実的なアプローチを示している。日本のクラウド/サーバレス開発現場でも参考になる設計と実装パターンが多い。
