---
layout: post
title: "Forged Between Coal and Code - 石炭とコードのあいだで鍛えられて"
date: 2026-04-08T11:14:52.078Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://dev.to/anchildress1/forged-between-coal-and-code-phi"
source_title: "Forged Between Coal and Code - DEV Community"
source_id: 3423911
excerpt: "アパラチア炭鉱記憶をWeb技術で没入表現する制作手法と実装秘話"
image: "https://media2.dev.to/dynamic/image/width=1200,height=627,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Fmgm4kwrmc8hv3icpalx7.jpg"
---

# Forged Between Coal and Code - 石炭とコードのあいだで鍛えられて
石炭のほこりから光るダイヤへ——コードで紡ぐアパラチアの没入型メモワール

## 要約
アパラチアの炭鉱町で育った作者が、自身の体験をダイヤモンドの寓話としてCanvas・WebGL・GSAP・Howler.jsなどで可視化した没入型作品「Carbon Trace」を技術的に解説した投稿。視覚・音声・動的エフェクトを重ねて「感じさせる」ことを狙ったプロダクションだ。

## この記事を読むべき理由
日本でも「データだけでは伝わらない体験」が重要になっています。視覚×音響×インタラクションで物語を伝える手法や、少人数チームでの高品質なフロントエンド設計、AIとテストを組み合わせた実装ワークフローは、プロダクト制作やポートフォリオ制作に即役立ちます。

## 詳細解説
- 表現意図：物語は「石炭→ダイヤ→回路→光」のメタファで、回路トレースの可視化やゴーストテキスト、環境音で「感覚」を作る設計。ナレーションは作者の方言で録音し、AIでは代替できない「声」を重視。
- 技術スタック：Vanilla JS（14 ESモジュール）＋Canvas2D（画像レイヤ）＋PixiJS（WebGLで変位/ディスプレイスメント）＋GSAP（タイムライン）＋Howler.js（多重オーディオ）。DOMはテキスト/操作系、レンダリングは4層構成で各ループを独立制御。
- アーキテクチャ：5状態のステートマシン（Loading → Paused → Scene Active → Transitioning → Credits）で全サブシステムを同期。シーン定義は scenes.json に集中管理し、振る舞いは設定ベースで追加できる設計。
- オーディオ設計：Ambient と Narration の2チャンネルを並列再生。クロスフェード、プリバッファ、フェード、バッファ回復（nudge→reload→exhaustion）のエスカレーションを実装。オーディオ解析（AnalyserNode）でエフェクトに連動。
- レンダリング／効果：マスク領域限定のPixiJSエフェクト（波紋・熱・グロー）を音データで動的制御。シーン進行で「回路トレース」が徐々に明瞭になる演出。
- 開発プロセス：AIを実装・レビュー補助に活用（Claude, Copilot, Codex 等の「対抗」レビュー）、ADR（Architecture Decision Records）13件、CI（Sonar, Trivy）、テスト：685ユニット・220 E2E、Playwright、Lighthouse。画像生成はLeonardo.ai等で何百枚も試作しプロンプトルールを確立。

## 実践ポイント
- まずは一シーンのプロトタイプを作る：Canvasで画像表示、Howlerでナレーション、簡単なGSAPタイムラインを組めば没入感を試せる。
- シーンをJSONで定義して挙動を設定化する（config-firstで拡張性向上）。
- Pause対応は必須：PausableTimer や状態機構で全サブシステムを停止・復帰させる。
- オーディオは2層構成（ambient/narration）で混合制御。ブラウザのバッファ問題に備えた回復ロジックを入れる。
- 小規模でもADRを残すと意思決定が明確になり、レビューや将来の保守が楽になる。
- 参考に作品を体験：Carbon Trace（https://carbon-trace.anchildress1.dev）を音ありで見ると設計思想が直感的に理解できる。

--- 
作品は技術と個人的物語を結びつけた好例で、日本の制作現場でも学べる点が多いはずです。
