---
layout: post
title: "New Apple Silicon M4 and M5 HiDPI Limitation on 4K External Displays - 新しいApple Silicon M4/M5での4K外部ディスプレイ向けHiDPI制限"
date: 2026-03-30T03:36:28.872Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://smcleod.net/2026/03/new-apple-silicon-m4-m5-hidpi-limitation-on-4k-external-displays/"
source_title: "New Apple Silicon M4 & M5 HiDPI Limitation on 4K External Displays | smcleod.net"
source_id: 47569502
excerpt: "M4/M5搭載Macで4K外部モニタが2.0×HiDPI不可、文字がぼやける原因と回避法まとめ"
image: "https://smcleod.net/2026/03/new-apple-silicon-m4-m5-hidpi-limitation-on-4k-external-displays/macOS.jpeg"
---

# New Apple Silicon M4 and M5 HiDPI Limitation on 4K External Displays - 新しいApple Silicon M4/M5での4K外部ディスプレイ向けHiDPI制限
M4/M5搭載Macで「4Kを選ぶと文字がぼやける」原因と回避のヒント

## 要約
M4/M5世代のApple Siliconでは、4K外部ディスプレイに対してフルの2.0x HiDPI（3840×2160の見た目で7680×4320のバックストア）を割り当てられず、約1.75x（3360×1890のHiDPI）までに制限される。ハードは対応していても、GPUドライバ側のフレームバッファ割当ポリシーが原因。

## この記事を読むべき理由
多くの日本の開発者・クリエイターがMac＋4K外部モニタを使っているため、この制限は作業効率（画面解像度と文字の鮮鋭度）に直結する。M5 Maxが公式に8K対応を謳っていても、実際のUI体験が損なわれる事例として知っておく価値がある。

## 詳細解説
- 何が起きているか：M2/M3では4K外部で2.0x HiDPI（見た目3840×2160）のモードが使えたが、M4/M5ではWindowServerに列挙されるモードからそのオプションが消える。結果、ユーザーは「フルの4K（非HiDPIで文字がぼやける）」か「3360×1890 HiDPIでUIが大きくなる」のどちらかを選ぶことになる。
- 原因の所在：ディスプレイの能力（DCPが返すMaxW/MaxH/MaxActivePixelRate）はM2と同じで、ハード側制限ではない。問題はGPUドライバ（AppleDisplayCrossbar）側に導入された「動的フレームバッファ割当ポリシー」で、各ディスプレイパイプに対して最大約1.75×のバックストアしか割り当てないため、2.0×が許容されない。
- 試した対策と結果：
  - display override plist（scale-resolutions）やEDIDのソフト上書きはM5で無効。DCPは実機EDIDを使うため、ソフト層だけの変更は効かない。
  - モニタEEPROMへのEDIDフラッシュも効果なし（多くの機種は書き込み不可か、書き換えが反映されない）。
  - IOKitレジストリ直接変更はカーネルドライバが拒否。
  - SkyLightの非公開API経由でも、DCP由来のモードリスト検証を迂回できず。
- まとめ：制限はカーネル空間のドライバ側ポリシーであり、ユーザ空間からは解除できない。根本解決はApple側の修正を待つ必要がある。

## 実践ポイント
- 今すぐできる対処
  - 一時的な回避：解像度を「3360×1890 HiDPI」に設定して文字を鮮明にするか、非HiDPIの3840×2160を選んで作業領域を優先する（どちらを妥協するか選ぶ）。
  - ケーブル/入力切替は劇的改善を期待しにくいが、念のためDP 1.4（HBR3）接続を使う。
  - もし可能ならネイティブ5K/8Kモニタを使うとこの制限を回避できる（DCPがネイティブで大きなバッファを割り当てるため）。
- 調査・報告用コマンド（ターミナルで実行）
```bash
# DCPの上限値確認
ioreg -l -w0 | grep -o '"MaxActivePixelRate"=[0-9]*\| "MaxW"=[0-9]*\| "MaxH"=[0-9]*' | paste - - - | sort -u

# システムの表示概要
system_profiler SPDisplaysDataType
```
- Appleへのフィードバック：この記事の問題点とBetterDisplay議論（例: discussion #4215）を参照してAppleにバグレポートを出す。多くの報告が集まれば優先度が上がる可能性がある。

以上。問題の本質は「ハードではなくドライバの設計変更」にあるため、最終的な解決はApple側の対応を待つか、ハード的に別のモニタ構成に変えることになります。
