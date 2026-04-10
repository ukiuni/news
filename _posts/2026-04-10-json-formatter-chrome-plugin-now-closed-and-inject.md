---
layout: post
title: "JSON Formatter Chrome Plugin Now Closed and Injecting Adware - JSON Formatter Chrome拡張がクローズ化＆（報告される）広告挿入"
date: 2026-04-10T20:14:07.932Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/callumlocke/json-formatter"
source_title: "GitHub - callumlocke/json-formatter: Makes JSON easy to read. · GitHub"
source_id: 47721946
excerpt: "愛用のJSONビューアがクローズ化、更新で広告挿入の報告—今すぐ代替版へ切替を"
image: "https://opengraph.githubassets.com/2a8a44c8ffa5865c90c2dd31d9d74944ca636cb533df2d8d65121056bf1d32eb/callumlocke/json-formatter"
---

# JSON Formatter Chrome Plugin Now Closed and Injecting Adware - JSON Formatter Chrome拡張がクローズ化＆（報告される）広告挿入
魅力的なタイトル例: 「愛用のJSONビューアが急変：オープンソース終了で『クラシック版へ切り替え』が必須になった理由」

## 要約
人気のChrome拡張「JSON Formatter」が作者の方針変更でオープン開発を終了し、クローズド／商用モデルへ移行しました。ユーザーからはアップデート後の望ましくない挙動（広告表示など）の報告もあり、注意が必要です。

## この記事を読むべき理由
JSONビューワはAPI開発やデバッグで日常的に使うツールです。拡張がクローズド化・挙動変化するとセキュリティやプライバシー、ワークフローに直結するため、日本のエンジニアやQA担当者も影響を受けます。

## 詳細解説
- 変更点の本質：リポジトリは「ARCHIVED（開発終了）」と明記され、今後はクローズドな商用版へ移行する旨が示されています。作者は最終のオープンソース版を「JSON Formatter Classic」として残しています。  
- 機能の概要：元の拡張は高速レンダリング、ダークモード、構造化表示（折りたたみ）、URLのクリック可能化、Raw/Parsedの切替などを提供。パース後のデータはグローバル変数`json`としてコンソールから確認可能でした。  
- 実装上の注意点：JSON判定は主にContent-Typeヘッダに依存し、場合によってはページ構造を解析して判定します。大きな数値はJavaScriptのNumberの制約（Number.MAX_SAFE_INTEGER）により精度が落ちること、オブジェクトキーの順序はJSON.parse後の表現に依存することなど、仕様由来の振る舞いがあります。  
- 問題点とリスク：拡張がクローズド化するとコードレビューできなくなるため、更新で広告挿入や望ましくない通信が入るリスクが高まります。配布元や更新履歴、権限変更を確認することが重要です。報告内容はソース内の明記と利用者報告に基づくもので、確定的な悪意の断定は避けるべきですが、慎重な対応が推奨されます。

## 実践ポイント
- 今すぐ：Chrome拡張の自動更新を一時オフにし、最新更新の変更ログと権限を確認する。  
- 代替手段：作者が残した「JSON Formatter Classic」などのオープンソース版へ切り替える、あるいは別の信頼できるオープンソース拡張を使う。  
- 検証方法：拡張のネットワーク通信をDevToolsのNetworkタブで監視し、不審な外部接続や広告スクリプトの挿入を確認する。  
- 開発者向け：ローカルでソースをビルドしてアンパック拡張として利用する（READMEにbunを使ったビルド手順あり）。  
- チーム運用：社内ポリシーで許可する拡張のリスト管理と定期的なセキュリティチェックを導入する。

（参考）元リポジトリはアーカイブされており、最終オープン版が別名で残されています。利用前に公式告知とユーザー報告を必ず確認してください。
