---
layout: post
title: "Windows: Prefer the Native API over Win32 - Win32よりNative APIを優先する理由"
date: 2026-02-18T18:10:51.939Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://codeberg.org/ziglang/zig/issues/31131"
source_title: "Windows: Prefer the Native API over Win32"
source_id: 47013324
excerpt: "ntdllのNative APIでZigが小型高性能化する利点と互換・検知リスクを具体解説"
---

# Windows: Prefer the Native API over Win32 - Win32よりNative APIを優先する理由
Windows内部の“より低レイヤ”なAPI（ntdllのNative API）を使うことで、Zigランタイムと標準ライブラリが得た性能・柔軟性と、その注意点を初心者にも分かりやすく解説します。

## 要約
ZigはWindowsでkernel32等のWin32 APIに直接依存するより、ntdllが提供するNative APIを優先して利用する方針を進めています。これにより性能やエラー処理の改善、小さなバイナリ、より豊富な機能が得られますが互換性やAV検出など注意点もあります。

## この記事を読むべき理由
- Windowsでネイティブに近いレイヤを使う利点・欠点を知れば、アプリ設計や標準ライブラリの挙動が理解できる。  
- 日本でもWindows向けランタイムやネイティブ拡張を書く機会は多く、実践的な判断材料になる。

## 詳細解説
- 構成と違い  
  - Win32は「サブシステム」として実装され、最終的にはntdll → カーネルに処理が渡る。ntdllが公開するNative APIはより低レイヤで、Win32はその上位ラッパや互換層になっている。  
- 利点（Native APIを使う理由）  
  - 性能: Win32の互換レイヤを省くことで関数呼び出しのオーバーヘッドを減らせる。  
  - 高機能: Win32が隠す詳細（より豊富な情報や細かいフラッシュ制御など）に直接アクセスできる。例: ReadDirectoryChangesW は内部で NtNotifyChangeDirectoryFile(Ex) を使い、NtFlushBuffersFileEx は FlushBuffersFile より細かい制御が可能。  
  - エラー処理: Win32の BOOL/GetLastError 型より、Nativeの NTSTATUS は情報量が多く一つの switch で扱いやすい。  
  - 依存削減: kernel32 等の互換DLLに依存しない実行単体の小さいバイナリが作れる（早期ブートや特殊環境で有利）。  
- 欠点・リスク  
  - 非公開／未文書化部分があり、Microsoftが内部実装を変更するリスクがある（ただし頻度は低い）。  
  - 古いWindows互換性を犠牲にする場合がある（Zig標準は Windows 10/11 を対象）。  
  - 一部AV製品がNative呼び出しを怪しい挙動と判定することがある。  
  - Wine/ReactOSとの差異でテストが必要になる場合がある。  
- どこまで置き換えるか  
  - すべてを置き換えるわけではない。コンソール周り、Winsockの置き換え、ライブラリロード、プロセス生成（NtCreateUserProcess系）は脆弱性や複雑さがあるため慎重に扱われる。  
  - 多くのWin32関数は単なる forwarder/薄いラッパーなので置き換えが容易なケースも多い。  

## 実践ポイント
- 互換性優先ならWin32呼び出しを使い続ける（特に古いWindowsをサポートする場合）。  
- Native API を使う場合は NTSTATUS を直接扱う設計にし、エラーマッピングを用意する。  
- 標準ライブラリの変更でビルドが壊れる可能性があるため、重要なAPI定義はプロジェクト内にコピーするか zigwin32 等を利用する。  
- AVやWineでの挙動をCIで確認し、問題が出たら報告／ワークアラウンドを用意する。  
- 危険領域（プロセス作成、Winsockの直接操作など）は安易に置き換えない。必要ならよく調査して小さな実験で挙動を確認する。

以上を踏まえ、Windows向けの低レイヤ実装を検討する際は「性能と機能のメリット」と「互換性・運用リスク」を天秤にかけて選んでください。
