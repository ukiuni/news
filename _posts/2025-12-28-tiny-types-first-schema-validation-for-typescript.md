---
layout: post
title: "Tiny, types-first schema validation for TypeScript"
date: 2025-12-28T19:18:31.890Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/easrng/schema"
source_title: "Tiny, types-first schema validation for TypeScript"
source_id: 751648051
excerpt: "Type優先で超軽量、VSCode補完で型と実装を即検証できるTS向けランタイムバリデータ"
---

# Type優先で超ミニマムなバリデーション — TypeScript開発がぐっと楽になる「@easrng/schema」

## 要約
TypeScriptの型から直接ランタイムバリデータを作る軽量ライブラリ。エディタ補完と親和性が高く、導入コストが低いのが特徴。

## この記事を読むべき理由
型安全性を重視する日本のフロント／バックエンド開発で、軽量かつエディタ体験を損なわずにランタイム検証を追加したいエンジニア向け。大規模ライブラリを持ち込まずに型→バリデーションを実現できるため、フロントのバンドルサイズやサーバーレス環境にも好適です。

## 詳細解説
@easrng/schemaは「types-first」アプローチを取る小さなライブラリで、TypeScriptの型宣言を起点にしてランタイムの検証器（validator）を定義・実行できます。特徴は以下。

- 軽量：依存が少なく、最小限のランタイムで動く設計。
- エディタ補完（VS Codeとの相性）：型に合わせた文字列スキーマをエディタで補完でき、宣言と実装のズレを減らすワークフローをサポート。
- Standard Schema準拠の文字列スキーマを扱う（READMEで示されているJSON形式のスキーマ）。
- ヘルパー群：is（型狭め）、assert（エラーを整形して表示）などを提供しており、テストやデバッグがしやすい。

基本的な使い方（抜粋・要点）：
```typescript
import { schema, type Schema } from "@easrng/schema";

interface MySchema { hello: "world" }

// 型注釈付きでスキーマを宣言。エディタ補完が効く
const mySchema: Schema<MySchema> = schema('{"type":"object","properties":{"hello":{"const":"world"}},"required":["hello"]}');

// バリデートして結果を扱う
const result = mySchema.validate(0);
if (result.issues) {
  console.error(result.issues);
} else {
  console.log(result.value);
}
```

補助ユーティリティ例：
```typescript
import { is } from "@easrng/schema/util";
if (is(stringSchema, someUnknown)) {
  // ここでsomeUnknownはstringとして扱える
}
```

また、prettyのassertを使うとエラーメッセージを見やすく整形してくれるため、デバッグやCIログでの可読性が向上します。

## 日本市場との関連
- TypeScript採用が進む日本のプロダクト（フロント、Node API、サーバーレス）で、型と実際の入力値の乖離を低コストで検出したいニーズは高いです。
- モノリポ／ビルド最適化を重視するチームでは、Zodやio-tsのような重量級依存を避けたい場面で代替になり得ます。
- エッジ関数やブラウザ側での簡易検証など、ランタイムコストを抑えたいユースケースと相性が良いです。

## 実践ポイント
- まずは小さなモジュールに導入して、既存の型に対するバリデーション結果と差異を確認する。
- VS Codeでschema()に文字列を入れてみると補完が動くので、スキーマ文字列の自動補完を活用して型と実装の差を早期に発見する。
- テストではassertやisを使い、エラー出力の可読性を高めることでデバッグコストを下げる。
- バンドルサイズやランタイム負荷が重要なプロジェクトでは、まずはbundle analyzerで比較検証を行う（@easrng/schemaは小さめだが実環境での確認を推奨）。

## 引用元
- タイトル: Tiny, types-first schema validation for TypeScript
- URL: https://github.com/easrng/schema
