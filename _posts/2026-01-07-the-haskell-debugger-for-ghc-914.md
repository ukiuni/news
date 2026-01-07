---
  layout: post
  title: "The Haskell Debugger for GHC 9.14 - GHC 9.14向け Haskell デバッガー"
  date: 2026-01-07T20:47:35.660Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://discourse.haskell.org/t/the-haskell-debugger-for-ghc-9-14/13499"
  source_title: "The Haskell Debugger for GHC 9.14 - Announcements - Haskell Community"
  source_id: 1191313436
  excerpt: "GHC9.14対応の公式HaskellデバッガがVSCode/Neovimと連携し即試せる"
  image: "https://us1.discourse-cdn.com/flex002/uploads/haskell/original/1X/89166504e40f4869ea825dd70048017861ec8578.png"
---

# The Haskell Debugger for GHC 9.14 - GHC 9.14向け Haskell デバッガー
魅力的なタイトル: 初めてでも安心！GHC 9.14対応の「Haskell Debugger」で関数型コードの壁を壊す

## 要約
GHC 9.14 対応の公式 Haskell Debugger が公開され、VS Code や Neovim と DAP 経由で統合できるようになりました。大規模コードベース対応も目標に据えた実用的なデバッグ環境が手に入ります。

## この記事を読むべき理由
- Haskell を実務や学習で使う日本のエンジニアにとって「デバッグ体験の改善」は採用と生産性に直結します。  
- GHC 9.14 が必須なので、最新のツールチェーンを使う日本のプロジェクトでも即試せる点が魅力です。

## 詳細解説
- 対応バージョン: デバッガーは GHC 9.14（記事では 9.14.1）専用です。まず GHC のバージョン確認が必須です。
- インストール: cabal 経由で haskell-debugger をインストールします（一部依存関係に対して --allow-newer 指定が必要な場合あり）。Windows ではオプション指定に注意があります。
- エディタ統合: Debug Adapter Protocol (DAP) 経由でエディタと連携します。公式は VS Code 用拡張、Neovim 用の nvim-dap 設定例を案内しています。ほかエディタでも DAP を介して接続可能です。
- 設計と目的: 本デバッガーは小さなスクリプトから大規模コードベースまでを視野に入れた設計で、GHC アプリケーションとして GHC の機能を活用します。HLS（Haskell Language Server）同様、hie-bios による自動セッション設定に対応します。
- 現状と課題: 安定性とパフォーマンスに重きを置いており、テストや GHC 本体のデバッグでの検証も行われていますが、特に大規模プロジェクトではバイトコード生成に時間がかかったり、ライブラリのコードが解釈できないなど使い勝手の残課題があります。ロードマップにはコールスタックやマルチスレッド対応強化が含まれます。
- スポンサーと開発体制: Mercury の支援を受け、Well-Typed チームが中心になって開発しています。ユーザーからのバグ報告や機能要望を歓迎しています。

インストール確認の例（要 GHC 9.14）:
```bash
# bash
ghc --version
cabal install haskell-debugger --allow-newer=base,time,containers,ghc,ghc-bignum,template-haskell --enable-executable-dynamic
# Windows の場合は --enable-executable-dynamic を付けない
~/.local/bin/hdb --version
```

## 実践ポイント
- まずは GHC を 9.14 系に揃える（ghc --version で確認）。  
- 小さなサンプルプロジェクトで導入検証する：まずは単一モジュールの関数にブレークポイントを置いて挙動を確認する。  
- エディタは VS Code が導入と設定が最も簡単（公式拡張あり）。Neovim ユーザーは nvim-dap を利用。  
- パフォーマンスやクラッシュを見つけたら issue トラッカーへ報告することで改善に貢献できる。  
- 大規模プロジェクトでは bytecode 生成時間や外部ライブラリ非解釈の影響が出るため、まずはホットスポット（デバッグしたい箇所）周辺だけを対象に分割して試すと効率的。  
- 将来的な機能（コールスタック表示やマルチスレッド対応）に期待しつつ、現状は「実用的な対話的デバッグ環境」として活用するのが現実的です。

元記事とドキュメントは公式アナウンスおよび haskell-debugger のリポジトリ／issue で随時更新されています。日本の Haskell コミュニティでも導入・検証レポートを共有すると他の現場での採用が進みます。
