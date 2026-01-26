---
layout: post
title: "Screeps: How a game about programming exposed thousands of players to remote code execution - Screeps：プログラミングのゲームが数千人のプレイヤーを遠隔コード実行に晒した話"
date: 2026-01-26T02:28:37.454Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://outsidetheasylum.blog/screeps/"
source_title: "Screeps: How A Game About Programming Sold Its Players a Remote Access Trojan"
source_id: 837858406
excerpt: "ScreepsのSteamクライアント脆弱性で数千人がRCEに晒され、サンドボックス欠如の重大教訓"
image: "https://outsidetheasylum.blog/screeps/header.png"
---

# Screeps: How a game about programming exposed thousands of players to remote code execution - Screeps：プログラミングのゲームが数千人のプレイヤーを遠隔コード実行に晒した話
あなたのSteamクライアントが“プレイ中に乗っ取られる”まで — プログラミングMMOが露呈した現実的なセキュリティ教訓

## 要約
プログラミングが主題のMMO「Screeps」は、プレイヤーがアップロードするJavaScriptをサーバで実行する設計ゆえに、脆弱なクライアント／コンソールの実装が悪用されれば他プレイヤーに遠隔コード実行（RCE）を許す状態になっていた。問題はSNSで拡散後に修正されたが、運営の対応やコミュニティの無自覚さが議論を呼んだ。

## この記事を読むべき理由
- 日本のエンジニアや学習者に人気のある「コードで遊ぶ」サービスで起きた事例は、学習用途のプラットフォーム設計や運用上の落とし穴を明確に示すため。  
- Steam／ネイティブクライアントやNW.js系アプリを使う国内ユーザーにも直接影響する実務的な注意点が学べる。

## 詳細解説
- ゲーム構造：ScreepsはプレイヤーがJavaScriptでユニット（creep）の挙動を定義し、そのコードをサーバ上で周期的（tickごと）に実行するMMO。サーバ側で“プレイヤーのコードをそのまま実行”する設計が前提。  
- リモートコンソール経路：クライアントは開発者向けに「ローカルコンソール」機能を用意し、ブラウザで打ったコマンドや出力をサーバに送受信できる。ログ表示はHTMLをパースしてレンダリングしていたため、ログやクリープ名に悪意あるスクリプトを埋め込むとXSS的に動作した。  
- ブラウザ => ネイティブ差異：Web版では被害が限定的だが、SteamのネイティブクライアントはNW.js（Node統合）を流用しており、ネイティブ側からはNodeのAPI（例：child_process.exec）が利用可能だった。これによりブラウザ上のXSSがそのままRCEに拡大する危険があった。  
- 運営とコミュニティ：報告から修正までに長期間を要し、運営は当初リスクを軽視。コミュニティ内には脆弱性を利用した“クライアント改造”や共有スニペットが存在し、新規プレイヤーへの注意喚起が不十分だった。  
- その他の品質問題：UIの遅延やドキュメントの誤り、tickの遅さ、サンドボックスの脆弱性（例：特定データでJSON.stringifyがゲームプロセスを壊す）など、運用面の問題も複合している。

## 実践ポイント
- プレイヤー向け（即実行できる対策）
  - ネイティブ／Steamクライアントの使用を避け、サンドボックス化したブラウザプロファイルかVM上でプレイする。  
  - 他人のコードやスニペットをコピペする前に内容を精査する。特にconsole.log等で外部入力をそのまま出力するコードは危険。  
  - クライアント側でログをサニタイズする簡易対策（例）：

```javascript
// javascript — 簡易HTMLエスケープでconsole.log置換
const esc = s => String(s).replace(/[&<>"']/g, c=>({ '&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;' }[c]));
const rawLog = console.log.bind(console);
console.log = (...args) => rawLog(...args.map(esc));
```

- 開発者／運営向け
  - ユーザー提供コードは厳格にサンドボックス化し、ホスト環境（Node等）からの脱出経路を排除する（Node統合の無効化、プロセス実行を許可しない）。  
  - 出力のHTMLレンダリングはやめ、必ずサニタイズする。ログや名前等ユーザ入力はエスケープして扱う。  
  - 脆弱性報告に迅速に対応し、問題の深刻さを過小評価しない。運用上の品質（ドキュメント、レスポンス遅延）も放置しない。  
  - 新機能の追加より先にセキュリティと安定性を優先する姿勢を公開する。

短い結論：教育的で魅力ある設計の裏に「実装・運用の盲点」が潜んでいた事例。ユーザーはクライアント選択とコードの出所に注意を払い、開発者はサンドボックスと入力サニタイズを最優先に。
