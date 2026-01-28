---
layout: post
title: "Rust at Scale: An Added Layer of Security for WhatsApp - 大規模導入されたRust：WhatsAppのセキュリティにもう一層の防御"
date: 2026-01-28T10:22:21.228Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://engineering.fb.com/2026/01/27/security/rust-at-scale-security-whatsapp/"
source_title: "Rust at Scale: An Added Layer of Security for WhatsApp - Engineering at Meta"
source_id: 46791742
excerpt: "WhatsAppがRustでメディア処理を再実装し、30億端末へ危険ファイル検出の防御層を展開"
image: "https://engineering.fb.com/wp-content/uploads/2026/01/Eng-Blog-Self-Serve-Hero-Images-PRIVACY-WhatsApp2.jpg"
---

# Rust at Scale: An Added Layer of Security for WhatsApp - 大規模導入されたRust：WhatsAppのセキュリティにもう一層の防御
WhatsAppが“Rust化”で守る理由 — 30億ユーザーを狙うメディア攻撃を封じる新防御

## 要約
WhatsAppはメディア検証ライブラリをC++からRustで再実装し、フォーマット不整合や悪意ある添付ファイルから端末を守る新しい防御層「Kaleidoscope」を世界規模で展開しました。大規模配布と多プラットフォーム対応を通じて、Rustの実運用性とメモリ安全性を示しています。

## この記事を読むべき理由
メッセージアプリが直面する「未加工メディアを扱うリスク」と、その対策としてのRust採用・差分ファズ（differential fuzzing）やフォーマット検査の実践は、日本のモバイル開発者やセキュリティ担当にも直結する教訓だからです。

## 詳細解説
- 背景: 2015年のAndroid「Stagefright」脆弱性は、OS側のメディア処理の弱点がアプリ利用者を直撃する例。OS更新が浸透するまでの間、アプリ側で防ぐ必要があるとWhatsAppは判断しました。
- 改善対象: WhatsAppの既存MP4整形ライブラリ（wamedia）をRustで新規実装。C++版と並行開発し、互換性は差分ファズ＋単体／統合テストで担保。
- 技術的要点:
  - メモリ安全が主目的：バッファオーバーフロー等のメモリ由来脆弱性を低減。
  - 規模と成果：160,000行のC++（テスト除く）を90,000行のRust（テスト含む）に置換。性能・ランタイムメモリ使用で優位を確認。
  - 配布の課題：Rust標準ライブラリによるバイナリ肥大、マルチプラットフォーム向けビルドサポートを整備して克服。
- Kaleidoscope: ファイルフォーマット準拠チェック、不正な構造や高リスク要素（PDF内の埋め込みファイルやスクリプト）、拡張子／MIME偽装、実行ファイルなどの危険な型の一律フラグ付けを組合せた防御層。
- 全面展開: Android、iOS、Mac、Web、Wearablesなど数十億デバイスへ配信。WhatsApp／Messenger／Instagram向けライブラリとして広範に展開。
- セキュリティ方針との整合: E2E暗号化や脆弱性報告、ファズ／静的解析／サプライチェーン管理、バグバウンティ強化と並ぶ戦略の一部。

## 実践ポイント
- メディア・パーサは「最初から」メモリ安全言語（Rust等）で書くことを検討する。  
- C/C++を残す場合は差分ファズ＋自動テストで互換性と安全性を検証する。  
- フォーマット準拠チェック、埋め込み要素検査、MIME／拡張子の突合は必須の防御層。  
- マルチプラットフォーム配布を想定してビルド基盤とバイナリサイズ対策を計画する。  
- 供給網・解析・報告体制（サプライチェーン管理、静的解析、バグバウンティ）を組合せた防御深度を設計する。

---  
元記事: "Rust at Scale: An Added Layer of Security for WhatsApp"（Engineering at Meta, 2026-01-27）
