---
layout: post
title: "Fix Your Robots.txt or Your Site Disappears from Google - robots.txt を直せ、さもなくばサイトがGoogleから消える"
date: 2026-01-19T20:02:50.277Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.alanwsmith.com/en/37/wa/jz/s1/"
source_title: "Fix Your robots.txt or Your Site Disappears from Google"
source_id: 46681454
excerpt: "robots.txtが不達だとGoogleにサイトが消えるため、今すぐ存在と200応答を確認せよ"
image: "https://www.alanwsmith.com/neo-files/theme-files/og-images/main-og-image.jpg"
---

# Fix Your Robots.txt or Your Site Disappears from Google - robots.txt を直せ、さもなくばサイトがGoogleから消える
robots.txtを放置すると検索トラフィックが激減するかもしれない — 今すぐ確認して守るべき簡単手順

## 要約
Googleの公式サポート動画によれば、Googlebotはまず robots.txt を探し、これにアクセスできないとクロールを停止してサイトが検索結果から見えなくなる可能性がある。対策はルートに正しいrobots.txtを配置して公開状態を保つこと。

## この記事を読むべき理由
日本の個人運営サイトや中小サービスでも、CDNやサーバ設定の些細な不具合でrobots.txtが届かなくなり得る。気づかないまま検索流入が消えるリスクがあるため、基本のチェックと対処法を今すぐ実行する価値がある。

## 詳細解説
- 何が起きているか：Googleのドキュメント/動画では「Googlebotはまず robots.txt を見に行き、アクセスできないとクロールを止める」と説明されている。つまりrobots.txtが「到達不能」(タイムアウト・5xx・ネットワークエラーなど)だとクロールが停止し、ページがインデックスされない可能性がある。
- 404（ファイルなし）と到達不能の違い：従来はrobots.txtが存在しない（404）でもGoogleはクロールを続けることが多かった。ただし公式の説明は「アクセスできない」ケースを問題視しており、サーバ障害やファイアウォール設定、CDNのオリジン接続失敗などが原因になりやすい。
- 技術的要点：robots.txtはサイトルート（例: https://example.com/robots.txt）に配置し、通常はMIMEタイプ text/plain で200レスポンスを返すことが重要。RFC 9309（robots排除プロトコル）では Allow: / 等の記述が認められている。Googleは自前の推奨例を公開しているため、それに従うのが最も安全。
- なぜ今重要か：大量の自動クローラーやセキュリティ設定変更、CDN利用拡大によりrobots.txtへのアクセスが思わぬ理由で阻害されるケースが増えている。検索流入に頼るサイトほど影響が大きい。

## 実践ポイント
- まず確認：ブラウザまたはcurlで robots.txt にアクセスし、HTTP 200 が返るか確認する。
```bash
# bash
curl -I https://example.com/robots.txt
```
- 最低限のファイル例（サイト全体を許可）:
```text
User-agent: *
Allow: /
```
- すぐやることリスト：
  - サイトルートに robots.txt を置く（ファイル名は小文字で固定）。
  - サーバ/CDNが robots.txt を返すよう設定（キャッシュ・オリジン接続を要確認）。
  - Google Search Console の「robots.txt テスター」や「URL検査」で検証する。
  - サーバログで Googlebot のアクセスとステータスを監視。エラーが続く場合はファイアウォールやレート制限を疑う。
  - 監視を追加：robots.txtのレスポンスを外部監視ツールで定期チェックする。

短時間の手順で防げる問題なので、まずは robots.txt の存在と200レスポンスを確認することが最優先。
