---
layout: post
title: "Announcing winapp, the Windows App Development CLI - winapp：Windowsアプリ開発用CLIを発表"
date: 2026-01-22T18:34:35.724Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://blogs.windows.com/windowsdeveloper/2026/01/22/announcing-winapp-the-windows-app-development-cli/"
source_title: "Announcing winapp, the Windows App Development CLI - Windows Developer Blog"
source_id: 421502344
excerpt: "ワンコマンドで環境構築からMSIX化・デバッグまで完了するWindows開発CLI「winapp」登場"
image: "https://blogs.windows.com/wp-content/uploads/sites/3/2026/01/winapp.png"
---

# Announcing winapp, the Windows App Development CLI - winapp：Windowsアプリ開発用CLIを発表
Windows開発の“面倒”を一気に解消するwinapp — ワンコマンドで環境構築・デバッグ・MSIX化まで

## 要約
Microsoftが公開プレビューした「winapp」は、Electron/.NET/C++/Rustなど幅広いツールチェーンでWindowsアプリ開発の面倒を自動化するオープンソースのCLIです。環境セットアップ、Package Identity付与、マニフェスト／証明書管理、MSIXパッケージ化を簡単にします。

## この記事を読むべき理由
日本でもデスクトップ／クロスプラットフォームアプリの需要は高く、Windows固有の署名・マニフェスト・パッケージ作業は学習コストが高いです。winappにより初学者やWeb系エンジニアでも短時間でWindowsネイティブAPI（AIや通知など）を試せるようになります。

## 詳細解説
- 対象と狙い：Visual Studio/MSBuild以外のツールチェーン（Electron、CMake、.NET、Rust、Dart等）を使う開発者向けに、複数SDK・マニフェスト・証明書・パッケージ化の手順を統一するCLI。
- 主要コマンド：
  - init：SDKダウンロード、C++/WinRTなどのプロジェクション生成、マニフェストや開発証明書の作成までワンコマンドで実行。
  
    ```bash
    winapp init
    ```
  - restore：複数マシンやCIで同一環境を再現。
  - create-debug-identity：実行ファイルにPackage Identityを追加し、インストールせずにidentityが必要なAPIをデバッグ可能に。
  
    ```bash
    winapp create-debug-identity my-app.exe
    ```
  - manifest update-assets：ロゴ画像からappxmanifestの画像アセットを自動更新。
  
    ```bash
    winapp manifest update-assets C:\images\my-logo.png
    ```
  - cert generate：自己署名の開発証明書を生成／インストール。
  
    ```bash
    winapp cert generate
    ```
  - pack：ビルド出力からMSIXを作成・署名してストア向け／サイドロード向けパッケージを生成。
  
    ```bash
    winapp pack ./my-app-files --cert ./devcert.pfx
    ```
- Electron連携：npmパッケージとして提供され、ネイティブアドオンのスキャフォールディングや実行中プロセスへPackage Identity注入が可能。これによりnpm startでWindows AI API等をデバッグできます。
  
  ```bash
  npm install --save-dev @microsoft/winappcli
  winapp node add-electron-debug-identity
  ```
- 配布・CI対応：WinGetやnpm経由で導入可能。GitHub/Azure DevOps用アクションでCIに組み込めます。
- 将来性：公開プレビュー段階でフィードバックを集め中。Node用のWindows AIプロジェクションなど実験的機能も登場しています。

## 実践ポイント
- まずはインストールして試す：
  - winget：`winget install microsoft.winappcli`
  - npm（Electron向け）：`npm install --save-dev @microsoft/winappcli`
- 新規プロジェクトの初期化はまず一度 `winapp init` を実行して手順を確認。
- Package Identityが必要なAPIを試すなら `winapp create-debug-identity` で素早くデバッグループを回す。
- MSIX化は `winapp pack` で一発。証明書や署名に不慣れならまず開発証明書で流れを掴む。
- Electron開発者は `@microsoft/winappcli` と統合して、ネイティブ機能やWindows AIを試してみる。

公式GitHubとドキュメントで導入ガイドやサンプルが公開されているので、興味があればすぐ試してフィードバックを送ってください。
