---
layout: post
title: "Guix for Development - 開発に使うGuix"
date: 2026-01-26T01:16:35.887Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://dthompson.us/posts/guix-for-development.html"
source_title: "Guix for development — dthompson"
source_id: 46690592
excerpt: "Guixでプロジェクトごとに汚さず再現可能な開発環境を数分で構築しCI連携まで自動化する方法"
---

# Guix for Development - 開発に使うGuix
もう環境構築で時間を無駄にしない — Guixでプロジェクト毎にサクッと再現可能な開発環境を作る方法

## 要約
Guixは「プロジェクト単位」の再現可能な開発環境を手軽に作れるパッケージマネージャ／ディストリビューション。guix shellやguix.scmで依存関係をコード化し、ホストを汚さずにビルドやテストができます。

## この記事を読むべき理由
日本の現場でも、複数プロジェクトやレガシー依存のせいで環境構築に時間を取られがち。Guixを使えば「git clone → build」までの手順を確実に短縮・自動化でき、CIやチーム共有の信頼性が上がります。

## 詳細解説
- Guixとは：任意のLinuxディストリ上で動くパッケージマネージャであり、独立したディストリにもなる。パッケージは再現可能にビルドされ、既存のシステム領域（/usr）を汚さない。
- guix.scm：パッケージ定義をSchemeで書く「設定をコード化する」ファイル。依存（inputs）やビルド手順、native-inputs（ビルド時ツール）を明示できるため、環境の全ツリーを確実に再現する。
- guix shell：プロジェクト直下のguix.scmを読み取り、その環境を一時的なシェル内に提供。./configure や make をそのまま実行すれば、必要なライブラリやツールが揃った状態で動く。
- 分離レベル：--pureで環境変数をクリア、--containerでLinux名前空間ベースのコンテナ風隔離が可能。必要に応じて選べる（多くはデフォルトで十分）。
- 他ツールとの比較：言語固有の仮想環境（venv, rvm, nvm）は言語に限定される。Dockerは強力だが重く/隔離が強すぎる場合がある。Guixはシステム依存を最小化しつつホストとの相互作用（GUI等）を保てる点が特徴。
- ワークフロー拡張：guix build -f guix.scm でクリーンなビルド検証、guix package -f guix.scm でインストール確認。direnvやエディタ（例：Emacs＋emacs-direnv）と連携して開発フローに組み込める。
- セキュリティ／運用：初回はプロジェクトディレクトリを認可リストに追加する手順が必要（guix shellの安全設計の一環）。Guixは既存のUbuntu等に重ねて導入可能なので、段階的採用が容易。

簡単な例（ワークフローの概念）:
```bash
# リポジトリをクローンしてプロジェクトを許可
git clone <repo>
cd <repo>
echo $PWD >> $HOME/.config/guix/shell-authorized-directories

# 開発環境を立ち上げてビルド
guix shell
./configure
make
```

## 実践ポイント
- まずは既存の小さなプロジェクトでguix.scmを作り、guix shellで動かしてみる。失敗から学ぶのが早い。
- direnvを使い、`eval $(guix shell --search-paths)` を .envrc に入れてエディタやシェルで自動有効化する。
- ビルドの再現性チェックには `guix build -f guix.scm` をCIに組み込む。
- 必要に応じて `--pure` / `--container` を使い分け、ホストとの連携（GUIやX11など）が必要なプロジェクトではデフォルトのまま使う。
- 導入は段階的に：まずはGuixを既存ディストリに追加（Ubuntu上で動く）して運用感を掴むのが現実的。

短時間で確実に「再現可能な開発環境」を試したい日本のエンジニアにとって、Guixは強力な選択肢です。導入は小さく始めて、効果を実感してください。
