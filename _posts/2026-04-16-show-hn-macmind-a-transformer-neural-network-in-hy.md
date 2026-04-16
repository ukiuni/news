---
layout: post
title: "Show HN: MacMind – A transformer neural network in HyperCard on a 1989 Macintosh - HyperCard上のTransformer「MacMind」（1989年製Macで動作）"
date: 2026-04-16T15:18:53.082Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/SeanFDZ/macmind"
source_title: "GitHub - SeanFDZ/macmind: Single-layer transformer in HyperTalk for the classic Macintosh · GitHub"
source_id: 47792525
excerpt: "HyperCardだけで1989年MacがTransformer学習とFFT構造再発見を実演"
image: "https://opengraph.githubassets.com/86887edbf4fa714cc33c19aab7f3609e75e86ddbcf3213410285887c4a06040c/SeanFDZ/macmind"
---

# Show HN: MacMind – A transformer neural network in HyperCard on a 1989 Macintosh - HyperCard上のTransformer「MacMind」（1989年製Macで動作）
魅惑のレトロAI：1987年のスクリプト言語で「注意機構」と「逆伝播」を動かした話

## 要約
MacMindは、HyperTalk（HyperCard）だけで実装されたシングルレイヤーのトランスフォーマーで、1980年代のMac上でビット反転順序（FFTの前処理）を学習します。規模は小さいが、現代の大規模モデルと同じ数学を「目で見て触れる」形で再現しています。

## この記事を読むべき理由
AIの「仕組み」を理屈だけでなく実行可能な形で可視化できる貴重な実例です。日本の教育現場や趣味のレトロコンピューティング、入門者が「注意（attention）」「逆伝播（backprop）」を直感的に理解するための教材として最適です。

## 詳細解説
- 何をしているか：HyperCard上のHyperTalkスクリプトだけで、順伝播→損失計算→逆伝播→重み更新（確率的勾配降下法）を実装。外部ライブラリやコンパイル済みコードは一切使いません。
- 学習課題：8要素列の「ビット反転順序」を学習。例：8要素インデックスの2進表現を反転して位置を並べ替える。具体的には $1(001)\to4(100)$ などの写像を自己注意と勾配降下で発見します。
- アーキテクチャ（要点）
  - パラメータ総数：1,216
  - トークン埋め込み：10×16（160）／位置埋め込み：8×16（128）
  - Q,K,V 各投影：16×16（各256）／出力投影：16×10（160）
  - データ流：入力8 → 埋め込み＋位置 → Q,K,V → Attention（8×8）→ Context → 残差 → 出力ロジット（8×10）→ ソフトマックス
- 可視化：学習後の注意重みはFFTの「バタフライ」ルーティングを示し、モデルがCooley–Tukeyの構造を独力で再発見する様子が見られます。
- 実行環境：実機はMacintosh SE/30（System 7.6.1）で、エミュレータ（Basilisk II／SheepShaver）でも動作。HyperTalkはインタプリタなので、1ステップ数秒、完全収束まで数百〜千ステップ（数時間）かかります。
- 検証：リポジトリには同じ処理をNumPyで実装した validate.py があり、結果を照合できます。

## 実践ポイント
- すぐ試す：リリースの MacMind-Trained.img（学習済み）をエミュレータで開き、Card 3で New Random → Permute を試すだけで動作を確認できます。
- 学習を体験する：MacMind-Blank.img を使えば Card 2 で Train 10 や trainN 1000 と打ち込んで学習の進行を観察可能。HyperCardのメッセージボックスで一時停止やログクリアもできます。
- 教育応用：授業やハンズオンで「小さいモデルで Attention と Backprop を可視化」する教材に最適。実機（博物館展示）やエミュレータで手を動かしながら学べます。
- 日本での活用案：大学の入門講義、ハッカソンのデモ、レトロPC愛好家コミュニティでのワークショップ、また企業の社内勉強会で「AIの数学は規模の問題でしかない」を示すデモとして使えます。
- 技術検証：手元の環境で再現する場合は validate.py（Python + NumPy）で挙動を確認すると確実です。

興味がある方は元リポジトリ（SeanFDZ/macmind）をチェックして、実際に動かしてみてください。
