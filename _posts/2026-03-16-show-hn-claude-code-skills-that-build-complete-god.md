---
layout: post
title: "Show HN: Claude Code skills that build complete Godot games - Claude Codeスキルで完全なGodotゲームを自動生成"
date: 2026-03-16T22:01:54.230Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/htdt/godogen"
source_title: "GitHub - htdt/godogen: Claude Code skills that build complete Godot 4 projects from a game description · GitHub"
source_id: 47400868
excerpt: "Claude Codeで設計〜アセット生成〜実行確認を自動化し、Godot4の動くプロトタイプを短時間で生成"
image: "https://opengraph.githubassets.com/502411296c0799142c05ebbabc3b62885fd77eafffd37eaa26acb0b40c4f00d1/htdt/godogen"
---

# Show HN: Claude Code skills that build complete Godot games - Claude Codeスキルで完全なGodotゲームを自動生成
AIにゲーム開発を任せる――Godot 4プロジェクトをゼロから生成するClaude Codeパイプライン

## 要約
ユーザーのゲーム説明から、設計→アセット生成→コード生成→実行確認までを自動化し、実際に動くGodot 4プロジェクトを出力するオープンソースツールチェーン（godogen）の紹介。

## この記事を読むべき理由
少人数や個人のインディー開発でも、AIを使って短時間でプロトタイプを作れる時代が来たことを実感できる。日本の小規模チームやハッカソン参加者にとって即戦力になる手法とツールが公開されている。

## 詳細解説
- 全体の仕組み  
  - 「計画するスキル（planner）」と「実行するスキル（executor）」という2つのClaude Codeスキルがパイプラインをオーケストレーション。各タスクは新しいコンテキストで実行され、焦点を保つ設計。  
  - 出力は実際に動くGodot 4プロジェクト：整理されたシーンツリー、読みやすいGDScript、資産フォルダ構成まで整備される。

- アセット生成と視覚的QA  
  - 2Dアート／テクスチャはGemini、画像→3Dモデル変換はTripo3Dを利用。  
  - 実行中のエンジンからスクリーンショットを取り、Gemini Flashで視覚的なQAを行う（z-fighting、テクスチャ抜け、物理の破綻などを検出・修正）。

- GDScript対応策  
  - GDScriptはLLMの訓練データが薄いため、850+のGodotクラスを補足するカスタム言語リファレンスと遅延ロードAPIドキュメントで補強して正確なスクリプト生成を行う。

- 実行環境と制約  
  - 必要なもの：Godot 4（ヘッドレス可）、Claude Code、Python3、環境変数にAPIキー（GOOGLE_API_KEY、TRIPO3D_API_KEY）。  
  - 単一生成は数時間かかることがあり、GPU付きクラウドVM（例：GCEのT4/L4）が推奨。Ubuntu/Debianで動作確認済み、macOSはスクリーンキャプチャの追加対応が必要。

- 開発フローの始め方  
  - リポジトリにはスキル群とテンプレがあり、publish.shで新規プロジェクトフォルダを生成してClaude Code内からゲームを指定するとパイプラインが動く。

- 代替と今後の展望  
  - Claude Code（Opus 4.6）が最良、SonnetやOpenCodeでも動く。今後は画像生成コスト削減やアニメスプライト生成、Androidビルドレシピ追加などを計画。

## 実践ポイント
- まずリポジトリをクローンし、必要なAPIキーを環境変数に設定する。  
- 簡単なプロジェクト作成例：
```bash
# bash
./publish.sh ~/my-game        # デフォルトのCLAUDE.mdを使用
./publish.sh ~/my-game local.md  # カスタムCLAUDE.mdを指定
```
- 長時間処理とGPUが必要なので、クラウドVM（T4/L4等）を用意すると効率的。  
- Teleforge設定でスマホから進捗監視が可能（日本からも使いやすい）。  
- コスト管理を意識してアセット数やレンダ回数を調整すること。  
- GodotやGDScriptに不慣れでも、このワークフローでシーン構成やスクリプト設計の学習材料が得られる。

元リポジトリ: https://github.com/htdt/godogen
