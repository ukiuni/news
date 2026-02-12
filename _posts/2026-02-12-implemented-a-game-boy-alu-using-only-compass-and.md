---
layout: post
title: "Implemented a Game Boy ALU using only Compass and Straightedge constructions. It takes 15 minutes to boot Pokémon Red. - コンパスと定規だけでGame BoyのALUを実装。ポケモン赤の起動に15分"
date: 2026-02-12T21:43:47.284Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/0x0mer/CasNum"
source_title: "GitHub - 0x0mer/CasNum"
source_id: 444469777
excerpt: "コンパスと定規でALUを実装しポケモンが15分で起動、作図可視化も可能"
image: "https://opengraph.githubassets.com/8ce21815befba70bdae02cc90a2589ee62a53419301b4a70747a6fa4694baeec/0x0mer/CasNum"
---

# Implemented a Game Boy ALU using only Compass and Straightedge constructions. It takes 15 minutes to boot Pokémon Red. - コンパスと定規だけでGame BoyのALUを実装。ポケモン赤の起動に15分

古代ギリシャの作図だけでコンピュータ算術を再現？コンパス＆定規で動く「Game Boy」が生まれた実験プロジェクトの話。

## 要約
CasNumはコンパスと定規（Euclid的作図）だけで任意精度算術を実装したライブラリで、ALUを置き換したGame Boyエミュレータを動かし、ポケモンの起動に約15分かかることを示しています。

## この記事を読むべき理由
- 計算の「定義」を図形的に再解釈するユニークな実験は、計算理論・数値表現・教育用途で刺激的。  
- Pythonでの実装例とエミュレータ統合が公開されており、手を動かして学べる点が魅力。

## 詳細解説
- 基本アイデア：CasNumは数値$x$を平面上の点$(x,0)$で表現し、コンパス＆定規の5つの基本作図（2点を通る直線、中心を決めた円、直線同士の交点、直線と円の交点、円同士の交点）を「ISA」と見なして演算を構築します。  
- 算術の実装例：
  - 加算：点の中点を取って倍にする作図で実現。  
  - 乗除：相似三角形などの幾何的関係から構築。  
  - 論理演算（AND/OR/XOR）：代数的に綺麗ではないため、やや冗長な幾何構成で実現。  
  - 円同士の交点は4次方程式相当の計算を含み、実装は複雑（repo内の circle.py に長大な式あり）。  
- 実用面：PyBoy（Game Boyエミュ）にCasNumを差し替えてALUを実装。opcodes_gen.pyのみの最小修正で統合。初回は多くの演算を作図で行うため非常に遅く、ポケモン起動に約15分。キャッシュ（Pythonの lru_cache）により同一プロセス内の再実行は高速化し、2回目は0.5〜1FPS程度まで改善。  
- ビジュアライザ：pygletを使った作図表示（viewer）があり、作図過程を観察可能。  
- 付属例：基本例、RSA例、さらにzlibライセンスの2048.gbが付属（著作権のあるゲームROMは自分で用意する必要あり）。

## 実践ポイント
- クローンして動かす（最小手順）:
```bash
# bash
git clone --recursive git@github.com:0x0mer/CasNum.git
cd CasNum
pip install -r requirements.txt
python3 -m examples.basic
python3 -m examples.rsa
```
- PyBoy統合：examples/PyBoyに自分のROM（例: Pokemon.gbは配布不可）を置き、READMEの手順どおりに起動。2048.gbはリポジトリ付属で試せます。  
- 学びどころ：計算の幾何的表現、数値表現の設計、Pythonsのキャッシュ戦略、可視化による教育利用。授業デモやワークショップのネタに最適。  

興味があるならリポジトリ（0x0mer/CasNum）を覗いて、作図ビジュアライザと例を動かしてみてください。
