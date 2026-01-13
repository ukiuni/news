---
layout: post
title: "Using CORS + Google Sheets is the cheapest way to implement a waitlist for landing pages - CORS と Google Sheets で作るランディングページの最安ウェイトリスト"
date: 2026-01-13T06:58:07.476Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://medium.com/@taninsea/using-cors-google-sheets-is-the-cheapest-way-to-implement-a-waitlist-for-landing-pages-a4843ddf1a53"
source_title: "Using CORS + Google Sheets is the cheapest way to implement a waitlist for landing pages"
source_id: 428120353
excerpt: "CORSとGoogleスプレッドシートでサーバー不要、数分で作れる最安ウェイトリスト"
---

# Using CORS + Google Sheets is the cheapest way to implement a waitlist for landing pages - CORS と Google Sheets で作るランディングページの最安ウェイトリスト
魅力的タイトル: 「サーバー代ゼロで待機リストを作る方法 — CORS と Google Sheets で数分デプロイ」

## 要約
CORS と Google Sheets（＋Google Apps Script）を組み合わせれば、サーバーを立てずにランディングページのウェイトリストを最小コストで実装できる。スタートアップやMVPに最適な手法。

## この記事を読むべき理由
サーバー構築や外部データベースを用意する時間・費用を節約したい日本の起業家やエンジニアにとって、手元の Google アカウントだけで実用的な登録機能を短時間で用意できる点が魅力。予算が限られる早期フェーズのプロダクト検証にぴったり。

## 詳細解説
基本アイデア
- Google Sheets をデータ保存先にする。
- Google Apps Script（GAS）で Web アプリ（HTTP エンドポイント）を作り、Sheet に書き込む処理を実装する。
- ランディングページ側（ブラウザ）から fetch を使って GAS のエンドポイントへ POST。ここで CORS をクリアする必要があるため、GAS 側で適切にレスポンス（およびプリフライトの対応）を行う。

技術的ポイント（初心者向け要点）
1. Google Apps Script の Web アプリ化  
   - スプレッドシートを用意し、Apps Script を紐付ける。  
   - doPost(e) を実装して POST データを Sheet に追記する。  
   - 「アプリを実行するユーザー」「アクセスできるユーザー」を適切に設定してデプロイ（一般公開する場合は「全員（匿名でも可）」にするケースが多い）。
2. CORS（クロスオリジン）対策  
   - ブラウザが別ドメインへ送るとき、プリフライト（OPTIONS）要求が来る。GAS 側で OPTIONS を受け取って Access-Control-Allow-* ヘッダを返すか、あるいはレスポンス側で Access-Control-Allow-Origin を許可する必要がある。  
   - セキュリティの観点でワイルドカード（*）を使うと誰でも送信できるため、実運用ではドメイン限定やトークンチェックを検討する。
3. 制限と注意点  
   - GAS と Sheets は無料枠や呼び出しレート、1日の処理量に制限がある。大量トラフィックには向かない。  
   - スプレッドシートに個人情報を置く場合はプライバシーと法令（個人情報保護法）に注意。  
   - スパム対策（reCAPTCHA、メール二重確認、トークン）を必ず組み合わせること。

簡単なコード例（イメージ）
- Google Apps Script（スプレッドシートに書き込む最小の doPost）:

```javascript
// javascript
function doPost(e) {
  var sheet = SpreadsheetApp.openById('SPREADSHEET_ID').getSheetByName('Sheet1');
  var body = JSON.parse(e.postData.contents);
  sheet.appendRow([new Date(), body.email || '', body.name || '']);
  var output = ContentService.createTextOutput(JSON.stringify({status: 'ok'}));
  output.setMimeType(ContentService.MimeType.JSON);
  return output;
}
```

- フロントエンド（ランディングページ）からの送信例:

```javascript
// javascript
fetch('https://script.google.com/macros/s/YOUR_DEPLOY_ID/exec', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ email: 'user@example.com', name: 'Taro' })
})
.then(r => r.json())
.then(console.log)
.catch(console.error);
```

（実践ではプリフライト対応や CORS ヘッダの確認、reCAPTCHA の検証を追加する。）

## 実践ポイント
- まずはプロトタイプで有効性をテスト：GAS＋Sheets で 100〜数千件程度の登録を試す。問題なければ次に移行。
- スパム対策は必須：reCAPTCHA とサーバー側での簡単な検証を併用する。
- 移行戦略を用意：トラフィックが増えたら Cloud Functions / Firebase / API サーバー + DB に切り替えやすく設計する（ログを保管しておけば移行が楽）。
- 日本の事業者向け注意：個人情報の取り扱い・保存場所を明示し、必要に応じて利用規約とプライバシーポリシーを用意する。

まとめ
- コスト最小で早く試すには有効な手法。ただし規模拡大・セキュリティ・法令順守は事前に検討すること。まずは小さく試して、実運用フェーズで適切に強化するのが現実的なアプローチ。
