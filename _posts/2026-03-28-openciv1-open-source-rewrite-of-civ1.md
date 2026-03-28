---
layout: post
title: "OpenCiv1 – open-source rewrite of Civ1 - OpenCiv1（Civilization 1 のオープンソース再実装）"
date: 2026-03-28T22:29:00.447Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/rajko-horvat/OpenCiv1"
source_title: "GitHub - rajko-horvat/OpenCiv1: Open source rewrite of the original Civilization 1 Game designed by Sid Meier and Bruce Shelley in year 1991 · GitHub"
source_id: 47557064
excerpt: "Civ1を.NET/Avaloniaで再構築、オリジナル資源で遊べるオープンソースプロジェクト"
image: "https://opengraph.githubassets.com/49b29524971b9ae0fb9406cb8b76358ed00100ebf947f7840f4dcffc1dddc8d3/rajko-horvat/OpenCiv1"
---

# OpenCiv1 – open-source rewrite of Civ1 - OpenCiv1（Civilization 1 のオープンソース再実装）
魅力タイトル：懐かしの「Civ1」をモダンに復活させるプロジェクト――自分で動かし、直せるレトロ戦略の再誕

## 要約
1991年の名作「Civilization 1」を、著作権に配慮しつつ.NET 8＋Avaloniaで書き直したオープンソースプロジェクト。元の挙動を再現しつつ、クロスプラットフォーム化と将来的な機能拡張を目指している。

## この記事を読むべき理由
レトロゲームの保存・再活用に興味がある開発者、.NETやクロスプラットフォームGUIに触れてみたい人、あるいはCiv好きで「自分で直したい／翻訳したい」人にとって、実践的に関われる入口があるから。

## 詳細解説
- 技術スタック：言語はC#、ランタイムは.NET 8、UIはAvalonia（Windows / Linux / macOS 対応のクロスプラットフォームUIフレームワーク）。コードはMITライセンスで公開。
- 再実装の方針：オリジナルはDOS／16bitで著作権があるため、ゲーム本体のコードや資源はそのまま含めない。DOS版（バージョン475.05）の逆アセンブルを参照し、一部は仮想CPUで旧アセンブリをエミュレート、その他はC#で書き直して挙動を再現している。
- 著作権と起動条件：公開リポジトリだけでは完全動作しない。法的にはユーザー自身がオリジナルDOS版のリソース（.txt, .pic, .pal 等）を所有している必要がある。将来的にはグラフィック／音声を著作権フリーのものへ完全置換予定。
- 現状と目標：現状はプレイ可能（但しオリジナル資源が必要）。短期はコード置換とバグ修正、中長期はWeb化（Razor）、高画質グラフィック／音声、マルチプレイヤー、プラグイン対応などを計画。
- コントリビュートの入口：バグ報告、擬似アセンブリ→C# 翻訳、デフォルト／カスタムのビジュアル＆音声テーマ作成（SVG、MIDI/SoundFont 推奨）など明確なタスクがある。

## 実践ポイント
- まず試す：リポジトリをクローンして dotnet build -c Debug でビルド（.NET 8 SDK 必須）。公開リリースはオリジナルDOS版のインストールディレクトリにリリースファイルを置いて実行。
- 必要環境：.NET 8、（Windowsでは）Visual C++ 2015–2019 再頒布パッケージが必要な場合あり。
- 貢献方法：Issue提出／翻訳作業／テーマ制作／テスト。開始前にリポジトリの CONTRIBUTING と README を確認。
- 法的注意：オリジナルのゲーム資源を第三者に配布しないこと。個人で保有して動かす分にはプロジェクト方針に沿っている。
- 日本向けの着眼点：日本語翻訳やローカライズ、MIDIベースの音源差し替え、日本のレトロゲームコミュニティとの協業は貢献しやすく効果的。

興味がある人は GitHub の rajko-horvat/OpenCiv1 をチェックし、Civilization Fanatics Forum やリポジトリの Issue で参加してみてください。
