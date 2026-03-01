---
layout: post
title: "What even are Breeze, QtQuick, QtWidget, Union..? - Breeze、QtQuick、QtWidget、Unionって一体何？"
date: 2026-03-01T20:10:11.089Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://akselmo.dev/posts/what-are-breeze-widgets-quick-union/"
source_title: "What even are Breeze, QtQuick, QtWidget, Union..?"
source_id: 1376731434
excerpt: "UnionでBreezeやQtQuick、QtWidgetsの見た目をCSS風に統一する実践ガイド"
---

# What even are Breeze, QtQuick, QtWidget, Union..? - Breeze、QtQuick、QtWidget、Unionって一体何？
魅力的タイトル: KDE開発者が教える「見た目の不一致」を一発解決するUnion入門 — BreezeからQtQuickまで簡単ガイド

## 要約
Qtの古いUI（QtWidgets）と新しいUI（QtQuick）は見た目や挙動がバラバラになりがち。KDEが進めるUnionは、CSS風の単一のスタイル定義を両者に供給して整合を取る仕組みです。

## この記事を読むべき理由
日本でもデスクトップアプリや組込みUIをQtで作る開発者が増えています。UIの一貫性やテーマのカスタマイズはユーザー体験に直結するため、Breeze／Kirigami／Unionの違いを知っておくと設計・保守で差が出ます。

## 詳細解説
- QtWidgets：従来のC++中心のUI。柔軟性は低めだが成熟している。QStyleを通じて外観を定義する。
- QStyle：ウィジェット描画用の抽象クラス。スタイルごとに描画ロジックを実装する場所。
- Breeze：KDE標準の見た目（テーマ）。QtWidgetsコンテキストだとQStyle実装として振る舞うことが多い。
  - Repo: https://invent.kde.org/plasma/breeze/
- QtQuick（QML）：宣言的にUIを書く新しい方法。C++はデータやロジックのバックエンド役に回る。
- qqc2-desktop-style：QtQuickアプリ向けにBreeze風の見た目を与えるスタイル定義。
  - Repo: https://invent.kde.org/frameworks/qqc2-desktop-style/
- Kirigami：QtQuickアプリ向けの共通コンポーネントとレイアウト単位（spacingなど）を提供するライブラリ。アプリ開発効率を上げる。
- 問題点：QtWidgetsとQtQuickでスタイルやメトリクスを別々に管理すると、微妙な不一致やメンテ性の悪化を招く。
- Unionの登場：UnionはCSSに似た単一のスタイル定義を入力に、QtQuickとQtWidgets両方に出力する「スタイルエンジン」。目標は両ツールキット間で一貫した外観を保つこと。ユーザーがカスタムCSSファイルでテーマを変えられる点も特徴。
  - Repo: https://invent.kde.org/plasma/union/
- Plasmaスタイル（SVGベース）は別系統。Unionが最終的にどう関わるかは未定。

## 実践ポイント
- 今すぐできること：
  1. Breeze / qqc2 / Kirigami のリポジトリを眺めて、どのコンポーネントが使われているか確認する（上記リンク参照）。
  2. QtQuick＋Kirigamiで新しいUIを作ると、将来のテーマ統一が楽になる。
  3. UnionのCSSサンプルでローカルにテーマを作り、QtWidgetsアプリとQtQuickアプリで見え方を比べてみる（CSSはWeb用と完全互換ではない点に注意）。
- 日本市場への示唆：
  - Linuxデスクトップや業務端末UIをQtで作る場合、早めにKirigami/Union対応を視野に入れると保守性とカスタマイズ性が高まります。

参考（公式ドキュメント）:
- QtWidgets: https://doc.qt.io/qt-6/qtwidgets-index.html
- QtQuick/QML: https://doc.qt.io/qt-6/qtquick-index.html / https://doc.qt.io/qt-6/qtqml-index.html

（元記事: What even are Breeze, QtQuick, QtWidget, Union..? — Akseli Lahtinen）
