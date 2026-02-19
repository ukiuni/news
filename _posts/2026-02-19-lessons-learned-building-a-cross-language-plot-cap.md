---
layout: post
title: "Lessons learned building a cross-language plot capture engine in R & Python - R と Python におけるクロス言語プロットキャプチャエンジン構築での教訓"
date: 2026-02-19T17:18:44.986Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://quickanalysis.substack.com/p/capturing-plots-in-r-and-python-a"
source_title: "Capturing Plots in R and Python: A Tale of Two Architectures"
source_id: 438955531
excerpt: "Pythonは表示パイプ差替えで一括捕捉、Rは明示publishが現実的な理由を実例で解説"
image: "https://substackcdn.com/image/fetch/$s_!_BI1!,w_1200,h_675,c_fill,f_jpg,q_auto:good,fl_progressive:steep,g_auto/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb3f5689c-6014-49c1-918d-f1d04c2f1af9_1892x1086.png"
---

# Lessons learned building a cross-language plot capture engine in R & Python - R と Python におけるクロス言語プロットキャプチャエンジン構築での教訓
「ノートブックの“表示”を丸ごと奪って自動公開する仕組み」は、言語ごとの設計差でこうも変わる

## 要約
GoFigr が Jupyter/Python と R で同じ「プロットを自動検知して公開する」機能を実装した際、Python 側は中央集中の表示パイプ（DisplayPublisher）を差し替えるだけで広範囲を捕捉できたが、R 側はグラフィックスデバイスと命令型描画の設計により自動捕捉が難しく、明示的 publish 呼び出しが現実的で安定する──という話。

## この記事を読むべき理由
- Jupyter／RStudio で可視化ワークフローを作る日本のデータエンジニア／研究者／エンジニアが、なぜ言語ごとに自動化戦略を変える必要があるかを理解できる。
- ノートブック拡張や可視化公開ツールを作るときの実装トレードオフ（簡潔さ vs 再現性）が学べる。

## 詳細解説
- Python（Jupyter）の強み
  - IPython の DisplayPublisher が単一の「出力 choke point」になっている。display(obj) やセルの自動表示が最終的に display_pub.publish() を通るため、ここを薄いラッパーで置き換えるだけで matplotlib / plotly /plotnine などあらゆる出力を捕捉できる。
  - 実装例（概念）：  
    ```python
    class GfDisplayPublisher:
        def __init__(self, pub, display_trap=None): ...
        def publish(self, data, *args, **kwargs):
            # trap → 必要なら元 publish を呼ぶ
    shell.display_pub = GfDisplayPublisher(native_pub, display_trap=...)
    ```
  - MIME 辞書を受け取り、スタックトレース走査で実際の Figure オブジェクト（matplotlib.figure.Figure や plotly.graph_objs.Figure）を取り出す。ライブラリ固有フック不要で新ライブラリ対応も比較的容易。

- R の構造的障害
  - R は「グラフィックスデバイス」（C レベルの DevDesc）へ直接描画命令（line, rect, text…）を投げる設計。すべてが単一関数を経由するわけではないため、Python のような一元的フックが存在しない。
  - プロットの二種類：
    - オブジェクト指向系（ggplot2, lattice）：print() で描画されるので print をオーバーライドして捕捉できるケースあり。
    - 命令型（base graphics）：plot() 等が即時描画するため「オブジェクト」が存在せず、そのままでは構造化して再レンダリングできない。
  - GoFigr の R 戦略
    - 推奨：明示的にパイプで gofigR::publish() を呼ぶ（安定かつ R ユーザーに自然）。例：
      ```r
      # ggplot
      ggplot(mtcars, aes(wt, mpg)) + geom_point() %>% gofigR::publish()
      # base graphics
      gofigR::publish(~ { hist(rnorm(1000)); }, figure_name = "Histogram")
      ```
    - 実験的自動化：.GlobalEnv に print を差し替えて print() 経由で来るオブジェクトを捕捉するが、as.ggplot に変換可能なケースに限られる（ggplotify を利用）。
  - 他案の問題点
    - カスタムグラフィックスデバイスは低レベルで「図の起点・意味・データ」を知らないため不十分かつ高コスト。
    - knitr フックを使うと確実に全種類のプロットを捕捉できるが、ファイルベース（画像）になり再レンダリングや実行時環境の紐付けができず機能制限が大きい。

- 本質的結論
  - 言語・エコシステムの設計（集中表示層 vs. デバイス直接描画）が自動化の可否と実装コストを決定する。実用的には「Python は自動で強力、R は明示呼び出しが現実的」という棲み分けが妥当。

## 実践ポイント
- Jupyter/Python ユーザー
  - DisplayPublisher をラップする方式で比較的簡単に全可視化ライブラリを捕捉可能。ノートブック拡張を作るならここを狙う。
- R ユーザー
  - まずは明示的に gofigR::publish() を使う運用を推奨（再現性・メタデータ添付が容易）。
  - 自動化を試すなら print の差し替えは有効だが、ggplotify で変換できるケースに限定されることを理解する。
- R Markdown / Quarto
  - knitr フックは全図を捕捉できるが「画像のみ」でセッション情報が取れないため、レポート生成のパイプラインと目的を見て使い分ける。
- ライブラリ作者へ
  - 可能なら「再レンダリング可能なプロットオブジェクト」を公開すると、外部ツールからの捕捉・公開が容易になる。

短く言えば、技術的には「同じ目的」でも言語設計により現実的な解が変わる。ツールやワークフローを作る側はその違いを受け入れて公開戦略を選ぶのが近道。
