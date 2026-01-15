---
layout: post
title: "How I built a \"Magic Move\" animation engine for Excalidraw from scratch published - Excalidraw用“Magic Move”アニメーションエンジンをゼロから作った話"
date: 2026-01-15T19:18:02.422Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://dev.to/behruamm/how-i-built-a-magic-move-animation-engine-for-excalidraw-from-scratch-published-4lmp"
source_title: "How I built a &quot;Magic Move&quot; animation engine for Excalidraw from scratch published - DEV Community"
source_id: 3166603
excerpt: "差分検出とイージングでフレーム描くだけで図が滑らかに遷移する鍵不要アニメの実装手法"
image: "https://media2.dev.to/dynamic/image/width=1000,height=500,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Fbqwk6rhxjjaof93gzaif.png"
---

# How I built a "Magic Move" animation engine for Excalidraw from scratch published - Excalidraw用“Magic Move”アニメーションエンジンをゼロから作った話
魅せるドキュメントへ一歩：スライド不要で図が動き出す「キー不要アニメーション」の作り方

## 要約
Excalidraw上の静的スケッチを、タイムライン不要で「フレームA→フレームB」を描くだけで滑らかに遷移させるKeyless（キー不要）アニメーションエンジンの設計と実装を技術的に解説する記事です。Diff（差分検出）、補間、レンダーループ、そして「重さ」を感じさせるイージングが肝です。

## この記事を読むべき理由
ドキュメントやアーキテクチャ図を“動かして”説明したい開発者・プロダクト担当に必読。日本の技術発表やセールス資料、リモート会議での説明力を手早く上げられる実装知見が得られます。

## 詳細解説
1) 目標と設計方針  
- 「After Effects のようなタイムラインは不要」：手軽さが最優先。  
- 操作フローは単純。Frame1を複製して要素を移動・変更すると、エンジンが自動で遷移を生成する（Keyless Animation）。

2) コア：状態の差分（diffing）  
- 要素は安定IDで識別し、3カテゴリに分類する。  
  - Stable：両フレームに存在し視覚的に同一（そのまま保持）  
  - Morphed（変化）：両フレームに存在するが見た目が変わった（移動・サイズ・色など）  
  - Entering / Exiting：片方にしか存在しない（フェードで登場/退場）  
- 実装ポイントはマップを使ったO(n)近い分類。簡略化した例：

```javascript
// javascript
function categorizeTransition(prevElements, currElements) {
  const prevMap = new Map(prevElements.map(e => [e.id, e]));
  const currMap = new Map(currElements.map(e => [e.id, e]));
  const stable = [], morphed = [], entering = [], exiting = [];

  currElements.forEach(curr => {
    if (prevMap.has(curr.id)) {
      const prev = prevMap.get(curr.id);
      if (areVisuallyIdentical(prev, curr)) stable.push(curr);
      else morphed.push({ key: curr.id, start: prev, end: curr });
    } else {
      entering.push({ key: curr.id, end: curr });
    }
  });

  prevElements.forEach(prev => {
    if (!currMap.has(prev.id)) exiting.push({ key: prev.id, start: prev });
  });

  return { stable, morphed, entering, exiting };
}
```

3) 補間（interpolation）の注意点  
- 数値（x,y,w,h）は線形補間で十分。  
- 色はRGBAに分解して各チャネルを補間→再合成。  
- 角度は「最短経路」で補間する必要がある。たとえば10°→350°は -20°回転を選ぶべき。実装例：

```javascript
// javascript
function angleProgress(oldAngle, newAngle, t) {
  let diff = newAngle - oldAngle;
  while (diff > Math.PI) diff -= 2 * Math.PI;
  while (diff < -Math.PI) diff += 2 * Math.PI;
  return oldAngle + diff * t;
}
```

4) レンダーループと重なり（overlap）  
- CSSトランジションではキャンバスの複雑な描画タイミングを揃えにくいため、requestAnimationFrameベースで独自ループを回す。  
- フェーズ（Exit → Morph → Enter）を単純に直列で行うと不自然。著者はフェーズを重ねて再生（EnterをMorphの終盤に始める等）することで説得力のある動きを作成。

5) イージングで「物理感」を出す  
- 単純な線形進行は退屈。進行度にスプリング系や4次イーズアウトをかけることで「重い塊が落ちる」ような感触を出す。例：quartic ease-out。

6) 実運用での問題点と対策  
- 大きな図や画面録画時は60FPSレンダリングで重くなる。要素数制限やレイヤー分離、描画最適化が必要。  
- Excalidraw本来のズーム/パン挙動と固定フレームのぶつかり（UX差）が課題。

## 実践ポイント
- 小さく始める：まずは2フレームだけで要素を移動して差分→補間を確認。  
- 要素IDを安定化：自動生成IDが変わると差分が取れないため、コピーでIDを保つ運用が重要。  
- パフォーマンス対策：要素数が多い場面では描画をバッチ化、不可視要素はスキップ、Canvasの部分更新を検討する。  
- 見せ方のコツ：EnterをMorphの終盤に被せる、重みのあるイージングを使う、で“Apple風”に見せられる。  
- 拡張案：サブステップ（フレーム内で段階的に要素を出す）、キャンバス録画→MP4出力（MediaRecorder APIやCanvasCaptureStreamを利用）などが実用的。

---

元実装はNext.js + Excalidraw + Framer Motionを組み合わせ、ソースやデモ（postara.io）も公開されています。日本語での導入や資料作成に応用すると、技術説明の説得力が格段に上がります。興味があれば、まずは自分の簡単な図で「複製→移動→再生」を試してみてください。
