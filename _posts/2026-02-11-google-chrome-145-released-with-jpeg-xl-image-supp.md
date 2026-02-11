---
layout: post
title: "Google Chrome 145 Released With JPEG-XL Image Support - Google Chrome 145 が JPEG-XL 画像をサポート"
date: 2026-02-11T12:12:46.581Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.phoronix.com/news/Chrome-145-Released"
source_title: "Google Chrome 145 Released With JPEG-XL Image Support - Phoronix"
source_id: 864995643
excerpt: "Chrome 145でRust製デコーダ採用のJPEG-XLが再導入、表示品質と帯域節約を今すぐ検証"
image: "https://www.phoronix.net/image.php?id=2026&image=chrome_145"
---

# Google Chrome 145 Released With JPEG-XL Image Support - Google Chrome 145 が JPEG-XL 画像をサポート
驚きの再導入：Chrome 145で「JPEG-XL」が戻ってきた理由と今すぐ試したいポイント

## 要約
Chrome 145 が正式リリースされ、廃止されていた JPEG-XL デコーディングが再導入されました。実装は Rust ベースの jxl-rs を採用し、安全性と安定性を狙っています。

## この記事を読むべき理由
画像中心のWebが当たり前の日本市場では、より高圧縮で高画質なフォーマットが通信コストや表示速度に直結します。開発者・運用担当は今後の画像配信戦略や互換性対応を早めに検討する価値があります。

## 詳細解説
- JPEG-XL 復帰: 2022年に一度削除された JPEG-XL デコードが Blink エンジンへ再導入されました。これは Chrome/Chromium 系ブラウザでのネイティブ対応の再開を意味します。  
- 実装の注目点: Google は C++ の libjxl ではなく、Rust 製の jxl-rs デコーダを用いています。Rust による実装はメモリ安全性を高め、バッファオーバーフロー等の脆弱性リスクを低減します。  
- 有効化方法: 現状は機能フラグ（enable-jxl-image-format）で制御されています（chrome://flags から切り替え）。将来的にデフォルト有効化される可能性があります。  
- 追加の改善点: text-justify の CSS サポート、multicol のカラム折り返し、Device-bound session credentials、IndexedDB の SQLite バックエンド、デフォルトでのユーザーエージェント短縮、Upsert などの強化も含まれます。これらはレンダリング制御やストレージ挙動、セキュリティ・プライバシーに影響します。

## 実践ポイント
- テスト環境で有効化: chrome://flags で enable-jxl-image-format をオンにして自分のサイトを表示確認する。特にレスポンシブ画像や高解像度アセットをチェック。  
- 変換と配信戦略を検討: JPEG/WEBP と比較し、圧縮率・品質・エンコード速度を測定して CDN・ストレージコスト削減を試算する。  
- フォールバック対応: まだ全ブラウザでデフォルト有効化されていないため、既存フォーマット（WebP/AVIF/JPEG）とのフォールバック実装を維持する。  
- セキュリティ恩恵を評価: Rust 実装による安定性向上は特に大規模サービスや組み込み端末向けでメリットが大きい。社内QAでメモリリークやクラッシュの再現テストを行う。  
- 新CSS・IndexedDB機能も確認: text-justify や multicol の挙動、IndexedDB の SQLite バックエンド切替がアプリ挙動に与える影響を合わせて検証する。

以上を踏まえ、まずは開発環境で JPEG-XL を有効化して互換性・表示品質・圧縮効果を確認することをおすすめします。
