---
layout: post
title: "You can't cancel a JavaScript promise (except sometimes you can) - JavaScriptのPromiseはキャンセルできない（ただし、場合によってはできる）"
date: 2026-04-07T16:30:38.328Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.inngest.com/blog/hanging-promises-for-control-flow"
source_title: "You can&#x27;t cancel a JavaScript promise (except sometimes you can) - Inngest Blog"
source_id: 47675155
excerpt: "Promiseは取消不可だが、未解決Promiseでasyncを中断・再開する実用トリック"
image: "https://www.inngest.com/assets/blog/hanging-promises-for-control-flow/featured-image.jpg"
---

# You can't cancel a JavaScript promise (except sometimes you can) - JavaScriptのPromiseはキャンセルできない（ただし、場合によってはできる）
動くコードでわかる「awaitをそっと止める」トリック — サーバレスのワークフローで使える中断法

## 要約
Promiseに標準のキャンセルはないが、「解決しないPromiseで待機を永続化→ガベージコレクタで掃除される」テクニックを使えば、throwも例外処理も使わずにasync関数の途中で実質的に中断（そして再開）できる。

## この記事を読むべき理由
サーバレスや短時間実行環境で長時間ワークフローを動かす必要がある場面（日本でも増えるイベント駆動・分散ワークフロー）で、ライブラリやランタイム側がユーザーの普通のasync/awaitコードを壊さずに「中断→保存→再開」する方法を理解できる。

## 詳細解説
- 問題点：Promiseに .cancel() は無く、throwで中断するとユーザーのtry/catchに捕まって意図しない挙動を招く。ジェネレータならcaller側が.next()を止めれば安全に中断できるが、yield記法は可読性/並列性で不利。
- トリック：新しいステップを見つけたら、そのawaitで「決して解決しないPromise」を返すことで関数実行を"停止"させる。Nodeは未決のPromiseだけではイベントループを維持しないため、他にアクティブなハンドルが無ければプロセスは終了し、実行スタックごとGCの対象になる。
- マイクロタスク／マクロタスク：既に完了したステップのawaitはマイクロタスクで連続実行される。次の新しいステップ検出のタイミングを安定させるために setTimeout(...,0) のようなマクロタスクで一旦制御を返し、マイクロタスクを枯渇させてから新ステップの有無を確認する。
- メモ化と再実行：ステップごとの結果を永続化（実例ではMapだが実運用はDB）しておき、再実行時は既存結果を即返す。新ステップに到達したらそのコールバックを実行して保存し、次のランでまた中断する。
- GCの挙動：未解決Promise自体はGCの対象になりうる。関数とそこに閉じたPromiseへの参照が切れればFinalizationRegistryで回収が観測できる（テストには --expose-gc が必要なケースあり）。つまり「永遠に残る」わけではない。
- トレードオフ：この手法はユーザコードを書き換えずにランタイム側で制御できるが、長期運用では参照保持のバグに注意。ジェネレータやAbortControllerの代替ではなく補完として考える。

重要コード（抜粋例）:

```javascript
// javascript
async function interrupt() {
  return new Promise(() => { /* 決して解決しない */ });
}

async function execute(fn, stepState) {
  let newStep = null;
  // 実行を開始。ユーザー側は step.run() が新ステップなら永遠に待つ
  fn({
    run: async (id, callback) => {
      if (stepState.has(id)) return stepState.get(id);
      newStep = { id, callback };
      return new Promise(() => { });
    }
  });
  // マクロタスクでマイクロタスク群を枯渇させる
  await new Promise(r => setTimeout(r, 0));
  if (newStep) {
    const result = await newStep.callback();
    stepState.set(newStep.id, result);
    return false; // 未完了（中断した）
  }
  return true; // 完了
}
```

日本市場との関連性：
- AWS Lambda / Azure Functions / Google Cloud Functionsを用いたサーバレス設計は日本のスタートアップや大企業でも主流化しており、短時間の実行制限内で長期ワークフローを実現するニーズが高い。上記トリックはSDKやランタイム実装側で採用でき、ユーザー側の普通のasync/awaitコードを壊さずにワークフローのチェックポイント化が可能。

## 実践ポイント
- ユースケース：外部API呼び出しや人手ステップを含む長時間ワークフローの分割再実行に有効。
- 実装上の注意：
  - ステートは必ず永続化（DB）すること。メモリMapはデモ用。
  - try/catchで中断が飲み込まれる問題を避けられるが、ユーザーの意図する例外処理と衝突しない設計にする。
  - setTimeout(...,0) 等でマイクロ/マクロタスクを理解して正しいタイミングで検出する。
  - GC挙動を検証するには環境依存（Nodeのバージョンやフラグ）を確認する。
- 代替案：ジェネレータを使えば明示的に中断が可能だが、記法と並列処理の扱いでUXコストが高い。状況に応じて使い分ける。

この記事で紹介した手法はランタイム側で透明にワークフロー制御を提供したい場面で強力です。まずは小さなプロトタイプで挙動（イベントループ、GC、例外処理）を確認してください。
