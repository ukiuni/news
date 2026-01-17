---
layout: post
title: "Beebo, a wave simulator written in C - Cで書かれた波のシミュレータ「Beebo」"
date: 2026-01-17T05:39:35.969Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://git.sr.ht/~willowf/beebo/"
source_title: "~willowf/beebo -  Wave Simulator written in pure C with SDL2 -  sourcehut git"
source_id: 46612661
excerpt: "C＋SDL2で動く波シミュレータ、シェーダと境界で表現を自在に遊べる"
---

# Beebo, a wave simulator written in C - Cで書かれた波のシミュレータ「Beebo」
CとSDL2で動く“水面シミュレータ”を手元で動かして遊んでみませんか？

## 要約
Beeboは純粋なCとSDL2で実装されたインタラクティブな波シミュレータで、離散ラプラシアンに基づく波動計算と複数のシェーダで多彩な見た目を楽しめます。ビルド済みバイナリかソースから動かせ、設定ファイルで挙動を調整可能です。

## この記事を読むべき理由
- CやSDL2で「物理ベースのビジュアル」を手早く試したいエンジニア／学生／趣味の開発者に実践的な入り口を提供します。  
- 日本のワークショップや電子工作（Raspberry Pi等）向けにも扱いやすく、教育・プロトタイピングの題材になります。

## 詳細解説
- 基本的な仕組み：Beeboは2次元格子上で離散化したラプラシアン演算子を用い、波面の時間発展をシミュレートします。離散ラプラシアンの代表式は例えば次のようになります：
$$
\Delta u_{i,j} \approx u_{i+1,j} + u_{i-1,j} + u_{i,j+1} + u_{i,j-1} - 4u_{i,j}
$$
この差分を使って次の時間ステップの高さや速度を更新し、波が広がる様子を再現します。

- レンダリング：8種類のシェーダが用意されており、水面風、レーダー風、レーザー風など見た目を切り替えられます。シェーダを変えるだけで同じ物理場が別の表現になります。

- 境界条件：デフォルトの四角境界に加え、円形や六角形の境界を選べるため、境界形状による干渉パターン（幾何学模様）を観察できます。

- 実装と依存：言語はC、描画とフォントにSDL2/SDL2_ttfを使用。リポジトリは sourcehut 上にあり、Makefileでビルド可能（Makefileは ~/.config/ の存在を前提）。セーブファイル処理や設定（速度やスケール）も用意されています。

- 配布とデモ：開発ビルドのバイナリ配布ページやデモ動画が公開されています（開発者ページ／YouTube）。

## 実践ポイント
- まず動かす（バイナリがある場合）
bash
```bash
# 設定ディレクトリとフォントを作成／取得（Beeboの手順に準拠）
mkdir -p ${HOME}/.config/beebo/ttf
pushd ${HOME}/.config/beebo/ttf
wget https://git.sr.ht/~willowf/beebo/blob/master/ttf/Urbanist-Regular.ttf
cd ..
wget https://git.sr.ht/~willowf/beebo/blob/master/sample-beebo-config.txt -O beebo-config.txt
popd

# ダウンロードしたビルドを置いたフォルダで実行
./beebo.x64
```

- ソースからビルドする（Ubuntu系の例）
bash
```bash
sudo apt install libsdl2-dev libsdl2-ttf-dev build-essential git
git clone https://git.sr.ht/~willowf/beebo
cd beebo
make
./beebo.x64
```

- カスタマイズ：設定ファイルは ~/.config/beebo/beebo-config.txt。デフォルトの光速（計算の係数）やスケールを変えて波の伝播速度や視覚的な解像度を調整できます。

- 改造／学び方の提案：
  - シェーダを改変して独自のビジュアル表現を作る（アート／インスタレーション向け）。
  - 境界条件や初期刺激の入れ方を変えて波の干渉やモードを探索する（物理学・授業素材）。
  - Windows対応やパッケージ化（Flatpakなど）を行って配布性を高める。

参考リソース（原リポジトリ／ビルド配布／デモ）
- リポジトリ: https://git.sr.ht/~willowf/beebo/  
- ビルド配布: https://builds.sr.ht/~willowf  
- デモ動画: https://www.youtube.com/watch?v=fl1ayTLeICs

短くまとめると、Beeboは「C＋SDL2で学びつつ遊べる」良質な小プロジェクトです。手を動かして波の物理とシェーダ表現を試せば、教育・プロトタイプ・デジタルアートのいずれにも使える発見があるでしょう。
