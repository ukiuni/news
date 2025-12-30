---
layout: "post"
title: "Windows 2 for the Apricot PC/Xi - Apricot PC/Xi用のWindows 2"
date: "2025-12-27T19:41:23.067Z"
categories:
- tech
- world-news
tags:
- tech-news
- japan
source_url: "https://www.ninakalinina.com/notes/win2apri/"
source_title: "Windows 2 for the Apricot PC/Xi"
source_id: "46403915"
excerpt: "Apricot PC/XiへWindows 2を移植し実機でWord/Excelを動かした技術記録"
---

# Windows 2 for the Apricot PC/Xi - Apricot PC/Xi用のWindows 2

## 要約
イギリス製のレトロ機Apricot PC/Xi（Intel 8086非互換機）にWindows 2を移植し、結果的にWordやExcelが動作するようになったという2年半の技術的挑戦の記録。

## この記事を読むべき理由
レトロPCの保存・復元に興味のある技術者や、制約下でOS／ドライバを動かすノウハウが欲しいエンジニアにとって、ハードウェア非互換を克服する具体的な方針とツールの使い方が学べるから。

## 詳細解説
- Apricot PC/Xiの概要  
  - CPUはIntel 8086（IBM PCの8088とはバス幅などで差異あり）で、非IBM PC互換機。  
  - 当時として先進的な3.5インチフロッピー採用（西側で最初期）、9インチ800×400ピクセルの高精細CRT、Rodime RO352製の10MB 3.5インチハードディスクを搭載するモデルあり。  
  - MS‑DOS 2.0〜3.20は動くが、IBM PC向けバイナリはそのままでは動作しないためソフト資産は非常に限定（総量で数百MB未満）。  

- なぜWindows 2がターゲットになったか  
  - Apricot用に保存されていたWindows 1の移植が存在し、Windows 1と2のドライバ構造は互換性が高かったため。Windows 2を動かせれば、当時の主要アプリ（Word、Excel、Illustratorなど）を実機で動かせる可能性があった。  

- 技術的ハードルとアプローチ  
  - 必要となる主要ドライバ群は SYSTEM.DRV、DISPLAY.DRV、KEYBOARD.DRV、MOUSE.DRV、可能なら COMM.DRV。これらをApricotのBIOS／ハードウェア仕様に合わせて再実装する必要があった。  
  - デバイス固有の割り込み、グラフィック出力（800×400、CRT特性）、およびドライブ制御（3.5"ドライブ、Rodimeの制御）をWindows 2の期待するインターフェースに翻訳する作業が中心。  
  - ツールチェーンはMicrosoft C、Turbo Pascal、Open Watcomなどが利用可能で、既存の技術文書（回路図、BIOSリファレンスマニュアル、サンプルコード）が移植作業を支えた。  
  - 実機での画面は緑CRTから撮影されたため、スクリーンショットの品質が揺らぐ点に注意。  

- 成果と影響  
  - 移植によりWindows 2上で当時の主要アプリを動作させられるようになり、ソフトウェア保存・利用の観点でApricotエコシステムが大きく拡張された。移植プロジェクトはsr.htで公開され、エミュレータ上でも試せる。  

## 実践ポイント
- 試すための最低条件：Apricot PC / PC‑Xi / Xenの実機かエミュレータ＋少なくとも512KBのRAMを用意する。  
- 試用・入手先：プロジェクトはsr.htで公開されている（元記事参照）。実機が無ければまずエミュレータで動作確認。  
- 移植に取り組む際の優先タスク：DISPLAY.DRV → KEYBOARD.DRV → MOUSE.DRV → SYSTEM.DRVの順で実装して、段階的に起動チェーンを確認する。  
- 開発ツール：既存のCコンパイラ（Open Watcomなど）とApricotのBIOSドキュメント、サンプルコードを手元に揃える。  
- 保存・寄与のすすめ：スクリーンショットやドキュメントはオリジナルCRTで撮ると雰囲気は出るがデジタル保存は高解像度で行う。改良やドライバ共有でコミュニティに貢献しやすい。  

