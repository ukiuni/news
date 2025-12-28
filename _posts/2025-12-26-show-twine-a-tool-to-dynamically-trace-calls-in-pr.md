---
layout: post
title: "Show: Twine - A tool to dynamically trace calls in production Elixir systems"
date: 2025-12-26T21:07:34.875Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/ollien/twine"
source_title: "Show: Twine - A tool to dynamically trace calls in production Elixir systems"
source_id: 1601729135
excerpt: "本番稼働中のElixirを安全に“生で覗き”、関数呼び出しを絞って即座に原因特定できるTwineツール紹介"
---

# 本番稼働中のElixirを“生で覗く” — Twineで安全に関数呼び出しをトレースする方法

## 要約
TwineはFerdのrecon_traceをElixir寄りにラップしたツールで、本番BEAMプロセスの呼び出しを安全かつ可読なElixir構文で出力できる。問題箇所の特定を素早く行いたいエンジニアに最適。

## この記事を読むべき理由
本番環境での一時的なデバッグはリスクとコストが伴う。Twineは低オーバーヘッドで呼び出しを捕捉し、Elixirのパターンマッチで狙い撃ちできるため、Phoenix/GenServer周りの難読なバグや性能問題を素早く切り分けられる。日本でもマイクロサービスやリアルタイム系でBEAM採用が増える中、即戦力となる知見。

## 詳細解説
- 背景: recon_traceはBEAM上で安全にトレースする強力なライブラリだが、生の出力やAPIが扱いにくい部分がある。Twineはそれをラップして「Elixirらしい」呼び出し表現と簡潔なAPIを提供する。
- 何ができるか: 指定した関数呼び出しをキャプチャして標準出力にElixir構文でプリントする。回数制限やパターンマッチを使ったフィルタリングが可能。
- 安全性: recon_traceの安全設計を踏襲しており、通常のトレースより低い侵襲性。ただしホットループや高頻度呼び出しを無制限にトレースすると影響が出るため、回数制限や対象プロセスを絞ることを推奨。
- ライセンス: BSD-3-Clause（OSSプロジェクトとして安心して参照可）。

基本的な使い方（ランタイムのリモートシェルで実行）:
```elixir
# mix.exsに追加
defp deps do
  [{:twine, "~> 0.5.0"}]
end
```

実行例 — 関数呼び出しを3回だけ出力:
```elixir
# リモートシェル (iex --remsh ...) 上で
require Twine
Twine.print_calls(MyModule.my_function(_arg1, _arg2), 3)
```

パターンマッチで特定の呼び出しを狙う例（GenServerの:pingを監視）:
```elixir
require Twine
Twine.print_calls(MyModule.handle_call(:ping, _from, _state), :infinity)
```

補足: HexのドキュメントやREADMEに細かなオプション（フォーマット、フィルタ、タイムアウトなど）が記載されている。

## 実践ポイント
- まずはステージングで挙動確認: 本番導入前にステージングで影響と出力量を確認する。
- 絞り込みをかける: 回数（例: 3）やパターンマッチで対象を限定し、ノイズと負荷を減らす。
- リモートシェルから実行: 実行は稼働中ノードに接続したIEx上で行う（iex --remsh / :ssh + :rpc等）。
- ログ連携: Twine出力は標準出力なので必要ならLoggerにパイプして加工・保存する。
- 過度な常時トレースは避ける: ホットパスで無制限トレースを走らせるとパフォーマンス劣化の恐れがある。短時間・限定的に使う。
- 代替手段との併用: Telemetryや分散トレーシングと併用して、トレースで原因箇所を掴む → 計測で再現性を保つ、というワークフローが有効。

