---
layout: post
title: "ChatGPT Won't Let You Type Until Cloudflare Reads Your React State - ChatGPTはCloudflareがReactの状態を読むまで入力を許さない"
date: 2026-03-29T21:14:46.430Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.buchodi.com/chatgpt-wont-let-you-type-until-cloudflare-reads-your-react-state-i-decrypted-the-program-that-does-it/"
source_title: "ChatGPT Won&#x27;t Let You Type Until Cloudflare Reads Your React State. I Decrypted the Program That Does It."
source_id: 47566865
excerpt: "CloudflareがReactの状態を読み取りChatGPTの入力を止める仕組み"
---

# ChatGPT Won't Let You Type Until Cloudflare Reads Your React State - ChatGPTはCloudflareがReactの状態を読むまで入力を許さない
「ChatGPTが“入力を止める”理由を解剖した：Cloudflare TurnstileはブラウザだけでなくReactアプリの中身まで確認している」

## 要約
研究者がCloudflare Turnstileのバイトコードを復号し、ChatGPTの各メッセージ送信で走るプログラムが「ブラウザ指紋 + ネットワーク情報 + ChatGPTのReact内部状態」を必ずチェックしていることを明らかにした。

## この記事を読むべき理由
自動化・スクレイピング、E2Eテスト、プライバシー監査、あるいは国内サービスのCDN設計に関わる技術者は、この仕組みが自分たちのテストや運用、法令対応に与える影響を理解しておく必要がある。

## 詳細解説
- 全体像  
  CloudflareのTurnstileがブラウザで静かに動作する小さなVMプログラムを配布し、実行結果をもとにOpenAI側へトークン（OpenAI-Sentinel-Turnstile-Token）を返す。研究者は377回分を復号・解析し、チェック項目が毎回同一の55プロパティであることを確認した。

- 復号チェーン（概略）  
  サーバ応答のフィールド(turnstile.dx)をまずXORで外側バイトコードにし、その中に埋まった別の暗号化ブロブをさらに、プログラム内に埋められた浮動小数点リテラルを鍵としてXOR復号する、という手順で中身を取り出せる。鍵は送信データ内に含まれており、暗号というより難読化の様相を呈する。

- 何をチェックしているか（3レイヤー）  
  1) ブラウザ指紋（WebGL、画面サイズ、ハードウェア情報、フォント測定、DOMプローブ、ストレージ等）  
  2) Cloudflareエッジ由来のネットワーク情報（都市・緯度経度・接続元IP・リージョン等）  
  3) アプリケーション層（React内部の __reactRouterContext、route loaderのloaderData、SSRing由来のclientBootstrap）—ここが決定的で、実際にChatGPTのSPAがレンダリング・ハイドレートされていることを確認する。

- 追加レイヤー  
  Signal Orchestrator（キーダウンやポインタ移動等の振る舞い計測）やProof-of-Work（軽量なハッシュキャッシュ）も併用され、挙動・計算コストの両面からボット検知を強化している。

- トークン生成  
  収集した指紋をJSON化し、再びXORで加工して親フレームに返す流れでヘッダが形成される。検出項目はローカルストレージにも書き戻され、ページ間で持続される。

- 意味合い  
  単純なUser-Agentやヘッダ偽装だけでは突破できない「アプリケーション層でのボット検出」を実現しており、ヘッドレス／API接続だけでの自動化は失敗しやすい。難読化はあるが復号可能であり、隠蔽より運用上の柔軟性を優先する設計と考えられる。

## 実践ポイント
- 自動化／スクレイピングを行う場合は、単なるHTTPクライアントではなく「フルブラウザレンダリング（JS実行）＋ユーザー挙動の再現」が必要になる可能性が高い。  
- E2EテストやCIでは、ヘッドレスブラウザがCloudflare経由で検出されないかを検証し、必要なら実ブラウザや人間に近い入力シミュレーションを導入する。  
- プライバシー面：React内部構造やローカルストレージに書かれる指紋情報は、サービス設計・利用規約・国内の個人情報保護方針と照らして監査しておく。  
- ネットワーク運用：Cloudflareエッジヘッダに依存した判定があるため、社内プロキシや非Cloudflare経路を使う外部連携は挙動が変わる点に注意する。  
- セキュリティ／法律：端末側でアプリ内部が読み取られる設計は議論を呼ぶ可能性があるので、導入側（事業者）と利用者双方の説明責任を整理する。

出典：Buchodi「ChatGPT Won't Let You Type Until Cloudflare Reads Your React State」(要約・再構成)
