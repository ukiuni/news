---
  layout: post
  title: "How I detect the “current paragraph” on arbitrary web pages (and mask everything else) - 任意のウェブページで「現在の段落」を検出し、それ以外をマスクする方法"
  date: 2026-01-06T04:00:50.299Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://chromewebstore.google.com/detail/parsely/ackaeneemjkgbjpbmpogdbkpkfeobamj?hl=en-US"
  source_title: "Parsely - Chrome Web Store"
  source_id: 471171219
  excerpt: "任意ページで注目段落を自動検出して他をマスクし、集中読書を実現する手法を解説"
  image: "https://lh3.googleusercontent.com/_A7zpwfjkL6PQ63qeVJIlbzk8Krfq2eNWKwA4maaPSN5G5-LT35aGcHt3Q8BL1OQI1I5Uqrhhi7eJTD_dO86DB3HYbM=s128-rj-sc0x00ffffff"
---

# How I detect the “current paragraph” on arbitrary web pages (and mask everything else) - 任意のウェブページで「現在の段落」を検出し、それ以外をマスクする方法
魅惑の一段ずつ読書 — ウェブ記事を「今この段落だけ」に集中させる視覚化テクニック

## 要約
ウェブページ上の任意の段落を自動検出し、残りを半透明で覆うことで「段落単位の集中読書」を実現する手法と、その実装上の要点（DOM解析、可視性判定、マスキング、パフォーマンス、ローカル保存）を解説する。

## この記事を読むべき理由
日本の長文記事やニュースサイトはサイドバーや広告が多く、集中読書が難しい。Parselyのような段落単位フォーカスは、リサーチ、長文消化、読書疲労軽減に直結する実用的なUIパターンで、ブラウザ拡張やサイト改善を考えるエンジニアにとって有益な設計例となる。

## 詳細解説
- 検出の第一歩 — メインコンテンツ抽出  
  多くの実装は Mozilla の Readability ライクな手法や単純なヒューリスティクスを併用する。手順は概ね：本文候補要素（<p>、<article>、テキスト比率の高い<div>）を抽出 → テキスト長、リンク密度、表示領域（boundingClientRect）で絞り込む。日本語サイトでは署名や広告の日本語テキストも含まれるため、リンク密度とブロックサイズの閾値調整が重要。

- 「現在の段落」判定  
  ブラウザのビューポート中心点やスクロール位置を基準に、各段落要素の bounding rect と重なり度（被覆率）を計算して最も「視線がある」と推定される段落を選ぶ。より反応良くしたければ IntersectionObserver を使い、交差比率が最大のノードを現在段落にする方法が実装負荷と性能の両面で現実的。

- マスキングとハイライトの実装テクニック  
  全画面の半透明オーバーレイを敷き、現在段落部をクリップ（clip-path）でパンチアウトする手法が簡潔。代替として、他要素に低い不透明度や blur を与え、現在段落に z-index と柔らかな境界線を与える方法もある。重要なのは再描画コストを抑えること（頻繁な style 書き換えは避ける）。

- 操作体験と補助機能  
  キーボード（矢印／スペースで移動、Escで終了）や自動保存（localStorage／IndexedDB に URL ベースで段落インデックス保存）を用意する。注釈・ブックマークはローカル保存に限定することでプライバシーを保てる（Parsely はブラウザ内保存を謳っている点が参考）。

- パフォーマンスと堅牢性  
  DOM読み取り（getBoundingClientRect 等）はまとめて行い、レイアウトスラッシングを防ぐ。スクロールイベントは throttle して requestAnimationFrame 経由で処理。動的に変化するページ（画像遅延読み込み、広告挿入）には MutationObserver で要素変化を監視し、段落リストを差分更新する。

- 日本語サイト固有の注意点  
  政治・経済系サイトやメディアは段落を<div>で分割している場合が多く、単純な<p>検出では抜け漏れが出る。文字幅や行数で段落境界を推定するルールを設けると精度が上がる。

## 実践ポイント
- まずは Parsely を試して、挙動（段落選択、ハイライト、保存）を観察する。  
- 拡張を自作する場合の基本構成：content script（段落抽出・UI制御） + options page（フォント・不透明度設定） + storage（localStorage/IndexedDB）。  
- 「現在段落」判定は IntersectionObserver の交差比最大ノードを第一候補にし、フォールバックでビューポート中心との距離を使う。  
- マスクは clip-path を使うと簡潔だが、古いブラウザ互換性を要する場合は overlay＋要素スタイル変更の組合せにする。  
- パフォーマンス対策：DOM測定はバッチ化、スクロール監視は throttle、動的変更は MutationObserver で差分更新。  
- プライバシー配慮：ユーザの読書データや注釈はデフォルトでローカル保存にし、外部送信は明示的な同意を得る。

簡潔に言えば、段落検出は「本文ブロック抽出 → 可視性スコアリング → IntersectionObserver／中心点判定 → クリップマスク」で設計し、パフォーマンスと日本語サイト特性に合わせた調整を行えば、実用的で集中できる読書モードが作れる。
