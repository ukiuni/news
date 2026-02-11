---
layout: post
title: "GLM-OCR: Accurate × Fast × Comprehensive - GLM-OCR：正確×高速×包括的"
date: 2026-02-11T15:34:04.780Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/zai-org/GLM-OCR"
source_title: "GitHub - zai-org/GLM-OCR: GLM-OCR: Accurate ×  Fast × Comprehensive"
source_id: 46924075
excerpt: "0.9Bで高精度・低レイテンシ、表や数式も読める業務向け次世代OCR"
image: "https://opengraph.githubassets.com/379afcf79ac3193fde28f61cf623287c7e12db872e5f4a589040ad133d778361/zai-org/GLM-OCR"
---

# GLM-OCR: Accurate × Fast × Comprehensive - GLM-OCR：正確×高速×包括的
魅了するタイトル: 「0.9Bでここまでできる！表・数式・契約書まで高速に読める次世代OCR『GLM‑OCR』入門」

## 要約
GLM‑OCRは小型（約0.9Bパラメータ）かつ高速なマルチモーダルOCRで、MTP損失や安定化された強化学習を導入し、レイアウト解析＋並列認識の二段階で高精度かつ現場向けに最適化された結果を出します（OmniDocBenchで94.62点、複雑な表や数式にも強い）。

## この記事を読むべき理由
日本の業務文書（請求書、申請書、契約書、技術資料、帳票など）は多様なレイアウトと手強い要素（表・数式・封印・コード片）を含みます。低レイテンシで運用可能なGLM‑OCRは、オンプレ／エッジ運用やクラウドAPI運用どちらにも適し、実務適用のメリットが大きいため知っておく価値があります。

## 詳細解説
- 基盤構成  
  - ビジュアルエンコーダ：CogViT（大規模な画像–テキスト事前学習）  
  - 軽量なクロスモーダルコネクタ（効率的なトークンダウンサンプリング）  
  - 言語デコーダ：GLM‑0.5B  
  - 全体で約0.9Bパラメータ（小さめで推論コスト低め）
- 学習と推論の工夫  
  - Multi‑Token Prediction（MTP）損失：複数トークンを同時に予測して学習効率と精度を改善  
  - 安定化されたフルタスク強化学習：汎化性能を向上  
  - 推論最適化：vLLM／SGLang／Ollama対応で低レイテンシ運用が可能
- パイプライン設計  
  - 二段階：PP‑DocLayout‑V3によるレイアウト解析 → 領域ごとの並列OCR  
  - 結果はJSON／Markdownで出力、クロップ画像などの出力も可能
- 実績と適用範囲  
  - OmniDocBench V1.5で94.62点でトップ（表・数式・情報抽出など主要ベンチで高精度）  
  - 実務に沿った頑健性：複雑表、コード入り文書、押印・印章などに強い
- 利用方法／デプロイ選択肢  
  - MaaS（ZhipuクラウドAPI）でGPU不要の即時利用（APIキーで簡単接続）  
  - 自前運用：vLLM/SGLang/Docker/Ollamaを使ったローカルデプロイでフルコントロール  
  - SDK・CLI・Python APIが用意され、1行でparseできる手軽さ
- ライセンス  
  - コード：Apache‑2.0、モデル：MIT。PP‑DocLayoutV3等の依存ライセンスに注意

## 実践ポイント
- サクッと試す：まずはMaaSモードでAPIキーを取得し、SDKを有効化して1枚の画像をparseしてみる。出力のJSON/Markdownを確認。  
- ローカルで高速化：高同時接続や機密文書処理ならvLLMやOllamaで自己ホスト。MTP設定やspeculative推論パラメータを調整すると応答が改善。  
- 日本語業務文書向けの調整：テンプレート（請求書・給与明細）ごとにポストプロセスを追加して精度を向上させる。ResultFormatterを拡張して独自フォーマットに変換。  
- 導入前チェック：使用ケースに応じて表・数式のサンプルでベンチし、必要なら領域分割（layout）を有効化する。  
- ライセンスと運用ルール確認：商用利用や再配布が絡む場合はApache‑2.0／MITの取り扱いを必ず確認する。

以上を踏まえ、まずは公式リポジトリのREADMEにある「parse」コマンドを試し、出力サンプルで現場適合性を評価することをおすすめします。
