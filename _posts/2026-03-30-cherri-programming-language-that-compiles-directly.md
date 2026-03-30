---
layout: post
title: "Cherri – programming language that compiles directly to a Apple Shortuct - Cherri — 直接Apple Shortcutsにコンパイルするプログラミング言語"
date: 2026-03-30T17:51:51.322Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/electrikmilk/cherri"
source_title: "GitHub - electrikmilk/cherri: Siri Shortcuts Programming Language 🍒 · GitHub"
source_id: 47549824
excerpt: "コードで直接Shortcutsを生成し、署名・配布までワークフロー化する言語"
image: "https://repository-images.githubusercontent.com/554016681/945834d8-b32a-4e77-a675-307823b8a508"
---

# Cherri – programming language that compiles directly to a Apple Shortuct - Cherri — 直接Apple Shortcutsにコンパイルするプログラミング言語
ショートカット開発を「コード」で本気化する：Macで作る大規模・保守可能なApple Shortcuts入門

## 要約
Cherriは、コードで書いてそのまま実行可能なApple Shortcutを生成するDSL（専用言語）で、CLI・VSCode拡張・macOS IDE・パッケージ管理など開発体験を揃え、短期的なスクリプトではなく長期的に保守できるショートカット開発を目指します。

## この記事を読むべき理由
日本でも業務自動化や個人の生産性向上でShortcuts利用が増える中、GUIだけでは管理が難しくなる「大きなショートカット」をチームで扱う手法が求められています。Cherriはコード化によって再利用・型安全・パッケージ化を実現し、現場の運用コストを下げられるポテンシャルがあります。

## 詳細解説
- コンパイル先：Cherriはソースを直接「有効な実行可能Shortcut（.shortcut）形式」に変換する。つまりGUIで一つ一つ組む代わりにソースからエクスポートできる。  
- 開発体験：CLI、VSCode拡張、macOS用のIDE、オンラインPlaygroundを提供。ローカルで編集→ビルド→署名→配布まで一貫可能。  
- 言語設計：Goで実装。Goっぽい/他言語に近い読みやすい構文で、型推論、列挙型、オプショナル、デフォルト値、raw actions（手動でAction IDとパラメータ指定）などをサポート。多くのアクションや型がCherriで書かれており「半ブートストラップ」状態。  
- デバッグと最適化：可能な限り1対1でShortcutアクションに翻訳し、デバッグを簡潔に。生成物はメモリとサイズを抑える工夫あり。--debugでplist出力や詳細スタックトレース取得可。  
- 署名と配布：macOSの署名を使い、必要に応じて署名サーバ（HubSignなど）にもフォールバック。iCloudリンクからのインポート変換機能も有る。  
- パッケージ管理：Gitリポジトリベースの組み込みパッケージマネージャで、ライブラリ化・自動更新が可能。大規模プロジェクト向けにファイル分割（include）やトップレベルで独立スコープの関数定義が可能。

## 実践ポイント
- まずはPlaygroundで試す → VSCode拡張でシンタックスハイライトを導入 → 小さなShortcutをCherriで書いてビルド・署名してiCloudで配布。  
- チームではパッケージ管理を活用し、共通アクションをGitリポジトリ化して再利用。  
- 大きなループやデータ処理は関数でスコープを分けて、ショートカット実行時のメモリ負荷を下げる設計を心がける。  
- インストールはHomebrewやNixが便利（例: brew tap electrikmilk/cherri && brew install electrikmilk/cherri/cherri）。  
- Shortcutsの制約（アクション数やメモリ）を意識しつつ、UIでの手作業をコードに置き換えて保守性を高めるのが狙い。

短時間でGUIを置き換える魔法ではありませんが、ショートカットをチームや長期プロジェクトで運用したい人には実務的な選択肢になります。
