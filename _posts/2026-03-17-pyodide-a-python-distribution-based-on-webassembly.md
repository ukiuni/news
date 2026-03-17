---
layout: post
title: "Pyodide: a Python distribution based on WebAssembly - WebAssemblyベースのブラウザ/Node.js向けPython配布「Pyodide」"
date: 2026-03-17T09:07:13.112Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/pyodide/pyodide"
source_title: "GitHub - pyodide/pyodide: Pyodide is a Python distribution for the browser and Node.js based on WebAssembly · GitHub"
source_id: 47367298
excerpt: "ブラウザ上でNumPy/Pandasが動くPyodideで即時クライアント解析"
image: "https://opengraph.githubassets.com/75da9c71a349cedfd40f582ef1cb4b0d7d13ee0a289daf1d874fcaceec88cbf7/pyodide/pyodide"
---

# Pyodide: a Python distribution based on WebAssembly - WebAssemblyベースのブラウザ/Node.js向けPython配布「Pyodide」
ブラウザ上でそのまま動くPythonを使って、データ処理や可視化をクライアント側で完結させる—Pyodideが実現する「ブラウザ内データサイエンス」の全貌

## 要約
PyodideはCPythonをWebAssembly（Emscripten）で動かすプロジェクトで、ブラウザやNode.js上で多くのPythonパッケージ（NumPy, pandas, SciPy, Matplotlib, scikit-learn等）を動作させ、JS⇄Pythonの双方向インターフェースを提供します。

## この記事を読むべき理由
ブラウザ中心のサービスや社内ツールが増える日本市場で、インストール不要でPythonコードを配布・実行できる点は、教育、データ可視化ダッシュボード、プロトタイピング、オフライン対応アプリ開発に直結する実用的な選択肢になります。

## 詳細解説
- コア技術
  - CPythonをWebAssemblyへ移植（Emscriptenベース）。ブラウザがPython実行環境になる設計。
  - JavaScript⇄PythonのFFIを備え、例外処理やasync/awaitを含む高度な相互運用が可能。
- パッケージ互換性
  - micropipでPyPIの純Pythonパッケージをインストール可能。
  - C/C++/Rust拡張を持つ主要ライブラリ（NumPyなど）も多数ビルド済みで利用可能。ただし全てのネイティブ拡張が対応しているわけではない。
- 実行環境
  - ブラウザとNode.js双方をサポート。ブラウザではWeb APIへ直接アクセスできるため、DOMやWebSocket等と組み合わせたインタラクティブなアプリが作れる。
- プロジェクト構成と運用
  - パッチを当てたCPython本体、FFIレイヤー、JSでのインタプリタ管理、Emscriptenプラットフォーム定義、クロスビルドツールチェーンで構成。
  - オープンソース（MPL-2.0）。コミュニティ主導で開発・スポンサー支援あり。
- 制約と注意点
  - WASM初期ロードとバンドルサイズ、ブラウザのメモリ制約、全てのネイティブ拡張未対応など、パフォーマンス/互換性面の考慮が必要。

## 実践ポイント
1. まずは公式REPLで試す（pyodide.org）。インストール不要で実動作を確認できる。  
2. CDNから読み込んで簡単に実行（例）:

```javascript
import { loadPyodide } from "https://cdn.jsdelivr.net/pyodide/v0.29.3/full/pyodide.js";
(async () => {
  const pyodide = await loadPyodide();
  await pyodide.runPythonAsync('print("Hello from Pyodide", __import__("sys").version)');
})();
```

3. PyPIパッケージは micropip で追加可能（ただし純Pythonホイール推奨）。大きなネイティブ依存がある場合はビルド済みパッケージを使うか、自分でクロスビルドする。  
4. 企業や教育用途では、初回ロードをサーバ側でホストしてキャッシュ戦略を練るとUXが大幅に改善する。  
5. フロントエンド（React/Vue等）と統合してクライアントでの解析・可視化を実現できるため、プロトタイプ高速化や配布の手軽さで即戦力。

短くまとめると、Pyodideは「インストール不要でブラウザにPython環境を持ち込み、既存のPythonエコシステムを活かしたインブラウザ開発」を可能にする技術で、日本のWeb開発／データ活用の現場でも使いどころが多いツールです。
