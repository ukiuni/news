---
layout: post
title: "Final Fight: Enhanced - Final Edition - Complete breakdown - Final Fight: Enhanced - Final Edition — 完全解説"
date: 2026-02-16T22:42:09.307Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://prototron.weebly.com/blog/final-fight-enhanced-final-edition-complete-breakdown"
source_title: "Prototron"
source_id: 440001495
excerpt: "AmigaでFinal Fightを2MB化し画面拡張・OS依存排除して最適化した再開発記録"
image: "http://prototron.weebly.com/uploads/6/6/9/6/6696786/editor/ffep-2024.png?1768316927"
---

# Final Fight: Enhanced - Final Edition - Complete breakdown - Final Fight: Enhanced - Final Edition — 完全解説
魅入られるレトロ開発物語：Amigaで「もう一度」作り直した男の徹底リファイン術

## 要約
2025年に再着手されたAmiga向け同人移植プロジェクトが、画面幅拡大・速度安定化・AmigaOS依存排除という3つの目標を中心に、ディスクI/Oとメモリ管理を根本から作り直して最終版を完成させた記録。

## この記事を読むべき理由
古いハードで高密度なゲームを動かす「最適化と逆向きエンジニアリング」の実例は、組込み・レトロ開発・低レイヤ最適化を学びたい日本のエンジニアにとって実践的な教科書になるため。

## 詳細解説
- 目標：画面幅を288→320ピクセルへ広げ、7MHz ECS〜14MHz AGAで速度が均一に動く同期、AmigaOSを使わず2MBのフラットRAMで動作させること。
- 問題点：幅拡大はタイル描画列が増え、2人同時時の描画負荷と遅延を招く。高速機での速度上昇は同期方式の違いが原因。
- OS切り離し：AllocMem()/OpenFile()/Read()/CloseFile()/FreeMem() 等のAmigaDOS/EXEC呼び出しをやめることでRAMを確保し高速化を図る。
- RNC Toolkit活用：Rob Northenのツール群（CopyLock/ProPack/SectorLoad/MakeBoot）を手掛かりに、特にSectorLoad（ディスクセクタ単位の入出力）を解析・改良。ネット上の「NOMAD LOADER」を逆解析し、不足部分を補完。
- 専用ファイルシステムとPROTOWRITE：ディスク上に連続セクタ配置を保証する独自ファイルマップ（Bootblock直後のセクタ）を作り、INCBINから順次書き込むツールPROTOWRITEを実装。Codetapperから正式なDiskIOルーチンを入手して完成させ、書き込みスピードのバグはrossパッチで解決。
- ブート戦略：MakeBootの制約を避け、$80等の低アドレスへ生バイナリをロードする自作ブートブロックを作成。DiskMonToolsでセクタやブート内容を検証。
- メモリ最適化：BSSやds領域を廃してオフセット定数で配置予測。イントロを外部バイナリ化して常駐させず12KBを削減。ボスやプレイヤーのスプライトテーブルを必要時に読み込む方式にして総メモリを2MB以下に収めた。
- ハード制約：Amigaのブリッタが持たないリアルタイムマスクやフリップ機能の不足で、反転・マスク済みスプライトを多重保持する必要があり、チップメモリの大部分を占有している点は設計上の宿命。
- 開発道具とデバッグ：WInUAEデバッガやDiskMonToolsを活用し、低レイヤの不具合を潰していった。

## 実践ポイント
- レトロ環境での最適化は「OS依存の排除」と「I/Oルーチンの再設計」で大きく進む。まずファイルI/Oのどの部分がRAMやCPUを食っているか特定する。
- 既存ツール（ProPackやSectorLoad等）を調べ、ソース／ドキュメントが無ければ逆解析＋コミュニティ（例：Codetapper）に頼る手は有効。
- メモリ節約は「常駐データ→オンデマンド読み込み」に置き換える方針が強力。スプライトやボスデータは外部バイナリ化を検討する。
- ブートローダーやファイル配置までコントロールできれば、限られたチップメモリで大きなゲームを動かせる。

興味があれば、具体的なSectorLoadの解析ポイントやPROTOWRITEの設計要点を別稿でまとめますか？
