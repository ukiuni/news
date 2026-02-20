---
layout: post
title: "Wikipedia bans Archive.today after site executed DDoS and altered web captures - WikipediaがArchive.todayをブラックリスト化、DDoS実行とアーカイブ改ざんの疑いでリンク削除へ"
date: 2026-02-20T20:32:03.845Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://arstechnica.com/tech-policy/2026/02/wikipedia-bans-archive-today-after-site-executed-ddos-and-altered-web-captures/"
source_title: "Wikipedia blacklists Archive.today, starts removing 695,000 archive links - Ars Technica"
source_id: 47092006
excerpt: "Archive.todayがDDoSと保存改ざん疑惑、Wikipediaが約69万リンクを削除"
image: "https://cdn.arstechnica.net/wp-content/uploads/2026/02/wikipedia-1152x648-1771611351.jpg"
---

# Wikipedia bans Archive.today after site executed DDoS and altered web captures - WikipediaがArchive.todayをブラックリスト化、DDoS実行とアーカイブ改ざんの疑いでリンク削除へ
クリックせずにはいられない：信頼していた「ウェブアーカイブ」が攻撃に加担し、保存したページを書き換えた――あなたの情報ソースは本当に安全か？

## 要約
英語版WikipediaがArchive.todayを即時非推奨・スパムブラックリスト化し、約69万5千件のリンク削除を進める決定をした。理由はArchive.todayがあるブログへのDDoSに利用され、さらに保存したスナップショットを書き換えた疑いが出たため。

## この記事を読むべき理由
ウェブアーカイブは検証可能な情報源として広く使われるが、今回の件は「アーカイブ自体が改ざんや攻撃に使われるリスク」を露呈した。日本のジャーナリスト、研究者、エンジニア、法務担当者も引用の信頼性とセキュリティ対策を見直す必要があります。

## 詳細解説
- 発端：Archive.todayのCAPTCHAページに埋め込まれた悪性コードが、特定ブロガーを狙ったDDoSトラフィックの送出に使われたと報告された。  
- 改ざん疑惑：Wikipedia編集者が検証したところ、Archive.todayの保存スナップショットに標的の名前が差し替えられている例が確認され、アーカイブの「信頼性」が失われたと判断された。  
- スコープ：英語版Wikipedia上のArchive.todayリンクは約695,000件、約40万ページに散在。編集コミュニティは代替手段への置換を推進。  
- 対応：archive.today系ドメイン（archive.today, archive.is, archive.ph, archive.fo, archive.li, archive.md, archive.vn）を削除・置換対象に指定。代替としてInternet Archive（Archive.org）、Ghostarchive、Megalodonなどを推奨。  
- 余波：FBIがArchive.todayの運営者特定を調査中。Wikimedia側も独自のアーカイブサービス設立を検討する可能性を示唆。

## 実践ポイント
- Wikipediaや自分の資料でarchive.todayリンクを見つけたら、まず原典が同一ならその原典リンクに差し替える。  
- アーカイブを使う場合は、信頼できるサービス（Internet Archiveなど）を優先し、複数ソースで保存・比較する。  
- 重要な引用はローカル保存（PDFやWebrecorder）とハッシュ（ファイルのチェックサム）で整合性を確保する。  
- 自社/プロジェクトで外部アーカイブに依存するなら、内部アーカイブ戦略を検討（定期スナップショット、アクセス監査、CSPやサンドボックスで外部スクリプトを無効化）。  
- ジャーナリストや研究者は、アーカイブのメタデータ（保存日時、保存元URL、差分）を記録して改ざん検出に備える。

以上を踏まえ、参照元の“保存先”そのものの信頼性を日常的にチェックする習慣を持つことが今後ますます重要になります。
