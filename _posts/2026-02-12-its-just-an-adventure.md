---
layout: post
title: "It's Just An Adventure - ただの冒険じゃない"
date: 2026-02-12T14:19:15.819Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/Madcarak/ItsJustAnAdventure_APK"
source_title: "GitHub - Madcarak/ItsJustAnAdventure_APK: Jeu vidéo d&#39;aventure type JDR textuel basé sur la folie"
source_id: 443519910
excerpt: "狂気パラメータで分岐するAI活用のWeb製テキストRPG、Android対応"
image: "https://opengraph.githubassets.com/c690efa996822e1845c1b39e689676cec6c80a4e283f036ee52cbbaf0e16068c/Madcarak/ItsJustAnAdventure_APK"
---

# It's Just An Adventure - ただの冒険じゃない
狂気が演出するテキストRPG──Web技術とAIで作られたダークファンタジー体験

## 要約
フランス発のテキスト主体のJDR（RPG）「It's Just An Adventure」は、主人公の「精神状態（狂気）」が物語分岐に直結するWeb/Android対応の小規模プロジェクト。JavaScript/HTML/CSSとCapacitorで構成され、AI（ChatGPT 5.2）と生成画像（Midjourney 6.1）を活用しています。

## この記事を読むべき理由
- Web技術だけで体験型ゲームを作る実例が学べる（フロントは www フォルダに集約）。
- Capacitorを使ったWeb→APK化のワークフローが見られるため、ハイブリッドアプリ化の参考になる。
- ストーリー分岐の設計やAIを補助生成に使う実践例は、プロダクト開発や企画にも応用可能。

## 詳細解説
- 技術スタック：主に JavaScript（ロジック）、HTML/CSS（UI）、Capacitor（Androidパッケージ化）。リポジトリには android、www、package.json 等が含まれます。
- ゲーム設計：コアは「ナラティブの動的分岐」。プレイヤーの選択と「精神状態（狂気）」パラメータがシナリオ分岐やテキスト出力に影響します。こうした状態管理は一般に状態オブジェクト＋分岐ロジック（条件分岐/シーンツリー）で実装されます。
- 配布と実行：ローカルでの Web 実行（ブラウザ推奨）に加え、Android 用のデバッグ APK がビルド出力として含まれています（README にビルド成果物のパスあり）。対応は Android 13 を想定。
- AI/アセット活用：テキスト生成に ChatGPT 5.2、画像は Midjourney 6.1 を利用。これによりコンテンツ制作コストを下げつつ、多彩な表現を得ています。
- 現状の課題：言語はフランス語のみ、コンテンツはデモ版。ローカライズ、アクセシビリティ、テストやセキュリティ強化の余地あり。

## 実践ポイント
- まず動かす：リポジトリをクローンして www 内の index.html をブラウザで開き、挙動を確認。Android 実機で試すならデバッグ APK を端末へインストール。
- カスタマイズ箇所：www フォルダがフロント実装の中枢。テキスト/分岐ロジックは JS ファイルにまとまっているはずなので、精神値や分岐条件を触って挙動を確かめる。
- 日本語化案：まずは JSON 等でテキストを抽出し翻訳ファイルを作成。日本語化で UX がどう変わるかを検証すると良い。
- 拡張案：自動テスト（シナリオの網羅）、アクセシビリティ（スクリーンリーダー対応）、ローカル保存によるセーブ機能追加、さらなるビルド自動化（CI/CD）を優先課題に。
- 貢献する：興味があれば翻訳、バグ報告、UI改善案のPRでプロジェクトを支援できる。小規模リポジトリはコントリビューションのハードルが低めです。

（参照元：GitHub リポジトリ "Madcarak/ItsJustAnAdventure_APK" の README 抜粋に基づく要約）
