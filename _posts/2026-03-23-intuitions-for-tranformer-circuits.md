---
layout: post
title: "Intuitions for Tranformer Circuits - トランスフォーマー回路の直感"
date: 2026-03-23T02:16:33.749Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.connorjdavis.com/p/intuitions-for-transformer-circuits"
source_title: "Intuitions for Transformer Circuits - by Connor Davis"
source_id: 47484227
excerpt: "残差ストリームを共有メモリ化しQK/OVのサブスペース読写を直感解説"
image: "https://substackcdn.com/image/fetch/$s_!5wXL!,w_1200,h_675,c_fill,f_jpg,q_auto:good,fl_progressive:steep,g_auto/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2ef1b05a-5fb2-4bc4-8082-1ad7d8b5cf47_2371x2006.png"
---

# Intuitions for Tranformer Circuits - トランスフォーマー回路の直感
完成度を超えて理解する：残差ストリームを「共有メモリ」として読み解く短期集中ガイド

## 要約
トランスフォーマー内部を「残差ストリーム＝共有メモリ」と見ることで、注意機構（QK）と値経路（OV）がどのサブスペースを読み書きするかを直感的に理解できる、という解説。

## この記事を読むべき理由
メカニスティック・インタープリタビリティ（MI）はモデルの「なぜ動くか」を解明し、AIの安全性・説明性に直結する。日本のプロダクト開発や研究でも、LLMの誤動作や有害出力対策、効率的なデバッグに直結する知見が得られる。

## 詳細解説
- 残差ストリーム：各トークンごとに次元 $d_{model}$ のベクトルが並ぶ「共有メモリ」。レイヤーはここに逐次的に読み書きする。モデルはこの空間を用途ごとのサブスペースに分割して利用する。
- 注意（Attention）：トークンの「どの行（トークン位置）を読むか」を決める。Q,K を使うQK回路は入力列に依存するアクティベーションで、パターンは
  $$A = x W_Q W_K^T x^T$$
  と表される（$x$ は残差ストリーム行列）。
- OV回路：選ばれたトークンから何を読み出して書き戻すかを決める。これは
  $$x W_V W_O$$
  で表され、全体のヘッドは
  $$A x W_V W_O$$
  となる。
- サブスペーススコア（virtual/composition scores）：Attention が行インデックス（トークン）をソフトに指定するのに対し、OV/QK の低ランク性（$d_{head} \ll d_{model}$）は「どの列（次元サブスペース）を読むか」を係数として学習させる。簡単に言えば「トークン:サブスペース」という論理アドレスで読み書きする。
- 実例的手法：埋め込みや位置エンコーディングが使うサブスペースの割合は PCA や Frobenius 比で測れる。例えば
  $$\frac{\|W_A W_B\|_F}{\|W_A\|_F \|W_B\|_F}$$
  といった比で、あるヘッドが埋め込み寄りか位置情報寄りかを定量化できる。
- 回路の直感：QK はどこを参照するか（トークン選択）、OV は参照先のどの情報を持ってくるか（サブスペース選択）を分担する。これが「誘導（induction）ヘッド」や「前トークンコピー」などの振る舞いを生む。

## 実践ポイント
- ARENA の入門問題を解いて手を動かす：理論が腑に落ちる。
- 小さめモデルで埋め込み・位置エンコーディングの PCA を見る：どのくらいの次元が実際に使われているか把握する。
- ヘッド単位で QK/OV のサブスペーススコアを計算して、役割（位置情報／語彙情報）を推定する。
- プロダクト視点：重要な情報を「特定サブスペース」に限定することで、情報流出や有害出力の検査ポイントを設計できる可能性を検討する（サブスペース監査やフィルタリングの導入）。
- 研究／実装：$d_{head}\ll d_{model}$ の低ランク性を利用した可視化・デバッグツールは、日本の研究・事業環境でもすぐ導入可能。

参考として、まずは小さな注意のみ（MLP除去）のモデルで上記解析を試すことを推奨する。
