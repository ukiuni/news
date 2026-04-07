---
layout: post
title: "Issue: Claude Code is unusable for complex engineering tasks with Feb updates - Claude Codeが2月の更新で複雑なエンジニアリングに使えなくなった問題"
date: 2026-04-06T23:52:38.217Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/anthropics/claude-code/issues/42796"
source_title: "[MODEL] Claude Code is unusable for complex engineering tasks with the Feb updates · Issue #42796 · anthropics/claude-code · GitHub"
source_id: 47660925
excerpt: "2月の更新でClaude Codeの思考が消え、複雑開発で破壊的編集と品質崩壊が頻発"
image: "https://opengraph.githubassets.com/730792836c4f68ade4003869cb446151ac4f10c5a67cb3ef953c2ab3dfb65371/anthropics/claude-code/issues/42796"
---

# Issue: Claude Code is unusable for complex engineering tasks with Feb updates - Claude Codeが2月の更新で複雑なエンジニアリングに使えなくなった問題
思わず詳しく知りたくなるタイトル：深い「思考」が消えた？Claude Codeの2月以降の更新で発生した品質崩壊の全貌

## 要約
AnthropicのClaude Codeで、2月以降に導入された「thinking（内部推論） redaction」が複雑な長時間ワークフローの品質低下と強く相関しているとする分析報告。読み込みより編集を優先する挙動や、自己矛盾・未完了停止の増加など運用上の重大な影響が確認された。

## この記事を読むべき理由
日本のソフトウェア企業（組み込み、GPU/ドライバ、ML基盤など）でも長時間・高精度の自動化ワークフローが増えており、AIアシスタントの「深い思考」が減ると実務に致命的なミスを招く可能性があるため。

## 詳細解説
- データと手法：6,852セッション、234,760回のツール呼び出し、17,871のthinkingブロックを解析。redact-thinkingの段階的展開（2月中〜3月）と品質指標の悪化が時間的に一致。  
- 思考深度の低下：推定median thinking長が基準期に比べ約67%減少。redactionで可視化できなくなったが、シグネチャから深度低下は明確。  
- 挙動変化（主要指標）：
  - Read:Edit比が6.6→2.0へ低下（編集前のリサーチ不足）。  
  - 編集前未読の編集割合が6.2%→33.7%に増加（ファイル文脈無視で破壊的編集）。  
  - 全体書き換え（full-file write）が倍増（4.9%→10%）、精密な差分編集が減少。  
  - 理由ループ／自己修正の増加（ツール呼び出し当たりの逆転回数が3倍近く）。  
  - 「stop hook」（自動検出）発火が0→173回／短期間。所有回避や早期停止、許可確認の増加。  
- 影響を受けるワークフロー：複数エージェントでの長時間セッション、複雑なプロジェクト固有規約（数千語のCLAUDE.md相当）、大規模マルチファイル修正など。  
- 考察：内部の「思考トークン」を削った結果、モデルはコスト最小の行動（読み飛ばして書く、止める、簡単な回避策）を選びやすくなり、結果として品質が下がる。

## 実践ポイント
- API応答でthinking_token等の指標を要求・監視する（可視化が不可なら使用監視を強化）。  
- Canaryテストを用意：長時間セッション／多ファイル変更に対する品質ゲートを自動化（read:edit比や編集前未読率を監視）。  
- CIで自動差分検証と大規模リグレッションテストを追加し、AI出力の「破壊的編集」を検出。  
- モデルバージョン固定（pin）とロールバック計画を用意。更新後は必ず既存ワークフローで回帰テスト。  
- ベンダーへ要望：思考予算の階層（"max thinking"プラン）、thinkingメトリクスの開示、パワーユーザー向けのカナリア指標提供。  
- 短期対策：重要タスクは細分化して安定性を確かめる、出力に対する自動検証ステップを挟む。

以上を踏まえ、長時間・高度処理をAIに委任する現場は「思考トークン」の可視化と品質ゲート構築を急ぐべきです。
