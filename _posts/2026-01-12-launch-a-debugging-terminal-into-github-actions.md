---
layout: post
title: "Launch a Debugging Terminal into GitHub Actions - GitHub Actions にデバッグ端末を起動する方法"
date: 2026-01-12T13:02:51.317Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://blog.gripdev.xyz/2026/01/10/actions-terminal-on-failure-for-debugging/"
source_title: "Using WebRTC to launch a debugging terminal into GitHub Actions | gripdev.xyz"
source_id: 46587498
excerpt: "ブラウザからWebRTCでGitHub Actionsランナーに直接接続し即時デバッグ"
---

# Launch a Debugging Terminal into GitHub Actions - GitHub Actions にデバッグ端末を起動する方法
魅力的なクリックタイトル: 「Actionsが落ちた瞬間にブラウザでその場デバッグ — WebRTCでGitHub Actionsの端末に直接つなぐ方法」

## 要約
WebRTC を使って、GitHub Actions の実行環境（ランナー）にブラウザから直接インタラクティブ端末を接続できる仕組み。シグナリングだけサーバーで行い、端末データは P2P（ピアツーピア）で流れるため低コストで安全性を高められる。

## この記事を読むべき理由
ローカルでは動くのに Actions では失敗する――この「プッシュ→待つ→プッシュ」の無限ループを短縮できる。日本の開発現場でも CI のデバッグ時間削減やコスト節約、セキュリティ対策として即効性のある手法であり、社内ポリシーやネットワーク制限下での運用注意点も理解できる。

## 詳細解説
- 背景と狙い  
  Actions の失敗時に「その場で」コマンド実行やログの確認ができれば、試行錯誤の時間を大幅に短縮できる。フルリレー型サービスは帯域コストが高くなるため、WebRTC の P2P（UDP hole punching）を使って直接データをやり取りするアプローチが採られている。

- 接続の仕組み（概念）  
  1) シグナリングサーバー：ブラウザと Actions ランナーが出会うための仲介。接続情報（ICE candidate 等）を交換するのみで、端末データは通さない。  
  2) P2P（WebRTC）：ブラウザ ←→ ランナー に直接データチャネルを張り、端末ストリーム（シェル入出力）を流す。  
  3) 認証：ブラウザは GitHub OAuth、ランナー側は Actions が発行する OIDC トークンでそれぞれ身元を証明。サーバーは双方を“引き合わせる”が、最終的な信頼はトークン検証で担保する。

- セキュリティのポイント  
  シグナリングサーバーは「紹介係」に留めるが、もし悪意あるサーバーに乗っ取られた場合のリスクを軽減するためにワンタイムパスワード（OTP）／TOTP を追加して、ランナー側が接続相手をローカルで検証する仕組みを導入している。これによりサーバーが仲介ミスをしても、OTP を知らない第三者は端末操作できない。

- 実装の主要要素（技術メモ）  
  - Actions ランナー：pty を spawn して標準入出力を WebRTC datachannel に流す。  
  - ブラウザ：xterm.js 互換のライブラリ（記事では ghostty）で表示。端末の列数／行数はフォントサイズから推定してランナー側に伝え、正しいサイズで pty を起動する。  
  - トークン検証：Actions の OIDC トークンを JWKS で検証して、実行レポジトリやトリガーしたユーザーを確かめる。  
  - ホスティング：シグナリングサーバーは極めて軽量なので、Railway のような「必要な分だけ課金」型プラットフォームでほぼ無料に近い運用が可能。サービスを「sleep」させておけるため、アイドル時のコストも小さい。

- ネットワークの注意点  
  UDP hole punching ができない（企業の厳しいファイアウォールやプロキシ環境）と P2P 接続が張れない。TURN（リレー）を用意しない限り、その環境では接続不可になる可能性が高い。日本の企業ネットワークでは要確認。

## 実践ポイント
- Actions ワークフローで id-token を許可する（workflow permissions に `id-token: write` を設定）。  
- ランナーから OIDC トークンを取得してサーバーへ送信（サーバー側で JWKS による検証を行う）。簡単な例（Node.js）：
```javascript
// javascript
const requestURL = process.env.ACTIONS_ID_TOKEN_REQUEST_URL;
const requestToken = process.env.ACTIONS_ID_TOKEN_REQUEST_TOKEN;
const url = new URL(requestURL);
url.searchParams.set('audience', 'https://your-signaling.example');
const resp = await fetch(url.toString(), {
  headers: { Authorization: `Bearer ${requestToken}`, Accept: 'application/json' },
});
const { value: id_token } = await resp.json();
```
- ランナー側で pty を spawn して datachannel へ橋渡し（概念例）：
```typescript
// typescript
const shell = pty.spawn(SHELL, [], { name: 'xterm-256color', cwd: process.env.GITHUB_WORKSPACE });
shell.onData(data => datachannel.send(data));
datachannel.onMessage(msg => shell.write(msg));
```
- セキュリティ強化：OTP/TOTP を併用してゼロトラスト的に検証する。1Password 等の自動補完が使えると運用が楽。  
- ネットワーク確認：社内ネットワークで UDP が通るか、必要なら TURN サーバー（リレー）を検討する。  
- 自前運用を検討する場合：シグナリングサーバーは軽量なので Docker 化して Railway や安価なクラウドで稼働可能。プライベート運用ならドメイン管理とログ監査を強化する。

補足：この記事ベースの実装は OSS として公開されており、無料で試せる公開デモも存在する（元記事参照）。企業で使う場合はネットワーク制約と社内セキュリティ要件を事前確認すること。
