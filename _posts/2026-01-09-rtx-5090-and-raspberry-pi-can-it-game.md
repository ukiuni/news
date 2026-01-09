---
layout: post
title: "RTX 5090 and Raspberry Pi: Can It Game? - RTX 5090 と Raspberry Pi：これでゲームはできるか？"
date: 2026-01-09T21:06:24.385Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://scottjg.com/posts/2026-01-08-crappy-computer-showdown/"
source_title: "RTX 5090 + Raspberry Pi: Can it Game? | Scott's Blog"
source_id: 46558148
excerpt: "Raspberry Pi 5＋RTX5090はPCIeとCPU制約で最新作不可、古めのゲームは可"
image: "https://scottjg.com/hero-5090-and-rpi5.jpg"
---

# RTX 5090 and Raspberry Pi: Can It Game? - RTX 5090 と Raspberry Pi：これでゲームはできるか？
Raspberry Pi 5 に超高級 GPU（RTX 5090）を繋いで本気でゲームできるか確かめてみたら、意外な現実が見えた話

## 要約
Raspberry Pi 5 や同価格帯の小型PCに OCuLink ドック経由で RTX 5090 を接続してゲームを試した結果、最新作はCPU側のエミュレーションボトルネックで事実上プレイ不可。2010年代前半の古いゲームなら実用範囲に入ることが分かった。

## この記事を読むべき理由
国内でもラズパイや小型SBCを趣味プロジェクトや省電力PCとして使う人が増えています。高級GPUを“外付け”してゲーミングを目指す実験は夢がある一方で、実際の課題（PCIe 帯域、ARM→x86 互換レイヤ、ドライバ互換性）は日本のDIYゲーマーや組み込み開発者にも直接参考になります。

## 詳細解説
- 実験対象
  - Beelink MINI-S13（Intel N150、PCIe Gen3 x4）
  - Radxa ROCK 5B（RK3588、ARM、PCIe Gen3 x4）
  - Raspberry Pi 5（BCM2712、ARM、NVMe HAT 経由で PCIe Gen2 x1 ≒ 約500 MB/s）
  - eGPU は OCuLink ドック＋RTX 5090（Founders Edition、32GB VRAM）
- なぜ問題になるか（技術的ポイント）
  - PCIe 帯域差：Pi の Gen2 x1 は ~500 MB/s、一方で Gen3 x4 は ~4,000 MB/s と約8倍の差。GPU を活かすためのデータ転送で不利。
  - CPU/互換レイヤ：ARM 上で x86 向けゲームを動かすには FEX（ユーザ空間での互換レイヤ）＋Proton/Wine 等が必要。FEX によるオーバーヘッドは非常に大きく、ラズパイはx86換算で2008年頃のCore2クラスに相当する性能になってしまう。
  - ドライバ互換性：ARM 環境は DMA 整合性やメモリ整列の違いでそのままでは NVIDIA ドライバが動作しない。@mariobalanca のパッチがあり、Ubuntu/Fedora 用に作者がパッケージ化して配布している（導入は自己責任）。
  - グラフィック変換層の落とし穴：DX→Vulkan を仲介する DXVK は ARM＋FEX 環境で不安定な場合が多く、OpenGL を使う WineD3D に切り替える（PROTON_USE_WINED3D=1）ことで回避した例がある。
- ベンチ結果の要点
  - 最新大作（例：Cyberpunk 2077）: Pi は 1080p Ultra でも約15 FPS にとどまり実用的でない。ROCK 5B は低設定で 20～25 FPS 台に届くことがある。Beelink（x86）は圧倒的に有利。
  - 古いゲーム（2010年前後）: Just Cause 2 や Portal 2 などは Pi でも実用域。Portal 2 は native ビルドだと 4K 60FPS 超えを観測（GPU がボトルネックにならないため）。
  - CPU ボトルネックの顕在化: Doom のベンチで GPU は 90FPS を出せても CPU 側が足を引っ張り合計フレームレートは 30FPS 未満になる場面が頻出。
- 電力効率
  - Pi 5 のCPU部分は負荷時でも ~9W 程度と非常に省電力。Beelink は同負荷で ~30W。エネルギー効率だけ見れば ARM の優位性はあるが、互換レイヤのペナルティで性能は奪われる。

## 実践ポイント
- 「試してみたい」なら
  - まずは古いタイトル（2010年前後）やネイティブ Linux ビルドのゲームを狙う。GPU に過剰投資しなくて済む。
  - ARM 環境で DXVK が落ちる場合は PROTON_USE_WINED3D=1（OpenGL にフォールバック）を試すと安定することがある。
  - GPU を繋ぐ際は OCuLink と M.2 アダプタ、外部電源が必要。SBC の PCIe スロットを占有するためストレージ配置を考慮（USB SSD を併用）。
  - ドライバはパッチが必要。@mariobalanca 等のコミュニティパッチと配布パッケージを確認する（Ubuntu/Fedora 向けの手順あり）。
- 実用的な結論
  - 「高級GPUをSBCに繋いで最新作を遊ぶ」は現時点では綺麗な実験ネタに留まり、費用対効果は悪い。
  - 小型で手軽にゲームしたいなら x86 ベースの低価格ミニPC（Beelink など）に Windows を入れて遊ぶ方が現実的。
  - 将来的には ARM 向けネイティブ最適化（Valve の ARM 動向や NVIDIA の SoC の噂）で状況は良くなる見込み。興味があるならコミュニティのパッチとドライバの進展を追う価値あり。

この実験は「できるか」を示す好奇心に富んだ挑戦であり、日本の趣味コミュニティや組み込み系の人にとっては学びが多い結果になっています。高価なGPUを繋ぐ前に、目的（レトロ中心か最新作か）をはっきりさせることをおすすめします。
