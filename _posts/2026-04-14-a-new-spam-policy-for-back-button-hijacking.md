---
layout: post
title: "A new spam policy for \"back button hijacking\" - 「戻るボタンのハイジャック」に対する新しいスパムポリシー"
date: 2026-04-14T04:01:42.570Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://developers.google.com/search/blog/2026/04/back-button-hijacking"
source_title: "Introducing a new spam policy for &quot;back button hijacking&quot; &nbsp;|&nbsp; Google Search Central Blog &nbsp;|&nbsp; Google for Developers"
source_id: 47760764
excerpt: "Googleが「戻るボタン妨害」をスパム扱いに、ECサイトでの履歴操作は検索順位や信頼を失う危険あり"
image: "https://developers.google.com/static/search/blog/images/social-share-blog.png"
---

# A new spam policy for "back button hijacking" - 「戻るボタンのハイジャック」に対する新しいスパムポリシー
検索結果からの離脱を許さない悪質手法に終止符？Googleが「戻るボタン妨害」をスパム扱いへ

## 要約
Googleは「戻る（Back）ボタン」をユーザーの意思と反して無効化・迂回する行為をスパムとして新たに定義し、検索結果での掲載や評価に影響を与える対応を始めます。

## この記事を読むべき理由
日本のECやメディア運営でも、離脱防止やコンバージョン最適化のためにクライアント側で履歴操作を行うケースがあり、これが検索トラフィックや信頼性に直結するため、早めの対策が必要です。

## 詳細解説
- 何が問題か  
  - 「戻るボタン妨害」は、ブラウザの履歴API（pushState/replaceState、popstate等）やダイアログ・リダイレクトを使って、ユーザーが戻ろうとすると移動を妨げたり別ページへ飛ばす挙動を指す。意図的な迷わせや離脱阻止を目的とする実装が対象。
- Googleの狙いと影響範囲  
  - ユーザー体験を損なう行為をスパムとして定義し、検出時は検索での表示やランキング、場合によっては手動対策の対象とする方針。クロール時やユーザーの報告で検出され得る。
- 技術的な検出ポイント（要点）  
  - 履歴APIで不自然に循環する履歴を生成する、戻る操作で自動的に別ドメイン／別URLへリダイレクトする、閉じられないモーダルや連続ダイアログで戻れない状態を作る等。
- 正当な利用との線引き  
  - SPA（Single Page Application）や正当なナビゲーション制御自体は許容。ただし「ユーザーの戻る意図を妨げる」「意図的に離脱を阻止する」実装はNG。

## 実践ポイント
- すぐやること（優先度高）  
  - 自サイトで履歴APIやpopstateハンドラを使っている箇所を洗い出す。戻るで元のページへ戻れるかを実機（モバイル含む）で必ず確認する。  
- 実装ガイドライン  
  - 戻る操作は基本的にユーザーの期待通りに動かす。離脱防止は非侵襲（例：明確なconfirmや一度きりの案内）に留める。強制リダイレクトや無限戻り阻止は避ける。  
- テストとモニタリング  
  - 自動化テストでブラウザの履歴操作を検証し、Search Consoleやアクセス解析で直帰率・離脱ポイントを監視する。ユーザーからの「戻れない」報告が増えたら優先修正。  
- ビジネス上の注意点（日本市場向け）  
  - ECやサブスク登録ページで過度な離脱阻止を行うと信頼低下やコンバージョン逆効果、検索流入減につながる。広告やプロモーションで使う“強引な導線”は見直すこと。

以上を踏まえ、技術的に便利な履歴操作はユーザー主体のUX設計を最優先に実装・監査してください。
