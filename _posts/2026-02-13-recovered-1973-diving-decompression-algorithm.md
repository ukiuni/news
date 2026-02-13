---
layout: post
title: "Recovered 1973 diving decompression algorithm - 1973年の潜水減圧アルゴリズム復元"
date: 2026-02-13T11:36:16.903Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/edelprino/DCIEM?tab=readme-ov-file"
source_title: "GitHub - edelprino/DCIEM"
source_id: 442776256
excerpt: "1973年のFortran原典を実行再現し、古典減圧モデルと現代手法の違いを検証できるリポジトリ"
image: "https://opengraph.githubassets.com/80edb58d8b81df47bd7176b1801594bfb1b239340b77c7af75a29c8004273a43/edelprino/DCIEM"
---

# Recovered 1973 diving decompression algorithm - 1973年の潜水減圧アルゴリズム復元
1973年のFortran原本を忠実に再現した“動く歴史資料”を触って学ぶ — 潜水減圧理論の古典実装をローカルで再現し、現代アルゴリズムと比較する入門ガイド

## 要約
1973年の報告書 "Digital Computation of Decompression Profiles"（Nishi & Kuehn）に基づくDCIEM減圧モデルをFortran IVで忠実に写したリポジトリ。原典の入力形式と出力例を残し、歴史的・研究目的で実行できるようになっている。

## この記事を読むべき理由
減圧理論の「原点」を動かして確認できる珍しいアーカイブ実装。日本でもダイビング研究、教育、古い科学ソフトの再現・検証、Fortran学習素材として実用性が高い。現代アルゴリズムとの違いを理解することで、安全設計や研究の基礎理解が深まる。

## 詳細解説
- 何が入っているか：src/main.f にあるFortranソースが1973年文献のコアロジックを転写している。dives/ 配下に複数のダイブ入力ファイルと、報告書から取り出した期待出力例が含まれる。run スクリプトは元のデッキ形式入力を模した実行インターフェースを提供する（例: ./run "Impulse Dive - 200ft 30m"）。
- 技術的ポイント（初心者向け要約）：
  - 減圧モデルは「組織コンパートメント」のガス取り込み・放出を数値的に計算し、体内の不溶性ガス分圧が安全限界（M-value等）を超えないように減圧停止を設計する古典的手法に基づく。
  - 実装はFortran IVのスタイル（デッキ入力、手続き的計算）で書かれており、現代のC/Python実装とは入出力や数値処理の扱いが異なる点が学べる。
  - リポジトリにはDockerfileやMakefileもあり、環境差を抑えて再現実行しやすい構成になっている。
- 注意：リポジトリ自体が「歴史的・研究用の再現」であり、実運用やダイブ計画には使えない旨の明確な安全警告が付されている。

## 実践ポイント
- 試す手順（短縮）：
  1. リポジトリをクローン
  2. gfortran 等でビルドするか Docker を使う（Dockerfileあり）
  3. ./run "例のダイブ名" で付属の dives/ 入力を実行し、期待出力と比較
- 学びどころ：
  - 古典モデルの数値アルゴリズムを追い、現代のBühlmannやRGBM等との挙動差を比較することで、なぜ現代アルゴリズムが改良されたかを理解できる。
  - Fortranコードを読むことで、科学計算ソフトの歴史や再現性の重要性を体感できる。
- 絶対に守ること：このコードは教育・研究用の歴史的再現であり、実際の潜水計画や生命維持の判断には使用しないでください。
