---
layout: post
title: "Looking for collaborators: Open-source tool for writing books & scripts - コラボ募集中：書籍・脚本向けオープンソース執筆ツール"
date: 2026-01-10T13:08:22.722Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/orielhaim/storyteller"
source_title: "GitHub - orielhaim/Storyteller: The modern, open-source writing studio for authors."
source_id: 467614950
excerpt: "チームで育てる小説・脚本向けOSS執筆スタジオ、Storytellerが日本語対応や拡張を募集中"
image: "https://opengraph.githubassets.com/c01c803930e26425354885d1d18450c3a3d7cbbfeee9ee349ff8e8361f373390/orielhaim/Storyteller"
---

# Looking for collaborators: Open-source tool for writing books & scripts - コラボ募集中：書籍・脚本向けオープンソース執筆ツール
魅力的な日本語タイトル: 小説・脚本作成を“チームで”高速化するデスクトップ執筆スタジオ — Storytellerの全貌

## 要約
StorytellerはElectron＋Reactで作られたオープンソースのデスクトップ執筆アプリで、シリーズ管理やキャラクターDB、分割ビューなど小説・脚本制作に特化した機能を揃え、コラボレーターを募集中です。GPLv3で公開されており、自分で動かして拡張・貢献できます。

## この記事を読むべき理由
日本でもライトノベルや同人作品、脚本の共同制作が盛んな中、ローカルで高速に動く、カスタマイズ可能な執筆環境は需要が高いです。商用ツールに依存せず、チームやコミュニティで独自機能（日本語レイアウトや入力補助など）を追加できる点は特に魅力的です。

## 詳細解説
- コア機能  
  - プロジェクト管理：シリーズ→本→パート→章→シーンといった階層をドラッグ＆ドロップで整理。複数書籍を同一コンテキストで管理可能。  
  - エディタ：Notionライクなリッチテキスト体験、遅延の少ない操作感、集中モードを搭載。複数シーンをタブや分割ビューで同時に編集可能。  
  - ワールドビルディング：キャラクターやロケーション、アイテムの詳細シートを保持。今後タイムライン表示も予定。  
- 技術スタック（開発者向け）  
  - Electron（デスクトップ実行環境） + React（UI）  
  - 状態管理：Zustand、UI：Tailwind CSS + shadcn/ui、リッチエディタ：TipTap  
  - レイアウト管理にDockview、ローカルDBはSQLite、ORMはDrizzle ORM  
  - 開発ツール：pnpmベースで起動・ビルド、リポジトリはGPL-3.0ライセンス  
- コラボレーションと拡張性  
  - OSSとしてIssueやPRでの貢献が歓迎されている。日本語化、入力補助（縦書き対応や句読点の自動整形）、ルビ/縦組みプレビューなど日本市場特有の拡張が考えられる。  
- ライセンスの注意点  
  - GPLv3のため、派生物を配布する場合は同ライセンスで公開する必要がある。組織で商用に使う前に法務チェックを推奨。

## 実践ポイント
- ローカルで試す（開発用起動）:
```bash
# bash
git clone https://github.com/orielhaim/storyteller.git
cd storyteller
pnpm install
pnpm dev
```
- 日本語対応で貢献する案:  
  - UIの日本語翻訳（i18n）、縦書きプレビューやルビ対応、IME周りの改善を提案・実装する。  
- テスト/検証: Windows・macOS・Linuxでの日本語入力やフォント表示を確認してIssueに報告。  
- コミュニティ参加: Issueで機能提案、READMEやROADMAPを参照してRoadmapへのフィードバックやコントリビューションを行う。  
- ライセンス対策: 企業利用やクローズドな拡張を考える場合はGPLv3の条件を確認し、必要ならライセンス専門家に相談する。

Storytellerは「自分たちの書き方に合わせて育てる」タイプのツールです。日本語特有のニーズを持つチームほど、OSSに貢献する価値が高いはずです。興味がある開発者や作家はまずローカルで動かしてみましょう。
