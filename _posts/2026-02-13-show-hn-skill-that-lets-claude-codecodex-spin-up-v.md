---
layout: post
title: "Show HN: Skill that lets Claude Code/Codex spin up VMs and GPUs - Claude Code/CodexにVMやGPUを立ち上げさせるスキルを公開"
date: 2026-02-13T20:21:21.865Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://cloudrouter.dev/"
source_title: "cloudrouter — Cloud VMs/GPUs for Claude Code/Codex"
source_id: 47006393
excerpt: "ローカルからワンクリックでGPUクラウド環境を起動しAIに作業を任せるツール"
---

# Show HN: Skill that lets Claude Code/Codex spin up VMs and GPUs - Claude Code/CodexにVMやGPUを立ち上げさせるスキルを公開
ローカルから1コマンドでGPU付きクラウド開発環境を即起動／AIエージェントに操作させる「cloudrouter」

## 要約
cloudrouterはローカルディレクトリやリポジトリからワンクリック（CLIコマンド）でクラウドサンドボックス（VM/GPU）を作成し、VS CodeやVNC、ターミナル、Chrome自動操作まで一貫して扱えるツール。Claude CodeやCodexなどのAIエージェント用の「スキル」として組み込めます。

## この記事を読むべき理由
日本でもモデル推論や微調整、コンテナ開発を手元のマシンで完遂できない場面は多く、手早くGPU環境を立ち上げてAIエージェントに作業を任せられるのは開発効率を大幅に上げます。ローカル開発→クラウド実行のハンドオフが簡単になるため、小規模チームや個人研究者に有用です。

## 詳細解説
- インストール／スキル導入  
  - AIエージェントのスキルとして導入:  
    ```bash
    npx skills add manaflow-ai/cloudrouter
    ```
  - 単独CLIとして:  
    ```bash
    npm install -g @manaflow-ai/cloudrouter
    cloudrouter login
    ```
- 主要ワークフロー  
  - カレントディレクトリからサンドボックス作成:
    ```bash
    cloudrouter start .
    ```
  - GPU付き起動例:
    ```bash
    cloudrouter start --gpu T4 .
    cloudrouter start --gpu H100:2 .
    ```
  - アクセス方法: ブラウザ版VS Code（cloudrouter code <id>）、VNC、対話ターミナル（pty）、一回コマンド実行（ssh）
- ブラウザ自動化（Chrome CDP）  
  - サンドボックス内のChromeをCLI経由で操作（ナビゲート、フォーム入力、スクリーンショット、アクセシビリティツリー取得）。
  - 例: 要素に入力してクリックする自動化が可能。
- ファイル同期とwatchモード  
  - upload / downloadコマンドでローカル⇄サンドボックス同期。--watchで変更時自動アップロード。
  - リモートパス指定は -r フラグを使う点に注意。
- GPU種類と用途（抜粋）  
  - T4（16GB）: 小規模推論/微調整  
  - A100（40/80GB）: 大規模モデル学習・推論  
  - H100/H200/B200: 研究・最先端モデル向け（多くは承認が必要）
- 注意点（運用上の重要指示）  
  - startでは原則 --size を指定しない（デフォルトは large = 8 vCPU, 32GB）。小さくしすぎるとビルド失敗の原因に。  
  - cloudrouter ssh のコマンド文字列は必ず引用符で囲む（フラグ誤解釈を防ぐ）。  
  - npm系の初回エラー回避: サンドボックスで npm を使う前に所有権修正が必須。
    ```bash
    cloudrouter ssh <id> "sudo chown -R 1000:1000 /home/user/.npm"
    ```

## 実践ポイント
- まずはインストール→ログイン→カレントディレクトリから起動:
  ```bash
  npm install -g @manaflow-ai/cloudrouter
  cloudrouter login
  cloudrouter start .
  cloudrouter code <id>
  ```
- GPUで試したいなら自己申請不要なT4/L4/A10Gから試す。大量GPUは承認が必要。  
- 連携するAIエージェントにスキルを追加すると「AIに環境作成→テスト→スクリーンショット取得」を自動化させられる。CIやプロトタイピングで有効。  
- ファイル同期は -r を正しく使い、--watch でローカル編集→即反映の開発体験を得る。  
- 日本の企業での活用ではデータやコスト管理、コンプライアンス（機密データを外部GPUへ送らない等）を事前に確認すること。

短時間でGPU環境を作って手元の開発環境をクラウドに移行したい場合、cloudrouterはすぐに試す価値があります。
