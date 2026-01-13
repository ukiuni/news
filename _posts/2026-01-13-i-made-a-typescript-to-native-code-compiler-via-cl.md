---
layout: post
title: "I made a TypeScript to native code compiler via CLR and NativeAOT - TypeScriptをネイティブコードに変換するコンパイラを作った"
date: 2026-01-13T17:34:48.033Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/tsoniclang/tsonic"
source_title: "GitHub - tsoniclang/tsonic: Compile TS to native code via NativeAOT"
source_id: 1044714855
excerpt: "TypeScriptをC#経由で単一ネイティブ化し、Node不要で高速起動を実現するTsonicとは"
image: "https://opengraph.githubassets.com/fed1974bdbfab93b1c256f97b598c46e2e395cd99ebe5f5ac9ae018eed0af599/tsoniclang/tsonic"
---

# I made a TypeScript to native code compiler via CLR and NativeAOT - TypeScriptをネイティブコードに変換するコンパイラを作った
TypeScriptでそのまま「単一ファイルのネイティブ実行ファイル」を作れる時代が来た――TsonicでJS/TSをネイティブ化して配布コストと起動時間を劇的に削る方法

## 要約
TypeScriptのソースをC#に変換し、.NET NativeAOTで単一の自己完結型ネイティブ実行ファイルを生成するオープンソース工具「Tsonic」を紹介する。Node不要で.NETライブラリへ直接アクセスできるのが特徴。

## この記事を読むべき理由
日本の現場では配布や起動時間、セキュリティの観点から単一バイナリやネイティブ実行が求められることが多い。TypeScriptの開発生産性を維持しつつ、.NETエコシステムの性能や入出力機能を活かせる選択肢は魅力的だ。

## 詳細解説
- 仕組み
  - TsonicはTypeScriptコードを内部でC#に変換（生成）し、.NET 10 SDKのNativeAOTを使ってネイティブ実行ファイルを作る。結果は単一ファイルで自己完結（single-file, self-contained）。
  - TypeScript側からは @tsonic/dotnet/* というESMモジュールをimportすることで .NET BCL（System, System.IO, Collections など）を直接呼べる。
  - オプションでJS風APIを使う @tsonic/js が用意されている。

- 主要機能
  - TypeScript → ネイティブ実行ファイル（NativeAOT）
  - .NETフレームワークと完全に相互運用（NuGetやDLLを導入可能）
  - ES module準拠のimport（.js指定）
  - マルチパッケージ（npm workspaces）対応でライブラリ/アセンブリ分割が可能

- CLIとワークフロー（代表的コマンド）
  - tsonic project init — プロジェクト初期化（src/App.ts, tsonic.json, package.jsonなど生成）
  - tsonic build <entry> — ネイティブ実行ファイルをビルド
  - tsonic run <entry> — ビルドして実行
  - tsonic add nuget <id> <ver> — NuGetパッケージ追加
  - tsonic generate <entry> — C#コードのみ生成（デバッグに有用）

- 要件と注意点
  - Node.js 22+、.NET 10 SDKが必要。macOSではXcode CLI Toolsが必要になる場合がある。
  - 現状は成熟途上（小規模なコミュニティ、リポジトリはアクティブだが実験的）ため商用導入前に互換性やパフォーマンス確認が必須。
  - 一部のNode固有APIやネイティブモジュールはそのままでは動かない可能性あり（.NET側への橋渡しが必要）。

- 開発者向け内部展開
  - 生成されるC#コードは generated/ 配下に出力されるので、問題解析や最適化のために確認できる。
  - 出力バイナリは out/ に置かれる。npmワークスペースと組み合わせれば複数アセンブリの管理も可能。

## 実践ポイント
- まず手元で試す（推奨）
  1. 前提を満たす：Node.js 22+、.NET 10 SDKをインストール
  2. グローバルインストールと初期化
     ```bash
     npm install -g tsonic
     mkdir my-app && cd my-app
     tsonic project init
     ```
  3. ビルドと実行
     ```bash
     npm run build   # 出力は ./out/app
     ./out/app
     # あるいは
     npm run dev
     ```

- 最小のTypeScript例（そのまま試せる）
  ```TypeScript
  import { Console } from "@tsonic/dotnet/System.js";

  export function main(): void {
    Console.writeLine("Hello from Tsonic!");
  }
  ```

- 実運用で気をつけること
  - ターゲットプラットフォーム指定（--rid）や最適化（--optimize size|speed）を適切に設定する。
  - 外部ライブラリは tsonic add nuget / add package でバインディング生成してから使う。
  - VS Codeなら生成されたC#やビルドログをエディタと統合ターミナル／出力パネルで確認するとデバッグがスムーズ。

- 日本市場での活用シナリオ
  - CLIツールやオンプレ配布のアプリケーションをTypeScriptで速く作りたい場合に有力。
  - .NET資産（既存のNuGetライブラリ）を活かしつつ、フロントのTypeScript開発体験を保ちたいエンタープライズ案件に合う。

最後に一言：Tsonicは「TypeScriptの書き心地」を残しつつ「ネイティブ実行の利点」を享受できる面白いツールだ。まずはローカルで小さなユーティリティを1本ビルドして、生成C#とバイナリの挙動を確かめてみることを勧める。
