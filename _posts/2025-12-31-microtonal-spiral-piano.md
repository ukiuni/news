---
layout: post
title: "Microtonal Spiral Piano - マイクロトーナル・スパイラル・ピアノ"
date: 2025-12-31T18:37:32.719Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://shih1.github.io/spiral/"
source_title: "Microtonal Spiral Piano"
source_id: 46390312
excerpt: "らせん状鍵盤で直感的に微分音を演奏・探索できるブラウザ実験デモ"
---

# Microtonal Spiral Piano - マイクロトーナル・スパイラル・ピアノ
音程の常識をらせんでほどく――直感で遊べるマイクロトーナル鍵盤

## 要約
Web上で動くインタラクティブな「らせん」インターフェースを使い、マイクロトーナル（微分音）を直感的に演奏・探索できる実験的なピアノ。JavaScript（Web Audio）で動作するためブラウザで即体験できる。

## この記事を読むべき理由
日本の電子音楽／ゲーム音響制作、音楽系プロダクト開発、あるいはUI/UXに興味あるエンジニアにとって、非標準音律を扱うためのインタラクティブ設計やWebAudio実装のヒントが得られる点で有益。マイクロトーナルはゲームBGMやサウンドデザインで独自性を出す強力な手段でもある。

## 詳細解説
- インターフェース概念  
  「らせん」レイアウトは音高を平面的に展開する代替表現。角度や半径に対して音高や強さ、フィルタ等を割り当てることで、従来の鍵盤とは異なる演奏感と音程遷移を実現する。らせんの一周をひとつの周期（オクターブや任意のスケール）に対応させる設計が典型。

- マイクロトーナルの扱い方（技術的なポイント）  
  通常の12平均律は周波数比$f = f_0 \cdot 2^{n/12}$で表されるが、マイクロトーナルではステップ幅を任意にし、センツ単位や任意比率で音高を決められる。例えばセンツによる一般化は
  $$
  f = f_0 \cdot 2^{\frac{\text{cents}}{1200}}
  $$
  のように表せる。らせん上の位置を$c$（センツ）や$n$（ステップ数）にマッピングして周波数を生成する。

- 実装スタック（想定）  
  元デモはブラウザ上で動くため、Web Audio APIを中心に、音源はOscillatorNodeやAudioWorkletで合成、視覚化はCanvasまたはSVG/ WebGLで行う設計が自然。インタラクションはpointer/touchイベントで扱い、連続的なピッチ制御を行う。

- ユーザー体験の利点  
  らせん配置は音程の隣接関係を空間的に表現するため、直観的な微分音探索が可能。スケール作成や微分音の耳トレにも適する。

## 実践ポイント
- まず試す：ブラウザでJavaScriptを有効にしてデモを触る。直感的な操作で音程の変化を確認するだけでも気づきが多い。  
- 開発に活かす：既存の音響プロジェクトに組み込むなら、WebAudioのAudioWorkletで低遅延合成を行い、らせんの座標を周波数にマッピングする実装を検討する。簡単なマッピング例：

```javascript
// javascript
// らせん上の角度 theta をセンツに変換して周波数を算出する例
const f0 = 440; // 基準周波数
function centsToFreq(cents) {
  return f0 * Math.pow(2, cents / 1200);
}
function thetaToCents(theta, centsPerRevolution = 1200) {
  return (theta / (2 * Math.PI)) * centsPerRevolution;
}
// 使用例
const theta = Math.PI; // らせんの角度
const freq = centsToFreq(thetaToCents(theta));
```

- 応用案：ゲーム音響で非西洋音階や不穏なムードを出す、音楽教育ツールで微分音の耳を鍛える、UIとして触覚的に音律を可視化するなど。  
- 日本市場向けヒント：和風音楽や伝統楽器の倍音構造を組み合わせると、邦楽アレンジで新しいテクスチャを生みやすい。

## 引用元
- タイトル: Microtonal Spiral Piano  
- URL: https://shih1.github.io/spiral/
