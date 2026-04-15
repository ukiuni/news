---
layout: post
title: "Fix monitor that goes black, off or blinks due to static electricity in chair - 椅子の静電気やEMIでモニターが暗転・点滅する問題を直す方法"
date: 2026-04-15T18:39:14.049Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://aalonso.dev/blog/2023/how-to-fix-monitor-that-goes-black-off-due-to-static-electricity-in-chair/"
source_title: "How to fix monitor that goes black, off or blinks due to static electricity in chair (and others) | Aitor Alonso | Senior Software Engineer"
source_id: 47738081
excerpt: "椅子の静電気やEMIでモニターが暗転する原因とフェライト/接地で短時間解決"
image: "https://aalonso.dev/images/articles/2023/how-to-fix-monitor-that-goes-black-off-due-to-static-electricity-in-chair/cover.jpg"
---

# Fix monitor that goes black, off or blinks due to static electricity in chair - 椅子の静電気やEMIでモニターが暗転・点滅する問題を直す方法
立ち上がるたびにモニターが消える？在宅ワークで起きる“椅子→静電気/EMI”トラブルの即効対策

## 要約
椅子の静電気蓄積やガスリフトの動作で発生するEMI（電磁ノイズ）が映像ケーブルに乗り、外部モニターが一瞬ブラックアウトしたり外れる問題が起きる。椅子を接地する・ケーブルにフェライトコアを付けることで大幅に改善する。

## この記事を読むべき理由
USB-C/DisplayPortのモニタ接続が増えた日本の在宅勤務環境でも発生しやすい問題で、原因が分かれば安価・短時間で解決できるから。機材交換や修理に出す前に試せる実用的な手順を紹介します。

## 詳細解説
- 発生メカニズム：プラスチック製キャスターや衣服で生じた静電気が人体に蓄積され、金属筐体に触れると放電ショックが発生。また、ガスリフトや座る/立つ動作でコイル状の接点が瞬間的なEMIスパイクを発生し、映像ケーブル（特にDisplayPortや変換アダプタ経由）にノイズが入るとモニターが黒画面・瞬断・再接続不能になることがある。
- 表面化しやすい環境：USB-C→DP、DP→HDMIなどアダプタ経由やDPケーブルを使う高解像度（4K等）の環境で報告が多い。オシロスコープでノイズが確認されている例もある。
- 根本対策と原理：静電気は“放電経路”を作れば軽減でき、EMIはケーブル周辺の磁界結合を抑えることで影響を減らせる。

## 実践ポイント
1. 再現確認：立ち上がる／椅子に触れるとショックやモニター消灯が起きるか観察する。
2. 簡易対処（すぐ試せる）：
   - 映像ケーブルの抜き差しで復帰する場合はまずケーブル接続を見直す（差込不良確認）。
   - 金属部に触れて体の静電気を逃がしてから機器に触る習慣をつける。
3. 恒久対策（効果大）：
   - 椅子を“接地”する：椅子フレームから床またはアースへ導通する金属チェーンやアースコードで放電経路を作る（感電や電源アースを扱う場合は専門家に相談）。
   - フェライトコア（フェライトリング）を映像ケーブルに取り付けてEMIを減衰させる。
   - プラスチック製キャスターを導電性のものに交換、または導電マットを敷く。
   - 可能なら変換アダプタを減らし、シールドの良い短いケーブルを使う。
4. それでも改善しない場合：
   - モニタ／ケーブルを別の入力方式（HDMIや直接USB-C）で試す。
   - メーカーサポートに症状を伝え、交換やファーム更新の有無を確認する。

安全注意：接地処理や電気系の改造は感電や機器破損のリスクがあるため、不安があれば電気の専門家に相談してください。

--- 
短時間の対処で劇的に改善することが多いので、まずはフェライトコア装着と椅子の放電経路確保を試してみてください。
