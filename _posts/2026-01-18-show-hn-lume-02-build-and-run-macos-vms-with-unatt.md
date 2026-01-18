---
layout: post
title: "Show HN: Lume 0.2 – Build and Run macOS VMs with unattended setup - Lume 0.2 — macOS VM を無人セットアップで構築・実行するツール"
date: 2026-01-18T19:21:10.627Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://cua.ai/docs/lume/guide/getting-started/introduction"
source_title: "What is Lume? | Cua"
source_id: 46670181
excerpt: "Apple Silicon上で無人セットアップ可能な高速macOS VMを即作成、CIや検証に最適"
---

# Show HN: Lume 0.2 – Build and Run macOS VMs with unattended setup - Lume 0.2 — macOS VM を無人セットアップで構築・実行するツール

魅力的なタイトル: Macで「即座に使える」仮想macOS環境を手元に作る — LumeでCI・自動化・安全検証がぐっと身近に

## 要約
LumeはAppleのVirtualization Frameworkをラップしたシンプルな単一バイナリで、Apple Silicon上で高速にmacOS/Linux VMを作成・実行し、無人セットアップやCI、サンドボックス用途に使えるオープンソースのツールです。

## この記事を読むべき理由
日本でiOS/macOSアプリ開発やテスト、自動化を行うエンジニアにとって、実機を複数台用意せずに異なるmacOSバージョンでの検証や安全な実行環境をローカルで素早く用意できる点は高い価値があります。Apple Siliconネイティブ動作で速度面の恩恵も大きいです。

## 詳細解説
- 仕組み：LumeはAppleのVirtualization Framework上の薄いレイヤーです。ハードウェア仮想化を使うため、CPU命令はネイティブに近い速度で実行されます。ストレージはスパースディスクを使い実使用分だけ消費。GPUはパラバーチャル化（GPU Family 5相当の基本サポート）を利用します。Rosetta 2もサポートしており、ARM上でx86バイナリを含む環境を扱えます。
- 形態：CLIで直接操作するか、`lume serve`でHTTP APIを公開してプログラム的に制御可能。CuaのComputer SDKはこのAPIを介してVM内のスクリーン操作や入力を自動化します。
- 無人セットアップ：IPSWからVMを自動でゴールデンイメージ化し、VNC＋OCRでセットアップアシスタントのクリック操作を自動化して「人手なし」で初期構成を完了できます。
- レジストリ連携：GHCRやGCSのようなレジストリと連携してVMイメージのpull/pushが可能で、共有やCI統合が簡単です。
- ユースケース：
  - macOSバージョン間でのテスト（特定バージョンをすぐに立ち上げて破棄）
  - CI/CDのローカル検証（ヘッドレス実行：`--no-display`）
  - 危険な操作のサンドボックス化（クリーンなスナップショットから即復旧）
  - AIエージェントが操作する仮想デスクトップの提供（スクリーンショット＋入力シミュレーション）
- 制約：Apple Silicon専用（Intel Macや他プラットフォーム非対応）。ライセンスはMITでオープンソースです。
- エコシステム事例：AnthropicのClaude Code用サンドボックスも同種のVirtualization Frameworkを活用しており、Lumeは同様の考え方で安全にコード実行環境を提供します。

### 触ってみるための基本コマンド例
```bash
# VMを作る（最新のIPSWを使う例）
lume create test-vm --os macos --ipsw latest

# 作ったVMを実行（ヘッドレスも可）
lume run test-vm
lume run test-vm --no-display

# HTTP APIを起動してプログラム制御する
lume serve
```

## 実践ポイント
- 今すぐ試す：公式のQuickstartに従い、手元のM1/M2/M3 Macでまず1台作ってみる。失敗してもVMを消せば済むので安心。
- CI統合：ローカルでビルドを再現してからリモートCIに流すことでデバッグ時間を短縮。自社のビルドキャッシュやイメージをGHCRに置くと効率的。
- 自動化の活用：無人セットアップ + ゴールデンイメージで、定期的にクリーン環境を再生成する運用を作ると検証の再現性が上がる。
- セキュリティ検証：未知のスクリプトや外部ツールを試す際はLume上のVMで実行して本体を守る。
- 注意点：必ずApple Silicon搭載Macで利用すること。Xcodeや開発環境のライセンスやAppleの利用規約に関する自社ルールも確認する。

興味があれば公式ドキュメントのQuickstartを参照し、まず小さなVMを立ち上げて動作感を確かめることをおすすめします。
