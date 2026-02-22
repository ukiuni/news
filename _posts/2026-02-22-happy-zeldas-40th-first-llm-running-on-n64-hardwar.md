---
layout: post
title: "Happy Zelda's 40th first LLM running on N64 hardware (4MB RAM, 93MHz) - ハッピーゼルダ40周年：N64で動く初のLLM（4MB RAM、93MHz）"
date: 2026-02-22T00:29:25.707Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/sophiaeagent-beep/n64llm-legend-of-Elya"
source_title: "GitHub - sophiaeagent-beep/n64llm-legend-of-Elya: World&#39;s First LLM-powered Nintendo 64 Game — nano-GPT running on-cart on a 93MHz VR4300"
source_id: 47105087
excerpt: "N64（4MB／93MHz）上で動く小型LLMがクラウド不要でゼルダ風会話を実現"
image: "https://opengraph.githubassets.com/666de885767cecea17686d1a58ec00426944780a75296c0f95a6ef35944c3b37/sophiaeagent-beep/n64llm-legend-of-Elya"
---

# Happy Zelda's 40th first LLM running on N64 hardware (4MB RAM, 93MHz) - ハッピーゼルダ40周年：N64で動く初のLLM（4MB RAM、93MHz）
N64が「考える」時代へ — 93MHz VR4300上で動く世界初のオンカートLLMが切り拓くレトロAIゲーム

## 要約
ニンテンドー64（VR4300 93.75MHz、4MB RDRAM）上で動く小型GPT（nano-GPT）をカートリッジ内でリアルタイム推論させたホームブリュー作品。「クラウド不要」で実機のMIPS CPU上だけで自然文生成を実現している点が革新。

## この記事を読むべき理由
レトロゲーム愛好家や日本のインディー開発者が、クラウド無しで“動くAI”を組み込める可能性を示す実例。ゼルダ系RPGや会話型アドベンチャーのようなジャンルで、新しいゲーム体験を低コストで作れるヒントが詰まっています。

## 詳細解説
- ハードウェア：NEC VR4300 @ 93.75 MHz（MIPS III）、標準RAM 4MB（Expansion Pakで8MB）。FPUを使わず、すべて整数固定小数点で動作。  
- モデル：2ブロックのトランスフォーマー、埋め込み128、ヘッド4、FFN 512、512KB弱ではなく重みファイルは約237.6KB、パラメータは約427k、コンテキスト長32トークン、バイト単位（vocab=256）。  
- 数値表現：Q4量子化（1バイトあたり2ニブル）＋32ブロック単位のfloat16スケール、推論はQ8.7固定小数点（int16）。FPUなしで乗算やLayerNorm、ソフトマックスの整数近似で動く工夫が施されています。  
- ソフトウェア構成：nano_gpt.c/.h（推論エンジン）をlibdragonプロジェクトに組み込み。ホスト向けビルドで挙動確認可能（nano_gpt_host.c）。学習はtrain_sophia.py（PyTorch、CUDA）で実行し、約7分（RTX 5070 指標）で学習済みバイナリを出力。  
- ビルド／実行：libdragon toolchainで make → legend_of_elya.z64 を生成。エミュレータ（ares）かEverDriveで実機動作確認。RSP向けマトリクス乗算実装で将来4–8×高速化予定。  
- ゲーム用途：NPCの文脈応答、手続き的クエスト生成、プレイヤー行動に応じた難易度適応など、従来のカートリッジ時代には難しかったダイナミックなゲーム設計が可能に。

## 実践ポイント
- 試す手順：リポジトリをクローン → libdragon toolchain を導入 → make で ROM をビルド。ホストテストは gcc -O2 で gen_sophia をビルドして確認。  
- カスタムモデル：train_sophia.py を使い独自コーパスで学習→SEAIバイナリを書き出し、Q4で量子化してカートに載せる。  
- 日本語対応の注意：元モデルは英語／バイト単位学習。日本語にするなら文字コードとトークナイゼーション（UTF‑8バイト単位か独自サブワード）を検討し、モデル容量とコンテキスト制約（32トークン）を意識する。  
- メモリ対策：4MB制約を忘れずに。Expansion Pakで8MB確保できれば余裕が増える。  
- 活用案：オカリナ系ゲームのNPCに過去会話を参照させる、イベント生成ツール、ローカルで文章生成するデバッグ支援など、レトロ×AIのプロトタイプ作りに最適。

興味があれば、まずリポジトリをクローンしてホストビルドで挙動を確認し、libdragonプロジェクトに nano_gpt.c/.h を組み込んでみてください。
