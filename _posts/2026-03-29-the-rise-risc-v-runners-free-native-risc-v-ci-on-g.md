---
layout: post
title: "The RISE RISC-V Runners: free, native RISC-V CI on GitHub - RISE RISC-V ランナー：GitHub上で無料・ネイティブなRISC‑V CI を提供"
date: 2026-03-29T17:42:01.132Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://riseproject.dev/2026/03/24/announcing-the-rise-risc-v-runners-free-native-risc-v-ci-on-github/"
source_title: "Announcing the RISE RISC-V Runners: free, native RISC-V CI on GitHub &#8211; Rise: RISC-V Software Ecosystem"
source_id: 47531576
excerpt: "実機RISC‑V上で無料で動くGitHub Actionsランナー、数分で実機CI導入可能"
---

# The RISE RISC-V Runners: free, native RISC-V CI on GitHub - RISE RISC-V ランナー：GitHub上で無料・ネイティブなRISC‑V CI を提供
RISC‑V対応を手軽に試せる――実機で動く無料のGitHub Actionsランナーが登場し、開発者の“最後の一歩”を後押しします。

## 要約
RISEが公開した「RISC‑V Runners」は、オープンソース向けに実機RISC‑Vボード上でジョブを実行する無料のGitHub Actionsランナー。GitHub Appを入れ、workflowのruns-onを1行変えるだけで実機CIが動きます。

## この記事を読むべき理由
RISC‑V普及の障壁は「ハードがないとテストできない」こと。日本の組込み・OS・コンパイラ開発者やライブラリ保守者にとって、実機でのCIを低コストで導入できるのは即戦力です。エミュレータでは見つけにくい実機固有の不具合を早期発見できます。

## 詳細解説
- 導入は数分：組織用／個人用のGitHub Appをインストールし、workflowのruns-onに ubuntu-24.04-riscv を指定するだけ。例：
```yaml
jobs:
  build:
    runs-on: ubuntu-24.04-riscv
    steps:
      - uses: actions/checkout@v4
      - run: uname -m # riscv64 が出る
```
- 実行の流れ：ワークフロー起動 → webhookでバックエンドへ → Kubernetes上に専用RISC‑Vノード用のポッドをプロビジョニング → エフェメラルなGitHub Actionsランナーとしてジョブ実行 → 実行後にクリーンアップ。
- 実機と環境：ScalewayのEM‑RV1（ベアメタルRISC‑V）を利用。各ノードは1ジョブのみで安定した性能を確保。Docker‑in‑Docker対応で docker build/run や Buildx 等も使える。
- オープンソースで公開：riscv-runner-app, riscv-runner-device-plugin, riscv-runner-images, riscv-runner-sample のリポジトリがあり、イメージは毎日再構築。ホワイトリスト不要で公開プロジェクトなら誰でも利用可。
- 期待効果：クロスコンパイル環境や自前ボード調達の負担を削減し、ライブラリ／カーネル／ツールチェーンのRISC‑V互換性テストを自動化できる。

## 実践ポイント
- まずGitHub App（Organization / Personal）をインストールして runs-on: ubuntu-24.04-riscv を追加する。
- 最初の確認は workflow内で uname -m を実行して riscv64 が返るかをチェック。
- Dockerを使うビルドはそのまま動くが、イメージやパッケージ不足に注意。必要なら riscv-runner-images リポジトリへPRを送る。
- 既存のworkflowにmatrixで riscv を追加して互換性テストを拡張する（並列性はノード数に依存）。
- ドキュメントとサンプルは riseproject-dev.github.io/riscv-runner を参照し、問題はリポジトリにIssueを立てて貢献する。

導入は簡単で効果が大きいので、まず1プロジェクトに組み込んで「本当に動くか」を確かめてみてください。
