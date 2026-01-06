---
  layout: post
  title: "Interpreter – Offline screen translator for Japanese retro games - Interpreter – 日本語レトロゲーム向けオフライン画面翻訳機"
  date: 2026-01-06T09:16:18.398Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://github.com/bquenin/interpreter"
  source_title: "GitHub - bquenin/interpreter: This application can translate text captured from any application running on your computer."
  source_id: 46460930
  excerpt: "プライバシー重視でレトロゲーム画面をオフラインで即時OCR翻訳して重ね表示"
  image: "https://opengraph.githubassets.com/c85308db1405e420e0791b65eb90f85ce88f652c2c2d254b16d50a0ea1a18c80/bquenin/interpreter"
---

# Interpreter – Offline screen translator for Japanese retro games - Interpreter – 日本語レトロゲーム向けオフライン画面翻訳機

レトロゲームの日本語テキストをローカルで即時英訳、画面に重ね表示する“オフライン翻訳オーバーレイ”ツール

## 要約
画面上の任意ウィンドウをキャプチャしてOCR→ローカル翻訳→オーバーレイ表示するオープンソースアプリ。クラウド不要でプライバシーを保ちながら、レトロゲームのピクセルフォントに最適化されたOCRで高精度に翻訳できる。

## この記事を読むべき理由
日本で根強いレトロゲーム文化やエミュレータ利用者、ローカル環境を重視する開発者／検証者にとって、ネット接続なしで“遊びながら理解できる”実用性は非常に魅力的。ローカライズ作業やプレイ実況、テストにも応用できる。

## 詳細解説
- アーキテクチャ（処理フロー）  
  1. 画面キャプチャ：対象ウィンドウを指定して定期キャプチャ  
  2. OCR：MeikiOCRを使用。レトロゲームのピクセルフォントに最適化済みで、文字切り出し精度が高い  
  3. 翻訳：Sugoi V4（ローカル実行）で日本語→英語へ翻訳  
  4. 表示：バナー（下部字幕）またはinplace（原文上に重ねる）でオーバーレイ表示

- オフライン／プライバシー  
  全処理がローカルで完結。クラウドAPIや外部サーバーにテキストを送らないため、個人情報やプレイ内容を外部に出したくない場面で有利。

- 主な機能・特徴  
  - 完全オフライン（初回はモデルのダウンロードあり）  
  - MeikiOCRによるピクセルフォント最適化  
  - 2種類のオーバーレイモード（バナー / inplace）  
  - 翻訳キャッシュとファジーマッチングで同一・類似文の再翻訳を削減  
  - マルチディスプレイ対応：オーバーレイはゲームの表示先に出る

- 対応環境と注意点  
  - Windows 10 (1903+)、macOS、Linux（X11 / XWayland / Wayland）  
  - Waylandではinplaceはフルスクリーンのみ（セキュリティ制約のため）。ネイティブWaylandキャプチャはGStreamer PipeWireプラグインが必要で、インストーラが自動で試行する  
  - Linuxのグローバルホットキーは入力グループ設定が必要（インストーラが案内）  
  - 初回起動時にモデル類を約1.5GB程度ダウンロード。以降は ~/.cache/huggingface/ を利用

- パフォーマンスと調整  
  - OCRの閾値（confidenceスライダー）で「検出の厳しさ」を調整可能。低くすると誤検出が増えるが抜けが減る。  
  - 重い場合は初回ダウンロード後のキャッシュ確認、不要プロセス停止、解像度／更新頻度の調整を推奨。  
  - アップデートはインストーラを再実行するだけ。

## 実践ポイント
- インストール（macOS / Linux）
```bash
curl -LsSf https://raw.githubusercontent.com/bquenin/interpreter/main/install.sh | bash
```
- インストール（Windows PowerShell）
```powershell
powershell -c "irm https://raw.githubusercontent.com/bquenin/interpreter/main/install.ps1 | iex"
```
- 起動：interpreter-v2 を実行してGUIからウィンドウ選択、OCR閾値、オーバーレイモードを設定する。  
- OCRが弱ければ：GUIのconfidenceを下げて検出範囲を広げる（ゴミ文字増加に注意）。  
- Waylandでinplaceを使う場合：ゲームをフルスクリーンで起動、GStreamer/PipeWireプラグインを導入。  
- 実用例：エミュレータで英語字幕を出しながら攻略、配信での視聴者向け翻訳、ローカルでの簡易ローカライズ確認。  
- ディスク／帯域対策：初回モデルDLで約1.5GB必要。複数マシンで使う場合はモデルを共有キャッシュに置くと高速化。  
- トラブル時：OCR精度・翻訳遅延は設定の調整でかなり改善可能。まずは解像度・更新レート・confidenceの3点を触ってみる。

以上を踏まえ、ローカルで手軽に日本語レトロゲームを“その場で理解”したい人は試してみる価値大。興味が湧いたらリポジトリ（README）をチェックして環境に合わせて導入してみてください。
