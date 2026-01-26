---
layout: post
title: "The browser is the sandbox - ブラウザがサンドボックスだ"
date: 2026-01-26T06:46:33.221Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://simonwillison.net/2026/Jan/25/the-browser-is-the-sandbox/"
source_title: "the browser is the sandbox"
source_id: 46762150
excerpt: "ブラウザ内で動くLLMエージェントでローカルとネットを安全に制限しデータ漏洩を防ぐ"
image: "https://static.simonwillison.net/static/2026/codo.jpg"
---

# The browser is the sandbox - ブラウザがサンドボックスだ
ブラウザで“安全に”LLMエージェントを動かす──ローカルファイルとネットワークを守る新しい実践

## 要約
ブラウザは既に「外部の敵対的コード」を安全に走らせる仕組みを備えており、これを使ってローカルファイル操作やネット接続を制限したLLMベースのエージェントを動かす試み（例：Co-do）が現実的になっている、という話です。

## この記事を読むべき理由
日本の開発者・企業にとって、データ流出リスクが低い「ブラウザ内で完結するエージェント」は、プライバシー規制や社内データ利用の観点で即応用可能な選択肢だからです。

## 詳細解説
- サンドボックスの要素は大きく三つ：ファイルシステム、ネットワーク、実行環境。  
- ファイル操作：File System Access API（現状は主にChrome系）でユーザー許可のもとローカルファイルにアクセスできる。加えて、input type="file"のwebkitdirectory属性を使えば、Firefox/Safari/Chromeでディレクトリ単位の読み取りが可能（読み取り専用）。  
- ネットワーク制御：CSPヘッダーと<iframe sandbox>で外部APIへのアクセスを制限できるが、ブラウザ間での挙動差やドキュメント不足が問題。投稿者は「二重iframe」などの工夫でネットワークルールを強化するテクニックを紹介している。  
- 実行の安全性：WebAssembly＋Web Workerを組み合わせれば、より厳格にサンドボックス化されたコード実行が可能。大規模なローカルコンテナを立てずに似た体験を提供できる点がポイント。  
- 実例のCo-do：フォルダ指定＋LLMプロバイダのAPIキー設定で、ブラウザ内だけでファイル操作とチャットインターフェースを組み合わせるデモ。Claude Coworkのようなローカルコンテナ不要の代替を示している。

制約としては、APIキーやブラウザ固有の実装差、File System Access APIの非一貫性、iframeの挙動差などが残る。

## 実践ポイント
- Co-doなどのデモを触って挙動を確認する（まずはローカルで小さなフォルダで試す）。  
- ディレクトリ読み取りはまずwebkitdirectoryで互換性を確認、Chrome限定機能は代替設計を用意。  
- ネットワーク制御はCSP＋sandboxを基本に、必要なら二重iframeパターンで境界を厳格化する。  
- 実行はWebAssembly＋Web Workerで分離し、APIキーはブラウザ側で安全に扱う（読み取り専用アクセスやユーザー同意を明確に）。  
- 社内利用なら「ブラウザ完結」でのデータ保護ポリシー策定を検討する（ログ出力や外部送信の可否を明確化）。

元記事はブラウザが持つ既存のサンドボックス機能を再評価し、LLMエージェントの安全で実用的な実装法を示しています。日本の現場でもすぐ試せるテクニックが多く含まれています。
