---
layout: post
title: "2d FFT Demo Video in Octave Terminal Mode. - Octaveターミナルモードでの2次元FFTデモ動画"
date: 2026-02-19T04:50:31.393Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://youtube.com/watch?v=ZI8-FZNsccw&amp;si=prDfIDvsd12LYg4B"
source_title: "매트랩(Octave)에서 2차원 푸리에변환 데모영상 - YouTube"
source_id: 438086227
excerpt: "Octaveターミナルで2D FFTを実演、周波数可視化と逆変換で画像のノイズ除去を体験"
image: "https://i.ytimg.com/vi/ZI8-FZNsccw/maxresdefault.jpg?sqp=-oaymwEmCIAKENAF8quKqQMa8AEB-AGICYAC0AWKAgwIABABGGUgRChCMA8=&amp;rs=AOn4CLAE6wElBMXngNUTORzr1XA5T8dVAg"
---

# 2d FFT Demo Video in Octave Terminal Mode. - Octaveターミナルモードでの2次元FFTデモ動画
驚くほどシンプルに見る「画像の周波数の世界」 — Octaveターミナルで学ぶ2D FFT入門

## 要約
Octave（MATLAB互換）をターミナルモードで使い、画像に対する2次元高速フーリエ変換（2D FFT）を実演して周波数成分の可視化と逆変換による再構成を紹介するデモ動画の内容を分かりやすく解説する。

## この記事を読むべき理由
画像処理や信号処理の基礎である2D FFTは、コンピュータビジョン、医用画像、無線など多分野で利用される。Octaveは無料で手軽に試せるため、日本の学生やエンジニアが手を動かして学ぶのに最適。

## 詳細解説
- 2D FFTの目的  
  画像を空間領域から周波数領域へ変換することで、周期的なパターンやノイズの分布を解析できる。2次元離散フーリエ変換は次の式で表される：  
  $$
  X(u,v)=\sum_{x=0}^{M-1}\sum_{y=0}^{N-1} f(x,y)\,e^{-j2\pi\left(\frac{ux}{M}+\frac{vy}{N}\right)}
  $$

- Octaveでの基本フロー（ターミナルでのコマンド）  
  動画はGUIに頼らずターミナルでコマンドを順に実行していく様子を見せる。典型的な手順は以下：
  ```octave
  img = imread('image.png');
  I = rgb2gray(img);
  F = fft2(double(I));
  Fc = fftshift(F);              % 低周波を中心へ
  S = log(abs(Fc)+1);            % 観察用に振幅を対数変換
  imagesc(S); colormap gray;
  ```

- fftshiftの重要性  
  FFTの出力はゼロ周波数が角にあるため、視覚的解析では中心に移動するのが一般的。中心付近が低周波（画像の大まかな構造）、外側が高周波（エッジやノイズ）に対応する。

- フィルタリングと逆変換  
  周波数領域でマスク（低域通過／高域通過）を掛け、ifft2で逆変換して効果を確認する。例えば、低域通過フィルタを適用すると滑らかな画像が得られる：
  ```octave
  [M,N]=size(I);
  [u,v]=meshgrid(1:N,1:M);
  cx = round(N/2); cy = round(M/2);
  D = sqrt((u-cx).^2 + (v-cy).^2);
  mask = D < 30;                   % 半径30ピクセルの低域マスク
  G = ifft2(ifftshift(Fc .* mask));
  imagesc(abs(G)); colormap gray;
  ```

- ターミナルモードの利点  
  コード実行のログが残るため再現性が高く、スクリプト化してバッチ処理や学習用ノートとして保存しやすい。GUIに頼らずコマンドを追うことで理解が深まる。

## 実践ポイント
- Octaveを入れて、まずはサンプル画像で上記のコマンドを試す。  
- fftshiftとlog(abs(...)+1)はスペクトル可視化の基本ワザ。必ず使う。  
- 周波数ドメインでマスクを作ってから ifft2 を試し、フィルタ効果を確かめる。  
- 日本語の資料や教科書（画像処理、信号処理の基礎）と組み合わせると理解が早い。  
- 実務ではノイズ除去、特徴抽出、圧縮（低周波優位）などに応用可能。
