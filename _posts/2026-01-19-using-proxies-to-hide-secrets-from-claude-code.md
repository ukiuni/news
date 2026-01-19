---
layout: post
title: "Using proxies to hide secrets from Claude Code - プロキシでClaude Codeから秘密情報を隠す方法"
date: 2026-01-19T02:28:49.433Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.joinformal.com/blog/using-proxies-to-hide-secrets-from-claude-code/"
source_title: "Using Proxies to Hide Secrets from Claude Code - Formal"
source_id: 46605155
excerpt: "mitmproxyでダミー鍵を渡し真鍵を注入してClaude CodeのAPIキー漏洩を防ぐ"
image: "https://formal1.wpenginepowered.com/wp-content/uploads/2026/01/Screenshot-2026-01-12-at-6.27.31-PM.png"
---

# Using proxies to hide secrets from Claude Code - プロキシでClaude Codeから秘密情報を隠す方法
Claude CodeにAPIキーを「見せない」——mitmproxyとプロキシで実現する現実的なサンドボックス運用術

## 要約
Claude Codeのサンドボックスはネットワーク経由で秘密を抜かれるリスクがある。mitmproxyなどのHTTPプロキシを挟んでダミー鍵を渡し、実際の鍵はプロキシ側で注入することで漏洩リスクを低減できる。

## この記事を読むべき理由
ローカル開発やdevcontainerを使う現場では、環境変数やローカルファイルに置いたAPIキーが意図せずエージェント（Claude Codeなど）に渡る危険がある。日本の開発現場でもリモートワークやクラウド連携が進む中、組織的に鍵を扱う安全対策は必須のテーマであり、本稿は即応用できる実践策を示す。

## 詳細解説
- 「致命の三要素（lethal trifecta）」
  - サンドボックスが何に晒されるか／外部とどう通信するか／どんな秘密を渡しているか、の3点を常に評価する必要がある。Claude Codeは親プロセスの環境変数や実行ディレクトリのファイルを参照できるため、.envやシークレット変数がそのまま流れる危険がある。

- devcontainerの“IPベース”ファイアウォールの限界
  - Anthropic公式のdevcontainerはinit-firewall.shでdig→iptablesにより特定IPへの通信を許可する。だがIP層の制御はSNIやHostヘッダを用いた振り分け（Domain Fronting）や、同一IP上の別サービスを通したリクエスト拒否には脆弱。さらにSSH(22)が開いていると任意の外部ホストへ接続される恐れがある。

- アプリケーション層での制御が必要
  - HTTP/HTTPSのリクエスト内容（パスやヘッダ）レベルでの制御ができれば、より細かく許可/拒否やログ取得ができる。これがプロキシ導入の主な狙い。

- プロキシを使った「鍵の隠蔽」手法
  - Claude Codeは2種類のプロキシ設定を持つ：プロセス全体用のHTTP_PROXYと、サンドボックス内のbashコマンド向けのhttpProxyPort。両者は独立するため両方設定する必要がある。
  - mitmproxyを立て、ClaudeにダミーのANTHROPIC_API_KEYを渡す。一方でmitmproxyのアドオンでapi.anthropic.comへのリクエストを捕まえ、本物のAPIキーをX-API-Key等のヘッダに書き換えて上流に転送する。これによりモデルやサンドボックスは本物の鍵を直接見ない。
  - TLSインターセプト時はmitmproxyのCAをNODE_EXTRA_CA_CERTSなどで信頼させる操作が必要（Nodeプロセス向け）。

- 組織的な最小権限と監査
  - Formalのようなコネクタを使い、人間のユーザー権限とClaude Codeのマシン権限を分離。プロキシ/コネクタ側でパスやメソッド単位のアクセス制御を行い、リクエストを記録すれば誰が何を呼んだかの可視化が可能になる。

- 実運用上の注意点
  - OAuthログインのフローなどで一時的に本物の鍵が必要になるケースがあり、その扱いには注意。devcontainer内の.envが作業ディレクトリに残っていると意味がない。鍵のローテーションや限定的な開発用鍵の運用が重要。

## 実践ポイント
- 簡単な初動
  - Claude Codeを動かす環境では本物のAPIキーを直接ENVに置かない。ダミーキーを渡し、必ずプロキシ経由で本物を注入する運用を作る。
  - .envファイルは. gitignore/.dockerignoreで管理するだけでなく、claudeを実行するディレクトリに置かない。

- mitmproxyでの実装方針
  - mitmproxyを起動し、ダミーキー→実鍵注入のアドオンを書いて運用する。
  - TLSインターセプト用にmitmproxyのCAをCIや開発マシンに配布（NODE_EXTRA_CA_CERTS等の設定を忘れずに）。

- きめ細かい制御と監査
  - プロキシ／コネクタでパス単位（例：/v1/messages）のホワイトリストやログ出力を行う。必要ならヘッダ書き換えやホスト転送（reroute_hosts.py）で互換性を保つ。
  - 開発者権限とAPI鍵の権限を分離し、可能なら鍵はコネクタ側で短時間で発行・消費する仕組みにする。

- テストと検証
  - 想定されるエクスフィルトレーション（SSH接続、npmパッケージ作成、Gist作成など）を模した検証を行い、防御が効いていることを確認する。

日本のプロダクト開発でも、ローカルで動くAIエージェントに対する秘密管理は急務。プロキシを使った「鍵を見せない」設計は、実装コストが比較的低く、即効性のある有効策なので、まずは小さなプロジェクトから導入して運用ルールを固めることを推奨する。
