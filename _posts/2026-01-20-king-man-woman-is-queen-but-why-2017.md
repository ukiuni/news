---
layout: post
title: "King – man + woman is queen; but why? - King – man + woman は queen; でもなぜ?"
date: 2026-01-20T10:26:34.256Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://p.migdal.pl/blog/2017/01/king-man-woman-queen-why/"
source_title: "king - man + woman is queen; but why? - Piotr Migdał"
source_id: 46641145
excerpt: "Word2Vec/GloVeが共起とPMIで王−男＋女＝女王の意味差を解き、日本語実務の工夫も解説"
image: "./queen-julia-vectors-facebook.jpg"
---

# King – man + woman is queen; but why? - King – man + woman は queen; でもなぜ?
「王 − 男 + 女 = 女王」はなぜ成り立つのか？――Word2Vec/GloVeが教える“言葉の掛け算”の直感

## 要約
単語をベクトル化すると、意味の類似性だけでなく「性別」や「時制」といった方向（ベクトル差）が現れ、たとえば $ \vec{v}_{king} - \vec{v}_{man} + \vec{v}_{woman} \approx \vec{v}_{queen} $ のようなアナロジーが成立する理由を、共起確率とPMI（Pointwise Mutual Information）を使って直感的に説明します。

## この記事を読むべき理由
NLPや検索、チャットボットを扱う日本のエンジニアやプロダクト担当には、語表現の内部構造を理解することが重要です。特に日本語は形態素分割や表記ゆれが多く、ベクトル表現をどう作るかで精度やUXが大きく変わります。本記事は初級者でも納得できる直感と実務で役立つヒントをまとめます。

## 詳細解説
- 分布仮説（distributional hypothesis）  
  「言葉はその周りに出現する語によって特徴づけられる」という考え方が出発点。たとえば未知語は文脈の近い語から意味を推測できます。

- 共起とPMI  
  単語の共起確率 $P(a,b)$ や条件確率 $P(a\mid b)$ を扱う代わりに、よく使われる指標がPMIです：
  $$ PMI(a,b)=\log\frac{P(a,b)}{P(a)P(b)} $$
  PMIは「ランダムならどれだけ起きにくい組み合わせか」を測ります。

- PMIとベクトル内積の関係  
  単語ごとに低次元ベクトル $\vec v$ を割り当て、PMIを内積で近似すると
  $$ PMI(a,b)\approx \vec v_a\cdot\vec v_b $$
  となり、これが語彙の高次元共起情報を圧縮して表現する鍵です。

- 類似度とコサイン距離  
  ベクトルの長さ（頻度の強さ）よりも「方向（共起パターン）」を重視するため、コサイン類似度
  $$ \cos(\vec v_a,\vec v_b)=\frac{\vec v_a\cdot\vec v_b}{\|\vec v_a\|\|\vec v_b\|} $$
  がよく使われます。

- アナロジー（差の方向性）  
  アナロジーは「ある性質の変化」をベクトル差で表現します。例えば性別軸を表す差分 $\vec v_{woman}-\vec v_{man}$ に単語を射影すると、その単語がどの程度“女性性”に近いかが分かります。一般に以下が成り立つと仮定します：
  $$ \vec v_w\cdot(\vec v_a-\vec v_b)=\log P(w\mid a)-\log P(w\mid b) $$
  この式は「ある特徴（a と b の違い）に対する単語wの相対的な出現傾向」を示します。差分ベクトルが同じ方向を示すと、対応する意味変化（性、時制、職業など）を共通に表現できます。

- モデルと実装上の注意  
  - 代表的手法：word2vec（Skip-Gram + Negative Sampling）、GloVe（共起行列の低ランク分解）。  
  - 実務では単語側とコンテキスト側で別々のベクトルを持つ設計や、$PMI=-\infty$ に対処するためのPPMI（非負化）などの工夫が必要。  
  - 日本語では形態素解析やサブワード（FastText）の利用が重要：語幹や表記ゆれ、漢字・仮名混在に強くなります。  
  - 近年はBERTなどの文脈化埋め込みが主流だが、静的な単語ベクトルは可視化や軽量なタスクで依然有用です。

## 実践ポイント
- まずは手を動かす：StanfordのGloVeやGoogleのword2vecの事前学習済みベクトルをEmbedding Projectorで可視化してみる。  
- 日本語の前処理は重要：MeCab / Sudachi / Jumanで正しい分割を行い、表記ゆれは正規化する。  
- サブワードを検討：FastTextやSentencePieceは未知語や派生語に強い。日本語では特に効果的。  
- アナロジーを試す：$\vec v_{king}-\vec v_{man}+\vec v_{woman}$ のように差分演算で意味軸を確認し、コサイン類似度で候補を絞る。  
- ドメイン適応：業務データで微調整（fine-tune）すると、業界特有の語義が反映される。  
- ツール＆ライブラリ：gensim（Python）、Embedding Projector、Word2viz、FastText を活用。

参照すべき入門資料：GloVe論文、Jurafsky & Martin（章：Vector Semantics）、および可視化ツールのデモ。日本語固有の前処理を押さえれば、単語ベクトルは検索・推薦・対話など多くのプロダクトで即戦力になります。
