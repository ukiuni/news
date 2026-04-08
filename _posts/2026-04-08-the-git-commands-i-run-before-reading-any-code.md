---
layout: post
title: "The Git Commands I Run Before Reading Any Code - コードを読む前に実行するGitコマンド"
date: 2026-04-08T10:17:15.545Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://piechowski.io/post/git-commands-before-reading-code/"
source_title: "The Git Commands I Run Before Reading Any Code"
source_id: 47687273
excerpt: "5つのGitコマンドで数分で修正集中やバグ多発箇所と担当者を特定"
image: "https://piechowski.io/post/git-commands-before-reading-code/cover_hu3f66e25b7571f7e32d40f355f31a2ca9_56928_1200x630_resize_box_2.png"
---

# The Git Commands I Run Before Reading Any Code - コードを読む前に実行するGitコマンド
読む前にわかる！数分でプロジェクトの“痛みどころ”を見抜くGitコマンド5選

## 要約
リポジトリを開く前に数分で回す5つのgitコマンドで、修正が集中するファイル、バスファクター、バグ多発箇所、開発速度や頻発する緊急対応を把握できる。

## この記事を読むべき理由
コードをいきなり読むと時間を浪費しがち。特に日本の企業ではレガシーや担当者偏りが多く、最短で「どこを最初に読むべきか」を把握するのが現場効率化につながる。

## 詳細解説
1) 何が最も変わっているか（変更頻度＝churn）  
bash
git log --format=format: --name-only --since="1 year ago" | sort | uniq -c | sort -nr | head -20
- 過去1年で最も変更されたファイル上位20を表示。高頻度＝必ず悪いわけではないが、修正が積み重なっているファイルは「触ると爆発する」可能性が高い。トップ5は後述のバグ箇所と照合する。

2) 誰が作ったか（貢献者分布＝bus factor）  
bash
git shortlog -sn --no-merges
- コミット数で貢献者をランク付け。1人が過半数ならバスファクター危険。最近の活動（例: --since="6 months ago"）と突き合わせて離職リスクを評価する。注意：squash-merge運用だと出力が乖離する。

3) バグはどこに集まるか（バグホットスポット）  
bash
git log -i -E --grep="fix|bug|broken" --name-only --format='' | sort | uniq -c | sort -nr | head -20
- コミットメッセージ中のキーワードでバグ修正の多いファイルを抽出。変更頻度と重なるファイルは最重要リスク。

4) プロジェクトは加速しているか停滞しているか（コミット推移）  
bash
git log --format='%ad' --date=format:'%Y-%m' | sort | uniq -c
- 月別コミット数を出し、安定なリズム・急落（人が抜けた可能性）・スパイク→沈黙（バッチリリース運用）などを読み取る。チームの勢いやリソース変化の手がかりに。

5) どれくらい“火消し”が発生しているか（revert/hotfix頻度）  
bash
git log --oneline --since="1 year ago" | grep -iE 'revert|hotfix|emergency|rollback'
- リバートやホットフィックスの頻度が高いと、デプロイやテストの信頼性に問題がある可能性。

## 実践ポイント
- まずクローンして上の5コマンドを数分で実行する。  
- churn上位5とバグホットスポットを突き合わせ、優先的に読解・改善対象にする。  
- shortlogの最近6ヶ月版でアクティブな維持者が誰か確認。バスファクターが高い場合はドキュメント整備やナレッジ移転を提案。  
- squash-merge運用や曖昧なコミットメッセージの影響を考慮し、結果は必ずチームに確認する。  
- --sinceの期間はプロダクト事情に合わせて（短期で頻繁リリースなら3〜6ヶ月、長期メンテなら1年）。  
- 見つけた「痛いファイル」はコードレビューで最初に覗くべき場所としてチェックリストに入れる。

この5コマンドで「どこを読むか」が決まり、初日の無駄を大幅に減らせる。
