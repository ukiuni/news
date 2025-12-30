---
layout: post
title: "Got tired of copy-pasting LICENSE files, so I built a tiny CLI for it (Homebrew) - LICENSEファイルのコピペに飽きたので小さなCLIを作った（Homebrew）"
date: 2025-12-30T11:20:19.166Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/kushvinth/lic"
source_title: "Got tired of copy-pasting LICENSE files, so I built a tiny CLI for it (Homebrew)"
source_id: 434765192
excerpt: "GitHub公式テンプレをTUIで選んで1発生成するmacOS向け小型CLI「lic"
---

# Got tired of copy-pasting LICENSE files, so I built a tiny CLI for it (Homebrew) - LICENSEファイルのコピペに飽きたので小さなCLIを作った（Homebrew）
もうLICENSEファイルで悩まない——ワンクリックで公式テンプレを引っ張るmacOS向けTUI「lic」

## 要約
GitHubの公式ライセンステンプレートをAPIから取得して、ターミナル上のTUIで対話的にLICENSEファイルを生成するmacOS向けの小さなCLIツール。Homebrewで簡単に導入でき、手作業のコピペを不要にする。

## この記事を読むべき理由
ライセンスの選択やテンプレ作成はOSS公開や社内リポジトリ作成で頻繁に発生する作業。日本の開発現場でも、誤ったテンプレや入れ忘れで手戻りや法務チェックが発生しがちなので、手早く正確にLICENSEを作れるツールは生産性向上に直結する。

## 詳細解説
- 何をするツールか  
  licは「GitHubの公式ライセンス一覧」をAPI経由で取得し、ターミナル上の簡易TUIでライセンスを選んでローカルにLICENSEファイルを生成する。Webでテンプレをコピーして貼る手順を省けるのが最大の利点。

- 技術スタックと配布方法  
  - 実装: Python（リポジトリは100% Python）  
  - UI: macOS向けのTUI（READMEにMacOS TUI Toolと明記）  
  - 配布: Homebrew公式でなく作者のtapから提供（brew tap kushvinth/tap && brew install lic）  
  - ライセンス: GPL-3.0（ツール自身のライセンス）  
  - リポジトリ構成: main.py、src/、README.md、pyproject.toml 等

- 使い方（READMEベース）  
  - Homebrew経由:
    ```bash
    brew tap kushvinth/tap
    brew install lic
    ```
  - ソースから:
    ```bash
    git clone https://github.com/kushvinth/lic.git
    cd lic
    uv install lic
    ```
  - 実行:
    ```bash
    lic
    ```
  - 貢献フロー: fork → ブランチ作成 → commit → PR（READMEに手順あり）

- 注意点  
  - macOS向けTUIとして設計されているため、Linux/Windowsでの動作保証は明示されていない。  
  - 生成されるテンプレートはGitHub公式のものを取得するため、最新のテンプレに沿うが、企業の法務要件には必ず確認が必要。

## 実践ポイント
- まずはテンプレ整備に導入：新規リポジトリ作成時のテンプレ生成をlicで自動化して、READMEテンプレと合わせてスキャフォールドに組み込む。  
- 社内ルールに合わせる：会社で使えるライセンス候補リストを決めて、開発者に選ばせるだけでなく、CIで所定のライセンスがあるか検証するワークフローを追加する。  
- コントリビューション: 小さな改善（例: 日本語ローカライズ、SPDX識別子の挿入、Linuxサポート）ならリポジトリにPRを投げやすい。  
- 法務連携: 自動化しても法務チェックは不要にはならない。生成後に必ず社内法務／ライセンス担当が確認するプロセスを残す。

## 引用元
- タイトル: Got tired of copy-pasting LICENSE files, so I built a tiny CLI for it (Homebrew)  
- URL: https://github.com/kushvinth/lic
