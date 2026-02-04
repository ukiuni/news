---
layout: post
title: "Recreating Epstein PDFs from raw encoded attachments - 生データ付き添付からEpsteinのPDFを再現する"
date: 2026-02-04T20:16:28.243Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://neosmart.net/blog/recreating-epstein-pdfs-from-raw-encoded-attachments/"
source_title: "Recreating Epstein PDFs from raw encoded attachments | The NeoSmart FilesThe NeoSmart Files"
source_id: 1173625507
excerpt: "破損したbase64添付をOCRと手作業で復元し，元のEpstein PDFを再構築する実践手順"
image: "http://neosmart.net/blog/wp-content/uploads/2026/02/Scanned-1-vs-l-zoomed-in.png"
---

# Recreating Epstein PDFs from raw encoded attachments - 生データ付き添付からEpsteinのPDFを再現する
赤裸々な“ゴミOCR”から元のPDFを蘇らせる方法 — 公開資料の転写ミスが生む復元チャンス

## 要約
DoJ公開資料のスキャン／OCRで壊れたbase64添付を、画像化→OCR→手直し→デコードで復元する手順と注意点を解説します。

## この記事を読むべき理由
公開情報やリーク文書の解析は日本でも増えています。OCRやエンコーディングの失敗は「読む価値ある証拠」を埋もれさせるため、技術的に復元するスキルはフォレンジックや調査に直結します。

## 詳細解説
- 問題点：DoJのPDFは「Quoted‑Printable/ base64 の添付を印刷→スキャン→OCR」の流れで壊れている。OCRで余分な文字が混入したり、Courier Newの等幅だが判別しにくい字形（1 vs l 等）やJPEGアーティファクトで誤認が頻発する。
- 一般的な流れ：
  1. PDFをページ単位の画像に変換（pdftoppm推奨。ImageMagickは大きなファイルでリソース不足を起こしやすい）。
  2. 画像を拡大してエッジを保ったままOCRにかける（TextractやTesseract）。Tesseractは文字種を制限することで精度向上が見込めるが、完全ではない。
  3. OCR出力から証拠スタンプ（例：EFTA...）や行頭の'>'を除去し、行結合してbase64に整形。誤認文字は手作業やルールで修正（特に1とl、/ と＾など）。
  4. base64をデコードしてPDFを復元。部分的に壊れていても qpdf や base64 -i 等で解析可能な断片を取り出せることがある。
- ツールの挙動：
  - pdftoppm: ページ毎にPNG出力、安定するが遅い。
  - tesseract: --psm 6 と tessedit_char_whitelist 指定でベース64字符のみを許可すると良い。ただし行長ズレや途切れ認識が起きる。
  - AWS Textract: 多くの場合改善するが非決定論的な箇所があるため結果を目視検証する必要あり。
  - qpdf: 破損PDFの内部圧縮を解除して中身を調べるのに有用だが、入力が壊れていると失敗する。

## 実践ポイント
- PDF→画像変換（poppler）
```bash
pdftoppm -png -r 300 input.pdf out
```
- Tesseract（文字種制限、PSM6）
```bash
tesseract out-01.png out-01 --psm 6 -c tessedit_char_whitelist='>ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/='
```
- OCR出力整形→base64復元（例）
```bash
# EFTAスタンプを除き、'>' を削る。環境に応じて調整
grep -v 'EFTA' ocr-*.txt | sed 's/^>//' | tr -d '\n' | base64 -d > recovered.pdf
```
- ポイントまとめ：
  - 画像は2×程度に拡大してからOCRすると精度向上することが多い。
  - Courier New の判別ミス（1 vs l 等）は自動化だけで解決できないので、差分検査・手動検証を入れる。
  - base64が部分的に壊れていても、base64 -iやqpdfで断片解析を試し、PDF内部のストリームを探す。
  - 法的・倫理的配慮を常に忘れずに：公開資料の解析でもプライバシーや法規制に留意すること。

興味があれば、具体的なスクリプト（pdftoppm→tesseract→整形→デコード）のサンプルを用意します。どの環境（Linux/Mac/WSL）で実行したいですか？
