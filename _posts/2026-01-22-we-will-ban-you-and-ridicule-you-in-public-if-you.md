---
layout: post
title: "We will ban you and ridicule you in public if you waste our time on crap reports - 無意味な報告なら追放します（curlのセキュリティ注意書き）"
date: 2026-01-22T11:44:27.098Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://curl.se/.well-known/security.txt"
source_title: "We will ban you and ridicule you in public if you waste our time on crap reports"
source_id: 46717556
excerpt: "curlが雑な脆弱性報告を公開で罵倒・追放する真意と正しい報告手順"
---

# We will ban you and ridicule you in public if you waste our time on crap reports - 無意味な報告なら追放します（curlのセキュリティ注意書き）
セキュリティ報告の「やるべきこと／やってはいけないこと」をcurlがストレートに伝える瞬間 — 開発者に敬意を払う報告の作法を学ぼう

## 要約
curlが公開している /.well-known/security.txt は、脆弱性報告の窓口・方針・期待値を明確に示しており、「雑な報告は受け付けない」と断言しています。報告者は方針に従い、英語で具体的な再現手順を提供する必要があります。

## この記事を読むべき理由
curlは世界中で広く使われるHTTPクライアント／ライブラリで、日本の開発環境やインフラでも頻繁に登場します。正しい報告の方法を知ることは、自分やチームの脆弱性対応能力を高めるだけでなく、オープンソースプロジェクトと建設的に関わるために重要です。

## 詳細解説
- /.well-known/security.txt は標準的な場所に置かれた「セキュリティ窓口情報」ファイルで、curl の例では次の情報が含まれます：連絡先メール（security@curl.se）、GitHubのセキュリティアドバイザリ、脆弱性開示ポリシー、優先言語（en）、謝辞ページ、期限・正規URL。
- curlは「報酬（バウンティ）は提供しない」と明記しつつ、確認済み問題には文書上での謝辞を約束しています。逆に「時間を浪費するような低品質の報告には制裁（banや公開での嘲笑）」と強い言い回しで注意喚起しています。これはプロジェクトの運用負荷を減らすための姿勢表明です。
- 技術的には、報告にはバージョン情報、再現手順、最小限の再現コードやログ、期待される挙動と実際の挙動を含めることが求められます。PoC（Proof of Concept）があると対応が早くなります。
- また「Preferred-Languages: en」とある通り、英語での報告がスムーズです。GitHubのsecurity advisories を使えば公開管理や追跡が容易になります。

## 実践ポイント
- まず公式ポリシー（https://curl.se/dev/vuln-disclosure.html）を読む。報告前の必須ステップ。
- 報告時に必ず書くこと：curlバージョン、OS/環境、再現手順、最小再現例（コード/コマンド）、ログ/クラッシュダンプ。
- 英語で簡潔に書く。難しければ要点は英語、補足を日本語で添えるのも可。
- 直接メール（security@curl.se）か GitHub の security advisory を使う。公開前にやり取りが必要な場合は非公開で連絡。
- 期待値を正しく設定する（金銭的報酬はないが、確認されれば謝辞あり）。雑な試行錯誤やノイズ報告は避ける。

短く言えば：curlは「真剣な、再現可能な報告」を歓迎します。日本の開発者としては、きちんと整理した情報を英語で提供できるよう準備しておくと、より建設的に貢献できます。
