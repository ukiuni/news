---
layout: post
title: "If You Have Ever Seen Beautiful CGI Simulations Of Realistic Flocking Behaviour With Birds, You Might Wonder How It Is Done - This Is How: - 美しい鳥群のCGIシミュレーションはどう作られているのか ― その方法"
date: 2026-01-16T15:42:17.199Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.youtube.com/watch?v=bqtqltqcQhw"
source_title: "Coding Adventure: Boids - YouTube"
source_id: 425383662
excerpt: "シンプルな3ルールでCGIの美しい鳥群を再現するBoidsの実装と最適化テクを解説"
image: "https://i.ytimg.com/vi/bqtqltqcQhw/maxresdefault.jpg"
---

# If You Have Ever Seen Beautiful CGI Simulations Of Realistic Flocking Behaviour With Birds, You Might Wonder How It Is Done - This Is How: - 美しい鳥群のCGIシミュレーションはどう作られているのか ― その方法

映像で見る鳥群の自然な動きは、シンプルなルールの組み合わせで驚くほどリアルに再現できる――Boidsアルゴリズム入門と実践のコツ。

## 要約
Boidsは「分離」「整列」「結合」の3つのローカルルールを使い、群れ行動（flocking）をリアルに再現するアルゴリズム。実装は単純だが、最適化とパラメータ調整で映える表現が可能。

## この記事を読むべき理由
ゲーム開発、CGアニメーション、群ロボット制御、交通や群集シミュレーションなど、日本の現場で応用できる技術。少ない計算で自然な動きを作れるため、プロトタイプ作成や教育用途に最適。

## 詳細解説
Boidsの基本は各個体（boid）が近傍の個体を観測し、次の3つのベクトルを計算して運動を決めること：

- 分離 (Separation): 近い個体と衝突しないように離れる力  
- 整列 (Alignment): 近い個体と向きを揃える力  
- 結合 (Cohesion): 群れの中心へ引き寄せる力

計算式（イメージ）：
$$
v_{\text{coh}} = \text{normalize}\Big(\frac{1}{|N|}\sum_{j\in N} p_j - p_i\Big)\cdot v_{\max}
$$
$$
v_{\text{ali}} = \text{normalize}\Big(\frac{1}{|N|}\sum_{j\in N} v_j\Big)\cdot v_{\max}
$$
$$
v_{\text{sep}} = \sum_{j\in N} \frac{p_i - p_j}{\|p_i - p_j\|^2}
$$
最終的な加速度は重み付き和：
$$
a = w_{\text{coh}} v_{\text{coh}} + w_{\text{ali}} v_{\text{ali}} + w_{\text{sep}} v_{\text{sep}}
$$
速度と位置は時間刻みで更新し、速度は最大速度 $v_{\max}$、加速度は最大力 $f_{\max}$ でクランプする。

実装上の注意点:
- 近傍検索はナイーブにすると $O(n^2)$。多数のboidsでは空間ハッシュ（セルグリッド）やクアッドツリーで高速化。
- 視野（視角）や視認距離で近傍を制限するとより現実的。
- 境界処理（ワープ、反射、戻す）や障害物回避を組み合わせると表現の幅が広がる。
- 大量の個体はGPU（シェーダ／Compute）やECSで処理すると高性能。

動画で紹介されることが多いテクニック:
- ランダムノイズやリーダー個体を混ぜて自然さを増す
- カメラ寄りの個体にLODを適用して負荷を下げる
- アニメーションの補間や姿勢（向き）の滑らかさを追加

## 実践ポイント
- 最低限の実装手順：位置・速度を持つBoid構造 → 近傍を検索 → 3つの力を計算 → 合成して速度・位置更新。
- パラメータ調整は視覚的重要：$w_{\text{sep}}$ を少し上げると散らばり防止、$w_{\text{ali}}$ を上げると波状運動が強調される。
- 最初は数十個で挙動確認、問題なければ空間ハッシュで数千〜万体へスケール。
- UnityならComputeShader／ECS、GodotやThree.jsなら空間ハッシュ＋GPUインスタンシングで効率化。
- デバッグ時は近傍線や速度ベクトルを可視化すると調整が楽。

簡単な更新ステップ（サンプル）:
```javascript
// javascript
// neighbors: 配列, p: position, v: velocity
let vCoh = normalize(avgPos(neighbors).sub(p)).mul(maxSpeed);
let vAli = normalize(avgVel(neighbors)).mul(maxSpeed);
let vSep = sum(neighbors.map(n => p.sub(n.pos).div(distSq(p,n.pos))));
let accel = vCoh.mul(wC).add(vAli.mul(wA)).add(vSep.mul(wS));
accel = clamp(accel, maxForce);
v = clamp(v.add(accel.mul(dt)), maxSpeed);
p = p.add(v.mul(dt));
```

日本の開発現場での応用例:
- インディーゲームの群集表現や敵AI
- 映像制作での群れシーン（短時間で質感の良い挙動）
- ドローン群制御の基礎シミュレーション
- 都市計画での歩行者シミュレーションのプロトタイプ

Boidsはシンプルだが奥が深い。まずは小さな実装で動きを確かめ、視覚的な調整と最適化を順に行うと短時間で魅力的な群れ表現が作れる。
