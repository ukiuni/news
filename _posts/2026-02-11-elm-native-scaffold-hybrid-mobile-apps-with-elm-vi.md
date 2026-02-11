---
layout: post
title: "elm-native – scaffold hybrid mobile apps with Elm, Vite, and Capacitor - elm-native：Elm・Vite・Capacitorでハイブリッドモバイルアプリを素早く立ち上げる"
date: 2026-02-11T12:13:59.609Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://cekrem.github.io/posts/elm-native/"
source_title: "elm-native – scaffold hybrid mobile apps with Elm, Vite, and Capacitor · cekrem.github.io"
source_id: 444363511
excerpt: "npxでElm＋Vite＋Capacitor雛形を即生成、型安全にネイティブ機能を試せる"
image: "https://cekrem.github.io/images/banner.jpg"
---

# elm-native – scaffold hybrid mobile apps with Elm, Vite, and Capacitor - elm-native：Elm・Vite・Capacitorでハイブリッドモバイルアプリを素早く立ち上げる

「npx elm-native」でElm製モバイルアプリがワンコマンドで立ち上がる — コンパイラの安全性を活かしたモダンなハイブリッド開発の最短ルート

## 要約
npx elm-native my-app で Elm + Vite + Capacitor の雛形が生成され、iOS/Android のネイティブシェル付きアプリをすぐに扱えます。UIは Elm、ビルドは Vite、ネイティブ連携は Capacitor が担当します。

## この記事を読むべき理由
Elm の型チェックでバグを早期に防ぎつつ、Capacitor によるネイティブ機能（カメラ／GPS／Safe Area など）を手軽に試せます。短時間でプロトタイプを作りたい日本の開発者やチームに向いた選択肢です。

## 詳細解説
- スキャフォールド：npx elm-native my-app でテンプレートをコピーし、npm install と npx cap add ios/android を自動実行。非対話でセットアップできるのがポイント。
- アーキテクチャ：
  - Elm：UI とアプリロジック（TEA パターン）を担当。flags 経由でネイティブ側情報を受け取る。
  - Vite：vite-plugin-elm を使って Elm を高速にビルド・ホットリロード。
  - Capacitor：Web アプリをネイティブシェルにラップし、プラグインでデバイス機能へアクセス。
- JavaScript ブリッジ：デバイス情報（例：Safe Area の top ピクセル）を取得して Elm に渡す薄い層だけを書けば良い設計です。例：

```javascript
import { Elm } from "./Main.elm";
import { SafeArea } from "capacitor-plugin-safe-area";

async function start() {
  let safeAreaTopInPx = 0;
  try {
    const { insets } = await SafeArea.getSafeAreaInsets();
    safeAreaTopInPx = insets.top;
  } catch (_) {
    // Safe area not available (e.g. browser dev)
  }
  Elm.Main.init({ flags: { safeAreaTopInPx } });
}
start();
```

- Elm 側の受け口は flags を使う典型パターンです（カウンターのテンプレートなど）。プラグインを入れて ports を経由すれば、カメラや GPS も従来の Web→ネイティブパターンで扱えます。

```elm
type alias Flags = { safeAreaTopInPx : Int }

init : Flags -> ( Model, Cmd Msg )
init flags =
  ( { count = 0, safeAreaTopInPx = flags.safeAreaTopInPx }, Cmd.none )
```

- コマンド例：
  - npm run dev — Vite 開発サーバ
  - npm run sync — ビルドしてネイティブプロジェクトに同期
  - npm run open:ios / npm run open:android — Xcode / Android Studio で開く

## 実践ポイント
- まず試す：Node と Capacitor の前提を満たし、npx elm-native my-app を実行して雛形を起動。
- Safe Area や画面サイズは早めに考慮：スマホのノッチやステータスバー対策は初期から flags で渡すと楽。
- ネイティブ機能：必要な Capacitor プラグインを npm で追加し、ports を通して Elm と接続する。
- ビルド運用：実機での動作確認、署名やストア用の設定はネイティブ側（Xcode / Android Studio）で行う。CI に組み込むなら native build スクリプトを用意する。
- 日本市場向け注意点：複数端末（特に Android の多様な画面比）での Safe Area/フォント・UI サイズ検証を入念に。法的／配布面では App Store／Google Play の審査要件も忘れずに。

小さな MVP を素早く作って動かしたいなら、Elm の安全性と Capacitor の移植性の組み合わせは試す価値があります。GitHub のリポジトリ（elm-native）をチェックして、まずはワンコマンドで動かしてみてください。
