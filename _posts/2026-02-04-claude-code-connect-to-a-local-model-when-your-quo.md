---
layout: post
title: "Claude Code: connect to a local model when your quota runs out - Claude Code：クォータ切れでもローカルモデルに接続する"
date: 2026-02-04T21:14:39.814Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://boxc.net/blog/2026/claude-code-connecting-to-local-models-when-your-quota-runs-out/"
source_title: "Claude Code: connect to a local model when your quota runs out - Tim Plaisted"
source_id: 46845845
excerpt: "クォータ切れでもLM Studioやllama.cppでローカルLLM（GLM-4.7等）に切替え開発を継続"
image: "https://boxc.net/blog/wp-content/uploads/2026/02/claude_code_limit_new_option_header2.png"
---

# Claude Code: connect to a local model when your quota runs out - Claude Code：クォータ切れでもローカルモデルに接続する
クォータ切れで作業が止まらない！Claude CodeをローカルLLMに切り替えて続きを書く簡単ワザ

## 要約
Anthropicのクォータに達したとき、Claude CodeをLM Studioやllama.cpp上のローカルOSSモデル（例：GLM-4.7-Flash、Qwen3-Coder-Next）に切り替えれば作業を継続できる。セットアップは比較的簡単だが、速度や生成品質は落ちる点に注意。

## この記事を読むべき理由
国内の個人開発者やスタートアップはAPIコストやクォータ制限で作業が止まりやすい。ローカルOSSモデルを使う運用を知っておくと、開発の中断を避けられ、データのローカル運用やコスト最適化にもつながる。

## 詳細解説
- クォータ確認
  - Claude Code内で /usage を打つと現在の利用量と残りが分かる。まずここでボトルネックを確認する。

- 手段1：LM Studio経由（初心者向け）
  - LM Studio（v0.4.1以降）はGUIでOSSモデルを探して動かせ、Claude Code（CC）への接続をサポート。
  - 基本手順（端末で）:
```bash
# サーバー起動（例ポート1234）
lms server start --port 1234

# 環境変数をClaude Codeへ向ける
export ANTHROPIC_BASE_URL=http://localhost:1234
export ANTHROPIC_AUTH_TOKEN=lmstudio

# Claude Codeをローカルモデルに向けて起動
claude --model openai/gpt-oss-20b
```
  - LM Studioは25Kトークン以上のコンテキストを推奨するモデルがある点に留意。

- 手段2：llama.cppに直接接続（上級者向け）
  - LM Studioは内部でllama.cppを使っている。LM Studioを使いたくない場合は直接llama.cppを立て、Claude Codeをそこに向けることも可能。ただしチューニングや特殊な要件がなければLM Studioの方が簡単。

- モデル選びとリソース
  - 記事時点の推奨モデル：GLM-4.7-Flash、Qwen3-Coder-Next。
  - ディスク・GPUが足りないなら量子化（quantized）版を使うとメモリ/速度トレードオフで実用的。
  - マシン性能が限定的だと応答遅延やコード品質低下が発生する点は覚悟する。

- 切替と戻し
  - どのモデルを使っているか確認／切り替えは /model コマンドで可能。Anthropicに戻したいときも同様。

## 実践ポイント
- まず /usage でクォータ確認。すぐ止まるならローカル切替を検討する。
- 初心者はLM StudioのGUIでモデルをインストール→サーバ起動→環境変数を設定する流れが最短。
- コマンドの例は上記を参照。実行前にGPU・ディスク容量を確認する。
- 小さめの量子化モデルでまず試し、速度と品質のバランスを確かめる。
- センシティブなデータを扱う場合はローカル運用で情報保護の利点がある。
- クォータ復活後は /model でAnthropicに戻すだけで元に戻せる。

以上。試した結果や使ったモデル名を共有すると、他の読者にも参考になります。
