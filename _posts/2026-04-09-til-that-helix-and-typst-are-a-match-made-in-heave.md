---
layout: post
title: "TIL that Helix and Typst are a match made in heaven - HelixとTypstは天国の相性"
date: 2026-04-09T14:09:18.538Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://ergaster.org/til/helix-typst-match-in-heaven/"
source_title: "Helix and Typst are a match made in heaven"
source_id: 1503462762
excerpt: "HelixとTypstをLSPで連携し、カーソル同期のライブプレビューで書く→確認が瞬時に快適化"
image: "https://ergaster.org/og/til/helix-typst-match-in-heaven.png"
---

# TIL that Helix and Typst are a match made in heaven - HelixとTypstは天国の相性
HelixとTypstで「書く→確認」が一体化する、いま使いたいドキュメント体験

## 要約
Typst（LaTeXより手軽）とHelix（モーダルエディタ）を、Typst用の言語サーバーtinymistでつなぐと、ライブプレビューがカーソル位置と同期して超快適な執筆環境になる、という話です。

## この記事を読むべき理由
MarkdownやOfficeの限界を感じている開発者・研究者にとって、手早く美しい組版ができるTypstは有力な選択肢。特に日本の技術文書や学術資料でも、LaTeXほどの学習コストをかけず高品質な出力が欲しい場面で役立ちます。

## 詳細解説
- Typst：LaTeXより直感的でモダンなドキュメント用マークアップ。見た目の調整やレイアウト指定が比較的シンプルに書ける。  
- Helix：モーダルで軽快なテキストエディタ。LSP（Language Server Protocol）を介して高度な編集支援が使える。  
- tinymist：Typst向けのLanguage Server。シンタックス強調、フォーマット、コードアクションに加え、目玉はライブプレビュー機能。Helix側でカーソル位置とプレビューが同期するため、編集→確認の往復がスムーズ。  
- 導入は簡単で、Homebrewでtinymistを入れ、Helixのlanguages.tomlにtypst用のLSP設定を追加するだけでライブプレビューが有効になります。

インストール例（macOS/Homebrew）:
```bash
brew install tinymist
```

Helix設定例（~/.config/helix/languages.toml）:
```toml
[language-server.tinymist]
command = "tinymist"
config = { preview.background.enabled = true,
           preview.background.args = [ "--data-plane-host=127.0.0.1:23635",
                                       "--invert-colors=never",
                                       "--open" ] }

[[language]]
name = "typst"
language-servers = [ "tinymist" ]
```

## 実践ポイント
- まず tinymist をインストールして、Helixのlanguages.tomlに上の設定を追加する。  
- .typ ファイルをHelixで開くと自動でLSPが動き、ライブプレビューが起動するはず。  
- 日本語組版やフォント、PDF出力の設定はTypst側で調整可能なので、まずテンプレートを作ると効率的。  
- LaTeXより短い学習コストで、技術文書・レポート作成のワークフローを改善できます。
