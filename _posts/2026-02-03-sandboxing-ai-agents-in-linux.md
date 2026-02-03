---
layout: post
title: "Sandboxing AI Agents in Linux - LinuxでAIエージェントをサンドボックス化"
date: 2026-02-03T21:55:11.066Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://blog.senko.net/sandboxing-ai-agents-in-linux"
source_title: "Sandboxing AI agents in Linux &mdash; Senko Rašić"
source_id: 46874139
excerpt: "bubblewrapでローカルAIを最小権限で安全隔離する実践ガイド"
image: "https://cdn.writeas.net/img/w-sq-light.png"
---

# Sandboxing AI Agents in Linux - LinuxでAIエージェントをサンドボックス化
ローカルを壊さずAIエージェントを使い倒す──軽量なbubblewrapで手早く安全性を高める方法

## 要約
ローカル開発環境でAIエージェント（例：Claude Code）を動かす際に、bubblewrapを使って最小限の権限でプロセスを隔離する手法を紹介する。軽量で実用的、かつ開発フローを壊さない設定例と調整方法を示す。

## この記事を読むべき理由
AIエージェントは便利だが「ファイル読み書き」「外部アクセス」を許すとリスクがある。日本の開発現場でも、社内データやAPIキーを守りつつ生産性を落とさない実践的な隔離策が求められているため、手元で試せる具体策はすぐ役立つ。

## 詳細解説
- なぜbubblewrapか：Dockerより軽く、Linuxのユーザーネームスペースやcgroups、マウント分離を使ってプロセスをジャイルに「牢」にできる。フルハードニングではないが日常的な誤用やうっかり漏洩の被害範囲を小さくできる。
- 目標（著者の要件）：ローカル開発環境を再現／外部情報への不要アクセスを遮断／現在プロジェクトへの書き込みのみ許可／ネットワークは必要に応じ許可／IDEから同じファイルを扱えること
- 主要オプションの意味：
  - --tmpfs /tmp：一時領域をクリーンにする
  - --dev /dev, --proc /proc：プロセス・デバイスを隔離されたビューで提供
  - --unshare-uts / --hostname：ホスト名などの識別を分離
  - --ro-bind / --bind：ホスト上のファイルやディレクトリを読み取り専用／読み書きで露出
  - --file：ファイル内容をサンドボックス内に注入して外側の書き換えを防ぐ
- 実用的トレードオフ：カーネルのゼロデイ等には耐えられない点は許容し、プロジェクトごとのAPIキー管理やバックアップ（git/GitHub）で被害範囲を限定する戦術が現実的。
- 問題発見法：straceで必要なファイルアクセスを追跡し、足りないバインドだけを追加して最小構成を目指す。

例：straceで必要ファイルを確認するコマンドと、簡易的なbwrap実行例
```bash
# straceでagentのファイルアクセスを記録
strace -e trace=open,openat,stat,statx,access -o /tmp/strace.log your-agent-command

# 最小のbwrap例（実運用は適宜追加）
/usr/bin/bwrap \
  --tmpfs /tmp \
  --dev /dev \
  --proc /proc \
  --unshare-uts --hostname bubble \
  --ro-bind /usr/bin /usr/bin \
  --ro-bind /lib /lib \
  --bind "$PWD" "$PWD" \
  --file /path/to/creds.json /home/user/.agent_creds.json \
  your-agent --some-flag
```

## 実践ポイント
- まずはbashをentryにして手動でagentを起動、straceで壊れる箇所を確認して順次 bwrap を整備する。
- プロジェクト専用のAPIキーを発行し、万が一の流出時に影響範囲を限定する。
- IDEと同じパスでプロジェクトを --bind しておくと開発効率が下がらない。
- 完全なセキュリティが必要ならリモートサンドボックス（クラウド／専用サービス）を検討する。
- 社内や顧客データを扱う場合は、ホスト側のポリシー（ログ保管、監査）と運用ルールを合わせて運用する。

（参考）まずは小さく始めて、straceログを見ながら必要最小限のバインドだけ追加する運用が実用的で効果的。
