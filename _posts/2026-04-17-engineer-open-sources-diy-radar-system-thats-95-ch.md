---
layout: post
title: "Engineer open-sources DIY radar system that's 95% cheaper than $250,000 commercial offerings, has 20 kilometer range — Moroccan engineer designs Aeris-10 radar, shares it on GitHub - モロッコの技術者が20km到達のオープンソース・レーダー「Aeris-10」を公開、既存機の95%安で自作可能に"
date: 2026-04-17T01:27:05.599Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.tomshardware.com/maker-stem/open-source-radar-system-is-95-percent-cheaper-than-usd250-000-commercial-offerings-has-20-kilometer-range-moroccan-engineer-designs-aeris-10-radar-shares-it-on-github"
source_title: "Engineer open-sources DIY radar system that's 95% cheaper than $250,000 commercial offerings, has 20 kilometer range &mdash; Moroccan engineer designs Aeris-10 radar, shares it on GitHub | Tom's Hardware"
source_id: 359724182
excerpt: "モロッコ技術者が20km到達の低価格位相配列レーダーAeris-10をGitHub公開"
image: "https://cdn.mos.cms.futurecdn.net/JMYio8e9yrxpprPZshHDzE-899-80.png"
---

# Engineer open-sources DIY radar system that's 95% cheaper than $250,000 commercial offerings, has 20 kilometer range — Moroccan engineer designs Aeris-10 radar, shares it on GitHub - モロッコの技術者が20km到達のオープンソース・レーダー「Aeris-10」を公開、既存機の95%安で自作可能に

DIYで軍用級の“見通し”を手に入れる？Aeris-10は位相配列を軸に、商用機に匹敵する性能を低コストで実現したオープンソース・レーダーだ。

## 要約
モロッコのエンジニアが設計したオープンソース位相配列レーダー「Aeris-10」がGitHubで公開された。短距離版（10N）は約3km、拡張版（10E）は最大20km到達をうたい、部品費は数千ドル規模と商用機に比べて大幅に安い。

## この記事を読むべき理由
位相配列やFPGAを使った実戦的なレーダー設計がオープンになった点は、日本の海事・研究・DIYコミュニティにとって重要。低コストで取得可能なセンサー技術が普及すれば、小型船舶の安全装置や研究教育用の実機教材としての応用が期待できる。

## 詳細解説
- バリエーション：10N Nexus（約3km、8×16パッチアンテナ）と10E Extended（最大20km、32×16スロット導波管アレイ）。±45°の仰俯角・方位調整が可能な位相配列設計を採用。  
- 主要ハードウェア：Xilinx XCA7A50T相当のFPGAでFFT処理、Moving Target Indicator（MTI）、ドップラー速度推定、CFAR（誤検知抑制）など信号処理を実行。制御系はSTM32F746系マイコンが周波数合成器、ADC/DAC、GPS、気圧計、ステッパーや冷却系を統括。  
- ソフトウェアと公開物：回路図、PCBレイアウト、部品表、ファームウェア、制御GUIなど一式をGitHubで公開。  
- コスト感：公開者推定で部品費は10Nが約5,000USD、10Eが約7,200USD。商用位相配列システム（数十万ドル級）と比べて桁違いに安価。  
- ライセンスと配布：当初MITだったライセンスをハードウェア向けの保護を意図したCERN-OHL-PTへ変更。量産・キット化はCrowed Supply経由での提供を目指している（予定：Q3 2026）。  
- 注意点：使用周波数帯は各国で厳しく規制されるため、運用には無線局免許や法令順守が必要。開発・試験用の測定装置や安全対策にも相応の準備が必要（テスト機器の費用は高額になる可能性あり）。

## 実践ポイント
- まずはGitHubで成果物を確認し、回路やファームウェアの構成を学ぶ。  
- 興味がある組織は研究・教育用途で大学や公共研究機関と連携し、法令面を確認した上で実験計画を立てる。  
- 商用導入を考えるなら、まずは短距離版（10N）で評価し、システムの信頼性・保守性・周波数適合性を検証する。  
- 国内の海運・漁業向けセンサー導入や、大学の通信・レーダー教育に応用する道を検討すると現実的。
