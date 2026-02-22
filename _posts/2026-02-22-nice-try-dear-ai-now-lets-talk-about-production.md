---
layout: post
title: "Nice try dear AI. Now let's talk about production. - AIよ、ご苦労。さて、本番運用の話をしよう"
date: 2026-02-22T04:58:57.673Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://krasimirtsonev.com/blog/article/nice-try-dear-ai-now-lets-talk-production"
source_title: "Nice try dear AI. Now let's talk about production."
source_id: 399732567
excerpt: "Copilotで作ったS3リリース脚本の落とし穴と本番運用の注意点を実例で解説"
image: "https://storage.googleapis.com/lumina_ktcom/KhVOdxkA1/ai_450x.png"
---

# Nice try dear AI. Now let's talk about production. - AIよ、ご苦労。さて、本番運用の話をしよう
「AI任せ」は危ない？Copilotと作ったS3リリーススクリプトで見えた“現場の勘所”

## 要約
著者はCopilotでS3へアップロードするリリーススクリプトを作らせ、何度も手直しして完成させる過程を通じて「AIは補助には強いが判断と文脈理解は人間が必要」と結論付ける。

## この記事を読むべき理由
日本の開発現場でもCopilot等を導入する流れが進む中、AI生成コードの落とし穴（環境前提、認証、運用フローの順序など）と、それを補うために必要な基礎知識が具体例で学べるから。

## 詳細解説
- 初期プロンプトと結果：著者は「別プロジェクトからnode path/to/scripts/release.jsで実行する」意図を伝えたが、Copilotはスクリプト内のprojectRootを誤解し、期待と違う動作（親フォルダ参照／npm packでtgz生成）をした。これはモデルが一般的なパターンを優先するため。
- AWS操作の実装選択：Copilotはaws CLIを使う案を出したが、著者はNode用の@aws-sdk/client-s3を使いたかった。ここでnpm installがE401（認証エラー）になり、.npmrcでのprivateパッケージ認証の重要性が浮上した。
- 設定とDX改善：最初はバケット情報をスクリプトに埋め込んでいたが、release.jsonという外部設定ファイルに切り出すことでプロジェクトごとの差分対応を実現。テンプレート生成や存在チェックも追加。
- 挙動の細部（望まれる振る舞い）の指示：単一tgzではなくdistフォルダの中身をアップロードする、CHANGELOGは1行の説明にする、環境（dev/stage/prod）ごとのバケット切り替え、operationの原子性（アップロードが成功してからpackage.json/CHANGELOGを更新）、バケット内のversion.jsonを更新して最新版を記録、などを逐次指示して仕上げた。
- 学んだ前提知識：CLIの設計、semantic versioning、CHANGELOGの意義、process.cwd()の挙動、Nodeのchild_process、npmのprivate認証(.npmrc)、設定ファイルパターン、運用順序の重要性、環境切替の考え方。

## 実践ポイント
- プロンプトは「文脈」を伝える：実行場所（process.cwd()）、期待する出力形（フォルダ vs tgz）、認証要件などを明記する。
- 小さく試す・逐次検証：AI出力をそのまま信じず、動作確認→不具合点を順に指摘して直すループを回す。
- 設定ファイルを最初から用意する：環境・バケット・フォルダはrelease.jsonなどで切り分けると再利用性が高まる。
- 認証と依存関係を確認：private npmやAWS認証が絡む場合は .npmrc や環境変数の前提を明示し、CI環境も含めて検証する。
- 操作の原子性を保つ：アップロード成功を確認してからpackage.jsonやCHANGELOGを更新するなど、途中失敗で不整合にならない順序を設計する。
- ドキュメントとDXを忘れない：release.mdで使い方・設定・認証手順を短くまとめ、導入障壁を下げる。

著者の結論：AIは生産性を高める「増幅器」であり、正しい判断や運用設計はソフトウェアエンジニアの基礎知識が必要。特に日本企業の複雑な認証やオンプレ・社内レジストリ等の事情を考えると、学習を怠らないことがより重要になる。
