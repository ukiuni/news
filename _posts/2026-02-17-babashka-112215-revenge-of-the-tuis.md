---
layout: post
title: "Babashka 1.12.215: Revenge of the TUIs - Babashka 1.12.215：TUIの逆襲"
date: 2026-02-17T17:52:02.578Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://blog.michielborkent.nl/babashka-1.12.215.html"
source_title: "Babashka 1.12.215: Revenge of the TUIs"
source_id: 810264660
excerpt: "Babashka 1.12.215がJLine3を同梱し即起動でリッチTUI構築と既存Clojure連携を一気に強化しました"
---

# Babashka 1.12.215: Revenge of the TUIs - Babashka 1.12.215：TUIの逆襲
即起動で作るリッチTUI！Babashka 1.12.215がTUI革命をもたらす

## 要約
Babashka 1.12.215はJLine3を同梱し、即時起動するネイティブClojureスクリプトで本格的なTUI（端末UI）を構築できるようになった大型アップデートです。REPL周り、SCI（インタプリタ）、deftype互換性なども強化され、既存ライブラリの利用やツール連携性が大幅に向上しました。

## この記事を読むべき理由
- 即時起動かつ小さなバイナリでリッチな端末アプリを作れるため、開発・CI・運用ツールのプロトタイプや配布が圧倒的に楽になります。  
- 日本の現場でもWindows対応やテストカバレッジ互換性が向上しており、既存のClojure資産を活かしやすくなりました。

## 詳細解説
- JLine3同梱＆TUIサポート  
  JLine3により歴史・タブ補完・スタイル出力・キーバインドなどがbbスクリプトから使えます。WindowsのPowerShell/cmd.exeも動作対象です。簡単な行読み取り例：
  ```bash
  # bash
  brew install borkdude/brew/babashka
  ```
  ```clojure
  ; clojure
  (import '[org.jline.terminal TerminalBuilder] '[org.jline.reader LineReaderBuilder])
  (let [terminal (-> (TerminalBuilder/builder) (.build))
        reader   (-> (LineReaderBuilder/builder) (.terminal terminal) (.build))]
    (try (loop [] (when-let [line (.readLine reader "prompt> ")]
                    (println "You typed:" line)
                    (recur)))
         (catch org.jline.reader.EndOfFileException _ (println "Goodbye!"))
         (finally (.close terminal))))
  ```

- babashka.terminal 名前空間  
  stdin/stdout/stderrが端末かを判定する `tty?` が追加。パイプ時と対話時の挙動切替（カラー表示やプログレスバー有効化など）が簡単にできます。
  ```clojure
  ; clojure
  (require '[babashka.terminal :refer [tty?]])
  (when (tty? :stdout) (println "Interactive terminal detected"))
  ```

- charm.clj互換性（即起動のTUIフレームワーク）  
  Elm風アーキテクチャの charm.clj がbbで動作。単一ファイルのカウンターなど即座にネイティブ実行でき、サンプルも提供されています。

- deftypeでのマップインターフェース対応  
  これまでbbで実装できなかった `IPersistentMap` 等をdeftypeで宣言できるようになり、core.cache等の既存ライブラリが修正なしで動作します。

- SCIの改善とRiddley/Cloverage互換性  
  macroexpand周りやdeftype/caseの展開がJVM Clojureに近づき、riddley経由のツール（cloverage等）がbbで動作可能になりました。Cloverageのテストも通っているとのことです。

- REPL体験の向上  
  rlwrap不要のマルチライン編集、Clojure-awareタブ補完、ゴーストテキスト、eldoc、ドキュメント取得、永続履歴、Ctrl+Cの挙動改善など。開発効率が上がります。

- その他の改善点（要約）  
  関数→インターフェース自動適応、型推論の強化、各種バグ修正、nREPLのスレッド動作改善、限定的な文字コード（cp437）サポート等。

- コミュニティとイベント  
  Babashka conf 2026 が開催予定（CFP募集中）。日本からの参加や発表も検討価値あり。

## 実践ポイント
- まずはインストールしてREPLを触る：
  ```bash
  # bash
  brew install borkdude/brew/babashka
  bb repl
  ```
- 対話的な端末機能を使いたいときは babashka.terminal の `tty?` を活用し、JLine3で行読み取りや補完を導入する。  
- charm.cljなどのTUIライブラリを試して、単一ファイルの即起動ツールや運用ツールをプロトタイプ化する。  
- 既存のClojureライブラリ（core.cache、cloverage等）をbbで使えるか確認して、CIや軽量ツールへ組み込む道を探る。  
- Babashka conf CFPは期日があるので、発表を考えている場合は早めに応募する。

以上を試せば、即時起動のClojureスクリプトで本格的な端末UIと既存Clojure資産の組み合わせを、すぐに現場で活用できます。
