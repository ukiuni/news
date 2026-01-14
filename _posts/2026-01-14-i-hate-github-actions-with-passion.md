---
layout: post
title: "I Hate GitHub Actions with Passion - GitHub Actionsが情熱的に大嫌いだ"
date: 2026-01-14T13:09:41.608Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://xlii.space/eng/i-hate-github-actions-with-passion/"
source_title: "I Hate Github Actions with Passion"
source_id: 46614558
excerpt: "GitHub ActionsのマトリクスでCIが失敗する原因と即効の回避策を実例付きで解説"
---

# I Hate GitHub Actions with Passion - GitHub Actionsが情熱的に大嫌いだ
GitHub Actionsに殺意すら覚えた日 — CIループ地獄から学ぶ、実務で使える回避テクニック

## 要約
作者はGitHub Actionsのランナー分離やマトリクス実行でハマり、ローカルで動くツールがCIでは動かないことで大量の無駄時間を使った。最終的に「Actionsにビルドロジックを任せない」方針にして問題を解決した。

## この記事を読むべき理由
日本でもGitHub Actionsは標準CIになりつつあり、Apple SiliconやLinux ARM（Graviton）など複数アーキテクチャ対応の必要性が増えています。本件は「なぜ同じコマンドがCIで失敗するのか」「どう防ぐか」を実践的に教えてくれます。

## 詳細解説
- 問題の核心：リポジトリのビルド時に build.rs 内で CUE バイナリを呼び出していた。CIは4つのマトリクス環境（Linux ARM / macOS ARM / Linux x86_64 / macOS x86_64）を回しており、CUEをインストールしたのはx86_64やmacOS ARMのホストだけ。Linux ARMランナーでは適切なバイナリが存在せず「コマンドが見つからない」エラーが発生した。
- ランナーの分離：GitHub Actionsのマトリクスは各実行環境が隔離されており、単に「一度インストールすれば全ランナーで使える」という期待は通用しない。さらに、アーキテクチャが違うとバイナリの置き方や実行可否で落ちる。
- 開発→CIのフィードバックループのコスト：小さなCI修正→push→待つ→失敗→修正…が2–3分単位で回り、合計で時間と気力を消耗する。本件では作者が数十回繰り返したとある。
- 解決策（作者の判断）：build.rsでの自動生成を止め、生成済みファイルをリポジトリにコミット、生成処理はMakefileに移してCI（およびローカル）から明示的に呼ぶ形に変更した。結果、CIの依存が減りデバッグコストが下がった。
- 折衷案：GitHub Actions自体はmacOS実機ビルドなど唯一無二の利点もあるため完全否定はせず、「Actionsに全てのロジックを預けない」「実行環境毎に正しいバイナリを確実に入れる」方針が合理的。

## 実践ポイント
- ビルド時の自動生成をCI任せにしない
  - 生成物は可能ならリポジトリにコミット、あるいはMakefile等の明示的なスクリプトで管理する。
- ランナーごとに正しいバイナリを入れる
  - アーキテクチャ検出して対応バイナリを落とす。例（シェルでの一例）:

```bash
# bash
arch=$(uname -m)
case "$arch" in
  x86_64) url="https://example.com/cue-x86_64" ;;
  aarch64) url="https://example.com/cue-aarch64" ;;
  *) echo "unsupported arch: $arch"; exit 1 ;;
esac
curl -L "$url" -o /usr/local/bin/cue
chmod +x /usr/local/bin/cue
```

- CIワークフローでの条件分岐例（イメージ）:

```yaml
# yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Install CUE for this runner
        run: |
          arch=$(uname -m)
          if [ "$arch" = "x86_64" ]; then
            # x86_64向けインストール
          else
            # aarch64向けインストール
          fi
```

- ローカルで早く回す工夫
  - ワークフローをローカルで検証するツール（例: act）や、自分用ランナーを立てる。これで「push→待ち」のループを減らせる。
- 小さな実験用ワークフロー
  - 本番履歴を汚さない「scratch」的なブランチやDraft PR、workflow_dispatchで手動トリガーするワークフローを用意して素早く試す。
- マトリクスは必要最小限に
  - 実機検証が不要なケースはマトリクス数を絞る。まずはx86_64で通してからARMを追加するなど段階的に。

まとめ：GitHub Actions自体を否定する必要はないが、「どこにロジックを置くか（Actionsに丸投げしない）」が重要。複数アーキテクチャに対応するならランナー依存を明示的に扱い、ローカル検証で無駄な往復を減らすと現場のストレスが大幅に下がる。
