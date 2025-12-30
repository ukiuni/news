---
layout: "post"
title: "The HTML Elements Time Forgot - 時間が忘れ去ったHTML要素"
date: "2025-12-26 04:03:35.656000+00:00"
categories:
- tech
- world-news
tags:
- tech-news
- japan
source_url: "https://htmhell.dev/adventcalendar/2025/22/"
source_title: "The HTML Elements Time Forgot - HTMHell"
source_id: "1124897989"
---
# The HTML Elements Time Forgot - 時間が忘れ去ったHTML要素

## 要約
かつてブラウザ黎明期に登場した奇妙で時代遅れのHTML要素を振り返り、現代の置き換え方や日本の現場でのリスクを簡潔に整理する。

## この記事を読むべき理由
古い社内ポータルやレガシーサイトがまだ動いている日本の現場では、非推奨・非標準の要素が残っていることが多い。互換性・アクセシビリティ・セキュリティの観点から監査・置換の優先順位が分かる。

## 詳細解説
- なぜ問題か  
  WHATWGのHTML Living Standardは「non‑conforming features」を列挙し、作者は使用を避けるべきと明示している。ブラウザの後方互換性で動いてしまうが、それは“動くから安全”の根拠にならない。

- 代表例と現代の置換
  - <marquee> / <blink>  
    自動で文字を動かす古典的タグ。視認性・アクセシビリティに悪影響。代替はCSSアニメーションやJavaScriptでの制御（ただし動きすぎに注意）。
  - <bgsound>  
    Internet Explorer固有の自動再生音機能。現代は <audio> を使い、ユーザー操作や許諾のもとで再生する。
  - frames / <frameset> / <frame> / <noframes>  
    ページ分割のための古い仕組み。スクリーンリーダーやリンク共有が扱いにくく、SPAやサーバー側ルーティング、<iframe>（埋め込み用途）へ置換するのが普通。HTML5では非推奨だがブラウザ互換で残ることがある。
  - コード表示系: <xmp>, <listing>, <plaintext>  
    <xmp> は特殊文字を解釈せずそのまま表示、<plaintext> は以降を全てテキスト扱いにするなど挙動が怪しい。現代は <pre> と <code> を組み合わせ、適切にエスケープ（HTMLエンティティ）して使う。MIMEを text/plain にして配信する手も有効。
  - レイアウト用 <spacer> やテーブル（レイアウト）  
    Flexbox / Grid / CSS に置き換え。意味のない要素を見直し、セマンティクスを回復する。

- なぜ今チェックすべきか（日本の事情）  
  多くの企業で古いIEベースの社内システムや移行途中のポータルが残る。EdgeのIEモードで動いていて発覚しにくいが、将来のブラウザ更新やアクセシビリティ要件で問題化しやすい。

## 実践ポイント
- 探す：コードベースをタグ名でgrep/検索（marquee, bgsound, frameset, xmp, plaintext など）して一覧化する。
- 優先度付け：ユーザー影響・セキュリティ面・アクセシビリティ観点で置換優先度を決める。
- 置換案の例  
  - 自動スクロール → CSSアニメーション＋ユーザー停止ボタン／prefers-reduced-motionを尊重  
  - 自動音声 → <audio> に autostart させない。ユーザー操作で再生。  
  - コード表示 → <pre><code> にエスケープ、あるいはサーバーで text/plain を返す。  
  - フレームレイアウト → SPA/サーバーサイドレンダリング＋history API、または埋め込みは <iframe>（必要最小限）へ
- テストとツール  
  - W3C Validator / HTMLHint で非推奨要素を検出  
  - axe や Lighthouse でアクセシビリティ確認  
  - 既存ユーザーに影響が出ないよう段階的にリファクタリング
- ポリシー化：新規機能で使ってはいけない要素をコーディング規約に明記し、CIで検出する。

