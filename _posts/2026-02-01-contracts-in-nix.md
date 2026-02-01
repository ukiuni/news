---
layout: post
title: "Contracts in Nix - Nixにおけるコントラクト"
date: 2026-02-01T16:13:28.947Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://sraka.xyz/posts/contracts.html"
source_title: "Yvan Sraka's blog - Contracts in Nix"
source_id: 1292249287
excerpt: "contractsライブラリでNixのJSONや既存コードの誤りをCIで早期検出し安全に扱う。"
---

# Contracts in Nix - Nixにおけるコントラクト
Nixで「型チェックをあとから付ける」――レガシー式やJSONを安全に扱うランタイム契約ライブラリ

## 要約
Nix言語に静的型はないが、yvan-srakaの「contracts」ライブラリはランタイムのバリデータ（＝コントラクト）を提供して、既存のNixコードやJSON入力を安全に検証できるようにする。

## この記事を読むべき理由
Nix／NixOSやFlakeを使う日本の開発者は、設定ファイルやパッケージ定義の間違いでCIが壊れることが多い。contractsは既存コードへ最低限の手を加えるだけで早期検出・良いエラーメッセージ・可逆的な失敗処理を実現し、CI運用やメンテ性を劇的に改善する可能性がある。

## 詳細解説
- 問題点：Nixは型システムを持たず、設定ミスや不正なJSONが実行時に破壊的なエラーを起こすことがある。  
- ライブラリの考え方：バリデータ（validator）は「値を受け取り真偽を返す関数」。これを「型（type）」のように定義し、名前や説明を付けられるようにしたのがcontractsのコア。declareで名前付きの型を作り、contract/isで値を検証する。  
- 構成要素：listOf、setOf、enum、fn、notなどの合成可能な型ビルダー、mkOption互換の型ラッパー、strictで強制評価、recoverableなエラー（tryEvalで捕まえられる）と詳細なトレース出力。  
- 実行時・遅延評価との相性：Nixの遅延評価と相性が良く、実際に評価された箇所だけチェックして正確なスタックトレースを返す。CIでのみ有効化する等のオプトアウトも可能。  
- 互換性と導入：flakes入力、niv、従来チャネルいずれでも導入可能。ライブラリはnixのビルトインのみ依存で自己完結的。

簡単なイメージ（抜粋）:
```nix
# language: nix
contracts = import <contracts> { enable = true; };

# JSONを型で検証して早期失敗
package = contract { name = "package.json malformed" } {
  bundleDependencies = enum [ Bool (listOf Str) ];
  dependencies = setOf Str;
} (builtins.fromJSON (builtins.readFile ./package.json));
```

## 実践ポイント
- まずはflakesやnivでcontractsを追加し、CIジョブでenableを有効化して導入テストを行う。  
- JSONや外部入力（package.json、users.jsonなど）をcontractでラップして早期に失敗させる。  
- declareで再利用可能な型（Email、Hash、Loginなど）を定義してドメイン固有の検証を共有。  
- パフォーマンスが気になる箇所は環境変数で無効化するか、必要箇所だけstrictで明示的に強制評価する。  
- tryEvalでrecoverableエラーとして扱えば、壊れた入力を安全に扱える。

導入は小さく始めて、エラーメッセージとトレースを確認しながら段階的に広げるのが効果的です。
