---
  layout: post
  title: "Darktable Styles mimicing Fujifilm's Film Simulations - Darktableで再現するFujifilmのフィルムシミュレーション"
  date: 2026-01-02T22:05:25.547Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://jssfr.de/dtsolve/2026-01-02-darktable-styles-fujifilm.html"
  source_title: "Darktable Styles mimicing Fujifilm's Film Simulations — jssfr.de"
  source_id: 1505630775
  excerpt: "darktableスタイルでフジの撮って出し風をRAWで忠実再現する導入手順"
  image: "https://jssfr.de/static/dtsolve/img/2026-01-02-og.jpg"
---

# Darktable Styles mimicing Fujifilm's Film Simulations - Darktableで再現するFujifilmのフィルムシミュレーション
Fujifilmの「出力JPEGっぽさ」をRAWで再現する—darktable用スタイル集で撮って出しの魅力を取り戻す

## 要約
作者は数値ソルバーでdarktableのパラメータを調整し、Fujifilmのフィルムシミュレーションに極めて近いdtstyle群を作成した。LUTではなく既存のdarktableモジュールを組み合わせることで、可変性と再配布性を確保している。

## この記事を読むべき理由
FujifilmのXシリーズは日本でも非常に人気で、出力JPEGの色味やトーンは多くのユーザーに支持されている。だがRAW現像で同じ見た目を得るのは容易でない。本記事は、そのギャップを埋める現実的なアプローチ（darktableスタイル）と、既存ワークフローにどう組み込むかを技術的に解説する。

## 詳細解説
- 問題意識：Fujifilmのカメラは「Film Simulations」をリアルタイムでプレビューし、撮影時点で多くの現像作業を済ませられる。一方、darktableにRAWを読み込むと初期表示が「平坦」で、OOC（Out‑Of‑Camera）JPEGとギャップが出る。
- 解法：著者はdtsolveという仕組みで、OOC JPEGを参照画像にして数値ソルバーがdarktableの既存モジュール（色補正、トーンマッピング、モノクロモジュール等）のパラメータを最適化する手法を採った。重要なのは「Fujifilmのコードをリバースエンジニアリングしていない」点。
- LUTとの比較：従来のアプローチはLUTを多用してきたが、LUTはトーンマッピングを固定してしまい微調整しにくい・配布が面倒という欠点がある。本プロジェクトはLUTを使わず、filmic rgb / sigmoid / AgXなどのモジュールと組み合わせることで「可変性」を保つ。
- 対象スタイル：Velvia、Provia、Classic Chrome、Acros、Eterna、Pro Neg. など主要フィルムシミュレーションをカバー。ただし一部（例：Nostalgic Neg）は現状で完全再現が難しい。
- ワークフローの実用性：比較時はホワイトバランスを「as shot in camera」、レンズ補正を有効、露出モジュールを+0.7EV等の前提で検証している。再現度はサイドバイサイドで概ね十分に近いレベル。

## 実践ポイント
- 入手：まずdtsolveの概要ページからdtstyleをダウンロードしてdarktableに読み込む。
- 初期設定：インポート後は色補正を「as shot in camera」にし、レンズ補正を有効にする。比較基準として著者は露出を+0.7EVにしているので必要なら参考に。
- 微調整：LUTベースよりもモジュール単位で調整できるため、filmic rgb / AgX / sigmoidなどでハイライト・シャドウの追い込みが行いやすい。
- 自動適用を待つ：将来的にはEXIFに基づき自動で該当スタイルを適用する仕組み（Lua拡張等）が想定されている。現状は手動インポート→適用が基本。
- カスタム化：dtsolveはLinux向けだが、同手法で自分の好みの参照画像（OOC JPEGや任意の参照）を使って独自のdtstyleを作ることが可能。

日本の写真文化ではフィルム的な色味が根強く好まれている。darktableで「撮って出しっぽい」RAWワークフローを構築すれば、現像の自由度を損なわずにFujifilmらしい仕上がりを得られる実用的な選択肢になるだろう。
