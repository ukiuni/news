---
layout: post
title: "Show HN: Marky – A lightweight Markdown viewer for agentic coding - Show HN: Marky – エージェント的コーディング向け軽量Markdownビューア"
date: 2026-04-16T23:27:17.181Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/GRVYDEV/marky"
source_title: "GitHub - GRVYDEV/marky: A lightweight easy to use markdown viewer · GitHub"
source_id: 47795468
excerpt: "CLIで即起動、ライブ反映する軽量macOSMarkdownビューア—Obsidian連携可"
image: "https://opengraph.githubassets.com/149422c772c85793b61233a38099a624d9f3415c1617d730ac01e9cd596f60ea/GRVYDEV/marky"
---

# Show HN: Marky – A lightweight Markdown viewer for agentic coding - Show HN: Marky – エージェント的コーディング向け軽量Markdownビューア
端末からパッと開いて「そのまま読む」ための、軽量で速いmacOSネイティブMarkdownビューア

## 要約
MarkyはTauri+Reactで作られた、CLI主体の軽量Markdownビューア。ファイルのライブリロード、Obsidian風ワークスペース、Shikiによる美しいシンタックスハイライトやKaTeX/Mermaid対応など、ドキュメント閲覧に必要な機能が揃っています。

## この記事を読むべき理由
ローカルで生成・編集されるドキュメント（エージェント出力、設計ノート、READMEなど）を即座に確認したい日本の開発者／ドキュメント担当者にとって、軽量で安全に使えるネイティブビューアは作業効率を大きく上げます。特にObsidianやVS Code中心のワークフローと相性が良い点は注目です。

## 詳細解説
- アーキテクチャ：Tauri(v2)をデスクトップシェルに、フロントはReact+TypeScript。Rust側がCLI、ファイル監視、フォルダ管理、ファジー検索（nucleo）を担当し、フロントがmarkdown-it中心のレンダリングパイプラインを担います。  
- 主な機能：
  - CLIファースト：`marky FILENAME` で即ウィンドウを開く。フォルダを指定するとワークスペースとしてサイドバーに保持。
  - ライブリロード：ディスク上の編集を即反映（エディタやAI生成の出力をリアルタイム確認可能）。
  - シンタックスハイライト：Shiki＋VS Codeテーマを利用しコードが美しく見える。
  - 数式・図表：KaTeXで $inline$ / $$display$$ 数式、MermaidをSVGでレンダリング。
  - GFM完全対応（テーブル、タスクリスト、フットノート等）とDOMPurifyによるサニタイズで未知のMarkdownも安全に表示。
  - 軽量：Electronを使わずネイティブWebViewで、配布用.dmgは約15MB未満（現時点で署名待ちの注意あり）。
- 開発者向け：ソースビルドはRust/Node.js/pnpmが必要。プロジェクト構成はRustバックエンド（src-tauri）とReactフロント（src）に分離。

## 実践ポイント
- まず試す（Homebrew）:
```bash
bash
brew tap GRVYDEV/tap
brew install --cask GRVYDEV/tap/marky
# 未署名バイナリの場合のみ
xattr -cr /Applications/Marky.app
```
- 使い方の基本:
```bash
bash
marky README.md       # 単一ファイルを開く
marky ./docs/          # フォルダをワークスペースで開く
marky                  # 最後のセッションを復元
```
- 便利ショートカット：Cmd+K（ファイル検索）、Cmd+O（ファイルを開く）、Cmd+Shift+O（フォルダ追加）、Cmd+F（ページ内検索）。
- 自分でビルド／カスタマイズする場合（開発用）:
```bash
bash
git clone https://github.com/GRVYDEV/marky.git
cd marky
pnpm install
pnpm tauri build
./scripts/install-cli.sh
```
- 日本の現場での活用例：ObsidianやVS Codeと組み合わせてノート・設計書の即時プレビュー、AI（例：Claude）によるドキュメント生成をリアルタイムで確認、軽量な差分確認用ビューアとしての導入。

興味があれば公式リポジトリでデモやソースをチェックし、ローカルワークフローに組み込んでみてください。
