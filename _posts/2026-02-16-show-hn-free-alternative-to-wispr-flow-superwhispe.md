---
layout: post
title: "Show HN: Free Alternative to Wispr Flow, Superwhisper, and Monologue - Wispr Flow／Superwhisper／Monologueの無料代替"
date: 2026-02-16T22:41:17.648Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/zachlatta/freeflow"
source_title: "GitHub - zachlatta/freeflow: Free and open source alternative to Wispr Flow / Superwhisper / Monologue / etc"
source_id: 47040375
excerpt: "月額ゼロで高速・プライバシー重視のmacOS音声文字起こしFreeFlowを試す"
image: "https://opengraph.githubassets.com/70d500be67292bd59325acac1927d41a518484691b44abf9953e327e237ed712/zachlatta/freeflow"
---

# Show HN: Free Alternative to Wispr Flow, Superwhisper, and Monologue - Wispr Flow／Superwhisper／Monologueの無料代替
月額ゼロで使えるmacOS向けAI文字起こし「FreeFlow」──プライバシー重視で即時変換

## 要約
FreeFlowはSwiftで書かれたオープンソースのmacOSアプリで、GroqのAPIを使って高速かつ文脈対応の音声→テキスト変換を行う。サーバーを持たずローカルでキーを使うため、SaaSよりプライバシー配慮が高く、月額課金を避けられる。

## この記事を読むべき理由
日本でもリモート会議やメール返信の効率化、コスト削減、企業のデータ取り扱いポリシー適合が求められており、FreeFlowは低コストかつプライバシー寄りの実用解として即戦力になり得るため。

## 詳細解説
- 仕組み：マイク入力をGroqのトランスクリプションAPIで文字起こしし、さらに同社のLLMで文脈補正（宛名の正しい綴り・返信先に合わせた言い回し）を行う。処理はほぼリアルタイム（<1s）を目指す設計。
- ローカル＋クラウドの選択理由：完全ローカルのLLMを入れるとレイテンシとバッテリー消費が悪化しUXが損なわれるため、現状はクラウドAPIを利用。
- プライバシー：FreeFlow自身にサーバーはなく、端末からGroqへAPIコールが行われるのみ。データ保持やサードパーティの保存ポリシーはGroqに依存する点に注意。
- 実装面：リポジトリはGitHub（Swift主体）、MITライセンスで公開。Apple Silicon／Intel両対応のビルドが提供されている。
- UX：任意のテキストフィールドでFnキー長押しで記録・貼り付け。Monologueの「Deep Context」に相当する文脈把握を実現。

## 実践ポイント
- まず試す：GitHubからFreeFlow.dmgを入手し、Groqの無料APIキーを取得して動かしてみる。
- 日本語の挙動確認：日本語固有の名前（漢字・読み）やメーラー連携での表記崩れをチェック。必要ならポストプロセスや辞書カスタムを検討。
- セキュリティチェック：社内ポリシーで音声データ送信が許可されるか確認。機密情報は送らない運用を徹底。
- カスタマイズ／貢献：オープンソースなので、ローカルモデル統合や日本語最適化パッチをコミュニティへ提案・実装可能。
- 将来検討：ローカルLLMやオンプレミス代替が高速化すれば完全オフライン運用も現実的に。

リポジトリ参考：https://github.com/zachlatta/freeflow
