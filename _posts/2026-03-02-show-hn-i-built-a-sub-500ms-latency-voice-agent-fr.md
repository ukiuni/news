---
layout: post
title: "Show HN: I built a sub-500ms latency voice agent from scratch - ゼロから作ったサブ500msレイテンシの音声エージェント"
date: 2026-03-02T23:19:53.006Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.ntik.me/posts/voice-agent"
source_title: "How I built a sub-500ms latency voice agent from scratch | Nick Tikhonov"
source_id: 47224295
excerpt: "サブ500ms音声エージェントの自作手順と高速化の実践知見で400ms達成の秘訣"
image: "https://ntik.me/voice-agent-essay/agent-logs.png"
---

# Show HN: I built a sub-500ms latency voice agent from scratch - ゼロから作ったサブ500msレイテンシの音声エージェント
会話が自然に感じられる“反応速度”を手に入れる方法 — 実戦的なアーキテクチャと最速化のコツ

## 要約
著者はTwilio→Deepgram(Flux)→LLM→TTSのストリーミングパイプラインを自作し、地理的配置とモデル選択（Groqのllama-3.3-70b等）でエンドツーエンドを約400msに短縮。商用SDKと比べ2×の改善を達成した。

## この記事を読むべき理由
音声UIはテキストとは別次元の“時間感覚”が求められます。日本のコールセンター自動化、スマートスピーカー、店頭音声UXなどで「違和感なく会話させる」ための実践的知見が詰まっており、低レイテンシ設計の優先順位を学べます。

## 詳細解説
- なぜ難しいか  
  音声は継続的でリアルタイム。重要なのは「ユーザーが話し終えた瞬間に最初の音節を出す」こと（TTFT: time-to-first-token/first-audio）。誤検知は会話の違和感に直結する。

- コアの考え方（ターンテイキング）  
  状態は2つ：ユーザーが話している / エージェントが話している。遷移は「ユーザー開始」で即座に生成とTTSを中断、「ユーザー終了」で生成→TTSをストリーミング開始すること。

- 構成（著者の実装）  
  Twilioが音声を受け取りWebSocketで送信 → Deepgram Fluxでストリーミング転写＋開始/終了イベント → 終了イベントで履歴と発話をLLMに投げる → LLMの最初のトークンを受け取り次第TTS（ElevenLabs等）へ流し、生成される音声パケットを即座にTwilioへ返す。  
  最適化例：TTSのWebSocketをプールして常時ウォームにする（接続確立で数百ms節約）、バージイン検出で生成/TTSを即キャンセル、各サービスを地理的に近接配置。

- 測定と効果  
  ローカル（遠隔）ではTTFT含め約1.6s。EUリージョンにデプロイして各サービスも近接にした結果、サーバ計測で約690ms（Twilioエッジ込みで約790ms）。さらに低TTFTの推論（Groq）を使うと平均約400msを達成。

- モデル選択の重要性  
  TTFTがボトルネックのため、最初のトークンを速く返す推論基盤を選ぶことが最も効果的。モデルサイズやプロバイダ特性（Groq vs OpenAI等）で数倍の差が出る。

## 実践ポイント
- まずはVADだけで“割り込み（barge-in）”と遷移ロジックを実装してレイテンシの下限を把握する。  
- ストリーミング転写（Deepgram Flux等）を使い、明確な start/end イベントをソースにする。  
- LLMのTTFTを計測（ファーストトークン待ち時間）し、最適なプロバイダ/モデルを選ぶ。  
- TTSは接続をウォームに：WebSocketプールで接続確立コストを削減。  
- バージイン時は即座に生成とTTSをキャンセルし、Twilio等へオーディオフラッシュ命令を送る。  
- 地理的配置を最優先：サービスとオーケストレーションを同一クラウドリージョン（日本ならTokyo/AP-Northeast）へ配置すると劇的に改善する。  
- コストと品質のトレードオフを意識：低TTFTインスタンスや専用推論は速いが高額になりうる。まずはプロトタイプで計測してから投資する。

以上を踏まえれば、既成SDKに頼らずとも「自然に感じられる」音声エージェントの核を自分で作れることがわかります。日本での導入なら、東京リージョン配置・日本語転写/TTSの品質確認・コールセンターや店舗での実地評価を早めに回すのがおすすめです。
