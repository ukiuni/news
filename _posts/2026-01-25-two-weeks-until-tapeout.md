---
layout: post
title: "Two Weeks Until Tapeout - テープアウトまで2週間"
date: 2026-01-25T02:00:52.234Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://essenceia.github.io/projects/two_weeks_until_tapeout/"
source_title: "Two weeks until tapeout &#183; Tales on the wire"
source_id: 46749671
excerpt: "2週間でJTAGと2×2 systolic MACをシリコン化した自動化フローと実践ノウハウ"
image: "https://essenceia.github.io/projects/two_weeks_until_tapeout/feature_layout.png"
---

# Two Weeks Until Tapeout - テープアウトまで2週間
魅力的すぎる「クラッシュ・プロジェクト」：2週間でJTAGと2×2 systolic MACをシリコンに送るまでの舞台裏

## 要約
実験的なTiny Tapeoutシャトルを使い、GlobalFoundries 180nmで無料枠を得て、JTAGデバッグ基盤と2×2のSystolic MACを短期でテープアウトした記録。OpenROAD/Librelane/Tiny Tapeoutの自動化フローと「小さく始めて拡張する」設計判断が肝。

## この記事を読むべき理由
日本のホビイスト、大学研究室、スモールスタートのハードウェアチームにとって、実際に「動くシリコン」を低コストで試作する現実的な手順と落とし穴が分かるため。ツールチェインやI/O制約、デバッグ哲学は国内プロジェクトにも直結する。

## 詳細解説
- 実験シャトルの位置付け：Tiny Tapeoutの実験シャトルは新プロセスやフローの検証場。参加は過去提出者に限定され、製造上のリスク（最終チップが不完全でもあり得る）を了承の上で無料枠が提供される点が特徴。
- 自動化フロー：OpenROAD（NHIL：人手介入を減らす設計指向）とLibrelaneが流れを束ね、RTLからGDSまでの自動化を実現。Tiny Tapeoutはテストベンチ実行とGDSアップロードを補完する。短期プロジェクトでの反復速度向上に貢献。
- 設計対象：メインは「JTAG TAP（オンチップのデバッグ入口）」と、動作確認用の2×2 systolic arrayによる8bit MAC。JTAGは後続テープアウトに使い回すため、早期にシリコンで検証したい重要コンポーネント。
- Systolic arrayの利点：データを配列内部で循環再利用することでメモリアクセスを削減。メモリ帯域のコストが高いため、計算対メモリ（compute-to-memory）比が高いほど効率的。
- エネルギー観点の理解：DRAMアクセスは演算より遥かに高コスト。小さな配列でも「データ再利用」が重要で、規模を大きくすれば相対的な効率は向上する。
- 制約：シャトル固有のピン数制限（入出力・GPIOの合計が限られる）、I/Oの最大周波数が未確定（手元では50MHz想定）、SRAMはPDKにあるがフロー側のサポート問題がある等。これらが設計トレードオフを決める。
- 開発プロセス：アーキテクチャ定義 → RTL設計 → Cocotb+iverilogでのシミュレーション → FPGAエミュ（Vivadoでワンコマンド化）→ ファームウェア整備 → 実装（OpenROAD等）→ 最終GDS生成、という流れを短期で回すことが成功の鍵。

## 実践ポイント
- Tiny TapeoutやOpenROADは国内でも使える実践的ルート。まずは小さく（JTAGなど再利用可能な基盤）テープアウトして経験値を稼ぐ。
- フローは自動化せよ：FPGAのビルドやシミュはスクリプト化（「make fpga_prog debug=1」のようなワンコマンド）で反復を速める。
- デバッグ回路を優先してオンチップに載せる：万一の失敗解析が圧倒的に楽になる。
- I/OとSRAMの制約を早期に洗い出す：ピン数・最大周波数・PDKサポート状況で実装方針が変わる。
- エネルギー/帯域の観点で「どこをオンチップ化するか」を判断する：DRAMアクセスのコストを見積もり、データ再利用可能なアルゴリズムを優先。

以上は短期テープアウトで得られる実践的な知見の要約。日本のコミュニティや教育現場でも応用可能な手順と注意点が詰まっている。
