---
layout: post
title: "Golf game built last night with Claude Code, Svelte and ThreeJS - 一晩で作ったゴルフゲーム（Claude Code、Svelte、Three.js）"
date: 2026-02-14T15:06:53.423Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.the-golf-is-golfing.com"
source_title: "the-golf-is-golfing"
source_id: 47014704
excerpt: "Claude Codeで一晩、Svelte×Three.jsで動く3Dゴルフを制作"
---

# Golf game built last night with Claude Code, Svelte and ThreeJS - 一晩で作ったゴルフゲーム（Claude Code、Svelte、Three.js）
AIで“プロトタイプ1夜”達成！Svelte×Three.jsで作るブラウザゴルフ体験

## 要約
Claude Code（コード生成AI）で素早くスケッチを作り、Svelteの軽量コンポーネントとThree.jsの3D描画で一晩で動くゴルフゲームを組み上げたという事例紹介。短時間でのプロトタイプ作成とWebでの配布が鍵。

## この記事を読むべき理由
・AIを使った高速プロトタイピングの実例が学べる。  
・SvelteとThree.jsというシンプルで導入しやすい組合せが、日本のインディー開発者や学習者に向いている。  
・ゲームジャムやPOC（概念実証）を短時間で回したい人に具体的な手順と工夫が参考になる。

## 詳細解説
- 全体アーキテクチャ  
  Claude Codeで基本的なファイル・コンポーネントや振る舞い（ボールの飛行、カメラ追従、クリック操作など）を生成し、SvelteでUIと状態管理、Three.jsでレンダリングを担当。SvelteはリアクティブなUI更新が簡単なので、スコアやショット強度メーターなどを素早く実装できる。

- Three.jsでの基本要素  
  シーン、カメラ（PerspectiveCamera）、レンダラー、ライト、マテリアル、メッシュを用意。 terrain は高さマップや単純なプレーンに頂点変位を入れる手法が簡単。ボールは低ポリゴンのSphereGeometryで十分。レンダーループは requestAnimationFrame で管理。

- 物理（簡易）  
  本格的な物理エンジンを使わなくても、ゴルフの飛距離は初速と角度で十分表現可能。空気抵抗を無視した理想弾道の水平到達距離は $$R=\frac{v^2\sin(2\theta)}{g}$$ で近似できる。衝突判定は地面との高さ比較で十分（複雑なバウンドは反射ベクトル計算）。

- Claude Codeの役割  
  コードスニペットやUI雛形、イベント処理の大枠を生成して開発速度を上げる。出力は手直しが必要だが、ゼロから書く時間を大幅短縮できる。

- 最適化ポイント  
  モバイル対応ならメッシュ削減・テクスチャ圧縮・シェーダー簡素化・インスタンシングを活用。描画負荷は frustum culling と LOD（距離に応じた簡素化）で抑える。

## 実践ポイント
- スタートコマンド（例）
  ```javascript
  // Svelteテンプレート作成
  npx degit sveltejs/template my-golf
  cd my-golf
  npm install
  npm install three
  npm run dev
  ```
- 最小実装の順序  
  1) Three.jsで球と平面を表示。  
  2) クリックで初速と角度を決め、弾道計算で位置更新。  
  3) SvelteでUI（ショット強度、スコア）。  
  4) Claude Codeで生成した雛形を統合して手直し。  
- 簡単な弾道更新（疑似コード）
  ```javascript
  // 毎フレームの位置更新（単位時間 dt）
  velocity.y += -g * dt;
  position.addScaledVector(velocity, dt);
  if (position.y <= terrainHeightAt(position.x, position.z)) {
    // 着地処理：速度を減衰させて跳ね返すなど
  }
  ```
- 日本での活用例  
  ゲームジャム、ハッカソン、技術勉強会の教材として最適。Svelteの採用企業やコミュニティも増えており、短期プロトタイプの需要と親和性が高い。

短時間で「動くもの」を作ることが目的なら、Claude Codeで素早く雛形を作り、Svelte＋Three.jsで磨くワークフローは非常に有効です。興味があれば、最初のボール・平面表示からの具体コード例も提示します。
