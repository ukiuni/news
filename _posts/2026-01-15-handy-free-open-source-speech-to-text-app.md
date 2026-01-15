---
layout: post
title: "Handy – free open source speech-to-text app - Handy（無料オープンソースの音声→テキストアプリ）"
date: 2026-01-15T07:14:53.079Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/cjpais/Handy"
source_title: "GitHub - cjpais/Handy: A free, open source, and extensible speech-to-text application that works completely offline."
source_id: 46628397
excerpt: "クラウドに送らない高精度オフライン音声入力アプリHandy、会議や機密作業に最適"
image: "https://repository-images.githubusercontent.com/931888694/1519efb0-ade3-433a-913a-ee7ddd8519a6"
---

# Handy – free open source speech-to-text app - Handy（無料オープンソースの音声→テキストアプリ）
もうクラウドに声を送らない：オフラインで動くオープンソース音声入力ツール「Handy」を今すぐ試す理由

## 要約
HandyはTauri（Rust + React/TypeScript）で作られたクロスプラットフォームのオフライン音声認識アプリ。ショートカットで録音→自動認識→任意のテキスト欄へ貼り付けまで完結し、音声をクラウドへ送らない点が最大の特徴です。

## この記事を読むべき理由
- 日本の企業や個人でプライバシー重視の音声入力を求める場面（会議録、医療・法律分野のメモ、機密業務）で即戦力になり得るため。  
- ローカルで動くためネットワーク制約やデータ保護規定に強く、社内検証やオフライン環境でも使える点が魅力です。

## 詳細解説
- アーキテクチャ：フロントエンドはReact＋TypeScript、バックエンドはRust（Tauri）でシステム統合・音声入出力・モデル推論を担います。  
- 音声処理の流れ：ショートカットで録音→SileroのVADで無音除去→選択した音声モデル（Whisper系またはParakeet）で推論→結果をアクティブなテキスト欄へ貼り付け。
- モデル選択：
  - Whisper（Small/Medium/Turbo/Large）…高品質だがGPUがあると恩恵大。GPUアクセラレーション可。  
  - Parakeet V3 …CPU最適化されたモデルで自動言語検出付き。日本語を含む多言語での運用に向く（GPU不要で軽量に動く）。
- プラットフォーム：macOS（Intel/Apple Silicon）、Windows x64、Linux（Wayland/X11）に対応。ただしWayland周りは追加設定や外部ツールが必要なことが多いです。
- Linux固有の注意点：Waylandでテキスト入力を自動貼り付けするには wtype や dotool、X11なら xdotool が推奨。Overlay表示がフォーカスを奪う問題や、環境変数での回避策（例：WEBKIT_DISABLE_DMABUF_RENDERER=1）があります。
- デバッグ/拡張：開発者向けのデバッグモードや、モデルを手動で置く手順、SIGUSR2で録音トグルなど拡張性・運用性に配慮されています。
- ライセンス：MIT。企業でのカスタマイズや二次制作がしやすい点も魅力です。

## 実践ポイント
1. まずはリリースをダウンロードして起動（マイク／アクセシビリティ許可を許可）。  
2. ノートPCで手軽に動かすなら Parakeet V3 を選ぶ（CPUで動く・自動言語検出）。GPUがある環境で高品質を狙うなら Whisper 系を検討。  
3. Linuxで使う場合（特にWayland）：
   - X11なら xdotool を入れる：
```bash
# bash
sudo apt install xdotool
```
   - Waylandなら wtype（推奨）または dotool：
```bash
# bash
sudo apt install wtype
# または
sudo apt install dotool
# dotool を使う場合、input グループに追加が必要
sudo usermod -aG input $USER
```
4. ネットワーク制限がある場合はモデルを手動配置：
   - アプリデータディレクトリ内に models/ フォルダを作成して、ダウンロードした .bin や展開したParakeetディレクトリを置く。再起動後に「Downloaded」と表示されます。
```bash
# macOS/Linux の例（パスは環境により異なる）
mkdir -p ~/.config/com.pais.handy/models
```
5. トラブルシュート：
   - Whisperモデルが特定環境でクラッシュするケースあり。開発者向けログを提出できると解決が早まります。  
   - Waylandでホットキーをウィンドウマネージャ側で管理する場合、HandyにSIGUSR2を送ることで録音を切り替え可能（例：swayのbindsymで利用）。
6. 日本の実務での活用例：
   - 会議議事録のラフメモ、取材やインタビューの下書き、アクセシビリティ支援（障害を持つ人の入力補助）など。オンプレ要件がある企業でも導入検討しやすい。
7. 貢献・カスタマイズ：
   - MITライセンスなので社内用途でフォークして機能追加や日本語固有の後処理（補正・句読点ルール、敬語変換）を入れるのも現実的です。IssueやPRでコミュニティに参加しましょう。

Handyは「完璧」な製品ではなく「自分で伸ばせる」土台です。プライバシー重視で手軽に音声入力を試したい日本の開発者やチームには非常に有用な選択肢になります。興味があればまずはリリースを落として、Parakeet V3でローカル動作を確かめてみてください。
