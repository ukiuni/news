---
layout: post
title: "What's Coming with LangChainJS and Gemini? - LangChainJSとGeminiのこれから"
date: 2026-01-10T00:25:56.527Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://dev.to/gde/whats-coming-with-langchainjs-and-gemini-4ocf"
source_title: "What&#39;s Coming with LangChainJS and Gemini? - DEV Community"
source_id: 3159025
excerpt: "LangChainJSがGemini連携を一本化、マルチモーダル開発が劇的に簡素化"
image: "https://media2.dev.to/dynamic/image/width=1000,height=500,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Fcua9w23h0j5dcq29wceb.jpeg"
---

# What's Coming with LangChainJS and Gemini? - LangChainJSとGeminiのこれから
LangChainJSがGemini連携を一本化 — マルチモーダル対応で開発がぐっとシンプルに

## 要約
LangChainJSが複数に分かれていたGoogle/Gemini向けパッケージを新しい単一パッケージ「@langchain/google」に統合し、LangChainJS 1.0 と Gemini 3 のマルチモーダル機能に合わせた標準的な入出力インタフェースを提供します。公開はアルファが2026年1月予定、正式版はその後数週間以内の見込みです。

## この記事を読むべき理由
- 日本のサービスでもGoogle CloudやGeminiを利用するケース（クラウド連携、OCR・音声・画像処理を伴う機能など）が増えており、開発依存が簡素化されることで導入コストと保守負担が下がります。  
- LangChainJS 1.0 の新APIに慣れておけば、今後のマルチモーダル機能を早期に活用できます。

## 詳細解説
- 統合の背景  
  これまでGemini連携用に複数のパッケージ（@langchain/google-genai、-gauth、-webauth、-vertexai 等）が存在しており、用途や実行環境（Node／ブラウザ／Google環境）によって使い分ける必要があり混乱を生んでいました。新パッケージ @langchain/google は REST ベースで動作し、AI Studio（Gemini）とVertex AIの両方に対応、認証はAPIキー／環境変数／ADC（Application Default Credentials）をサポートします。

- LangChainJS 1.0 と標準化されたマルチモーダル処理  
  LangChainJS 0 系ではテキスト中心の扱いが基本で、マルチモーダルはモデルごとに実装がばらついていました。1.0 では以下のように標準化が進みます：
  - response.text: テキストの最終出力を常に文字列で取り出せる（後方互換も維持）。
  - response.contentBlocks: マルチモーダルなレスポンスを一貫した ContentBlock.Standard 配列で扱える（画像・音声・中間推論パートなどを明確に区別可能）。
  - 入力側も ContentBlock.Standard 形式で画像・音声等を base64 等で送信できるため、チャット＋画像解析、音声前処理などが統一的に記述可能。

- 未対応・今後の課題  
  初期リリースでは埋め込み（embeddings）、バッチ処理、メディアマネージャー、セキュリティマネージャー、非-Geminiモデル対応などが不足する可能性があり、段階的な追加が予定されています。既存パッケージは移行期間を置いて非推奨にされ、最終的に @langchain/google に一本化される方針です。

## 実践ポイント
- まず試す（インストール／簡単な呼び出し）:
```javascript
import { ChatGoogle } from "@langchain/google";

const llm = new ChatGoogle({ model: "gemini-3-flash-preview" });
const res = await llm.invoke("空はなぜ青い？");
console.log(res.text);
```

- 画像を送って問合せする例:
```javascript
import fs from "fs/promises";
import { HumanMessage, ChatGoogle, ContentBlock } from "@langchain/google";

const llm = new ChatGoogle({ model: "gemini-3-pro-image-preview" });
const data = await fs.readFile("img/parrot.png");
const content = [
  { type: "text", text: "この画像には何が写っていますか？" },
  { type: "image", data: data.toString("base64"), mimeType: "image/png" },
];
const message = new HumanMessage({ contentBlocks: content });
const result = await llm.invoke([message]);
console.log(result.text);
```

- マイグレーションのチェックリスト
  1. 既存の @langchain/google-* パッケージ使用箇所を特定する。  
  2. ChatGoogle 等のインポート先を新パッケージへ変更する。  
  3. レスポンス取得は response.text を基本にし、画像/音声等は contentBlocks を利用するようにリファクタする。  
  4. 埋め込みやバッチなど未対応機能を使っている場合は、正式版リリース前に代替策を検討する（自前の呼び出しや別ライブラリ併用など）。  
  5. CIで認証パターン（API key / ADC / env）を確認し、本番環境に合わせて設定する。

- フィードバックを出す  
  リリース初期は機能や優先度の議論が活発になります。日本語のユースケース（日本語OCRや縦書き画像、音声認識の期待動作など）を共有すると優先対応につながる可能性があります。

以上を踏まえ、まずはアルファ版で手元のユースケース（画像解析＋対話、音声入力の流れなど）を試し、正式版リリースに向けて段階的に移行計画を立てることを推奨します。
