---
layout: post
title: "Signal creator Moxie Marlinspike wants to do for AI what he did for messaging - Signalの生みの親がメッセージングで成し遂げたことをAIで再現したい"
date: 2026-01-13T19:56:11.433Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://arstechnica.com/security/2026/01/signal-creator-moxie-marlinspike-wants-to-do-for-ai-what-he-did-for-messaging/"
source_title: "Signal creator Moxie Marlinspike wants to do for AI what he did for messaging &#x2d; Ars Technica"
source_id: 1553794047
excerpt: "Conferは端末鍵とTEEで会話を暗号化し運営者も読めないAIチャットを目指す"
image: "https://cdn.arstechnica.net/wp-content/uploads/2025/12/electronic-privacy-invasion-1152x648.jpg"
---

# Signal creator Moxie Marlinspike wants to do for AI what he did for messaging - Signalの生みの親がメッセージングで成し遂げたことをAIで再現したい
AIにも「Signal級の秘密」を──Conferが目指す“会話の自律”

## 要約
Signalの開発者Moxie Marlinspikeが、AIチャットでもプラットフォーム運営者や第三者が会話を読めないようにするオープンソースのアシスタント「Confer」を公開・試験中。端末に鍵を置き、TEE（信頼実行環境）とパスキーでL﻿L﻿Mとのやり取りを暗号化する設計が特徴。

## この記事を読むべき理由
日本でも業務・個人問わずAIチャットを使う機会が増える中、会話データの取り扱いや司法・運営側からの開示リスクは現実の問題。Conferの設計は、プライバシーを重視する日本の開発者や企業にとって参考になる実装パターンを示している。

## 詳細解説
- 基本設計
  - Conferは「利用者しか読めない」ことを第一に設計されたAIサービス。ユーザープロンプト、AI応答、保存データすべてを端末側の鍵で暗号化する。
  - サービス本体（LLMやバックエンド）はオープンソースで公開され、誰でもコードとビルドの整合性を確認できる点が信頼性に寄与する。

- パスキー（Passkeys）
  - FIDO系のパスキーで32バイト相当の鍵ペアを生成。公開鍵はサーバに置くが、秘密鍵はユーザー端末の保護領域（Secure Enclaveなど）にのみ保存される。
  - 指紋や顔認証、端末PINで鍵を使えるため利便性とセキュリティを両立する。鍵で入力／出力を暗号化し、サーバ上の会話は復号不可能な状態で保存される。

- TEE（Trusted Execution Environment）とリモートアテステーション
  - LLMの実行はサーバ上のTEE内で行い、メモリや実行コードをサーバ管理者でも読み取れないようにする。
  - リモートアテステーション機能により「そのサーバ上で正しく署名されたソフトウェアだけが走っている」ことを第三者が検証できる仕組みを提供する。さらにリリースは署名・透過ログに記録される。

- 前方秘匿性（Forward Secrecy）
  - 鍵素材を定期的に更新する設計により、万一鍵が漏れても過去や将来の会話を遡って復号されないようにしている。

- 他のアプローチとの違い
  - ProtonのLumoは既存の暗号エンジンを拡張してサーバ同期や選択的保存を提供。Veniceはローカル保存に振り切る方式。ConferはTEE＋端末鍵でクラウドの利便性と高い秘匿性を両立しようとしている点が特徴。

- 実務的な背景
  - 米国では裁判所命令でチャットログの保存・提出が命じられた事例があり、事業者側の「削除したつもり」は法的には不十分になる場合がある。日本でも個人情報保護法（APPI）や国際的な捜査協力を考えると、クラウドに平文で置くリスクは無視できない。

- プラットフォーム対応
  - macOS / iOS / Androidでネイティブ対応。Windowsはサードパーティの認証ツールが必要、Linuxは現状サポート不足という点は留意点。

コードの雰囲気（簡潔化した例）
```javascript
// javascript
const assertion = await navigator.credentials.get({
  publicKey: {
    challenge: crypto.getRandomValues(new Uint8Array(32)),
    allowCredentials: [{ id: credId, type: "public-key" }],
    userVerification: "required"
  }
});
const { prf } = assertion.getClientExtensionResults();
const rawKey = new Uint8Array(prf.results.first);
```

## 実践ポイント
- 利用前に想定する脅威モデルを明確にする（「運営者に見られたくない」か「運営者・法的要求も含めて防ぎたいか」など）。
- パスキー／端末保護を有効にする（端末PIN・生体認証を必ず設定）。
- TEEとリモートアテステーションをサポートするサービスを優先する。公開されたビルドや透過ログがあるか確認する。
- 業務用途ではAPPIや社内情報管理ルールとの整合性を確認する。特に秘匿性が高いデータはローカルモデルやオンプレ実行も検討する。
- まずは非機密データで試験運用し、同期やマルチデバイス挙動を確認する。

Conferは「AIとの会話もプライベートであるべき」という明確な設計哲学を示しており、日本の開発者や企業が自分たちのデータ戦略を見直すよいきっかけになる。まずは公式リポジトリや透明性ログを確認して、実装の整合性を自社で検証することを推奨する。
