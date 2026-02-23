---
layout: post
title: "AI-powered reverse-engineering of Rosetta 2 (for Linux VM) - Rosetta 2 の AI支援リバースエンジニアリング（Linux VM向け）"
date: 2026-02-23T22:52:01.182Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/Inokinoki/attesor"
source_title: "GitHub - Inokinoki/attesor: AI-powered reverse-engineering of Rosetta (2 for Linux)"
source_id: 47129415
excerpt: "AIで解析されたRosetta2相当のLinux向けAOT/JIT翻訳実装を公開"
image: "https://opengraph.githubassets.com/b6ce0435a3c6dc96b18335db9ec3d19d67aee37f85b40f9d308ee4a8687930a7/Inokinoki/attesor"
---

# AI-powered reverse-engineering of Rosetta 2 (for Linux VM) - Rosetta 2 の AI支援リバースエンジニアリング（Linux VM向け）
驚きの“Rosetta for Linux”分解レポート：AIで解き明かすAppleのバイナリ翻訳の中身

## 要約
AppleのRosetta 2（Intel x86_64→ARM64のバイナリ翻訳）を、AI支援で解析・再実装したオープンリポジトリの紹介。技術的な肝（AOT/JIT翻訳、命令マッピング、システムコール処理など）をC実装で再現・文書化しています。

## この記事を読むべき理由
日本でもM1/M2等のApple Silicon普及で、x86向けソフトを移行・検証する需要が高い。Linux VMや互換レイヤを理解すると、開発／デバッグ／移植の現実的な課題と対処法が学べます。

## 詳細解説
- プロジェクト概要: GitHub「attesor」はRosetta 2相当の動作を逆解析し、機能ごとにCで再実装・文書化。目的は教育・技術理解で、Appleのバイナリ自体は配布していません。AI（Claude, Qwen 3.5等）を補助に解析が進められています。
- 技術スタックと成果: 828関数を同定し、612関数をクリーンなCで実装。カテゴリは命令翻訳、SIMD/ベクトル処理、システムコール翻訳、翻訳キャッシュ管理、暗号処理、文字列最適化など多岐に渡ります。
- 翻訳アーキテクチャ:
  - AOT（Ahead-of-Time）: インストール時や起動時にx86_64→ARM64へ先回り翻訳しキャッシュ保存（~/.oahなど）。
  - JIT: 実行時に動的読み込みや自己書き換えコードをブロック単位で翻訳。
  - 命令／レジスタ問題: x86_64の16GPR→ARM64の31GPR、フラグレジスタ（x86 FLAGS → ARM NZCV）やRIPエミュレーションの扱いが中心課題。
  - SIMD変換: SSE/AVX（x86）→NEON（ARM）へのマッピングと、AVXの幅（256bit）をNEONで擬似実装する手法。
  - メモリ順序と例外処理: x86の強いメモリ順序（TSO）とARMの弱い順序の差をバリア等で補正、システムコール呼び出し規約の差分吸収。
- 実装・構成: rosetta_refactored.c / rosettad_refactored.c 等のファイル群、単一ヘッダでのインクルード版も提供。ビルドは通常のGCCで可能。
- ライセンスと注意点: MITライセンス。ただしAppleのプロプライエタリ実行ファイルを配布する目的ではなく、研究・教育用途が明記されています。

## 実践ポイント
- 試してみる（ローカルでビルド）
```bash
# bash
gcc -c rosetta_refactored.c -o rosetta_refactored.o
```
- 学び方: rosetta_refactored.c を読み、エントリポイント→AOT→JIT→syscallハンドラの流れを追うと翻訳パイプラインが理解しやすい。
- 比較研究: FEX-Emu や QEMU と比較して設計上のトレードオフ（AOTキャッシュの有無、SIMDの扱い等）を整理する。
- 日本の実務への応用: Apple Silicon 上の開発／CIで x86 向けバイナリを扱う際の互換性評価や、移植作業の方針決定に役立つ。
- 倫理・法的注意: 研究目的での解析は許されても、Appleの保護機構を回避する用途には使わないこと。

以上を踏まえ、興味があればリポジトリをクローンしてソースを追い、翻訳アルゴリズムやSIMD変換の実装例を読むことをおすすめします。
