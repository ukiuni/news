---
layout: post
title: "ISO PDF spec is getting Brotli – ~20 % smaller documents with no quality loss - ISO PDF仕様がBrotliに対応へ：品質を落とさず約20%小さく"
date: 2026-01-22T14:00:26.379Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://pdfa.org/want-to-make-your-pdfs-20-smaller-for-free/"
source_title: "Want to make your PDFs 20% smaller for free? &#8211; PDF Association"
source_id: 46717507
excerpt: "ISO版PDFがBrotli採用で品質維持のまま約20%縮小"
---

# ISO PDF spec is getting Brotli – ~20 % smaller documents with no quality loss - ISO PDF仕様がBrotliに対応へ：品質を落とさず約20%小さく

魅力的なタイトル: PDFが“軽く”なる時代到来 — ISO標準にBrotliが入り、配布コストと読み込みが劇的に改善

## 要約
PDFの標準（ISO 32000）にWebで実績のある圧縮アルゴリズム「Brotli」が導入される予定で、ファイルサイズが15〜25%小さくなり得る。読み書きのための実装は既にiTextなどで進められている。

## この記事を読むべき理由
PDFは政府・企業の公的書類や長期保存に多用され、日本でも容量・配布効率やクラウド費用の改善が直接的に利益になります。互換性の壁を乗り越えてISO準拠で導入されるため、現場で使いやすくなる可能性が高いからです。

## 詳細解説
- なぜ変化が難しかったか：PDFは後方互換性が最優先で、1996年から主流のDeflate（Flate）を使い続けてきた。新圧縮の導入は旧リーダーで読めなくなるリスクを伴うため、ISOの合意形成とロイヤリティフリー要件がハードルになっていた。
- なぜBrotliか：Googleが2015年に開発しWebで広く使われるBrotliは圧縮効率が高く（実運用で95%のトラフィックに採用されている基盤）、非劣化で15–25%のサイズ削減が期待できる。
- 技術的な実装要点：
  - デコード（読み取り）は比較的容易で、PDFのストリームに新しいフィルタ（/BrotliDecode）を追加するだけで既存のパイプラインで処理できる。iTextではGoogleのJava参照実装を埋め込んで動作させている。
  - エンコード（書き出し）は複雑。iTextは従来Flate固定だったため、圧縮戦略を抽象化するIStreamCompressionStrategyのような層を導入して差し替え可能にした。エンコーダーは公式がC++実装のみのため、ネイティブライブラリの配布問題を回避するために別モジュールで扱う設計を採用している。
  - セキュリティと安定性対策として、メモリ限界を守るデコーダやネイティブ依存を分離するアーキテクチャが重要視されている。

## 実践ポイント
- すぐに試す：iTextなどBrotli対応を謳うライブラリの最新版を確認し、テスト環境で既存PDFの出力比較（サイズ・表示）を行う。期待値は約15–25%削減。
- 互換性確認：受信側（社内ツールや顧客）が古いPDFライブラリを使っていないかをチェック。ISO採用後でも、古いリーダー対策として生成時にFlateでの出力を選べる仕組みを残す。
- 運用面：アーカイブ用途では長期可読性が重要なため、移行計画（いつからBrotliに切り替えるか）と外部配布ポリシーを定める。
- セキュリティ：デコード時のメモリ爆発（decompression bomb）対策がある実装を選ぶこと。
- 効果の可視化：CIやビルドパイプラインでPDF生成後のバイナリサイズを自動比較するテストを追加すると導入効果が分かりやすい。

短く言えば、Brotli対応は「同等品質でファイルを小さくする」現実的な手段であり、ISO準拠での採用により企業・公共分野での普及が期待されます。まずはライブラリの対応状況を確認し、テスト導入から始めてください。
