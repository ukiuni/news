---
layout: post
title: "From Nevada to Kansas by Glider - グライダーでネバダからカンザスへ"
date: 2026-01-19T22:00:36.303Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.weglide.org/flight/978820"
source_title: "WeGlide"
source_id: 46641036
excerpt: "WeGlideのJS描画を解析しIGC/トラックを取得する手順"
image: "/img/WeGlide.jpg"
---

# From Nevada to Kansas by Glider - グライダーでネバダからカンザスへ
砂漠から大平原へ──JSで描かれた飛行ログを“没入”して読む方法

## 要約
WeGlideのフライトページはクライアント側で大量のデータをJSで描画するため、ただ開くだけでは中身が見えないことがある。この記事では「表示できないページ」をどう解析して、フライトデータ（トラック/IGCなど）を取り出すかに焦点を当てる。

## この記事を読むべき理由
- 海外のフライトログや動的なWebアプリに遭遇したとき、単純な「ページ保存」では情報が得られない場面が増えています。  
- 日本のグライダー愛好者やデータ解析に関わるエンジニアにとって、クライアントレンダリングされたサービスから正しくデータを取り出すスキルは実践的価値が高いです。

## 詳細解説
WeGlideのようなモダンなサイトは、ページ本体は最小限のHTMLで、実データ（フライトトラック、メタ情報、地図タイルなど）はJavaScriptが動いてからAPI経由で取得して描画します。ユーザーが「WeGlideはJSが必要です」と見るのは、ブラウザでJSが無効なためにクライアントレンダリングが実行されないからです。

技術的ポイント
- クライアントサイドレンダリング（CSR）: サーバは骨格HTMLを返し、ブラウザがXHR/FetchでJSONやIGCファイルを取得して描画する。
- IGC/GPXなどのフライトログ: 多くのフライト共有サイトは元データ（IGCファイルやGeoJSON）をどこかに置いており、ネットワーク観察でURLを特定できることが多い。
- 解析手法: ブラウザ開発者ツールのNetworkタブでXHRを監視する、headlessブラウザでレンダリング後のDOMやXHRレスポンスを取得する、公式のエクスポート機能やAPIがあればそちらを使うのが最も確実で安全。

注意点
- サイトの利用規約や著作権・プライバシーに留意すること（データの自動取得・再利用は制限がある場合があります）。
- 高頻度の自動アクセスはサーバ負荷やアクセス制限につながる可能性があります。

## 実践ポイント
すぐに試せる手順とツール例：

1. まずは普通にブラウザ（Chrome/Firefox）でページを開き、DevTools → Network を開いてページを再読み込み。XHR/FetchでどんなJSONやファイルが読み込まれているか探す。  
2. 「View page source」と「Inspect element」は別物。ソースに無くても、Inspectでレンダリング後のDOMやスクリプトが見られる。  
3. 自動化が必要ならheadlessブラウザを使う（Puppeteerなど）。以下は簡単な例：ページをレンダリングしてXHRをログし、最終的なHTMLを保存する。

```javascript
// JavaScript
const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();

  // XHR/Fetchのレスポンスをログ
  page.on('response', async response => {
    const url = response.url();
    const ct = response.headers()['content-type'] || '';
    if (ct.includes('application/json') || url.endsWith('.igc')) {
      try {
        const text = await response.text();
        console.log('FETCHED:', url);
        // 必要ならここでファイル保存
      } catch (e) {}
    }
  });

  await page.goto('https://www.weglide.org/flight/978820', { waitUntil: 'networkidle2' });
  // ページのレンダリング後HTMLを取得
  const html = await page.content();
  console.log('Rendered HTML length:', html.length);

  await browser.close();
})();
```

4. 公式の「Download IGC」やエクスポートがあるならまずそれを使う。競技/解析用途ならIGCをSeeYouやXCSoarで読み込むのが手っ取り早い。  
5. 日本向けの応用例：同様の手法で日本国内のフライト共有サイトや、気象データAPI、ドローン飛行ログなどを組み合わせて可視化・解析に活用できる。

まとめ：見えないフライトログは「JavaScriptが描く世界」を理解すれば取り出せる。まずはDevToolsでXHRを確認し、公式エクスポートやheadlessレンダリングを選ぶ。安全性と規約を守れば、海外の興味深いフライト記録を技術的に追体験できます。
