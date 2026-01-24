---
layout: post
title: "Considering Strictly Monotonic Time - 厳密単調時刻の考察"
date: 2026-01-24T09:31:10.816Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://matklad.github.io/2026/01/23/strictly-monotonic-time.html"
source_title: "Considering Strictly Monotonic Time"
source_id: 751586767
excerpt: "同値時刻を排除する+1nsガードでログ突合とバグ検出力を劇的に向上"
---

# Considering Strictly Monotonic Time - 厳密単調時刻の考察
時刻が「単に変わる」だけでなく「必ず増える」ことを保証すると、バグ検出と因果関係の明確化が格段に楽になる

## 要約
OSの単調時計をそのまま信用せず、プロセス内で「guard」を使って補正する実装があるが、そこを一歩進めて「厳密に増加する（strictly monotonic）」ようにすることで同値の時刻が持つ曖昧さを排除できる、という指摘。

## この記事を読むべき理由
ログの突合、イベントの因果判定、タイムスタンプ比較が日常的な日本の開発現場（分散システム、組み込み、金融系など）では、同一数値の時刻が発生するとデバッグが難しくなる。厳密単調化は小さな実装変更で問題検出性を上げられるため実務的価値が高い。

## 詳細解説
よくあるパターン（疑似コード）：
```zig
fn now(clock: *Clock) Instant {
    const t_raw = os_time_monotonic();
    const t = @max(t_raw, clock.guard);
    assert(t >= clock.guard);
    assert(t >= t_raw);
    clock.guard = t;
    return t;
}
```
これはOSの単調時計が「基本は増える」という前提に立ちつつ、OSが破綻するケースに備えてプロセス内で下限を保つもの。しかし、この実装は等号を許すため、異なる箇所から同じ数値の時刻が返る可能性が残る。

提案は単純：guard に 1ns を足して clamp する。
```zig
const t = @max(t_raw, clock.guard + 1ns);
assert(t > clock.guard);
```
こうすると同値のタイムスタンプが意味するものは「完全に同一の now() 呼び出しに由来するものだけ」になる。結果として比較アサーションは `past <= present` から `past < present` に厳しくでき、同値を使ったバグ（「前の値を再利用してしまう」など）を捕まえやすくなる。

注意点：
- これはプロセス内ガードであり、マルチプロセス／マシン間では別手段（論理クロックや同期プロトコル）が必要。
- 時刻値の「解像度（値の粒度）」が十分高くないと +1 が未来に飛ばしてしまう可能性がある。ナノ秒精度なら現実的には問題になりにくい。
- マルチスレッド環境では guard の更新に原子操作やロックが必要。

## 実践ポイント
- まずは既存の now() 実装を見直し、guard を使っているなら +1 を適用してみる。
- マルチスレッドなら atomic compare-and-swap で guard を更新する（ABA に注意）。
- 単体テストで連続呼び出しや短時間の並列呼び出しを検証し、等値が発生しないことを確認する。
- 分散システムでは単独の厳密単調化だけでなく論理クロック（Lamport/HLC）や同期手段と組み合わせる。
