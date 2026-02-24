---
layout: post
title: "Reducing the size of Go binaries by up to 77% - Goバイナリを最大77%削減する方法"
date: 2026-02-24T14:23:22.410Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.datadoghq.com/blog/engineering/agent-go-binaries/"
source_title: "How we reduced the size of our Agent Go binaries by up to 77% | Datadog"
source_id: 857597530
excerpt: "Datadogが半年でGoバイナリを最大77%（1.22GiB→元サイズ）削減した実践手法公開"
image: "https://imgix.datadoghq.com/img/blog/engineering/agent-go-binaries/agent-go-binaries-hero.png?fit=crop&w=1200&h=630"
---

# Reducing the size of Go binaries by up to 77% - Goバイナリを最大77%削減する方法
「1つの変更で36MiB節約!? Datadogが半年でGoバイナリを元に近いサイズに戻した秘密」

## 要約
Datadogは半年間でAgentのGoバイナリを最大77%削減（1.22GiB→ほぼ5年前のサイズへ）し、依存関係の監査、ターゲットリファクタ、リンカ最適化の再有効化で実現した。

## この記事を読むべき理由
バイナリ肥大はサーバレス、IoT、コンテナ環境で直接コストと運用負担になる。日本のスタートアップやエンタープライズでも同様の課題があり、手法は即応用できるから。

## 詳細解説
- 問題の全体像：Datadog Agentは多環境対応のため多数のビルド（OS/アーキ/配布先）と機能フラグを持ち、長年の機能追加で依存が膨張。結果、v7.16.0で428MiBがv7.60.0で1.22GiBに増加した。
- 解決アプローチ（3本柱）
  1. 依存関係の系統的監査：どのパッケージがどのバイナリに入っているかを調べ、不要／重複する依存を削除。
  2. ターゲットリファクタ：一部のAPIや初期化コードが数百のパッケージを引き込んでいたため、参照を切るか局所化して取り除いた（「ある関数の削除で36MiB」級の改善）。
  3. リンカ最適化の再有効化：Goのデッドコード除去（method dead code elimination）を妨げていた設計（例：plugin利用や動的参照）を改め、リンカの最適化を再び効かせた。
- 技術上の気づき：Goコンパイラ／リンカの挙動に微妙な盲点があり、それらを解消する変更やツール貢献を行ってコミュニティにも還元した。
- ビルド戦略：ビルドタグとDIで機能を切り分けつつ、各ターゲットに必要な依存だけを含める方針に徹した。

## 実践ポイント
- まず「どのパッケージがバイナリに入っているか」を把握する（go list -deps / go tool nm / pprof 等で調査）。
- ビルドごとに必要な依存だけを含める（build tags／条件コンパイルで機能を分離）。
- 大きな外部SDKや汎用ライブラリは必要最小限に置き換えるか遅延ロードする。
- pluginや動的解決はデッドコード除去を阻害する場合があるため設計を見直す。
- リンカオプション（例: -ldflags="-s -w"）やGoのアップデートで得られる最適化を定期的に確認する。
- 変更は小さな単位で測定→反映。1つの関数や参照を切るだけで大きく改善することがある。

短期間で大きな削減を出した実例は、日本の現場でもバイナリ最適化の優先度を上げる価値があることを示している。
