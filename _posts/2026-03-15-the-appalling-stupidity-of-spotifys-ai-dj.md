---
layout: post
title: "The Appalling Stupidity of Spotify's AI DJ - SpotifyのAI DJの驚くべき愚かさ"
date: 2026-03-15T09:28:25.457Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.charlespetzold.com/blog/2026/02/The-Appalling-Stupidity-of-Spotifys-AI-DJ.html"
source_title: "Charles Petzold: The Appalling Stupidity of Spotify’s AI DJ"
source_id: 47385272
excerpt: "SpotifyのAIが交響曲の楽章順を無視し再生を混乱させる"
image: "https://www.charlespetzold.com/blog/2026/02/SpotifyDJ.png"
---

# The Appalling Stupidity of Spotify's AI DJ - SpotifyのAI DJの驚くべき愚かさ
AIが「交響曲」をめちゃくちゃに再生する時代：SpotifyのAI DJが露呈した音楽メタデータの根本問題

## 要約
SpotifyのAI DJがクラシック音楽の「作品＝複数楽章」という基本を理解できず、検索や再生で滅茶苦茶な順序や混合録音を再生する問題を報告。根本原因はポップ中心のメタデータ設計とAIの知識統合不足にある。

## この記事を読むべき理由
日本でもクラシック指向のユーザーや文化機関、音楽配信事業者が増える中で、ストリーミングAIが伝統的音楽表現を正しく扱えないと利用体験やアーカイブ活用に重大な影響を与えるため。

## 詳細解説
- 問題の症状：ユーザーが「Beethoven 7th Symphony」を要求しても、2楽章（Allegretto）だけを再生したり、楽章をバラバラかつ別録音で順不同に流したり、全く別ジャンルへ切り替えたりする。明確な「全楽章」指定でも誤再生が続く。
- 根本原因（技術面）
  - メタデータ設計が「Artist / Album / Song」中心で、クラシックの「composition/work」「movement」を表現するスキーマが弱い。結果として楽章の所属関係や順序が欠落する。
  - 学習データとビジネス要件がポップ偏重：AIは頻度の高いパターンを優先し、クラシック固有の構造を学習・優先できていない。
  - 検索・再生パイプラインの知識統合不足：外部知識（Wikidata/MusicBrainz等）やアルバム内のトラック順を参照して「作品単位」で正規化する処理が弱い。
  - プロンプト解釈とランダム化（「switch the vibe」的な推薦ルール）により、意図した明確な楽曲構成が破壊される。
- 可能な技術的対策
  - 楽曲を「ワーク／楽章」単位で一意に識別するメタデータ設計（MusicBrainzのwork/entity、ISWCなど）の導入。
  - 検索時にアルバムのトラック順を優先するルール、あるいは「演奏順を尊重する」再生モードの追加。
  - クラシック専用NLPプロンプトパイプラインの導入と外部知識ベース（Wikidata/Wikipedia/楽曲DB）との照合。
  - 推薦システムの多様性制御：明示的な要求（“complete”, “in order”）への高いコンプライアンスと、自動でのジャンル切り替え抑制。

## 実践ポイント
- ユーザー向け
  - クラシックは「Album」を選ぶ、検索語に「full」「complete」「movements I–IV」などを明記する。
  - 専門サービス（Idagio, Primephonic 等）や公式アルバム/演奏者のページを利用する。
  - 明確に誤動作する場合はフィードバック機能で報告する。
- 開発者／運用者向け
  - メタデータ設計を作品（work）中心に拡張し、外部識別子を導入する。
  - 検索→再生パイプラインでアルバムのトラック順と作品所属を優先するロジックを実装する。
  - クラシックを含む非ポップ領域のQAテストケースを追加し、モデルの推薦ルールをチューニングする。

短い結論：AIは期待通りに「賢く」動くとは限らない。特にクラシックのような構造化されたドメインでは、適切なメタデータ設計と外部知識統合が不可欠だ。
