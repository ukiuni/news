---
layout: post
title: "Your IDE is an Attack Vector - あなたのIDEが攻撃経路になる"
date: 2026-02-17T14:39:04.335Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://dev.to/aezur/your-ide-is-an-attack-vector-2i0b"
source_title: "Your IDE is an Attack Vector - DEV Community"
source_id: 3249896
excerpt: "VSCodeの自動タスクでリポジトリを開くだけで遠隔実行される攻撃と即対策"
image: "https://media2.dev.to/dynamic/image/width=1000,height=500,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Fqkslya75qjll07u9xch3.png"
---

# Your IDE is an Attack Vector - あなたのIDEが攻撃経路になる
開いた瞬間に感染？VSCodeを狙う巧妙なフィッシング手口と即実践できる防衛策

## 要約
VSCodeの「タスク」機能を悪用し、リモートから自動でコマンドを実行させるフィッシング手法が報告された。特にフリーランス向け求人を経由した標的選別と組み合わさる点が危険。

## この記事を読むべき理由
フリーランスやリモート開発が一般化した日本でも同様の手口は有効で、ウォレットやAPIキーを扱う開発者、外注先を選ぶ立場の人は知らないと被害に遭う可能性が高い。

## 詳細解説
- 攻撃の仕組み  
  - VSCodeはプロジェクトルートの .vscode/tasks.json でタスク（エディタから外部コマンドを起動する定義）を管理する。  
  - tasks.json の runsOn に "folderOpen" を指定すると、フォルダを開いたときに自動でコマンドを実行できる。  
  - VSCodeの「このワークスペースを信頼しますか？」で「信頼」すると、ユーザー設定でブロックしていても自動実行が許可される場合がある。  
- 社会工学の要素  
  - 攻撃者はUpworkのような求人サイトで高額かつ魅力的な案件を出し、関心のある開発者を「テストリポジトリ」をクローンさせる。  
  - タスクの中に長い空白で隠した wget やリモートのスクリプト実行コマンドが仕込まれ、リポジトリを開いただけでマルウェアが降ってくるケースが報告されている。  
- 影響範囲  
  - 特に仮想通貨／DeFi系の開発者は鍵やウォレット情報を扱うことが多く、狙われやすい。  
  - フリーランスの提案競争で焦って検査を怠るとリスクが増える。

## 実践ポイント
- 未知のリポジトリはデフォルトで「信頼」しない。ワークスペースの信頼確認は慎重に。  
- 不審なリポジトリはコンテナ（devcontainers）やVMで開く。ホストで直接開かない。  
- タスクとスクリプトを確認：.vscode/tasks.json、package.json の preinstall/postinstall を必ず読む。  
- 拡張機能を無効にして開く：code --disable-extensions . で挙動を確認。  
- 常用PCと検証環境を分離。サンドボックスで挙動を観察してから実作業に移す。  
- 自分のプロジェクトでは .vscode を .gitignore に入れるなど、不要なメタ情報を共有しない。

（参考元: "Your IDE is an Attack Vector"）
