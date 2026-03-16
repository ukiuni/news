---
layout: post
title: "Good Haskell Libraries - 良い Haskell ライブラリ"
date: 2026-03-16T09:03:43.506Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "http://jackkelly.name/wiki/haskell/libraries.html"
source_title: "Haskell (Libraries) | Wiki | jackkelly.name"
source_id: 694432982
excerpt: "日本の現場で役立つHaskellの隠れた名ライブラリ15選と実践的使いどころを解説"
---

# Good Haskell Libraries - 良い Haskell ライブラリ
クリックせずにはいられないタイトル: Haskellで本当に使える“隠れた名品”ライブラリ15選 — 日本の現場で役立つ使いどころガイド

## 要約
Haskellのライブラリ群から、実務で便利かつ見落とされがちな良ライブラリをカテゴリ別に厳選し、使い方や注意点をわかりやすく解説する。

## この記事を読むべき理由
日本のプロダクト開発や個人学習で「どのライブラリを選べばいいか分からない」場面は多い。ここでは互換性・実用性・運用上の注意点を踏まえ、すぐ使える候補と落とし穴を示す。

## 詳細解説
- Alternative Preludes  
  - ライブラリを書くなら標準Prelude推奨。依存を増やすと下流へ負担が行く。  
  - アプリならreludeが現実的：追加の非ブート依存が少なく、部分関数を隠すなど実用的なユーティリティを提供。NoImplicitPreludeで明示的にimportする運用がおすすめ。

- 開発者向け快適化  
  - placeholder：未実装箇所を警告付きで残せる。  
  - safe-wild-cards：RecordWildCardsの代替。未使用バインディングで警告を出す。

- データ構造系  
  - semialign：alignで「左か右か両方」の合流を扱える（These a b 型）。長さ違いのzipやMapの合流で有用。  
  - witherable：mapMaybeの一般化。多様な構造に対してフィルタ付きマップができる。

- 列挙・全列挙  
  - finitary：型レベルで集合の有界性（Cardinality）を扱い、安全な次/前/列挙を提供。GPLライセンスに注意。  
  - universe：軽量な代替で無限でない列挙に便利。

- エラー処理  
  - hoist-error：Maybe/Eitherの失敗ケースをMonadErrorに持ち上げ、本道（happy path）を簡潔に。  
  - validation-selective：Applicativeでエラーを累積するValidation実装。ドキュメント良好。  
  - monad-chronicle：Monadインスタンスが必要な場合の選択肢。ただしApplicativeでの累積度合いやWriterT類似の怠惰性（thunk肥大）に注意。

- 文字列／整形／色付け  
  - formatting：型安全な文字列整形DSL。printfより安全。  
  - safe-coloured-text：クロスプラットフォームの端末色付け。

- 正規表現  
  - Haskellではパーサーを使うことが多いが、regexが欲しいならregex-tdfaが純Haskell実装でFFI不要、移植性が高い。

- 可変状態・IO抽象化  
  - ref-tf：IOとSTの両方で動く参照操作を抽象化。テストと本番で同じAPIを使える。  
  - StateVar：参照ライクな値を抽象化する型クラス。OpenGLなど状態APIのラッパに有用。

- グラフ／探索  
  - algebraic-graphs：関数的に美しいグラフ表現。  
  - search-algorithms：BFS/DFS/Dijkstra/A*などを、グラフ表現に依存せず使える実装。

- ストリーミング  
  - streaming：好きなファンターを受け取れる柔軟なストリーム設計（Of a を用いる等）。conduit/pipesより表現力の面で利点がある場面も。  
  - ただしライブラリ間で繋ぐときは、既存エコシステムがconduitを使っていればconduitを選ぶ方が楽。

## 実践ポイント
- ライブラリ開発ではAlternative Preludeを避け、アプリならreludeを検討。ファイルごとにNoImplicitPreludeで明示import。  
- 入出力や端末表示を跨ぐCLI開発ではsafe-coloured-textを使い、WindowsとUnixでの差を吸収。  
- 正規表現は移植性重視でregex-tdfa。複雑な構文解析はパーサー（parsec/megaparsec）を優先。  
- エラーを「まとめて報告」したければvalidation-selective、Monadが必要ならmonad-chronicleだがメモリ・遅延評価の影響を測る。  
- ストリーミング処理：ライブラリ相互運用性を優先するならプロジェクトで既に使われているストリーミング実装に合わせる（conduitなど）。  
- テストしやすい設計のためにref-tfやStateVarで副作用を抽象化する。  
- finitaryのライセンスや依存の互換性は事前確認。商用プロジェクトでは特に注意。

（原著: "Good Haskell Libraries" を要約・日本語化。実務での使いどころと注意点に焦点を当てました。）
