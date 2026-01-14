---
layout: post
title: "The Unbearable Frustration of Figuring Out APIs - API を突き止める際の耐えがたい苛立ち"
date: 2026-01-14T09:51:18.853Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://blog.ar-ms.me/thoughts/translation-cli/"
source_title: "Abdul Rahman Sibahi | The Unbearable Frustration of Figuring Out APIs"
source_id: 427200851
excerpt: "SwiftでMacの翻訳機能をCLI化しAPIや非同期問題を乗り越える手順"
---

# The Unbearable Frustration of Figuring Out APIs - API を突き止める際の耐えがたい苛立ち
魅力的な日本語タイトル: 「Macの“翻訳”をCLI化したら地獄を見た — Swiftで学ぶAPIの落とし穴と対処法」

## 要約
著者は macOS のローカル翻訳機能を使ったシンプルな CLI ツールを Swift で作ろうとして、API ドキュメントの不完全さ、非同期処理、プラットフォーム指定、言語モデルのインストールといった思わぬ障害に遭遇する。最終的に NLLanguageRecognizer と TranslationSession を組み合わせ、AsyncParsableCommand ベースの動作する CLI を完成させる。

## この記事を読むべき理由
- macOS 上で「API を見つけて使う」際に実際に当たる具体的なトラブルとその回避法を学べる。  
- 日本でも Mac を使う開発者やローカライズ担当者が、外部 API を使わずにローカルモデルで翻訳や検出を行う際の実践的ノウハウを得られる。  
- Swift の CLI 開発、非同期設計、そしてシステム設定に依るモデル管理という実務で役立つ知識が得られる。

## 詳細解説
- なぜローカル翻訳か：ほとんどの翻訳 API はトークンや課金が必要だが、macOS は右クリック→翻訳の機能を持つ。これを CLI に流用すれば、認証不要でローカルモデルを使った翻訳ができる（プライバシー面の利点もある）。
- 言語とモデルの関係：TranslationSession はローカル翻訳モデル（言語ペア）に依存する。モデルが未インストールなら translate がエラーを返す。System Settings の「General > Language & Region > Translation Languages」からモデルを個別にダウンロードする必要がある点に注意。
- 言語識別：自動検出には NaturalLanguage フレームワークの NLLanguageRecognizer を使う。短いサンプルから dominantLanguage を取得し、Locale.Language に変換して TranslationSession に渡す流れ。
- 非同期処理の落とし穴：swift-argument-parser の従来の ParsableCommand では同期 run() が使われるため、async 関数を呼ぶと Task を使ったり semaphore で待つといったトリッキーな実装になりがち。公式の解決は AsyncParsableCommand を使い run() を async にすること（これで await できる）。
- ビルド環境の注意点：Package.swift の先頭コメントで指定する swift-tools-version の値に依存して platforms の macOS バージョン列挙子が使えるかが決まる（例：macOS 26 を使うにはツールバージョンを上げる必要がある）。LSP のドロップダウンが古い定義を表示する場合があるので、手動編集が必要な場合も。
- ドキュメントの難しさ：公開サンプルが SwiftUI 中心で、非 GUI の CLI 用にどう使えば良いかが明示されていないことが多い。試行錯誤で prepareTranslation() や LanguageAvailability のチェックを入れると安定する。

簡潔な処理の流れ（概念）：
1. 入力文字列を受け取る  
2. NLLanguageRecognizer で言語を特定する  
3. target 言語を決め LanguageAvailability で状態を確認（unsupported / supported / installed）  
4. 必要なら prepareTranslation()（ユーザーにモデルをダウンロードさせる動作）  
5. session.translate(input) を await して結果を出力する

簡単なコード例（要点のみ）:

```swift
import ArgumentParser
import NaturalLanguage
import Translation

@main
struct TranslateCLI: AsyncParsableCommand {
    @Argument var text: String

    func identify(_ s: String) -> Locale.Language? {
        let r = NLLanguageRecognizer()
        r.processString(s)
        guard let lang = r.dominantLanguage else { return nil }
        return Locale.Language(identifier: lang.rawValue)
    }

    func run() async throws {
        let target = Locale.Language(identifier: "en_US")
        guard let source = identify(text) else { print("> could not identify"); return }
        let availability = LanguageAvailability()
        let status = await availability.status(from: source, to: target)
        switch status {
        case .installed:
            let session = TranslationSession(installedSource: source, target: target)
            try await session.prepareTranslation()
            let resp = try await session.translate(text)
            print("> \(resp.targetText)")
        case .supported:
            print("> language pair supported but model not installed; please install via System Settings")
        default:
            print("> unsupported language pair")
        }
    }
}
```

（実運用ではエラーハンドリングや細かい API の差分対応を入れる）

## 実践ポイント
- Swift パッケージの先頭コメント（swift-tools-version）を適切に上げないと新しい platforms 列挙子が使えない。Xcode/LSP 表示に注意。
- CLI で async を扱うなら AsyncParsableCommand を使う。Task＋Semaphore のハックはデバッグ的には使えるが推奨されない。
- 言語自動検出には NLLanguageRecognizer を使う。短文だと誤認識することがあるのでフォールバック処理を用意する。
- 翻訳が "Unable to Translate" になったらまず LanguageAvailability の状態を確認し、必要なら System Settings でモデルをダウンロードする（General > Language & Region > Translation Languages）。
- 日本語対応：日本語は翻訳モデルが存在するので、日本語→英語や英語→日本語のローカル翻訳 CLI をオフラインで作る実用性は高い。社内ツールやローカライズ支援ツールに向く。
- ローカルモデルの利点：API キー不要、課金不要、プライバシー面で優位。社内データを外部に出したくない場合に有効。

まとめ：ドキュメントの欠落や環境差異でハマりやすいが、NLLanguageRecognizer と TranslationSession、AsyncParsableCommand を組み合わせればシンプルなローカル翻訳 CLI は作れる。Mac ユーザーやローカライズ担当には即戦力の技術であり、まずは言語モデルのインストール確認と async 設計を押さえることが鍵。
