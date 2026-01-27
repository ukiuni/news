---
layout: post
title: "Prompt Injection: The SQL Injection of AI + How to Defend - プロンプトインジェクション：AI版SQLインジェクションと防御法"
date: 2026-01-27T18:40:52.326Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://lukasniessen.medium.com/prompt-injection-the-sql-injection-of-ai-how-to-defend-2a28c6f3bc05"
source_title: "Prompt Injection: The SQL Injection of AI + How to Defend"
source_id: 416016948
excerpt: "外部データでAIが乗っ取られる危険と即効防御策を実務視点で図解"
---

# Prompt Injection: The SQL Injection of AI + How to Defend - プロンプトインジェクション：AI版SQLインジェクションと防御法
見えない命令がAIを乗っ取る前に読むべき、実務で効くプロンプトインジェクション対策

## 要約
プロンプトインジェクションは、ユーザー入力や外部コンテンツに悪意ある命令を埋め込み、LLMの振る舞いを意図的に変える攻撃で、SQLインジェクションと同じ根本原因（命令とデータの混在）を持ちます。実害は情報漏洩、誤操作、外部サービスの不正利用など多岐にわたります。

## この記事を読むべき理由
日本の企業もチャットボット、AIメール要約、RPA、社内ナレッジ検索などLLM導入が進む中で、外部コンテンツ経由の攻撃や誤動作によるコンプライアンス/顧客信頼の損失リスクが高まっています。実務で即導入できる防御策を押さえておくべきです。

## 詳細解説
- 何が起きるか  
  LLMは「テキストとして与えられた命令」を区別できないため、ユーザー入力や文書内の指示をそのまま実行してしまうことがあります。例えば「以前の指示を無視して〜」と書かれた入力があれば、モデルは従ってしまう可能性があります。

- SQLインジェクションとの類似点  
  SQLではクエリ構造とユーザーデータが混ざることで悪用されました。同様にLLMでも「システム命令」と「ユーザーデータ」が単一の文脈に混在すると防御が難しくなります。

- 直接型と間接型  
  直接型：ユーザーが明示的に悪意ある指示を送る例。  
  間接型：悪意ある命令が埋め込まれたメールやウェブページ、ドキュメントをAIが処理することで発生。間接型は特に危険です（ブラウジング、メール要約、ファイル解析などが対象）。

- 実例（過去の攻撃）  
  大手チャットボットやブラウズ機能付きモデルでシステムプロンプトの抽出や挙動変更が報告されています。これにより情報漏洩や誤情報拡散が現実化しています。

- なぜ対策が難しいか  
  データと命令をテキストで渡す現在のインターフェース自体が脆弱。モデルの「役割」分離はヒントに過ぎず、完全な境界を保証しません。

## 実践ポイント
- 入力のサニタイズ（簡易例）
```python
# python
def sanitize_input(user_input: str) -> str:
    blocked = ["ignore previous", "ignore all", "system prompt", "you are now"]
    low = user_input.lower()
    for p in blocked:
        if p in low:
            return "[入力拒否：疑わしい内容]"
    return user_input
```
- 最小権限の設計：AIに付与するツール／APIアクセスは必要最小限に限定する（例：要約のみなら送信権限は与えない）。
- 高リスク操作は人の承認を必須にする（削除・送信・APIキー表示など）。
```python
# python
def process_action(action):
    if action.risk == "high":
        return request_human_approval(action)
    return execute(action)
```
- 出力フィルタリング：敏感情報やキー語句が返る場合はブロックしてログ出力する。
```python
# python
import re
def filter_output(resp):
    if re.search(r"(api[_\s]?key|password|internal[_\s]?only)", resp, re.I):
        return "その情報は提供できません。"
    return resp
```
- プロンプト構造化：明確なデリミタで「システム命令」と「ユーザーデータ」を分け、ユーザーデータは「信頼できないデータ」として明示する。
- サンドボックス化：AIによるコード実行やツール操作はネットワークやファイルへの書き込みを制限した隔離環境で行う。
- モデル選定：プロンプト耐性を強化しているモデルやベンダーのセキュリティ機能を評価して採用する。
- 監査とアラート：全プロンプト／レスポンスをログ化し、疑わしいシグネチャでアラートを上げる。定期的にプロンプトインジェクションの模擬テストを行う。

日本市場へのワンポイント：社内に蓄積された日本語ドキュメントやメール文化（敬語、定型句）を悪用したステルスな指示埋め込みが想定されるため、日本語表現でのテストとサニタイズルールの整備が必須です。

実装は防御層の組み合わせが鍵です。1つの対策で安心せず、入力・権限・出力・実行環境・監査を同時に固めてください。
