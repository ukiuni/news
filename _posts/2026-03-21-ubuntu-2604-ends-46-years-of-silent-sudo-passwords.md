---
layout: post
title: "Ubuntu 26.04 Ends 46 Years of Silent sudo Passwords - Ubuntu 26.04、46年続いたsudoの「無音パスワード入力」に終止符"
date: 2026-03-21T07:19:34.032Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://pbxscience.com/ubuntu-26-04-ends-46-years-of-silent-sudo-passwords/"
source_title: "Ubuntu 26.04 Ends 46 Years of Silent sudo Passwords"
source_id: 47464134
excerpt: "Ubuntu 26.04でsudoのパスワードが46年ぶりに＊表示へ、管理者は設定確認を"
image: "https://pbxscience.com/wp-content/uploads/2025/12/cc251204-ubuntu.webp"
---

# Ubuntu 26.04 Ends 46 Years of Silent sudo Passwords - Ubuntu 26.04、46年続いたsudoの「無音パスワード入力」に終止符
魅惑の「＊表示」化：ターミナルの古い慣習がついに変わる理由と、あなたが今すぐ確認すべきこと

## 要約
Ubuntu 26.04（LTS）から、sudoのパスワード入力が従来の「画面に何も表示されない」仕様ではなく、1文字ごとにアスタリスク(*)を表示するようになります。これはsudoのRust実装（sudo-rs）での既定変更が原因で、賛否両論を呼んでいます。

## この記事を読むべき理由
日本の開発・運用現場でもUbuntuは広く使われており、ターミナル操作やSSH接続が日常的です。UIの小さな変更が混乱や運用ポリシーに影響するため、管理者・開発者は仕様変更と対応策を把握しておく必要があります。

## 詳細解説
- 何が変わるか：Ubuntu 26.04（Resolute Raccoon）ではsudoの既定実装がsudo-rs（Rustで書き直されたsudo）を通じて、pwfeedbackが有効になり、パスワード入力時にアスタリスクが表示されます。従来のC実装（いわゆるlegacy sudo／sudo-ws）は影響を受けません。
- 背景：sudoは1980年代の端末文化で「入力が見えない＝長さが隠れる」ことを重視してきました。一方で近年はGUIやログイン画面で入力が可視化される場面も多く、UX観点からフィードバックを出す流れが強まっています。sudo-rs導入とRustベースのコアユーティリティ採用は、メモリ安全性とモダン化の一環です。
- セキュリティ議論：反対派は「長さが露出すると肩越し攻撃に弱くなる」と主張。一方で賛成派は「実際に画面を見られる距離なら他の観察で漏れる」「多くのユーザーはsudoとログインで同じパスワードを使っており、一貫性の方が重要」と応じています。結論として、セキュリティ差は実用上ごく小さいと評価されています。
- タイムライン（要点）：sudoは1980年に登場 → Ubuntuは2025年10月からsudo-rsを導入 → 2026年初めにpwfeedback既定化のパッチが取り込まれ → 2026年4月23日に26.04 LTS公開予定。

## 実践ポイント
- 元に戻す方法（すぐできる）
  ```bash
  sudo visudo
  # sudoers に以下を追加
  Defaults !pwfeedback
  ```
  追加後、新しいターミナルセッションから即反映。visudoで編集すること。
- 管理者向けチェックリスト
  - 社内運用ドキュメントに変更を追記（スクリーン表示ポリシー、教育資料）
  - SSH接続環境での挙動確認（リモートでもアスタリスクが表示されます）
  - 大規模展開前にテスト環境で既定のsudo実装（sudo-rs／sudo-ws）を確認
  - パスワード運用の指針（使い回し禁止、パスワード管理ツール推奨）を周知
- 日本の現場への示唆：オフィスでの共有端末や説明会で「空白の入力が凍ったように見える」問題は初心者にとって障壁になりがち。UX改善を歓迎する現場ではデフォルト変更がプラスに働く可能性が高い。

以上。必要なら社内向けの短い告知文テンプレートや、sudo実装の判定コマンドを用意しますか？
