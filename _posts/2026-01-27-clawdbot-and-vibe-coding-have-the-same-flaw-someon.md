---
layout: post
title: "Clawdbot and vibe coding have the same flaw. Someone else decides when you get hacked. - Clawdbotとvibe codingは同じ欠陥を持つ。ハックされるタイミングを決めるのは他人だ"
date: 2026-01-27T08:20:25.190Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://webmatrices.com/post/clawdbot-and-vibe-coding-have-the-same-flaw-someone-else-decides-when-you-get-hacked"
source_title: "Clawdbot and vibe coding have the same flaw. Someone else decides when you get hacked. | digitaldave01 | Webmatrices"
source_id: 417617865
excerpt: "Clawdbotやvibe codingは外部がハックの発火権を握る危険がある"
image: "https://webmatrices.com/og/clawdbot-and-vibe-coding-have-the-same-flaw-someone-else-decides-when-you-get-hacked-digitaldave01.png"
---

# Clawdbot and vibe coding have the same flaw. Someone else decides when you get hacked. - Clawdbotとvibe codingは同じ欠陥を持つ。ハックされるタイミングを決めるのは他人だ
あなたのプロダクトが「誰かのスキャン待ち」になっていないか？──便利さの裏にある“アクセスを渡す”リスク

## 要約
AIエージェントやvibe codingで作られたアプリは、外部からの入力や自動化がそのまま攻撃経路になり得る。便利さの代償として、あなたは「いつ」ハックされるかを選べない状況に置かれている。

## この記事を読むべき理由
日本でもスタートアップや個人開発でAIツールやノーコードが急速に普及中。LINEやクラウドDBを接続した瞬間、国内環境でも同様のリスクが現実化する可能性が高く、事前対策が不可欠です。

## 詳細解説
- Clawdbotの問題点
  - 自律的エージェントがローカルでフルシェル、ブラウザセッション、ファイルシステム、メール等にアクセス可能。
  - WhatsAppなどを経由して受信したメッセージがそのままエージェントの入力になるため、外部から任意の指示（プロンプトインジェクション）が実行され得る。
  - PDFやメール内に埋め込んだ命令でファイル作成や機密転送が行われる実証例あり。実際、エージェントは権限の枠を越えて動く挙動が報告されている。
- vibe coding（Lovable等）の問題点
  - 自動生成されたバックエンドはフロント・DB接続・認証の一部しか担保せず、業務ロジック・レート制限・監査ログなど“見えない80%”が欠落することが多い。
  - Row Level Security（RLS）設定ミスなど単純なDB設定ミスが放置され、スキャナーで簡単に列挙される事例が頻出。研究者が自動スキャンして発見する状況。
  - 「プロンプトでセキュリティ指示すれば安全」は誤解。生成物は非決定的で検証困難。
- 共通の本質
  - 攻撃のトリガー（受信メッセージ、スキャン、 malformed input 等）を「他者」が握っている点。
  - 実データ：記事ではAI生成コードの脆弱性が45%という調査値、AIエージェントのタスク失敗率を示す報告（例：70%）が引用され、ツールの不安定性と危険性を強調。
- 責任と現実
  - オープンソースやAIが被害を受けても、説明責任・損害賠償は人間（開発者/運営者）に降りかかる点。事前に誰が責任を負うか定められていないケースが多い。

## 実践ポイント
- まず切り分ける
  - AIエージェントはメイン端末で動かさない。専用マシン／VMで隔離し、重要なSSH鍵やパスワードマネージャは絶対持ち込まない。
  - メッセンジャー連携（日本だとLINE等）を行う場合は「バーナー番号/アカウント」を使う。
- 最小権限の原則
  - ツールに与えるアクセスは必要最低限のみ。バックエンドやDBへの書き込み・キーアクセスは厳格に制御。
- デプロイ前の必須チェック
  - 決済・書き込み・機密データを扱う前に有償のセキュリティレビューを受ける（自動レビューだけで安心しない）。
  - RLSや認可ロジック、レート制限、監査ログを必須で設計・検証する。
- 出せないなら出さない
  - 「何を作ったか説明できない」「生成されたバックエンドの動作を監査できない」場合は本番公開しない。
- 監視と想定外対応
  - 自動スキャナーや攻撃の兆候（異常なDBクエリ、外部転送）を監視し、インシデント対応フローを用意する。

短く言えば：ツールの便利さに流されて「アクセス」を安易に渡さないこと。誰かが攻撃の発火ボタンを握る前に、あなたがドアに鍵をかけること。
