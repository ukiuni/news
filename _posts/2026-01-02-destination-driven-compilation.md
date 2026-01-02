---
  layout: post
  title: "Destination Driven Compilation - 宛先駆動コンパイル"
  date: 2026-01-02T17:08:18.078Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://tailrecursion.com/~alan/Lisp/DestinationDrivenCompilation.html"
  source_title: "DestinationDrivenCompilation"
  source_id: 1013668428
  excerpt: "コンパイラ設計でIIFEや一時変数を削減し、可読性と実行効率を高める宛先駆動手法"
  ---

# Destination Driven Compilation - 宛先駆動コンパイル
IIFE を激減させ、生成コードを人間に近づける「宛先駆動」コンパイラ設計

## 要約
従来の「式／文」コンテキスト（expression vs statement）で出力を切り替える方式は、値を無理やり作るためのラッパー（IIFE）や一時変数を生みがちだが、ノードを「値/副作用/末尾返却（value/effect/tail）」という宛先に向けて生成する方式にするとシンプルで効率的なコードが得られる。

## この記事を読むべき理由
TypeScript→JavaScript トランスパイラや、ミニマルなランタイムを狙うコンパイラを作る日本の開発者にとって、生成コードの可読性・実行効率・バンドルサイズ改善は直接的な利益になる。特にフロントエンドやサーバレスのコールドスタートでは、IIFE と不必要な一時変数の削減は効果が大きい。

## 詳細解説
- 文脈依存出力（context-sensitive emission）  
  多くのブラケット言語（JavaScript/Cなど）をターゲットにするコンパイラは「このノードは式として出すか、文として出すか」をノードに持たせ、子ノードへフラグを伝搬する手法を取る。利点はホスト言語の構文に対応しやすい点だが、表現上の不一致を埋めるために以下の問題が出る：
  - 式が必要な位置で値を作るための余計なラッパー（IIFE）を生成する
  - 子ノードがデフォルトで値を生成するため不要な一時変数が増える
  - 結果として後段でデッドコード除去や最適化パスが増える

- 宛先駆動コンパイル（destination-driven compilation）  
  ノードを「どこへ向かって生成するか（値を出す／副作用を行う／末尾で返す）」という観点で扱う。主な効果：
  - wrapper の除去：副作用宛先なら直線的な文を出すだけで済む（IIFE不要）、末尾宛先なら直接 return を出せる
  - 一時変数削減：値宛先のみローカルを導入するので temp の発生を制御できる
  - 子ノードが親と同じ宛先を継承できるため、未使用の値を捨てたり、末尾位置で直接 return を生成できる

- 具体例（概念的）  
  ソース（Lisp風）:
  ```lisp
  (let [x (if test (f) (g))]
    (h x))
  ```
  文脈依存出力（式が必要で IIFE を使う例）:
  ```javascript
  var x = (function(){
    if (test) { return f(); } else { return g(); }
  })();
  h(x);
  ```
  宛先駆動出力（値宛先を明示して直接代入）:
  ```javascript
  var x;
  if (test) { x = f(); } else { x = g(); }
  h(x);
  ```
  後者はそのまま人間が書く最適な JS に近く、不要なラッパーや temps を生まない。

- 背景・出典  
  この手法は Kent Dybvig によって広められ、ClojureScript のエミッタが採る式／文フラグとは対照的である。ターゲットが「文と式の明確な分離」を持つ言語（JS/C等）なら特に恩恵が大きい。

## 実践ポイント
- エミッタ API を「destination (value|effect|tail)」パラメータで統一する（子ノードへ継承）。
- 末尾位置や返却が確定する場所を静的に検出して tail 宛先を指定する（直接 return を出力）。
- 値が不要な箇所では副作用宛先にして、値生成を省く。値が必要な箇所だけローカルを作る。
- まずはホットパス（頻繁に呼ばれる小関数やループ内）で導入して、生成コード差分・バンドルサイズ・実行プロファイルを比較する。
- JavaScript 向けなら V8/Node でのプロファイルと sourcemap を重視し、IIFE 削減が最適化に与える影響を測る。

参考：Kent Dybvig の議論および ClojureScript の :context フラグ実装を読むと設計上のトレードオフが理解しやすい。
