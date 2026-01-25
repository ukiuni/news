---
layout: post
title: "Hands-on with two Apple Network Server prototype ROMs - Apple Network Server プロトタイプROMを触る"
date: 2026-01-25T11:20:53.620Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "http://oldvcr.blogspot.com/2026/01/hands-on-with-two-apple-network-server.html"
source_title: "Old Vintage Computing Research: Hands-on with two Apple Network Server prototype ROMs"
source_id: 699841604
excerpt: "実機で判明した未公開ANSプロトタイプROMの起動成功と限界を詳細レポート"
---

# Hands-on with two Apple Network Server prototype ROMs - Apple Network Server プロトタイプROMを触る

幻のROMを700で起動！Appleの「白い冷蔵庫」サーバーに眠る未公開ROMの実機リポート

## 要約
1996年のApple Network Server（ANS）で発掘された「Mac OS用」「Windows NT用」のプロトタイプROMを、実機（ANS 700）で試したレポート。NT ROMは単体ではNT導入に不十分、だがMac OS用のプリプロダクションROMは追加ハードウェアやバグを抱えつつ起動に成功した。

## この記事を読むべき理由
- ANSはAppleが最後に出した非-Mac系ワークステーションで、当時の“迷走期”を象徴する稀少機。ハードとROMの組合せでどう挙動が変わるかはレトロハードや組込み機の理解に役立つ。  
- 日本のレトロPC愛好者や教育機関、産業遺産の保存に関心ある技術者にとって、実機テストの手順・注意点が実践的に参考になる。

## 詳細解説
- 概要：ANSはANS 300/500/700のラインナップで、Power Macintosh 9500系をベースに改造された大型サーバ。公式OSはAIX（IBM）で高価・販売数は少ない。  
- ROM事情：今回の所持品は「Mac OSデモ用」とされるプリプロダクションROMと、別に手に入ったNT関連ROM。NT ROMだけではWindows NTを入れられない（ブート／ドライバや追加ファームが必要）。プリプロダクションROMはMac OS起動に成功するが、動作にバグと専用ハード依存が見られる。  
- ハードウェアのユニークポイント：
  - ROMはDIMM形状のROMスティックで、開発機で多用された設計。生産品は4MBの旧World Mac ROM。  
  - 内部SCSIはSymbios 53C825A（Fast Wide、20MB/s）×2。外部SCSIはCURIO＋NCR 53C94（5MB/s）。ANS専用コントローラで他機種と互換性が一部異なる。  
  - ビデオはCirrus Logic 54M30でこれもANS専用。  
  - CPUは専用の大きなdaughtercard形式（SMP対応を想定した設計）。L2キャッシュはモデルで異なり、700は1MB。  
  - メモリは168-pin DIMMで最大512MB（メモリコントローラ制限）。重要：最高性能は60nsのパリティRAMが必要で、非パリティDIMMが混在すると全体が70nsに落ちる。  
  - フロントの4行LCDと前後にキーイング（鍵）で物理保護や起動モードを切替える仕組みがある。  
- 実験運用：貴重な“生産機”を壊さないため、機能不良や保管部品で組んだ“部品箱700（holmstock）”を実験機に使用。起動不能時のLCD表示やCPUカードの緩み（再装着で解消）など、現物ならではのトラブルシュートが出る。

## 日本市場との関連
- 大学や研究機関、自治体の旧設備撤去で出るレトロ機材は国内にも存在し、ANSのような大型サーバの発掘／保存は日本でも起こり得る。ハード保全・資産管理の観点から、発掘時の取り扱い・記録手順は共通の参考になる。  
- また、AIXやRS/6000系資産を長年運用してきた企業や教育機関では、互換性やROM改変が引き起こす運用リスクを理解することが有益。

## 実践ポイント
1. プロトタイプROMは本番機に直接差し込まないで、動作確認用の“犠牲機”で試す。  
2. 起動トラブル（前面LCDが暗い等）はCPUカードの緩みが原因のことが多い。引き出し式ロジックボードを外して再装着を試す。  
3. PRAM電池は保管時に外す（液漏れで基板腐食の元）。作業中も電池外し推奨。  
4. メモリは60nsパリティDIMMを目標に揃える。非パリティ混在で性能低下。  
5. 内部SCSI／ビデオ等はANS固有チップ（Symbios 53C825A、Cirrus 54M30）を使用するため、外部Power Mac用周辺機器との互換性に注意。  
6. 重量物の取り回し・分解は二人作業で。引き出しやプラスチック部品は経年で脆くなっているので無理に力をかけない。  

以上。この記事で分かるのは「ROMだけでは環境は再現できない」ことと、「実機作業ではハード依存やメンテ手順が成功の鍵」だ。興味があれば実機保存や試験の具体手順を別稿でまとめますか？
