---
layout: post
title: "Introducing Script: JavaScript That Runs Like Rust - Script：Rustのように動くJavaScript"
date: 2026-01-27T22:53:16.687Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://docs.script-lang.org/blog/introducing-script"
source_title: "Introducing Script: JavaScript That Runs Like Rust | Script Language"
source_id: 415828225
excerpt: "TypeScriptの書き味でRust並み高速を狙う新言語Script登場"
image: "https://docs.script-lang.org/img/owl-light.png"
---

# Introducing Script: JavaScript That Runs Like Rust - Script：Rustのように動くJavaScript
JSの書き味のまま「ネイティブ速度」を狙う新言語、Scriptが本格登場

## 要約
ScriptはTypeScript互換の文法を保ちつつ、LLVM/Craneliftでネイティブコードにコンパイルし、所有権（ownership）と借用（borrow）によるメモリ安全を導入した言語。自己ホスティング済みコンパイラで「JSの書き心地 × Rust並みの性能」を目指す。

## この記事を読むべき理由
- Node.js/Bunでは難しい「予測可能で高速なネイティブ実行」がほしい場面に直結：サーバー、エッジ、CLIツール、組み込み系での利用価値が高い。  
- TypeScriptの知識を活かしてパフォーマンス改善や低レイテンシ化を図れるため、既存のJS/TSエンジニアにとって学習コストが低い可能性がある。

## 詳細解説
- ネイティブコンパイル：VMやJITではなくLLVMとCraneliftでAOT/JIT生成。結果としてスタンドアロン実行ファイル、起動即実行、JITオーバーヘッドなしを実現。  
- Rust風メモリ安全：Scriptは所有権と借用チェックを導入し、use-after-free・ダブルフリー・データ競合などのクラスのバグをコンパイル時に防ぐ設計。簡単な例：
```javascript
// javascript
let data = [1, 2, 3];
let borrowed = data; // 所有権が移動すると data は以後使えない
```
- TypeScript互換：型推論や関数シグネチャをサポートし、コンパイル時型チェックで誤りを減らす。
```typescript
// typescript
function add(a: number, b: number): number {
  return a + b;
}
let result = add(5, 10); // OK
// let error = add("5", 10); // コンパイルエラー
```
- ゼロオーバーヘッド抽象化：高水準のmap等が実行時コストを残さずネイティブに最適化されることを目指す。  
- 現状とロードマップ：コンパイラの自己ホスティング完了、コア言語（フェーズ0〜4）を通過。標準ライブラリは最小限で、@rolls/*エコシステムやパッケージ管理ツール（Unroll）、LSPなどが順次整備予定。ベンチマークではVM比でCranelift約6x、ネイティブ（LLVM）で約30xの改善が報告されている（I/Oサーバ系の比較はこれから）。

## 実践ポイント
- 試す手順（ローカルでコンパイルしてみる）：
```bash
git clone https://github.com/warpy-ai/script
cd script
cargo build --release
./target/release/script build hello.tscl -o hello
./hello
```
- まずは「CLIツールやホットパスのプロトタイプ」をScriptで書き、起動速度やスループットを比較する。  
- まだプレビュー段階のため、本番導入は慎重に。実運用では@rolls/*の成熟度、LSPやデバッグツール、セキュリティ監査の進捗を確認する。  
- 日本のユースケース：低レイテンシAPI、エッジ/IoTデバイスでの小型バイナリ配布、サーバレスのコールドスタート改善などに適合する可能性が高い。

短くまとめると、Scriptは「TypeScriptの親しみやすさ」を保ちつつ「システム言語並みの性能と安全性」を目指す挑戦的なプロジェクト。実用化に向けたエコシステム整備が今後の鍵になる。興味がある場合はリポジトリで自己ホスト版コンパイラを触ってみることを推奨する。
