---
layout: post
title: "The 49MB Web Page - 49MBのウェブページ"
date: 2026-03-15T20:32:38.315Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://thatshubham.com/blog/news-audit"
source_title: "The 49MB Web Page | thatshubham"
source_id: 47390945
excerpt: "49MB・422リクエストのニュース頁がバッテリーとUXを蝕む理由"
image: "https://thatshubham.com/img/news-audit-og.jpg"
---

# The 49MB Web Page - 49MBのウェブページ
見出しだけでなく“アルバム1枚分”をダウンロードしていませんか？ — ニュースサイトの「重さ」とUXを考える

## 要約
ある大手ニュース記事の読み込みで422リクエスト、49MBを消費――現代のニュースサイトが生む巨額のデータ/CPU/バッテリー負担と、それを生む広告／トラッキングの仕組みを解説します。

## この記事を読むべき理由
モバイル中心の日本市場では通信制限やバッテリーが重要。ユーザー体験が悪化すると信頼と閲読時間が失われ、結果的に収益にも響きます。エンジニア／プロダクト担当なら対策を知っておく価値があります。

## 詳細解説
- 何が起きているか：ページ開いた瞬間に大量の第三者JSや広告入札（プログラマティックオークション）がブラウザで並列実行され、ダウンロード→パース→コンパイルでメインスレッドとCPUを食う。結果、読み込みが遅くなり端末が熱くなる。  
- トラッキングの実態：ページ内で多数のPOSTビーコンやピクセルが飛び、ユーザーのクロスサイト識別が構築される。可視化されないが継続的に発火する。  
- UXの代償：GDPRバナーやニュースレター・モーダル、通知許可などが重なり「Z-Index Warfare（重なり合う障害）」を生む。これらはInteraction Cost（NN/g）を上げ、離脱を誘発。  
- レイアウトの急変（CLS）：広告が遅れて挿入されると文章がジャンプしユーザーの読書フローを破壊。GoogleのCore Web Vitalsでもペナルティ対象。  
- 経済的背景：出版社は短期的なCPM最適化で長期のリテンションを犠牲にしている。広告エコシステム自体がコンテンツと作り手を遠ざける構造になりがち。

## 実践ポイント
1. 計測から始める：Chrome DevToolsのNetwork/Performanceでリクエスト数と大きさ、メインスレッドの影響を確認。  
2. 第三者スクリプトを整理：不要なタグは削除、重要度に応じて遅延（defer/async）や条件読み込みにする。  
3. オーバーレイを直列化：モーダルは行動ベースで1つずつ表示（例：60秒or50%スクロール後に表示）。閉じたらlocalStorageに記録。  
4. 広告は遅延・スクロール連動で：広告リフレッシュはスクロール深度に紐づけ、読み途中での割り込みを避ける。  
5. CLS対策：広告・画像枠に固定高さorアスペクト比を確保してレイアウトのシフトを防ぐ。例：CSS
```css
/* CSS */
.ad-slot { min-height: 250px; background: var(--skeleton); aspect-ratio: 300 / 250; }
```
6. 動画はユーザー行動に依存：IntersectionObserverで画面外なら自動再生を止める。
```javascript
// JavaScript
const obs = new IntersectionObserver(entries => {
  entries.forEach(e => {
    if (!e.isIntersecting) e.target.pause();
  });
});
document.querySelectorAll('video').forEach(v => obs.observe(v));
```
7. 軽量版を提供：text/lite版やRSSを用意し、低帯域ユーザーに配慮する。  
8. UXの優先順位を再設計：コンテンツ優先でヘッダーや常駐要素は最小化。ポップアップはエンゲージメントの後に。

短期の収益最適化でUXを犠牲にすると長期的信頼を失う――技術的対策は明確です。まずはデータを取り、第三者負荷の可視化と優先順位付けから。
