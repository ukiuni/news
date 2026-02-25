---
layout: post
title: "Fake Job Interviews Are Installing Backdoors on Developer Machines - フェイク採用面接が開発者マシンにバックドアを仕掛ける"
date: 2026-02-25T12:00:49.701Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://threatroad.substack.com/p/fake-job-interviews-are-installing"
source_title: "Fake Job Interviews Are Installing Backdoors on Developer Machines"
source_id: 396971883
excerpt: "採用課題の偽Next.jsリポジトリを開くだけで開発機にバックドアが仕込まれる危険性と即対策"
image: "https://substackcdn.com/image/fetch/$s_!X2qO!,w_1200,h_675,c_fill,f_jpg,q_auto:good,fl_progressive:steep,g_auto/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1ba83610-1b91-4564-b483-93bd9a4c7626_1280x720.jpeg"
---

# Fake Job Interviews Are Installing Backdoors on Developer Machines - フェイク採用面接が開発者マシンにバックドアを仕掛ける
魅惑的なタイトル: 面接用の「コーディング課題」を開くだけでマシンが乗っ取られる――開発者が今すぐ守るべき3つの侵入経路

## 要約
マルウェア作者がNext.jsなどの偽リポジトリ（採用向け「技術課題」）を使い、開発者の日常ワークフロー（フォルダを開く、npm run dev、サーバ起動）をトリガーにバックドアを仕込む攻撃が確認された。複数の実行経路で同一の二段階C2に接続する。

## この記事を読むべき理由
日本でもVS Code＋Next.jsは一般的で、リモート採用やGitでの課題提出が増える中、業務端末や個人PCが企業のクラウド／コード資産を危険にさらす現実的なリスクがあるため。

## 詳細解説
攻撃は偽の「採用向け技術課題」リポジトリ（例: Cryptan-Platform-MVP1）を使い、開発者の普通の操作を悪用する。主な3経路：

- VS Codeワークスペース自動実行  
  - `.vscode/tasks.json` の `runOn: "folderOpen"` を悪用し、フォルダを「開いて信頼」した瞬間にタスクが自動実行される。

- ビルド/開発サーバ実行時のトロイ化資産  
  - `jquery.min.js` 等に難読化されたコードを忍ばせ、`npm run dev` 実行時にVercel等からJSローダを取得して実行する。

- サーバ起動時のリモート命令実行  
  - サーバルートが `.env` 内のbase64化エンドポイントを復号して `process.env` を送信、返却されたJSを `new Function()` 等で実行する。

これらはすべて共通の二段階C2へ接続する設計：軽量なレジストラが `instanceId` を払い、持続コントローラが `messages[]` 配列経由でJSタスクを送り、NodeにSTDINで流し込んで実行する。結果として資格情報・セッション・ソースコード・クラウドキーの窃取やファイルアップロードが行われ得る。

観測されたIOC（一部）
- ドメイン: `api-web3-auth.vercel.app`, `price-oracle-v2.vercel.app`  
- IP: 87.236.177.9, 147.124.202.208, 163.245.194.216  
- エンドポイント: `/api/errorMessage`, `/api/handleErrors`, `/hsocketNext`, `/upload`, `/uploadsecond`

## 実践ポイント
開発者向け（すぐできる対策）
- 不明リポジトリはVS CodeのWorkspace Trustで「信頼しない」。Restricted Modeを有効化。  
- リポジトリを開く前に ` .vscode/tasks.json`, `next.config.js`, 及び `package.json` のスクリプトを必ず確認。  
- オンライン面接や課題は業務PCで直接実行しない。隔離されたVM／サンドボックスを使う。  
- 採用通知は公式チャネルで確認し、レポジトリリンクのみで信用しない。

セキュリティチーム向け
- Node.jsが短周期で外部（特に `vercel.app` ドメイン）へ接続する通信を検出するルールを追加。  
- 親プロセスと切り離されたNode子プロセスや、Code.exe/node.exeによる `.env` など秘密情報ファイルへの不審なアクセスを監視。  
- Microsoft Defender のASR（攻撃面縮小）ルールで難読化スクリプト実行をブロック。IOCでのハンティングを実行。

短くまとめると：採用課題や外部リポジトリは「便利だが危険」──開く前に必ず確認し、実行は隔離された環境で。
