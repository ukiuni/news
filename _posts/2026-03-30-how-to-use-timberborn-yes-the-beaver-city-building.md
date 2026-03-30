---
layout: post
title: "How to use Timberborn 🦫 (yes, the beaver city-building game) as a database 💾 - ビーバー街づくりゲーム「Timberborn」をデータベースとして使う方法"
date: 2026-03-30T17:52:30.562Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://dev.to/thormeier/how-to-use-timberborn-yes-the-beaver-city-building-game-as-a-database-489c"
source_title: "How to use Timberborn 🦫 (yes, the beaver city-building game) as a database 💾 - DEV Community"
source_id: 3421937
excerpt: "TimberbornのHTTPレバーをビット列化して、セーブ連動のクラウド風保存を実現する"
image: "https://media2.dev.to/dynamic/image/width=1200,height=627,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Fac7h09s1z2863xlsyraf.png"
---

# How to use Timberborn 🦫 (yes, the beaver city-building game) as a database 💾 - ビーバー街づくりゲーム「Timberborn」をデータベースとして使う方法
ビーバーの自動化ギミックを悪用して、ゲーム内の「HTTPレバー」をビット列として読み書きする――ジョーク半分、本気半分のクラウド風ストレージの作り方。

## 要約
Timberbornの「HTTPレバー」はそれぞれON/OFFを制御するHTTPエンドポイントを持つため、これを1ビットとして扱い、JSON→ASCII→8bitでエンコードしてレバーに書き込み・読み出しすることで、セーブに紐づく永続ストレージを実現できる。

## この記事を読むべき理由
遊び心あるハックだが、ビット操作・HTTP API・シリアライズ/デシリアライズの基本が一通り学べる。日本のゲームモッダーや教育用途、ハードウェア的な論理回路の学習にも応用可能。

## 詳細解説
- HTTPレバーの仕組み：各レバーに「Switch-on URL」「Switch-off URL」があり、別々のHTTP呼び出しでON/OFFを切り替えられる。さらに全レバーの状態を返すAPI（/api/levers）が存在する。
- ビットとして扱う考え方：ON=1、OFF=0。複数レバーを番号順に並べれば任意長のビット列になる。
- 書き込みの流れ：アプリ側で保存したいオブジェクトをJSON文字列化 → 各文字をASCIIコードに変換 → 8ビットバイナリにパディング → 全ビット列をレバー数に合わせてパディング → 各ビットごとに対応するレバーのon/offエンドポイントへHTTPリクエストを投げる（例：1000レバーなら最大1000リクエスト）。
- 読み取りの流れ：/api/leversを取得 → レバー名から番号を取り出してソート → stateを1/0で連結 → 8bitごとに分割してparseInt( ,2)→ fromCharCodeで文字列復元 → JSON.parseして元のオブジェクトを得る。
- 実用上の制約：大量のHTTPリクエストでクライアント/OSが不安定になりやすい、バッチAPIが無いため遅い、レバー数を正確に揃える必要あり。Steamセーブと同期するため「永続化」は可能だが実運用向けではない。

小さなコード断片（ビット化のイメージ）:
```javascript
const json = JSON.stringify(obj);
const bits = json.split('').map(c => c.charCodeAt(0).toString(2).padStart(8,'0')).join('');
const padded = bits.padEnd(numberOfLevers,'0');
const urls = padded.split('').map((b,i) => `http://localhost:8080/api/switch-${b==='1'?'on':'off'}/HTTP Lever ${i+1}`);
await Promise.all(urls.map(u => fetch(u)));
```

## 実践ポイント
- まずは小さくテスト：レバー10〜50本で動作確認してから規模拡大する。  
- レバー数はマップ内の正確な数に合わせる（不足・過剰でデータ破損の可能性）。  
- パフォーマンス対策：連続fetchは短時間で大量送信になるので適切に間隔を空けるか再試行実装を入れる。  
- サンドボックス／Mod活用：大量のレバーを簡単に用意するならサンドボックスモッドを使うと楽。  
- 応用アイデア：教育用に「ビット演算を実際に動かす教材」にしたり、配信トリガーと組み合わせた遊び（いいねで花火）に。  
- 注意点：ゲームサーバや開発者の規約に違反しない範囲で楽しむこと。実運用のデータ保存手段としては推奨しない。

楽しい“やってはいけないけどやってみた”系のハックですが、プロトタイプ的に学習効果は高いです。興味があれば、具体的な実装例や簡易デモのコードを準備しますか？
