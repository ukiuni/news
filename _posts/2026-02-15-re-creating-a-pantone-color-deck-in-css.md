---
layout: post
title: "Re-creating a Pantone Color Deck in CSS - Pantoneカラー見本帳をCSSで再現する"
date: 2026-02-15T16:05:11.684Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://dev.to/madsstoumann/re-creating-a-pantone-color-deck-in-css-3108"
source_title: "Re-creating a Pantone Color Deck in CSS - DEV Community"
source_id: 3248930
excerpt: "最新CSSだけでPantone風の扇型カラーデッキをJS不要で忠実再現する手法を詳解"
image: "https://media2.dev.to/dynamic/image/width=1000,height=500,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Fskz1tl4rzcbhe2z3ot2i.jpg"
---

# Re-creating a Pantone Color Deck in CSS - Pantoneカラー見本帳をCSSで再現する
CSSだけで再現するPantone風ファンデッキ — JavaScript不要で“扇”の挙動とクリックでのフォーカスを実装する方法

## 要約
CSSの新機能（container-type / progress() / sibling-index()/sibling-count() / :has() / ::details-content）を組み合わせ、HTMLの<details name="…">で排他的アコーディオンを作り、JavaScriptなしでPantoneファンデッキの見た目と操作感を再現するテクニックを紹介します。

## この記事を読むべき理由
最新のCSS機能の実践例として、デザインツールやプロトタイプで「コードだけで動くインタラクティブな色見本」を作るヒントが得られます。日本のフロントエンド／デザイナーにも有用な、印刷・カラーワークフローに馴染むUIの作り方です。

## 詳細解説
- マークアップ: セクション内にカバーと色カードを配置。各色カードは
  details name="deck"
  として排他的に開閉できるようにする（ブラウザ側で一つだけ開く動作）。
- 重ね順と配置: sectionに
  container-type: inline-size;
  display: grid;
  place-items: end center;
  を指定し、子要素を同じグリッドセル（grid-area:1 / -1）に重ねる。z-indexは
  sibling-count() と sibling-index() で自動計算し、要素順に応じた自然なスタックにする。
- 扇の広がり: progress(100cqi, 300px, 1440px) でコンテナ幅を0→1に正規化し、--spreadから開始角・終了角を決定。これによりコンテナ幅に応じて扇の広がりが連続的に変化する。
- 各カードの回転: sibling-index()/sibling-count()で0..1の位置を計算し、start〜endの角度を補間。transform-originをリベット位置に合わせ、扇の回転軸を統一する。
- クリックでのフォーカス（JS不要）: details[name="deck"] の排他性で1つを開くと、そのカードに [open] が付与される。::details-content を使って内容を常に表示させつつ、:has() と隣接セレクタで
  --is-before / --is-active / --is-after / --has-active
  のフラグを立て、回転式の式に反映して「選択カードは垂直に」「前のカードは端へ畳む」「後のカードは反対へ押し出す」といった振る舞いを実現する。
- サポート状況: これらは比較的新しい仕様に依存するため、現時点ではChromium系とSafariが中心の実装状態。Firefox等は未追随の機能があるため、本番ではフォールバック設計が必要です。

簡略化した回転制御の例（抜粋）:

```css
/* css */
section { container-type: inline-size; display: grid; place-items: end center; }
section > * { grid-area: 1 / -1; 
  --spread: progress(100cqi, 300px, 1440px);
  --start-degree: calc(var(--spread) * -45deg);
  --end-degree: calc(var(--spread) * 45deg);
  rotate: calc( var(--start-degree) + (var(--end-degree) - var(--start-degree)) * (sibling-index() - 1) / (sibling-count() - 1) );
  transform-origin: calc(100% - var(--rivet)) calc(100% - var(--rivet));
  transition: rotate .25s linear;
}
details[name="deck"] { /* details本体のスタイル */ }
details::details-content { content-visibility: visible; display: contents; }
```

## 実践ポイント
- まずはCodePen等で小さなサンプル（カバー＋3〜6枚のカード）を作って、progress() と sibling-* の挙動を体感する。  
- ブラウザ互換を確認し、未対応ブラウザ向けは @supports() で簡易扇（固定角度）やJSで回転を計算するフォールバックを用意する。  
- 日本のデザインワークフローでは、色値（HEX / LAB / RGB）やアクセシビリティ（コントラスト）表示を各カードに入れておくと実用性が高まる。  
- 実装をデザインシステムに取り込む場合、カード数やリベット位置、spreadの最小/最大幅を変数化して調整しやすくする。

短時間で触れて学べます。まずはブラウザを最新にして、CodePenで動かしてみてください。
