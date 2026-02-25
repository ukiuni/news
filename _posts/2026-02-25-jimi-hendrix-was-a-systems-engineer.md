---
layout: post
title: "Jimi Hendrix Was a Systems Engineer - ジミ・ヘンドリックスはシステムズエンジニアだった"
date: 2026-02-25T20:30:50.223Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://spectrum.ieee.org/jimi-hendrix-systems-engineer"
source_title: "Jimi Hendrix's Analog Wizardry Explained - IEEE Spectrum"
source_id: 47157224
excerpt: "ヘンドリックスはFuzzやアンプ、フィードバックで音を回路設計した"
image: "https://spectrum.ieee.org/media-library/image.png?id=64983431&width=1200&height=600&coordinates=0%2C344%2C0%2C344"
---

# Jimi Hendrix Was a Systems Engineer - ジミ・ヘンドリックスはシステムズエンジニアだった
魅惑の音を「工学」で解剖する：ヘンドリックス流・アナログ信号設計の秘密

## 要約
ジミ・ヘンドリックスは手と足、機材配置でギターとアンプを一つの閉ループにした“アナログのシステム設計者”だった。Fuzz Face、Octavia、wah、Uni‑Vibe、Marshallアンプ、部屋の音響を含む信号連鎖が彼の声のような音色を生んだ。

## この記事を読むべき理由
音作りは単なるエフェクトの積み重ねではなく、非線形回路、インピーダンス相互作用、フィードバックを設計する工学問題であることが分かる。日本のギター／音響エンジニア、エフェクト開発者、DSP屋にとって再現可能な知見が得られる。

## 詳細解説
- 信号チェーン：ギター → Fuzz Face → Octavia → wah →（場合によっては Uni‑Vibe）→ Marshall 100W → 部屋／ギターでフィードバック閉ループ。Octaviaは特注（Roger Mayer）で、入力波形の山谷を反転・整流し第2高調を強調することで“オクターブ上”の明るさを得る。  
- Fuzz Face：2トランジスタのフィードバック増幅で正弦をほぼ方形波に変換。入力インピーダンスが低く（約20 kΩ）、ギターのピックアップ（モデル化例：抵抗6 kΩ、インダクタンス2.5 H、ケーブル容量あり）と直接相互作用するため、ボリューム操作で「クリーンに戻る」特性（cleanup effect）が生まれる。  
- Wah：帯域通過フィルタでセンター周波数を約300 Hz〜2 kHzでスイープし、母音的な変化を付与。  
- Uni‑Vibe：光抵抗制御の4段位相シフトを低周波で変調することで空間的な位相変化／うねりを作る。  
- システム視点：Marshallを歪み域近くに設定してサスティン（持続）を伸ばし、スピーカーと弦の音響結合で離位置・角度を変えることで複数の安定フィードバックモードを“歩いてチューニング”した。  
- 再現手法：著者は各機器の回路図をnetlist化してngspiceでアナログシミュレーションし、Pythonでプロットと音のサンプルを生成。リポジトリ（github.com/nahorov/Hendrix-Systems-Lab）でファイルと手順を公開。

## 実践ポイント
- ngspice＋Pythonで回路シミュレーションを試す（リポジトリ参照）。ハード特性をモデル化するとプラグインでは見えない挙動が分かる。  
- ギター側のインピーダンス（ピックアップ＋ケーブル）を意識し、ペダルの入力インピーダンスを変えて音の“抜け”やcleanup現象を試す。  
- ライブ環境ではアンプ出力とギターの位置/角度で意図的にフィードバックモードを探索する—単なるノイズでなく制御可能な音源になる。  
- 日本のペダルメーカーやライブエンジニアは、この「システム思考」を採り入れることで、より表現力の高いアナログ機材設計やセッティングが可能になる。

（参考）元記事解析と再現スクリプト：github.com/nahorov/Hendrix-Systems-Lab
