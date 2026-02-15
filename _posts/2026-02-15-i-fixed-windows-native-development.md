---
layout: post
title: "I Fixed Windows Native Development - Windowsネイティブ開発を直した"
date: 2026-02-15T15:58:36.300Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://marler8997.github.io/blog/fixed-windows/"
source_title: "Welcome to Johnny&apos;s World"
source_id: 47022891
excerpt: "msvcupでVisual Studio不要、数分で再現可能なWindowsネイティブ開発環境を構築"
---

# I Fixed Windows Native Development - Windowsネイティブ開発を直した
Visual Studioに頼らないWindowsネイティブ開発――msvcupで「誰でも再現できる」ビルド環境を作る

## 要約
Visual Studioの巨大なインストーラに頼らず、msvcupというCLIでMSVCツールチェインとWindows SDKをバージョン管理・分離し、数分で再現可能なビルド環境を作れるようにした話。

## この記事を読むべき理由
Windows向けネイティブ開発で「環境依存のビルド」や巨大なIDEインストールに悩む日本の開発者/CI担当は多いはず。msvcupはその悩みを減らし、CIやオンボードのハードルを下げます。

## 詳細解説
- 問題点
  - Visual Studioはエディタ・コンパイラ・SDKが一体化した巨大モノリス。ワークロード選択ミスやSDKバージョン違いでビルドが壊れやすく、レジストリ汚染やアンインストールの不完全さも常態化。
  - vcvars*.bat による環境のグローバル上書き、バージョン差による「Works on my machine」症候群が発生。

- msvcupの考え方と仕組み
  - Microsoftの公開するJSONマニフェストを解析し、コンパイラ／リンカ／ヘッダ／ライブラリに必要なパッケージだけをCDNから直接ダウンロード。
  - 各ツールチェイン／SDKをバージョンごとに隔離したディレクトリ（例: C:\msvcup\msvc-...）に配置。並列インストール、容易な削除が可能。
  - autoenv機能はvcvarsを直接呼ばず、ラッパー実行ファイルで環境変数を一時設定してツールを呼び出すため、グローバル環境を汚さない。
  - ロックファイル対応で「誰でも同じパッケージを使う」ことを保証し、CIでの再現性を担保。
  - クロスコンパイル対応が組み込みで高速・冪等。

- 利用効果
  - インストールが速く、初回以降はmsvcupコマンドがほぼ瞬時に完了。
  - ビルドスクリプトにインストール手順を入れれば「Install Visual Studio」の指示が不要に。
  - CIとローカルで同一ツールチェインを使えるためデバッグコストが下がる。

- 実例（簡易な build.bat）
  - リポジトリに置けばクリーンWindows上でツールチェインを自動取得してコンパイルできる。

```batch
@rem batch
@if not exist msvcup.exe (
  curl -L -o msvcup.zip https://github.com/marler8997/msvcup/releases/download/v2026_02_07/msvcup-x86_64-windows.zip
  tar xf msvcup.zip
  del msvcup.zip
)
set MSVC=msvc-14.44.17.14
set SDK=sdk-10.0.22621.7
msvcup install --lock-file msvcup.lock --manifest-update-off %MSVC% %SDK%
msvcup autoenv --target-cpu x64 --out-dir autoenv %MSVC% %SDK%
.\autoenv\cl hello.c
```

## 実践ポイント
- まずは小さなリポジトリで build.bat を置き、msvcupでビルドが再現できるか確認する。
- CI（GitHub Actions等）にmsvcupコマンドを組み込み、Visual Studio事前インストールを不要にする。
- msvcupのロックファイルをリポジトリ管理して、チームで同一ツールチェインを強制する。
- フルIDEが必要なケース以外はmsvcupで十分。レガシー環境のダウングレードやクロスビルドの管理が楽になる。

以上。元記事の詳細や最新の使い方は msvcup の README を参照すると良い。
