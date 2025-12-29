---
layout: post
title: Copy of Grand Theft Auto that runs in a web browser gets taken down by DMCA
  — Take-Two Interactive says DOS Zone infringed company’s intellectual property rights
  despite disclaimers and requirement to own original copy of title for full game
date: 2025-12-27 07:39:15.242000+00:00
categories:
- tech
- world-news
tags:
- tech-news
- japan
source_url: https://www.tomshardware.com/video-games/browser-run-copy-of-grand-theft-auto-gets-taken-down-by-dcma-take-two-says-dos-zone-infringed-companys-intellectual-property-rights-despite-disclaimers-and-requirement-to-own-original-copy-of-title-to-run-full-game-online
source_title: Copy of Grand Theft Auto that runs in a web browser gets taken down
  by DMCA — Take Two says DOS Zone infringed company’s intellectual property rights
  despite disclaimers and requirement to own original copy of title for full game
  | Tom's Hardware
source_id: 437144199
excerpt: ブラウザで動くGTAがDMCAで削除され、レトロ保存と権利問題の課題が浮上
---
# 「ブラウザで動くGTA」消滅──エミュ／レトロ保存と権利の狭間で起きた一件の教訓

## 要約
ブラウザ上で動作する『Grand Theft Auto』のコピーがTake-TwoのDMCA申し立てで削除された。エミュレーション技術と著作権・配布の境界が再び問題になっている。

## この記事を読むべき理由
レトロゲーム保存やブラウザ上でのプレイ体験を追求する開発者やコミュニティにとって、技術的な実装だけでなく法的リスクの理解が不可欠だから。

## 詳細解説
今回のケースは、DOS時代のゲームをブラウザ上で動かす取り組み（DOSBox系をWebAssemblyに移植したような技術）に、原作権利者がDMCAで対応した事例。運営側は「ゲーム実行にオリジナル所有を要求」「非営利・断り書きあり」としていたが、Take-Twoはゲーム自身のバイナリや資産の配布が著作権侵害に当たると判断した。技術面では、ブラウザ実行の実現にあたって以下が使われることが多い：
- DOSBoxや互換エミュレータのWebAssembly化（emscripten等）
- ゲーム資産（音声・画像・実行ファイル）のHTTP配信
- ランタイムでのファイルマウントや仮想FS

法的には、エミュレータ本体がオープンソースであっても、ゲームのROMや実資産を第三者に配布すると権利侵害の対象になりやすい。米国のDMCAはプラットフォーム運営者に対する迅速な削除手続きを強く持っており、海外で削除されたプロジェクトはホスティングやCDNの所在によっては即時影響を受ける。日本の場合、DMCAと同一の制度はないが、プロバイダ責任制限法や著作権法の規定で類似の対応が実務上行われるため、国内運営でも無関係ではない。

## 実践ポイント
- オリジナル資産をウェブ上で配布しない：ゲーム本体やアセットの配布は最もリスクが高い。
- ライセンス取得を優先：商業タイトルは必ず権利者許諾を得るか、権利フリー素材に置き換える。
- 技術的代替を検討：プレイ体験を再現するならリバースエンジニアや独自再実装（クリーンルーム設計）やオープンソースの代替プロジェクトを検討する。
- ローカル実行へ誘導：ブラウザでの簡易ラッパーは止め、ユーザーに原盤をローカルで読み込ませる方式にする（ただし法的安全性は保証されない）。
- コミュニティ／保存団体と連携：学術的・保存的な正当性を確保するため、権利者やアーカイブ団体と事前に協議する。

