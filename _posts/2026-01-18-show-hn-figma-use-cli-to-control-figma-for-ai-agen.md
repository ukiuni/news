---
layout: post
title: "Show HN: Figma-use – CLI to control Figma for AI agents - Figma-use：AIエージェントがFigmaをコマンド操作できるCLI"
date: 2026-01-18T13:46:02.137Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/dannote/figma-use"
source_title: "GitHub - dannote/figma-use: Control Figma from the command line. Full read/write access for AI agents — create shapes, text, components, set styles, export images. 100+ commands."
source_id: 46665169
excerpt: "JSXで実物コンポーネントをFigmaへ即生成、AI連携で自動化するCLIツール"
image: "https://opengraph.githubassets.com/7a6992b544af19cb0bf1f10340c45d936af7e8f1fcd619420565bb453dfd15f6/dannote/figma-use"
---

# Show HN: Figma-use – CLI to control Figma for AI agents - Figma-use：AIエージェントがFigmaをコマンド操作できるCLI
AIがJSXを書くだけでFigma上に本物のコンポーネントを作れる――「figma-use」はCLI中心でFigmaを爆速・自動化するツールです。

## 要約
figma-useはコマンドラインからFigmaを読み書きできるツール群で、JSXをそのままFigmaノードに変換する「render」機能や100以上の細かなコマンドを備え、AIエージェントとの連携を想定したSKILL.mdも同梱しています。

## この記事を読むべき理由
デザイン自動化は日本のプロダクト開発でも注目領域です。エンジニアがコードベースでUIを生成したり、AIにデザイン作業を任せて高速プロトタイピングする流れを簡潔に始められる実用的なツールだからです。

## 詳細解説
- 仕組み（高レベル）
  - CLI（figma-use）→ローカルproxy→Figmaプラグイン（内部のマルチプレイヤープロトコル）という構成。マルチプレイヤー経由の描画はプラグインAPIより高速（作者は約100xを主張）だが実験的でFigmaの内部変更で壊れる可能性がある。
  - AIフレンドリー設計：LLMはReact/JSXに強いため、JSXベースで操作できるrenderコマンドが用意されている。MCP（JSON RPC）よりトークン効率が良く、AIエージェントが多数の操作を行う場合に有利。

- 主な機能
  - render：JSXを受け取り、Frame、Text、Component、Auto-layout、インスタンスなど実際のFigmaノードを生成。
  - 直接コマンド：create/set/node/export/selectionなど、100+のCLI命令で細かな制御が可能。
  - コンポーネント定義：defineComponent / defineComponentSet でコンポーネントやバリアントをコードで定義してFigmaに反映。
  - 変数バインディング：defineVarsでFigma変数に色などを紐づけ可能（ランタイムで名前に基づくバインディング）。
  - AI統合：SKILL.md があり、Claude Code や他のエージェントへそのまま読み込ませることで自動化が容易に。
  - 互換性モード：MCPエンドポイントを公開して、MCP対応クライアント向けツール群も提供。

- セキュリティ・注意点
  - 内部プロトコルを利用する実験的機能があるため、重要ファイルでの運用は慎重に。作業時はファイルのバックアップやコピーで試すことを推奨。
  - ライセンスはMIT。

## 実践ポイント
- インストールと簡単な実行例
  - インストール（例）
```bash
# bash
bun install -g @dannote/figma-use
figma-use plugin install   # Figmaを終了してから実行
figma-use proxy             # proxyを起動
```
  - Figmaをデバッグモードで起動しておく（ローカル接続用）:
```bash
# bash
figma --remote-debugging-port=9222
```
  - JSXをstdinで渡してレンダリング（即実験可）:
```bash
# bash
echo '<Frame style={{width:200,height:100,backgroundColor:"#FF0000"}} />' | figma-use render --stdin
```
- AIと組み合わせる
  - SKILL.md を Claude Code 等のスキルフォルダに置くことで、エージェントにfigma-useコマンド群を使わせる運用がすぐ始められる。
  - token効率を意識する場面では、長いJSONよりJSX/CLIでの指示が有利。

- 日本向け活用案
  - デザインシステムのコード化：コンポーネント定義をリポジトリで管理し、CIでFigmaを更新してデザイン→実装の整合性を保つ。
  - 多言語・ローカライズのワークフロー自動化：テキスト差し替えをスクリプト化して差分スクリーンショットを生成。
  - プロトタイピング高速化：PM/デザイナーが要件をテキストで与え、AIにJSXを生成させて即座にFigma上で確認。

- 注意点まとめ
  - まずはテスト用ファイル／コピーで試すこと。
  - 内部プロトコル依存の機能はFigmaの更新で影響を受ける可能性あり。
  - 認証やチーム権限の扱いは導入前に確認すること。

このツールは「コードでデザインを扱う」流れを加速します。まずは小さなパーツ（ボタンやカード）をJSXで定義→renderして挙動を確認するところから始めると学習コストも低く、すぐに効果が見えます。
