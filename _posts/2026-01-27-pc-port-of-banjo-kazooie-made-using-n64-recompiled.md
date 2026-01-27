---
layout: post
title: "PC Port of Banjo-Kazooie made using N64: Recompiled - Banjo-Kazooie の PC 移植（N64: Recompiled 使用）"
date: 2026-01-27T17:34:36.954Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/BanjoRecomp/BanjoRecomp"
source_title: "GitHub - BanjoRecomp/BanjoRecomp: PC Port of Banjo-Kazooie made using N64: Recompiled (Windows/Linux/Mac)"
source_id: 416169756
excerpt: "静的再コンパイルで高フレーム・ワイド対応のBanjoKazooieをネイティブ移植"
image: "https://opengraph.githubassets.com/9186612e40f6ae7005ba1466f06ada13f115776cad9eae3ef87956b719850ce1/BanjoRecomp/BanjoRecomp"
---

# PC Port of Banjo-Kazooie made using N64: Recompiled - Banjo-Kazooie の PC 移植（N64: Recompiled 使用）
伝説のN64クラシックが“ネイティブ移植”で復活。高フレームレート・ワイドスクリーン・豊富なモッド対応で現代機に最適化されたBanjo-Kazooieを、静的再コンパイルという新手法で動かすプロジェクト。

## 要約
N64: Recompiled を使って Banjo-Kazooie を静的に再コンパイルしたPC向けポート。RT64レンダラーによるグラフィック強化、高フレームレート・ワイド対応、豊富なモッドサポートを特徴とする（オリジナルROMは必要）。

## この記事を読むべき理由
日本でもSteam Deckやレトロ復刻への関心が高まる中、ソース公開が無くても「実機挙動を保ったままネイティブ移植」できる技術とその実装例は、ゲーム保存・移植・モッディングに関心あるエンジニアや愛好家にとって学びが多いからです。

## 詳細解説
- 静的再コンパイルとは  
  元のN64バイナリを自動変換してターゲット環境用のネイティブ実行ファイルを生成する手法。ソースコード（デコンパイル）が無くても移植可能だが、デコンパイル結果の解析情報を補助的に利用して改善を行っている。
- 使用技術スタック  
  - N64: Recompiled：バイナリ→ネイティブ変換の基盤  
  - RT64：モダンなレンダリング（高フレームレート・ワイド対応・将来的なレイトレ検討）  
  - N64ModernRuntime / RecompFrontend：ランタイム置換・メニュー/入力管理  
  - 一部で Banjo-Kazooie Decompilation のヘッダ／関数定義を参照
- 主な機能と改善点  
  - プラグアンドプレイ：US 1.0 ROM を指定するだけで動作（外部資産は含まず）  
  - 高フレームレートでの描画整合性維持（物理やアニメ同期に影響なし）  
  - ワイド／ウルトラワイド対応、HUD調整、カットシーンの補正や柱箱化オプション  
  - 完全なオーディオ互換性（同期修正あり）  
  - モッドサポート：ドラッグ＆ドロップで導入、トグルや設定可能。Thunderstore等での配布予定  
  - デュアルアナログカメラ、低入力遅延、瞬間ロード、ノート保存のオプション切替  
  - Linux/Flatpak/Steam Deck 向けバイナリあり
- 要件と注意点  
  - GPU：Direct3D12 (SM6) / Vulkan 1.2 / Metal Argument Buffers Tier2 相当。古めのGPUは非対応の可能性あり。  
  - x86-64では SSE4.1 必須。ARM64対応ビルドもあり。  
  - リリースは GPL-3.0。プロジェクトとリリースにゲームデータは含まれない。ROMの入手は各自で法に従うこと。  
  - オーバーレイ（MSI Afterburner 等）や特定の外部フレームレート制限は不具合の原因になり得る。  
- コミュニティと開発状況  
  GitHubでスター約1.2k、DiscordでN64: Recompiledコミュニティが活発。ビルド手順は BUILDING.md、プリビルドバイナリはReleasesにあり。

## 実践ポイント
- まずは公式Releasesからプリビルド版を試す（オリジナルROMを所有していることを確認）。  
- Steam DeckではFlatpak/Linux版をデスクトップで「Add to Steam」してGaming modeで動かすのが手軽。  
- GPUドライバを最新にして、オーバーレイ類は無効化して動作確認する。  
- モッドを試すなら公式のモッドテンプレートとドキュメントを確認し、バックアップを取ってから導入する。  
- 法的に正当なROM所有を前提に利用し、配布や違法入手を助長しないこと。
