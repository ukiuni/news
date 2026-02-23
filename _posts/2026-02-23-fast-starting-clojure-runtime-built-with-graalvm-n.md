---
layout: post
title: "Fast starting Clojure runtime built with GraalVM native-image + Crema - GraalVM native-image + Cremaで高速起動するClojureランタイム"
date: 2026-02-23T09:17:32.852Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/borkdude/cream"
source_title: "GitHub - borkdude/cream: Fast starting Clojure runtime built with GraalVM native-image + Crema"
source_id: 1374037158
excerpt: "GraalVM+Cremaで約20ms起動のほぼフルJVM Clojure、実験的だがサーバレス向け"
image: "https://opengraph.githubassets.com/15612f25f5bbe057a639e01033f7d11e5149e9bb5ba6ef0c7c0ecdbce8dd99cb/borkdude/cream"
---

# Fast starting Clojure runtime built with GraalVM native-image + Crema - GraalVM native-image + Cremaで高速起動するClojureランタイム

ネイティブ実行で「ほぼフルJVM」のClojureを20msで起動する――Creamが切り拓くランタイム実験

## 要約
GraalVMのRuntimeClassLoading（Crema）とカスタムClojureを組み合わせ、ネイティブバイナリ上でruntime eval・require・ライブラリ読み込みなど「フルJVM」相当のClojureを高速起動させる実験プロジェクトがCream。現状は実験的で制約あり。

## この記事を読むべき理由
サーバレス／短命プロセスやエッジ環境で「JVMの互換性を保ちながら高速起動」を実現したい開発者にとって重要。日本でもマイクロサービスやCI/CDスクリプト、ツールの起動速度改善に直結する技術的示唆を含む。

## 詳細解説
- 構成要素  
  - GraalVM native-imageでネイティブバイナリを生成。通常のnative-imageは静的環境だが、CremaのRuntimeClassLoading（EA機能）を使うことで実行時のクラス読み込みを可能にする。  
  - Clojure本体はCrema向けに軽微変更したフォーク版を使用し、CreamバイナリにCremaインタプリタと必要パッケージを同梱している。

- 特長（技術面）  
  - runtime eval／require／JAR追加でのライブラリ読み込みが可能。definterface・deftype・gen-classなど、実行時にJVMバイトコードを生成する機能もサポート。  
  - 起動時間は約20ms（小さな例）と高速。JavaインタロップはSCIベースのBabashkaより高速に動作するケースがある（直接メソッド呼び出しになるため）。

- 制限・注意点  
  - CremaはEA機能：安定性・互換性問題あり。現状は実験的で本番運用非推奨。  
  - Java enum関連（enum.values()等）や直接呼ぶClass.forNameの一部が壊れる問題あり。http-kitや一部ライブラリは動作しない。  
  - バイナリサイズは約300MB（Cremaインタプリタと保持パッケージが原因）。  
  - Java相互運用でJDKの一部クラスを実行時に参照するため、場合によってJAVA_HOMEが必要。

- Babashkaとの比較（要点）  
  - Cream：フルJVM互換・任意ライブラリ読み込み可・Javaインタロップ強力だが大型で実験的。  
  - Babashka：軽量・成熟・小バイナリでスクリプト用途に強いがJava連携やdeftype周りに制約あり。

- ビルド／試用方法（概要）  
  - 事前にGraalVMのRuntimeClassLoading対応EAビルドが必要。カスタムClojureフォークをビルドしてnative-imageを作る手順がある。  
  - リリースバイナリが配布されているためまずはダウンロードして試すのが手早い。

簡単な実行例:
```bash
# ダウンロード済みcreamバイナリを実行（例）
./cream -M -e '(+ 1 2 3)'
# JARをクラスパスに追加してrequire
./cream -Scp "$(clojure -Spath -Sdeps '{:deps {org.clojure/data.json {:mvn/version "RELEASE"}}}}')" -M -e '(do (require [clojure.data.json :as json]) (json/write-str {:a 1}))'
```

## 実践ポイント
- まずはリリースバイナリをダウンロードして、簡単な式を実行して起動時間や互換性を確認する。  
- Javaインタロップを使う場合は環境変数JAVA_HOMEを設定して挙動を確認する。  
- ライブラリ互換性はプロジェクトごとに要検証（特にJava enumやClass.forNameを使うライブラリ）。  
- 起動速度や完全なJVM互換が必要ならCreamを、軽量スクリプト用途ならBabashkaを選択するのが現実的。  
- 日本のプロジェクトで採用する場合はバイナリサイズと安定性（EA依存）を考慮し、まずはPOCやツール用途で評価すること。

関連リンク（参照元）: Creamリポジトリ（README） — https://github.com/borkdude/cream
