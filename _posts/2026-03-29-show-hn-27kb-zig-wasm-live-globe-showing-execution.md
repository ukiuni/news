---
layout: post
title: "Show HN: 2.7KB Zig WASM – live globe showing executions at 300 CF edges - 2.7KBのZig製WASMが300箇所超のCloudflareエッジで動くライブグローブ"
date: 2026-03-29T14:34:42.818Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://mcpaas.live/globe"
source_title: "Globe — Where Your Code Runs | MCPaaS"
source_id: 47563325
excerpt: "2.7KBのZig製WASMを300超Cloudflareエッジで実行、実行地点を地球儀で可視化"
image: "https://mcpaas.live/og-globe.png"
---

# Show HN: 2.7KB Zig WASM – live globe showing executions at 300 CF edges - 2.7KBのZig製WASMが300箇所超のCloudflareエッジで動くライブグローブ
魅せるエッジ実行マップ — どこであなたのコードが動いているかが一目でわかる

## 要約
2.7KBのZigでコンパイルしたWASMバイナリを、300箇所以上のCloudflareエッジで実行し、その実行をインタラクティブな地球儀で可視化するデモ（MCPaaSのGlobe）。

## この記事を読むべき理由
エッジコンピューティングが普及する中で、「コードが本当にどこで動いているか」「レイテンシーや冷始動がどう変わるか」を直感的に理解できる。日本でのエッジ最適化やグローバル展開を考えるエンジニアにとって実践的な示唆を与える。

## 詳細解説
- 何がすごいか：Zigで最小限にチューニングされたWASMバイナリがわずか2.7KBという極小サイズで、エッジ環境への配布や冷始動コストを大幅に低減している点。
- インフラ：Cloudflareのエッジ（300地点以上）で実行しており、ユーザーから近い場所で処理できるため応答性が向上する。MCPaaSのGlobeは、実行が発生した場所をリアルタイムにプロットして可視化するUIを提供する。
- 技術的ポイント：Zigは低レイヤ制御とサイズ最適化に優れ、wasm32向けにビルドしてエッジ実行環境で安全にサンドボックス実行できる。観測は各エッジでの実行イベントを集約して表示していると推測される。
- セキュリティと運用：WASMのサンドボックス特性によりエッジでの安全な実行が可能。可視化はローリングデプロイやトラフィック分散の検証、障害検出にも使える。

## 実践ポイント
- まずGlobeを触ってみる：実行場所の可視化で自分の想定とズレがないか確認する（https://mcpaas.live/globe）。
- Zigで小さくビルドする例（wasm32向け、最小化オプション）：
```bash
zig build-obj src/main.zig -target wasm32-freestanding -O ReleaseSmall -fno-stack-protector -dynamic
```
- チェックリスト：
  - 小さなバイナリを目指す（不要なランタイムを避ける）
  - エッジでの冷始動とレイテンシーを計測する
  - 可視化を使ってリージョン別の挙動を検証する
  - 日本のユーザーに近いエッジ（東京、関西など）での応答を重視する

短時間でエッジ動作の実証ができるため、プロトタイプやパフォーマンス検証に最適です。
