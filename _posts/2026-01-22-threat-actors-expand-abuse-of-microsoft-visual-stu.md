---
layout: post
title: "Threat Actors Expand Abuse of Microsoft Visual Studio Code - 攻撃者がMicrosoft Visual Studio Codeの悪用を拡大"
date: 2026-01-22T02:14:58.752Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.jamf.com/blog/threat-actors-expand-abuse-of-visual-studio-code/"
source_title: "Threat Actors Expand Abuse of Microsoft Visual Studio Code"
source_id: 46713526
excerpt: "tasks.json悪用でVS Codeを開くだけで感染、採用リポジトリに潜むバックドア"
image: "https://media.jamf.com/images/icons/jamf-og-image.jpg"
---

# Threat Actors Expand Abuse of Microsoft Visual Studio Code - 攻撃者がMicrosoft Visual Studio Codeの悪用を拡大
VS Codeを開くだけで感染する？採用リポジトリを悪用した“見せかけの課題”攻撃の全貌

## 要約
攻撃者がGitリポジトリ内のVisual Studio Code設定（tasks.json）を悪用し、ユーザーがリポジトリを「信頼」して開くと自動でNode.jsベースのバックドアを取得・実行する手口が確認されました。被害はmacOSを含む開発環境に及びます。

## この記事を読むべき理由
日本の開発者や採用担当はGitHub/GitLabでの課題やサンプルコードを日常的に扱います。VS Codeの普及度が高い日本市場では、疑わしいリポジトリを開いただけで社内端末が乗っ取られるリスクが現実的です。

## 詳細解説
- 感染の入口  
  - 攻撃者は採用プロセスや技術課題に見せかけた悪意あるリポジトリを用意。被害者がリポジトリをクローンしてVS Codeで開き、「このフォルダーを信頼しますか？」に同意すると、tasks.jsonが自動処理され任意コマンドが実行されます。
- 実行フロー（高レベル）  
  - tasks.jsonからnohup + bash -c + curl … | nodeのようなコマンドで外部のJavaScriptペイロードを取得し、Nodeランタイムで実行。Vercelなどパブリックホスティングを悪用して配布されることが観測されています。
- ペイロードの中身（バックドア機能）  
  - 多数の無駄なコードで難読化されているが、実質は小さなルーチンで構成。主な機能は：  
    - 動的リモートコード実行（サーバから受け取ったJS文字列をnew Functionで実行し、requireを渡して追加モジュールも読み込める）  
    - システムフィンガープリント（ホスト名、MACアドレス、OS情報、公開IPを収集）  
    - 5秒間隔でC2サーバへビーコンを送り、受け取った応答（JS命令）を実行するポーリングループ  
    - 管理下プロセスの生成・終了管理（子プロセスのデタッチや強制終了など）  
- 運用・回避の工夫  
  - 攻撃者はペイロードURLを差し替え、ホスティング停止後も別URLへ移行するなど持続性を確保。DPRK関連活動との関連も報告されています。

## 実践ポイント
- リポジトリの「信頼」は慎重に：見知らぬリポジトリは必ず信頼せず、コードを読む・サンドボックスで開く。  
- VS CodeのWorkspace Trust機能を理解・利用する（自動実行を遮断）。  
- tasks.jsonや拡張機能、起動コマンドを開いたらまず確認する習慣をつける。  
- エンドポイントでNode実行や外向けHTTPを監視・制限する（社内ファイアウォールやプロキシで不審なIP/ドメインをブロック）。  
- 開発マシンに不要なランタイム（例: Node.js）がある場合は最小限にする、あるいは隔離された環境で作業する。  
- 不審なリポジトリは速やかにGitHub/GitLabへ報告する。  
- 採用担当へ注意喚起：提出物をそのままローカルで実行しない運用ルールを設ける。

短時間で感染→遠隔操作され得るシンプルだが効果的な攻撃です。日常的な開発フローの小さな「確認」を徹底することで被害を大幅に減らせます。
