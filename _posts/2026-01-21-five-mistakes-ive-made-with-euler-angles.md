---
layout: post
title: "Five Mistakes I've Made with Euler Angles - オイラー角で犯した5つの失敗"
date: 2026-01-21T18:39:57.081Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://buchanan.one/blog/rotations/"
source_title: "Five Mistakes I&#39;ve Made with Euler Angles | Fred's Blog"
source_id: 422286349
excerpt: "軸順・内外回転・角速度の落とし穴を示し行列/クォータニオン運用を勧める実践ガイド"
image: "https://buchanan.one/_astro/banner.CnWHTOeM.png"
---

# Five Mistakes I've Made with Euler Angles - オイラー角で犯した5つの失敗
オイラー角で遭遇する落とし穴をサクッと回避する — 現場で役立つ実践ガイド

## 要約
オイラー角は直感的だが、軸順・内/外回転・能動/受動・角速度の誤認・ギンバルロックといった典型的ミスで長時間のデバッグを招く。内部計算は行列やクォータニオンに任せ、オイラー角は入出力・ログに限定するのが現実的な対処法だ。

## この記事を読むべき理由
ゲーム開発、ロボット、ドローン、車載センサーやVFXなど、日本のプロジェクトでもオイラー角は依然頻繁に使われる。誤解で生じるバグは微妙で見つけにくく、知っておくだけで工数を大幅削減できる。

## 詳細解説
- DCMとオイラー角: 回転は線形なので行列で表現できる。典型的には基本回転行列 $R_X,R_Y,R_Z$ を掛け合わせて
  $$R = R_X R_Y R_Z$$
  のように表す（軸順の表記と実際の行列乗算順は逆になる点に注意）。
- ミス1 — 軸順（Axis Order）: ZYX と XYZ のように順序を間違えると同じ各角度でも最終姿勢が別物になる。プロジェクト内で軸順を固定し明記する。
- ミス2 — 内回転 vs 外回転（Intrinsic/Extrinsic）: 回転が「更新されたローカル軸」か「固定ワールド軸」かを混同すると意図しない逆順と同等の結果になる。設計で選択・文書化する。
- ミス3 — 能動/受動（Active/Passive）: オブジェクトを動かす表現か座標系を動かす表現かの違い。変換は逆行列で変換できるが、仕様で統一する。
- ミス4 — オイラー角の時間微分 ≠ ボディ角速度: オイラー角の微分と機体角速度 $[p,q,r]^T$ は一致しない。例えば ZYX（アクティブ）の場合、
  $$
  \dot\phi = p + q\sin\phi\tan\theta + r\cos\phi\tan\theta\\
  \dot\theta = q\cos\phi - r\sin\phi\\
  \dot\psi = q\sin\phi\sec\theta + r\cos\phi\sec\theta
  $$
  なので安直に等しいと扱うと誤積分を招く。
- ミス5 — 数値精度とギンバルロック: $\theta\to 90^\circ$ のとき $\tan\theta$ が発散し，数値的に不安定（ギンバルロック）。内部は行列やクォータニオンで運用し、オイラー角は可視化・シリアライズ用に留める。

出典: Fred Buchanan, "Five Mistakes I've Made with Euler Angles"（原著）

## 実践ポイント
- プロジェクト開始時に「軸順」「内/外回転」「能動/受動」を明文化する。  
- 内部はDCMまたはクォータニオンで計算し、オイラー角は入出力（UI/ログ/データ交換）のみに使う。  
- センサ/フレーム変換のテストケース（単純な90°回転など）を用意して変換チェーンを検証する。  
- 角速度を扱う場合は上記の微分式を使うか、角速度→回転行列/クォータニオン経由で積分する。  
- Unity/Unreal/Godot/Blender等、使用するエンジンのデフォルト慣習を確認して揃える（日本のチームでは混在が原因のバグが多い）。

原著（参考）: https://buchanan.one/blog/rotations/
