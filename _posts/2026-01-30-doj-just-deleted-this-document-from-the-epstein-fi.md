---
layout: post
title: "DOJ Just DELETED This Document from the Epstein Files - DOJがエプスタイン文書からこの文書を削除しました"
date: 2026-01-30T20:25:30.019Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.meidasplus.com/p/doj-just-deleted-this-document-from?fbclid=IwdGRjcAPp5E5jbGNrA-nkMGV4dG4DYWVtAjExAHNydGMGYXBwX2lkDDM1MDY4NTUzMTcyOAABHhzmcWzsmY7puDDLXY4EWKUoykdBqYIYQUabdEsoGYGR-06BZcTaz3Ym-0LQ_aem_F7QaBOr8H-rc-5hyTXHQWg"
source_title: "DOJ Just DELETED This Document from the Epstein Files. We Saved It."
source_id: 413464766
excerpt: "削除されたDOJのエプスタイン文書を保存し、改ざん疑惑の証拠を提示"
image: "https://substackcdn.com/image/fetch/$s_!6To4!,w_1200,h_675,c_fill,f_jpg,q_auto:good,fl_progressive:steep,g_auto/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff4846725-86e2-45d8-8744-c6eaec0d0a26_2244x1366.png"
---

# DOJ Just DELETED This Document from the Epstein Files - DOJがエプスタイン文書からこの文書を削除しました
消えたPDFの追跡──「削除」をどう記録し、証拠として残すか

## 要約
米司法省がエプスタイン関連の公開資料の一部を突然削除し、メディアが保存版を公開して波紋が広がった事例を扱う。公開・削除のタイムラインと、デジタル証跡を残す実務的な方法に焦点を当てる。

## この記事を読むべき理由
公的記録の公開・撤回は、民主的監視とデジタル保存の観点で重要です。日本でも行政文書や証拠の「消失」が問題となるため、技術者やジャーナリスト、関心を持つ市民にとって役立つ知識です。

## 詳細解説
- 何が起きたか：DOJが公開したエプスタイン関連ファイルのうち1件が、外部メディアのスクリーンショット拡散後にサイトから削除された。該当文書は複数の告発や人物名を含むとされ、後に同メディアがPDFを保存・配布した。数時間後にDOJ側で再掲されたが、差分や追加の墨塗り（redaction）がある可能性が指摘されている。
- 技術的観点：ウェブ上での「削除」は単にHTTPレスポンス（404/410）やメタ情報の変更として現れる。第三者がいち早くファイルを保存し、タイムスタンプやハッシュを取ることで、原本の存在・内容・改変の有無を証明できる。再掲時の比較はバイナリ差分やテキスト差分、PDFのOCR／メタデータ解析で行う。
- 法的・社会的含意：公開情報の突然の除去は透明性の問題を呼び、なぜ削除されたのか（誤掲載、未検証情報、プライバシー保護等）の説明責任が求められる。日本でも情報公開請求や公文書管理の運用改善に関わる論点と重なる。

## 実践ポイント
- 公的PDFを見つけたらまず保存し、同時にスクリーンショットを取りタイムスタンプを残す。
- ダウンロードとハッシュ化（例）
```bash
# ファイルを保存
curl -L -o saved.pdf "https://example.gov/path/to/doc.pdf"
# SHA256ハッシュを作成
sha256sum saved.pdf
```
- ウェブアーカイブへ送る（Wayback Machine / archive.today / Webrecorder）と、保存URLを記録する。
- 再掲／修正版と比較するには、PDFをテキスト化してdiffを取る（pdftotext等）か、バイナリ差分で変更箇所を確認する。
- 重要な公文書は複数の場所にバックアップを置き、公開された日時・取得したHTTPヘッダー（Date, ETag, Last-Modified）も保存する。

日本市場への関連：国や地方自治体の情報公開で同様の事例が起こり得るため、IT担当者や調査報道に携わる人は、単に「見た」ではなく「保存・証明する」ワークフローを持つことが重要です。
