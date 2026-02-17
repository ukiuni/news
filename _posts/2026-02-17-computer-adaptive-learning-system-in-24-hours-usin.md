---
layout: post
title: "Computer Adaptive Learning system in 24-hours using a custom Whisper v3 - カスタムWhisper v3で24時間で作ったコンピュータ適応学習システム"
date: 2026-02-17T23:22:35.028Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://medium.com/@brandonin/i-just-won-the-cartesia-hackathon-reinforcing-something-ive-believed-in-for-a-long-time-language-dc93525b2e48"
source_title: "Computer Adaptive Learning system in 24-hours using a custom Whisper v3"
source_id: 439120389
excerpt: "24時間で構築した音素評価型の即時個別最適化スピーキング学習システム"
---

# Computer Adaptive Learning system in 24-hours using a custom Whisper v3 - カスタムWhisper v3で24時間で作ったコンピュータ適応学習システム

たった1日で「話す力」をリアルタイムに評価・最適化するAI学習プロトタイプ — Cartesiaハッカソン優勝の裏側。

## 要約
音声認識を音素レベルで評価し、学習者の発話に応じて次の問題を自動選択する「コンピュータ適応学習（CAT）」アプリを24時間でプロトタイプ化。即時フィードバックで習得効率を高め、特に既存の一律教材に合わない学習者（例：ディスレクシア等）への応用を目指す。

## この記事を読むべき理由
話す力（スピーキング）が重視される英語教育や発話リハビリ領域で、即時かつ個別最適化されたフィードバックは日本の教育現場やEdTechプロダクトに直結する実装アイデアだから。

## 詳細解説
- コンセプト：学習者の「現在の発話性能」を基に次に出す練習問題を決める。評価が最終試験ではなく「航法（steering）」になる。
- ASRと評価の流れ：発話 → 音声認識（語と音素レベル）→ スコア化・欠点抽出 → コンピュータ適応エンジンが次のプロンプト選定 → 学習経路更新。
- 実装（主要技術要素）：
  - 音声認識基盤：CrisperWhisper / faster-whisper とカスタムトランスフォーマで単語タイムスタンプや正確な逐語書き起こし、幻覚（hallucination）緩和。
  - 音素アライメント：Montreal Forced Alignerで音素レベルの位置取りを取得し、どの音が苦手か特定。
  - 流暢性検出：延長、置換、削除、追加、反復などをヒューリスティクスで検出。吃音・フィラーはSEP-28k、PodcastFillersなどのデータで検出器を強化。
  - 適応学習：検出結果をAIエージェントに渡し、次に出す問題を自動生成／選択するコンピュータ適応ロジックを実装。
  - インフラ／プロトタイピング環境：Notionをバックエンドとしたコンテンツ管理、Cartesiaの音声レイヤ（SST/TTS/Line Agents）、Covalで評価ワークフロー、Dell/NVIDIAのDGX Spark（GB10 Grace Blackwell Superchip）でローカルホスティング・高速推論。
- 社会的文脈：UCSFでのディスレクシア検査経験に由来し、従来手法で拾えない個別のニーズ（反復が必要、特定音の練習、即時行動可能なフィードバック）に応える狙い。

## 実践ポイント
- 音素レベル評価は日本語にも有効：モーラやアクセントの誤り検出に応用できるため、まずはMontreal Forced Aligner等で日本語音素アライメントを試す。
- フィードバックは即時かつ具体的に：どの音（音素）が苦手かを示すだけで学習効果が上がる。
- 小規模プロトタイプはローカルGPUで高速化：試作段階ではDGXクラスは不要だが、ローカルGPUでWhisper派生モデルの推論を回すと反復が速い。
- データ拡張：日本語のフィラー・吃音データが少ない場合は自前で収集・ラベル付けして検出器の性能を高める。
- 教育現場への導入は段階的に：まずは診断／補助ツールとして教員やSLP（言語聴覚士）と連携して運用するのが現実的。

興味があれば、エドテック／音声処理分野での共同実装や日本語データセット整備の議論につなげられます。
