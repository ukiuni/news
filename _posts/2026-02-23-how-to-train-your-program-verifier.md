---
layout: post
title: "How to train your program verifier - プログラム検証器の鍛え方"
date: 2026-02-23T04:17:26.285Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://risemsr.github.io/blog/2026-02-16-halleyyoung-a3/"
source_title: "How to train your program verifier | RiSE MSR"
source_id: 47066446
excerpt: "AIと形式手法で自動学習するa3‑pythonが、DSEで再現可能な実バグだけを精度高く検出する"
---

# How to train your program verifier - プログラム検証器の鍛え方
魅力的なタイトル: AIが「自動で作り、磨く」プログラム検証器――Python実装 a3‑python が現場のバグをどう潰すか

## 要約
AIと形式手法を組み合わせ、自動生成・反復で生まれた a3‑python が多数の実運用Pythonコードでバグ候補を絞り込み、実入力で再現可能な本当のバグだけを報告する仕組みを示す。

## この記事を読むべき理由
Pythonは日本でも幅広く使われるが検証ツールは苦手とする領域。a3‑python はLLMとZ3等の形式手法を組み合わせ、実用的に「本当に問題になる箇所」を発見できるため、ソフトウェア品質向上やCI導入のヒントになる。

## 詳細解説
- アプローチ概観  
  - 生成→テスト→修正→理論修正をAI主導で回す「エージェント的反復」により検証器を自動で構築。主要構成はシンボリック解析、concolic（実値混合）実行、そして「障壁証明（barrier certificates）」等の定理的証明器の組合せ。
- 障壁（バリア）証明の直感  
  - 初期状態は安全側、危険状態は禁域側として、状態変化が境界を越えないことを示す関数 $B(s)$ を合成する。条件は例えば $B(s_{\mathrm{Init}})\ge 0,\; B(s_{\mathrm{Bad}})<0$、そして非負状態から遷移しても非負が保たれること。
  - これに基づき、Hilbert の Positivstellensatz、sums-of-squares、半定値計画法などの代数的手法を活用。
- 「キッチンシンク」パイプライン  
  - 実用性重視で多数の手法を順に試す：Assume‑Guarantee、PostCondition、RefinementType、InductiveInvariant、ControlFlow、Dataflow、Disjunctive、ValidatedParams、最後にDSE（有向シンボリック実行）で具体入力を生成。DSE が具体的入力を返せば「再現可能な本当のバグ」と判定。
- ライブラリ挙動の扱い（オラクル化）  
  - 実行で扱う外部呼び出しは実値で動かす（concrete execution）か、ライブラリ特性を公理化してZ3で扱う（axiomatization）。PyTorch のような数値ライブラリはガードや eps などの性質を公理として組み込み、誤報を減らす。
- 実績（抜粋）  
  - requests の主要ファイル183関数で潜在バグ183件 → a3 が179件を「形式的に安全」と証明、残り4件はDSEで実入力を生成して実バグと判定。  
  - PyTorch Adafactor の実装は21件すべてを安全と証明。一方、Guardの欠けた LLM2CLIP の実装では55潜在→5件がDSE確認の本当のバグ（DIV_ZERO, BOUNDS 等）。

## 実践ポイント
- 試す（ローカル）  
  - bash
  ```bash
  pip install a3-python
  a3 scan path/to/your_project/
  ```
- CI導入案：PR時に a3 を回して「DSE再現可能なバグ」をブロック、形式的に安全と証明された候補はノイズ低減に活用。  
- 自分のコードベース最適化：内部ライブラリの挙動（ガード・前提）を明示して公理化すると誤報が減る。  
- 候補管理：まずはDSE確認済みを優先修正。形式証明済みはリファクタ時の安心材料に。  
- 学び：LLMは理論→実装の発想を加速するが、人のレビューで公理化やテスト設計を補完することが重要。

短く言えば、a3‑python は「AIで理論を作り、形式手法と実行検証を組み合わせて現実のPythonコードで効く検査器を自動で育てる」ツールチェインの実例で、日本のプロダクト開発でも即応用可能な考え方を示している。
