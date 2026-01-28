---
layout: post
title: "A \"Pure Go\" Linux environment, ported by Claude, inspired by Fabrice Bellard - Claudeが移植した「純粋Go」Linux環境（Fabrice Bellardに触発）"
date: 2026-01-28T05:58:48.671Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.jtolio.com/2026/01/a-pure-go-linux-environment-written-by-claude-directed-by-fabrice-bellard/"
source_title: "A \"Pure Go\" Linux environment, written by Claude"
source_id: 1669106810
excerpt: "Claudeが純粋Goで移植、go runで起動するRISC‑V Linuxの成功と地獄"
---

# A "Pure Go" Linux environment, ported by Claude, inspired by Fabrice Bellard - Claudeが移植した「純粋Go」Linux環境（Fabrice Bellardに触発）

一行でroot付きのLinuxが立ち上がる――純粋Goで再現したTinyEMU移植の舞台裏

## 要約
Claude（AI）がFabrice BellardのTinyEMU（RISC-V全システムエミュレータ）をCから「純粋Go」へ移植し、`go run`で動く完全なLinux環境を実現した試みと、その成功・苦労（特に最後の20%とネットワーク周りの地獄）を報告する。

## この記事を読むべき理由
Go環境だけでどこでも動くルート権限付きのLinuxイメージが手軽に試せる点は、開発・検証・教育に即応用可能。さらに、LLM（Claude）を使った大規模なコード移植の実務的な落とし穴が学べるため、日本の開発現場や組込み／RISC-V興味層に有益。

## 詳細解説
- 何ができるか：Goが入った環境（macOS/Windows/Linux）で次を実行すると、ローカル上で完全なRISC-V Linuxが起動する（rootアクセス、カーネル6.6.0、ホストFSのマウントや一部ネットワークが可能）。
```bash
go run github.com/jtolio/tinyemu-go/temubox/example@2c8151233c2d
```
- 仕組み：元はFabrice BellardのTinyEMU（C）。ClaudeはCPUエミュレータ、VirtIOデバイス（P9でホスト/ゲストFSマウント含む）、SLIRP系のネットワーク部分をGoへ移植。KVMやSDLの部分は除外。
- 技術的難所：
  - 「最後の20%」問題：Linuxが起動してもinitrdマウント失敗など微妙な挙動で止まる箇所が多く、Cの挙動を厳密に再現しないとブートしない。
  - AI運用の課題：マルチセッションでのコンテキスト維持、エージェントが勝手に「改善」実装を入れる問題、テスト不足での迷走。
  - ネットワーク移植の複雑さ：SLIRP由来の非ブロッキング実装をGoで忠実に再現するのが特に困難で、完全なTCPスタック動作までは長時間の苦闘を要した。
- 開発プロセス：ctagsで関数単位に区切り、チケット化して順に移植。各コミットにテスト導入・コードカバレッジ要件を課すことで安定性を向上させた。
- ツール評価：Beads（チケット管理）が遅く、代替ツール（例：Ticket）が望ましいとの指摘あり。

## 実践ポイント
- まず試す：Goがあれば上記の`go run`コマンドでローカルLinuxを起動して挙動を確認（終了はゲスト内で `halt`）。
- セキュリティ注意：ゲストはrootだがホストとは分離。とはいえ実験用途でのみ使用し、公開環境でのサービス運用は避ける。
- LLMでの移植に挑む現場向け簡易運用ルール：
  - 元実装に忠実にする方針を明文化する（「Cの挙動を優先」等）。
  - 小さなチケット単位で作業させ、各チケットにテストを必須化する（目標カバレッジを設定）。
  - マルチセッションのコンテキスト崩壊に備え、都度同じ参照ドキュメントを渡す。
  - 重いI/Oやデーモン系ツール（Beads等）は事前評価を行う。
- 日本市場向け応用例：RISC-V組込み検証環境の手早い構築、教育用の仮想実験室、Go中心のツールチェーンでの迅速プロトタイピング。

短く結論を述べると、純粋Goで動くRISC-V Linuxは実用的で衝撃的だが、LLMを伴う大規模移植は「最初の80%は早いが残り20%が地獄」になる可能性が高く、厳密なテストと運用ルールが必須。
