---
  layout: post
  title: "A Comment-Preserving Cabal Parser - コメントを失わないCabalパーサ"
  date: 2026-01-02T12:03:23.989Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://blog.haskell.org/a-comment-preserving-cabal-parser/"
  source_title: "A Comment-Preserving Cabal Parser | The Haskell Programming Language's blog"
  source_id: 993330420
  excerpt: "コメントや空白を壊さずCabalを自動編集できるexactprinting導入の技術と実装課題を解説"
  image: "https://blog.haskell.org/images/haskell-opengraph.png"
---

# A Comment-Preserving Cabal Parser - コメントを失わないCabalパーサ
Cabalファイルを“そのまま”編集できる未来：コメント・空白・表記揺れを破壊しない正確プリンタの登場

## 要約
Cabalのパーサ／プリンタに「exact printing（バイト単位で元ファイルを再現する）」を導入する取り組み。キーはレキサーでコメントやトリビア情報を保持し、構文木の注釈に格納することで、ファイルをほぼ無損失で編集可能にすること。

## この記事を読むべき理由
CabalはHaskellパッケージ管理の中心であり、コメントやレイアウトを壊さずに自動修正や依存範囲の挿入ができれば、CIやエディタ統合（例：VS Codeの拡張／自動修正）、OSSのメンテ作業で差分ノイズを大幅に減らせる。日本のHaskellユーザーやライブラリ保守者にとって、より実用的な自動化ツールを期待できる重要な進展だ。

## 詳細解説
- 問題点の核心  
  現状のCabalパーサはコメントや空白、カンマ表記、if/elifの表記など「トリビア」を捨てて出力するため、ツールが自動で修正を施すと元の見た目が壊れ、不要な差分が生じる。例えば「モジュールがmanifestにない」と警告しても自動で追記できない、gen-boundsが端末出力に留まる、といった体験的欠陥がある。

- exact parser/printerの定義  
  exact parser/printerは、解析→出力で元のファイルとバイト単位で一致することを目指す。形式的には次の法則を満たすべき：
  $$
  \forall\ \text{cabalFile}.\ \text{IsValid(cabalFile)} \Rightarrow \text{exactPrint (exactParse cabalFile)} == \text{cabalFile}
  $$

- 実装アプローチ（主要技術）  
  1. レキサー（Alex）を変更してコメントを破棄せずTokenとして出力する。  
  2. 解析器の注釈（ann）にコメント列を格納する設計に変更。元のFieldデータ構造にCommentコンストラクタを追加する代わりに、注釈型を `WithComments ann` のように拡張して既存コードの互換性を保つ。  
  3. コメントはソース上の位置（Position）をキーにMapで保持し、未変更部分は元のバイト列をそのまま再利用して再出力する。  
  4. レキサーの状態遷移（スタートコード）を可視化して、どのコンテキストでコメントが現れうるかを解析。これが正確な復元に重要。  
  5. 型クラス設計やFunctorインスタンスの副作用（同じ注釈がネスト構造全体に付与される問題）など、実装上の落とし穴に注意を払う。

- トレードオフと課題  
  - コメントを注釈に乗せる方式は便利だが、「コメントのみのファイル」を表現できない（ただし無効なCabalファイルなので問題にならない）。  
  - Functor性により注釈がネスト階層に一括で付くことで望ましくない副作用が出る可能性。  
  - まだ完全なexact printには到達しておらず、共通スタンザのマージ停止や依存記述の空白（trivia）保持など追加作業が必要。

- 結果的なAPI変更例（概念）  
  既存の readFields :: ByteString -> Either ParseError [Field Position] に対し、コメント保持版として readFieldsWithComments :: ByteString -> Either ParseError [Field (WithComments Position)] を用意して後方互換を保っている。

## 実践ポイント
- ツール作者：Cabalを編集する自動化ツールは「pretty printer」に頼ると差分ノイズを生む。実装が取り込まれたら、コメント付きのパースAPI（readFieldsWithCommentsなど）を使い、未変更部分のバイト列を再利用する設計に切り替えると良い。  
- レポジトリ運用者：CIで自動整形を入れる場合は、exact printing対応を待つか、コメントやレイアウトを壊さないツールを選ぶと差分が減る。日本語コメントを含むファイルも同様に保護される。  
- エディタ/拡張開発者（VS Codeなど）：Language Serverやフォーマッタ拡張でCabal編集を行う際、exact print対応によりユーザーの手書きスタイルを守った自動編集が可能になる。拡張は新APIに対応する準備を。  
- コントリビューションの勧め：コメント・トリビアを壊す既存のpretty-printのテストケース（特殊な空白、カンマ表記、elifの形など）を用意して、exact printing統合時の回帰防止に貢献すると効果的。

