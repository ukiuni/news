---
layout: post
title: "C++ ♥ Python - Alex Dathskovsky - CppCon 2025 - C++ は Python を愛す"
date: 2026-01-17T14:05:51.171Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.youtube.com/watch?v=9uwDMg_ojdk"
source_title: "C++ ♥ Python - Alex Dathskovsky - CppCon 2025 - YouTube"
source_id: 424612711
excerpt: "pybind11やGIL対策でC++とPythonを高速安全に結合する実践ガイド"
image: "https://i.ytimg.com/vi/9uwDMg_ojdk/maxresdefault.jpg"
---

# C++ ♥ Python - Alex Dathskovsky - CppCon 2025 - C++ は Python を愛す
C++ と Python を“いいとこ取り”する実践ガイド：パフォーマンスと生産性を両立させる現場の技術

## 要約
C++ と Python を組み合わせる現実的な手法と落とし穴（GIL、メモリ管理、バインディング手法）を、CppCon 2025 のプレゼンから抽出してわかりやすく解説する。

## この記事を読むべき理由
日本のソフトウェア開発では、ロボティクス、組込み、金融、機械学習などで「高速なコアを C++、上位ロジックを Python」で組むケースが増えている。両者を安全かつ効率的に結合する方法を知れば、開発速度と実行性能を同時に改善できる。

## 詳細解説
Alex Dathskovsky の講演は、C++ と Python のインターオペラビリティ（相互運用）に関する現場ノウハウが中心。主な技術ポイントは次の通り。

- バインディング手法の選択肢  
  - pybind11：モダン C++ に馴染むヘッダオンリー。型変換や例外伝播が簡単。  
  - C API / CPython：最も低レベルで安定だが記述が冗長。拡張や組込みに向く。  
  - Cython：C 言語ライクな宣言で効率的に C/C++ を呼べる。型注釈で高速化可能。  

- パフォーマンスとオーバーヘッド  
  - 計算コアは C++ へ移すのが常套手段。Python ↔ C++ の呼び出しはコストがあるため、粒度（呼び出し回数）に注意。  
  - 大量データの受け渡しはバッファ参照（NumPy のビュー）を使いコピーを避ける。

- スレッドと GIL（Global Interpreter Lock）  
  - C++ 側で長時間実行する処理は pybind11 の `gil_scoped_release` などで GIL を解放して並列性を確保する。だが Python オブジェクトにアクセスする際は再取得が必要。

- ライフタイム管理と例外伝播  
  - 所有権（誰が delete/解放するか）を明確に。スマートポインタの扱いや、Python 側で参照されているオブジェクトの寿命を保証する API 設計が重要。  
  - 例外は C++→Python、Python→C++ 双方向に変換して安全に扱う実装を行う。

- ビルドと配布の実務  
  - CMake（scikit-build, pybind11 の CMake サポート）でクロスプラットフォームビルドを自動化。  
  - 日本向けなら Windows と Linux (特に Ubuntu) をターゲットにテスト、バイナリ配布は wheel（manylinux）を検討。

## 実践ポイント
- 小さく始める：まずは「計算の重い関数1個」を C++ に移して pybind11 でラップし、ベンチする。  
- 使うツールの選択基準：
  - 素早いプロトタイプ → pybind11 / Cython  
  - 最大の互換性と制御 → CPython C API  
- GIL ポイント：長時間ループや数値計算は C++ に寄せ、必要時に GIL を解放する。  
- データ受け渡し：NumPy 配列のメモリビューを使いコピーを避ける。  
- ビルド＆配布：CMake + scikit-build で wheel を作成し、CI（GitHub Actions 等）で Windows/Linux/macOS のテストを回す。  
- 日本市場での応用例：ロボット制御（ROS と併用）、金融の高頻度処理、組込み向け制御ロジックの高速化。

参考として、pybind11 の最小例（C++ 側のエクスポートと Python 呼び出し）：

```cpp
// cpp: add.cpp
#include <pybind11/pybind11.h>

int add(int a, int b) { return a + b; }

PYBIND11_MODULE(example, m) {
    m.def("add", &add, "A function that adds two integers");
}
```

```python
# python: test.py
import example
print(example.add(2, 3))  # 5
```

最後に：まずは小さなケースで C++ と Python の組合せを試し、バインディング、GIL、メモリの扱いに慣れること。CppCon の講演は具体的なティップスが豊富なので、実装に行き詰まったら動画を直接参考にすると効果的。動画はこちら（英語）：https://www.youtube.com/watch?v=9uwDMg_ojdk
