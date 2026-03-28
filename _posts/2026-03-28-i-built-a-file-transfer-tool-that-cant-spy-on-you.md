---
layout: post
title: "I built a file transfer tool that can’t spy on you even if it wanted to - 私はあなたを盗み見できないファイル転送ツールを作った"
date: 2026-03-28T22:30:02.843Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://dev.to/aliirz/i-built-a-file-transfer-tool-that-cant-spy-on-you-even-if-it-wanted-to-2p39"
source_title: "I built a file transfer tool that can’t spy on you even if it wanted to - DEV Community"
source_id: 3408110
excerpt: "URLフラグメントで鍵を保持、サーバが覗けない自己消滅型ファイル共有サービス"
image: "https://media2.dev.to/dynamic/image/width=1200,height=627,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Fgz96ymyrv3yzbw13zl02.png"
---

# I built a file transfer tool that can’t spy on you even if it wanted to - 私はあなたを盗み見できないファイル転送ツールを作った
ブラウザだけで完結する“覗けない”ファイル転送—鍵はURLのハッシュに隠す

## 要約
ブラウザ側でAES-256-GCMで暗号化し、復号キーをURLのフラグメント（#以降）に入れることでサーバ側が鍵を一切知らない「ゼロ知識」なファイル転送（phntm.sh）。リンク共有で受け取り側がブラウザで復号、自己消滅機能あり。

## この記事を読むべき理由
日本でも機密情報や個人情報の取り扱いは重要で、外部サービスへ丸投げできない場面が多い。ログイン不要で手軽に安全に送れる選択肢は、リモートワークや顧客データの一時共有で実務的価値が高い。

## 詳細解説
- 基本アイデア：ファイルはクライアント（送信者のブラウザ）で256ビットのAES鍵を生成してAES-256-GCMで暗号化。暗号文だけがサーバへ送られる。  
- 鍵の扱い：復号キーはURLのフラグメント（#以下）に埋め込む。RFC 3986によりブラウザはフラグメントをHTTPリクエストに含めないため、サーバは鍵を受け取らない（=「cannot read」）。  
- 受信側：受信者は同リンクを開き、ブラウザが暗号文を取得してフラグメント内の鍵でローカル復号してダウンロードする。アカウント不要。  
- オープンソース性：ソースを公開しているため、暗号処理や鍵の送信有無を第三者が検証できる。信頼は主張ではなく検証可能なコードで担保する設計。  
- 現状の課題：ブラウザ側でファイル全体をメモリにバッファするため大容量ファイルに弱い。Vercel Analyticsのようなサードパーティスクリプトがlocation.hrefを送信するとフラグメントが漏れる問題が発覚し、外部スクリプトの監査が必須だと判明。  
- CLIと実装面：CLIはGo（標準ライブラリのみ）で実装。Goのio.Reader/Writerの組合せで進捗表示とストリーム処理がうまく組める点が学び。将来的にはブラウザ側のストリーミング暗号化（Web Streams API等）でメモリ問題を解くのが自然な進化。

## 実践ポイント
- 使いどころ：アカウント不要で一時的に安全に渡したいファイル（小〜中容量）に有効。自己消滅設定で残存リスクを減らせる。  
- 注意点：LINEや一部のチャット・メールクライアントでURLフラグメントが扱われる／改変される場合があるため、実運用前に相手の環境で必ず動作確認を。  
- セキュリティ運用：サードパーティスクリプトを入れない／監査すること。フラグメントを送るような外部ライブラリは致命的。  
- 大容量対応：ブラウザでのバッファ問題がネック。大量ファイルはCLI版や別途ストリーミング対応のツールを検討する。  
- 検証先：実装や暗号層を自分で確認したい場合は公式サイトとGitHubリポジトリを参照すること。  
  - https://phntm.sh  
  - https://github.com/aliirz/phntm.sh  
  - https://github.com/aliirz/phntm-cli

短く言えば、「鍵をブラウザだけに置く」アプローチは実務上すぐ役立つが、運用上の小さな落とし穴（サードパーティ、メッセージングの扱い、大容量対応）を理解して使うことが重要です。
