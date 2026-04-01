---
layout: post
title: "Show HN: Git bayesect – Bayesian Git bisection for non-deterministic bugs - 非決定的バグ向けベイズ式Gitバイセクト"
date: 2026-04-01T19:28:03.409Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/hauntsaninja/git_bayesect"
source_title: "GitHub - hauntsaninja/git_bayesect: Bayesian git bisect · GitHub"
source_id: 47557921
excerpt: "ベイズ推論でフレークなテスト原因を即特定、CIコストを激減するgit_bayesectツール"
image: "https://opengraph.githubassets.com/0b4a4ef430149d2197dab8a637108781165e05b533f958da491ecc33b40a0d00/hauntsaninja/git_bayesect"
---

# Show HN: Git bayesect – Bayesian Git bisection for non-deterministic bugs - 非決定的バグ向けベイズ式Gitバイセクト
確率で「ぼんやりした」原因を見抜く──Flakyテストや不安定な障害を速攻で特定する新しい武器

## 要約
git_bayesectは「失敗確率が変わったコミット」をベイズ推論で探索するツール。従来の二分探索では難しいフレーク（非決定的）な不具合を、観測ごとに確率を更新しながら効率的に絞り込めます。

## この記事を読むべき理由
日本のCI現場でも増えている「たまに落ちるテスト」やランダムな障害は、通常のgit bisectでは発見が難しい。本ツールは確率モデルを使うので、テストの失敗確率が徐々に変化したケースや不安定な再現性の問題に強く、CIコストや調査時間を大幅に減らせます。

## 詳細解説
- アプローチ：各コミットに対して「そのコミット以降で失敗率が変わったか」をベイズ確率で表現し、観測（pass/fail）ごとに事後確率を更新します。  
- コミット選択：次にテストすべきコミットは「期待情報量（エントロピー）の最小化」を貪欲に行うことで決定。つまり、最短で不確実性を減らす候補を優先します。  
- 数理的工夫：失敗確率が未知でも扱えるように、Beta分布とBernoulliモデルの共役性（Beta–Bernoulli）を利用して事後計算を効率化しています。  
- 実装と使い方（主なコマンド）：
  - インストール: 
    ```bash
    pip install git_bayesect
    ```
  - 開始: 
    ```bash
    git bayesect start --old $OLD_COMMIT --new main
    ```
  - 観測記録（現在のコミットで失敗観測）:
    ```bash
    git bayesect fail
    ```
    または特定コミットでの成功:
    ```bash
    git bayesect pass --commit $COMMIT
    ```
  - 自動実行（コマンドで観測）:
    ```bash
    git bayesect run "pytest tests/test_flaky.py"
    ```
  - 追加機能：コミット毎に事前分布（prior）を設定したり、ファイル名やコミットメッセージから自動的にpriorを構築できます（例："timeout" が含まれるメッセージに重みを付与）。
- デモ：リポジトリに偽リポジトリ生成スクリプトとflakyスクリプトがあり、実際に挙動を試せます。

## 実践ポイント
- 使いどころ：再現性が低い・頻度が上下するテストやランダム障害の調査に最適。例えば夜間のCIでたまに落ちるテストを早く特定したい場合に有効。  
- CI連携：GitHub ActionsやGitLab CIに組み込み、flaky検出時に自動で`git bayesect run`を呼ぶワークフローを作ると効果的。  
- Priorの活用：過去の知見（特定ファイルやキーワードに関連する変更）をpriorに反映すると収束が速くなる。日本語コミットメッセージでもフィルタロジックに対応可能。  
- 調査手順（短縮版）：
  1. pipでインストール。  
  2. 問題の起きるブランチで`git bayesect start`を実行。  
  3. `git bayesect run`でテストコマンドを回す。  
  4. `git bayesect checkout`で疑わしいコミットを確認・デバッグ。  

元リポジトリ（READMEとデモ）を参照してまずはローカルで試し、CIに組み込むフローを作るのがおすすめです。
