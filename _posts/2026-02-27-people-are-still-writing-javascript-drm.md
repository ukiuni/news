---
layout: post
title: "People are STILL Writing JavaScript \"DRM\" - まだJavaScriptで「DRM」を書いている人たち"
date: 2026-02-27T17:35:19.758Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://the-ranty-dev.vercel.app/javascript-drms-are-stupid"
source_title: "The Illusion of JavaScript DRM: A Three-Round Demolition of HotAudio&#39;s Copy Protection"
source_id: 395168910
excerpt: "ブラウザだけのJavaScript“DRM”は容易に突破され、真の保護にはCDMや運用対策が不可欠。"
image: "https://the-ranty-dev.vercel.app/images/posts/javascript-drms-are-stupid/hero.png"
---

# People are STILL Writing JavaScript "DRM" - まだJavaScriptで「DRM」を書いている人たち
ブラウザだけで守れる？HotAudioのケースに学ぶ“見せかけのDRM”の実態

## 要約
HotAudioのような小規模配信サービスがJavaScriptで独自の“DRM”を作る事例を通し、「ブラウザ上のクライアント実装だけでは本物のDRMにならない」理由と、回避手法の代表例を分かりやすく解説する。

## この記事を読むべき理由
日本でもASMRや同人音声など小規模配信が増えており、運営者側・開発者側ともに「どこまで守れるのか」「何をすべきか」を現実的に理解する必要があるため。

## 詳細解説
- 本質：本物のDRMはハードウェア保護（TEE：Trusted Execution Environment）とCDM（Widevine/FairPlay/PlayReady）の組合せで成り立つ。これらはキーや復号バッファをホストOSやブラウザ外から隠す。  
- 小規模プラットフォームの現実：Widevine等は契約・ネイティブ統合・コストが高く、小さなサイトは採用不能。代替として「暗号化したチャンクをMSE（MediaSource Extensions）経由で配信し、再生前にJSで復号してappendBufferへ流す」方法が使われる。  
- PCM境界の脆弱性：最終的にブラウザのデコーダへ渡されるのは標準コーデック（PCM等）であり、JS側で復号したデータがappendBufferで渡される瞬間が「黄金の傍受ポイント」になる。つまりJSで復号する限り、拡張やフックで奪われる可能性が高い。  
- 実際の回避／防御のやり取り：攻撃側は拡張やスクリプト差し替えでSourceBuffer.appendBufferをフックしたり、HTMLMediaElement.playを監視してプレイヤー参照を得る。防御側はグローバル参照の隠蔽、スクリプト整合性チェック（ハッシュ/SRI）、関数のtoStringによる改変検出などを導入するが、攻撃側はtoStringを偽装したりフックの配置を工夫して回避する。  
- まとめ：ブラウザ内で完結する「JS DRM」は摩擦を生み出すだけで、決定的な防御にはならない。

以下は概念を示す最小例（参考）です。

```javascript
// javascript
// appendBufferを傍受する簡易例（実運用での使用は非推奨）
const orig = SourceBuffer.prototype.appendBuffer;
SourceBuffer.prototype.appendBuffer = function(data) {
  // 復号済みチャンクを保存
  window.__CAPTURED = window.__CAPTURED || [];
  window.__CAPTURED.push(new Uint8Array(data));
  return orig.apply(this, arguments);
};
```

攻撃側はさらにtoStringを上書きして検出ロジックを欺くことも可能です。

## 日本市場との関連性
- 日本でもASMR・同人音声配信はニッチ市場だが活発。小規模サービスがコスト負担でCDMを導入できない点は共通の課題。  
- 海外で使われる「JSベースの擬似DRM」は日本の配信者/プラットフォームでも流行りやすく、結果的にコンテンツ保護の過信がトラブルを招く可能性がある。

## 実践ポイント
- 本気で保護するなら：ネイティブアプリ＋CDM（Widevine/FairPlay/PlayReady）を検討する。  
- すぐできる対策（現実的）：
  - サーバー側での署名付きトークン／短寿命の署名付きURLを使う。  
  - 軽い難読化＋SRI・整合性チェックを組み合わせて自動化ツールに対する障壁を上げる（ただし突破は時間の問題）。  
  - ログ監視・レート制限・再生パターン解析で不正ダウンロードを検出・遮断する。  
  - 法的対応や透かし（ウォーターマーク）で追跡可能性を確保する。  
- 開発者へ：JSでの“復号→appendBuffer”という流れ自体が根本的な制約なので、設計段階で期待値（「完全なDRMは無理」）を明確にすること。

短い結論：ブラウザ上の工夫で「ダウンロード阻止」はある程度できるが、本当に守りたいならハードウェア支援のCDMや運用・検出・法的対策を組み合わせる必要がある。
