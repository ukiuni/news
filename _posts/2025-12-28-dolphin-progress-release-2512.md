---
layout: post
title: Dolphin Progress Release 2512 - Dolphin進捗リリース 2512
date: 2025-12-28 22:18:51.615000+00:00
categories:
- tech
- world-news
tags:
- tech-news
- japan
source_url: https://dolphin-emu.org/blog/2025/12/22/dolphin-progress-report-release-2512/
source_title: 'Dolphin Emulator - Dolphin Progress Report: Release 2512'
source_id: 46414916
excerpt: Dolphin 2512で遅延を大幅短縮し滑らか表示実現、対戦やモバイルで即活用できる新機能を解説
---
# Dolphin Progress Release 2512 - Dolphin進捗リリース 2512

## 要約
Dolphin Release 2512で、遅延を大幅に削減する「Rush Frame Presentation」と、フレームのバラつきを抑える「Smooth Frame Presentation」、さらにXFB即時表示やAndroid版RetroAchievements対応、ローカルBBAモードなど実用的な改良が導入された。

## この記事を読むべき理由
日本でもレトロ対戦やイベント、モバイルでの持ち運びプレイ、ローカルLANプレイ需要が根強く、これらの改善は対戦競技性の向上・配信品質改善・モバイル利便性に直結する。特にラグ感に敏感な競技プレイヤーやレトロ保存・検証をする開発者には必読。

## 詳細解説
- 低遅延の設計背景  
  GameCube/WiiのXFB（External Frame Buffer）出力経路を利用し、エミュレータ側でXFBコピーを早期に提示する「Immediately Present XFB」は、理論上コンソールに匹敵、あるいは一部環境でそれ以下の遅延を実現可能。ただしXFB処理に依存するゲーム（例：メニューで複数XFBを結合するタイトル）はフリッカーなどの不具合が出る。

- Rush Frame Presentation（新設）  
  Dolphinのスロットリング（フレーム制御）を「入力が読み取られた直後に可能な限り早くフレーム提示する」よう再配置。ホストが高速であればあるほど効果が出やすく、低フレームレートのタイトルで顕著に体感差が出る（実測で8–14msの改善例あり）。サブフレーム単位で動作するため、見た目のフレームレートは保持される。

- Smooth Frame Presentation（新設）  
  RushやImmediateと組み合わせたときに起きる“提示タイミングのばらつき”を約1–2ms遅延させて平均化し、VRRやモニタの動作域から外れないように安定化させる。XFBバイパスが原因の不規則なフレームタイミングを抑えて、滑らかな表示を取り戻す効果がある。

- 実測と検証  
  専門家（Slippi/Arte）協力のもと、専用アダプタ＋光センサで「クリック→画面変化（click-to-photon）」を測定。Wind Wakerなど理想例ではRush＋Immediateで約10ms改善、タイトル依存で効果は大きく変動。測定環境（低遅延144Hzモニタや高レートポーリングアダプタ）も結果に影響する点に注意。

- その他の実用改善  
  - Android向けにRetroAchievementsのコア機能を実装（ログイン・達成解除が可能に。ただしUIは未完成なのでWeb参照推奨）。  
  - 同一PCの複数Dolphinインスタンス間で接続できる「ローカルBBAモード」（Parsec等と組み合わせた利用に便利）。  
  - SDLベースのGameCubeコントローラ「Stock」プロファイル追加でマッピングが手早く設定可能（スティックの較正やデッドゾーン設定は推奨）。  
  - 設定をデフォルトに戻すオプション追加。

- 注意点  
  Immediately Present XFBやRushはゲームによっては表示破綻やフレームの不自然さを招くため、現状はデフォルトで無効。使う際は個別タイトルでの挙動確認が必要。

## 実践ポイント
- 試す場所：Configuration → Advanced タブで「Rush Frame Presentation」「Smooth Frame Presentation」「Immediately Present XFB」を切り替えられる。まずは1つずつ有効化してゲーム挙動を確認する。  
- 組み合わせ：Rush＋Immediateで最も遅延低減が期待できるが、見た目が崩れる場合はSmoothをオンにして安定化を試す。  
- 測定：対戦やラグが重要な場面では、高リフレッシュ低遅延モニタ＋高ポーリングアダプタで挙動を確認すると効果が分かりやすい。  
- コントローラ設定：SDL Stockプロファイルから始め、特にHall-effectスティックを使う場合はキャリブレーションとデッドゾーン調整を必ず行う。  
- Androidユーザー：RetroAchievementsを試すときは公式サイトをバックグラウンドで開いておくと達成一覧確認が楽。  
- ローカルBBA：LAN対戦やイベントで同一PC内の複数Dolphin接続が必要ならローカルBBAを活用（Parsec等のリモート操作と相性良し）。

