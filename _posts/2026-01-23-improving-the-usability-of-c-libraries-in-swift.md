---
layout: post
title: "Improving the usability of C libraries in Swift - CライブラリをSwiftで使いやすくする"
date: 2026-01-23T01:09:49.652Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.swift.org/blog/improving-usability-of-c-libraries-in-swift/"
source_title: "Improving the usability of C libraries in Swift | Swift.org"
source_id: 46726526
excerpt: "ヘッダを変えずAPIノートでCライブラリをSwiftらしく安全に扱う実践ガイド"
image: "https://swift.org/apple-touch-icon-180x180.png"
---

# Improving the usability of C libraries in Swift - CライブラリをSwiftで使いやすくする
Cライブラリを「書き換えずに」Swiftらしく、安全で扱いやすくする実践ガイド

## 要約
SwiftはCとの相互運用性を持つが、そのまま使うと「Cっぽい」APIになりがち。module mapとAPI notesを活用すると、ヘッダを書き換えずにSwiftらしい列挙型、メソッド、参照カウント管理、引数ラベルなどを付与できる。

## この記事を読むべき理由
既存のCライブラリをSwiftプロジェクトで再利用したいiOS/macOSエンジニアやライブラリメンテナに有益。再実装コストを避けつつ安全性と可読性を向上させられるため、日本で普及するネイティブ＋既存C資産の活用に直結する。

## 詳細解説
- 背景：そのままインポートするとCの関数名、グローバル定数、Unsafeポインタや手動参照管理がそのまま表出し、Swiftらしい記法・安全性を失う。
- 解決方針：module.modulemapでモジュール化し、API notes（.apinotes YAML）でCヘッダへ付加情報を与えてSwift側への投影を変える。ヘッダを直接編集する必要はない。
- 主要技術：
  - module map：CヘッダをSwiftモジュールとして読み込むための層を作る（例：module WebGPU { header "webgpu.h" export * }）。
  - swift-synthesize-interface：変換後のSwiftインターフェイスを確認するツール（Swift 6.2.3以降で動作検証）。
  - Enum変換：enum_extensibilityやAPI notesでC列挙をSwiftのenumに変換し、ケース名をSwift風にする。
  - 参照カウント型：SWIFT_SHARED_REFERENCE相当の情報をAPI notesで与えると、OpaquePointerの代わりにSwiftクラス（自動参照管理）として扱える。
  - 所有権注記：関数の戻り値が保持済み（returned with ownership）ならSWIFT_RETURNS_RETAINED相当をAPI notesで指定してSwift側で自動解放を行わせる。
  - 関数名／引数ラベル：SWIFT_NAME相当を用いてSwiftの引数ラベルやメソッド風呼び出しへマッピング可能。
- 注意点：一部の改善はSwift 6.2.3以降のバグ修正に依存。パッケージ構成やモジュール名をAPI notesと一致させる必要あり。

例（最小構成）
```text
module WebGPU {
  header "webgpu.h"
  export *
}
```

```yaml
# WebGPU.apinotes
---
Name: WebGPU
Tags:
- Name: WGPUAdapterType
  EnumExtensibility: closed
- Name: WGPUBindGroupImpl
  SwiftImportAs: reference
  SwiftReleaseOp: wgpuBindGroupRelease
  SwiftRetainOp: wgpuBindGroupAddRef
Functions:
- Name: wgpuDeviceCreateBindGroup
  SwiftReturnOwnership: retained
```

```c
// Cヘッダ側での意図（ヘッダを書き換えたくない場合はAPI notesで表現）
WGPU_EXPORT void wgpuQueueWriteBuffer(
  WGPUQueue queue,
  WGPUBuffer buffer,
  uint64_t bufferOffset,
  void const * data,
  size_t size
) WGPU_FUNCTION_ATTRIBUTE SWIFT_NAME("wgpuQueueWriteBuffer(_:buffer:bufferOffset:data:size:)");
```

## 実践ポイント
- Swift 6.2.3以降を使う（ツールやバグ修正が必要）。
- Cヘッダと同階層に module.modulemap と <ModuleName>.apinotes を置く（Swift Packageでは target の include 配下）。
- swift-synthesize-interface（またはXcodeのSwift interface）で変換後APIを確認し、期待通りか検証する。
- 典型的な注記：EnumExtensibility、SwiftImportAs/SwiftRetainOp/SwiftReleaseOp、SwiftReturnOwnership、関数のSwift名（引数ラベル）を使う。
- まずは小さな型（enum や一つの参照型）で試し、APIが改善されることを確認してから規模を広げる。
