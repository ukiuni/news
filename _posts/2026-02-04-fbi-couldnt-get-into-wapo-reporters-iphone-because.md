---
layout: post
title: "FBI Couldn't Get into WaPo Reporter's iPhone Because Lockdown Mode Enabled - FBIがワシントン・ポスト記者のiPhoneを解除できなかった理由：Lockdown Modeが有効だったから"
date: 2026-02-04T14:48:48.234Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.404media.co/fbi-couldnt-get-into-wapo-reporters-iphone-because-it-had-lockdown-mode-enabled/"
source_title: "FBI Couldn’t Get into WaPo Reporter’s iPhone Because It Had Lockdown Mode Enabled"
source_id: 46886237
excerpt: "FBIが解析に失敗した記者のiPhoneはLockdown Modeが外部解析を阻んだ実例"
image: "https://www.404media.co/content/images/size/w1200/2026/02/245839225_3814a454f9.jpg"
---

# FBI Couldn't Get into WaPo Reporter's iPhone Because Lockdown Mode Enabled - FBIがワシントン・ポスト記者のiPhoneを解除できなかった理由：Lockdown Modeが有効だったから
驚きの防御力：Lockdown ModeでFBIがiPhoneを解析できなかった実例と、日本での教訓

## 要約
米国の取材先捜索で押収された記者のiPhoneが、Appleの「Lockdown Mode（ロックダウンモード）」が有効だったためFBIの解析チームで抽出できなかったと裁判記録に記載されました。ローカル接続や一部機能を制限することで外部からの解析を困難にする機能の有効性が示されています。

## この記事を読むべき理由
iPhoneの普及率が高い日本でも、取材・内部告発・機密データの扱いで端末が法執行機関に押収される可能性は現実的です。今回の事例は、一般ユーザーでも利用できる防御機能が実際のフォレンジック（鑑識）を阻む効果を持つ可能性を示しています。

## 詳細解説
- 何が起きたか：記者の自宅捜索でiPhoneが発見され、端末は「Lockdown」と表示されたまま電源オンで充電されていました。FBIのComputer Analysis Response Team（CART）はその端末のデータ抽出に失敗したと裁判書類に記載されています。
- Lockdown Modeの仕組み（要点）
  - リモート攻撃面を削減：特定のメッセージ添付やウェブの挙動を制限。
  - 接続制限：外部アクセサリやコンピュータとの接続は端末がアンロック済みで明示的承認が必要に。
  - 通話・メッセージ制限：FaceTimeなどの着信についても直近の相手以外をブロックする設定がある。
- フォレンジックと物理接続ツール：
  - GrayKeyやCellebriteのような市販・法執行向けツールは物理接続やOSの脆弱性を突くことで抽出を試みますが、Lockdown Modeはその攻撃面や一部脆弱性を塞ぐ設計です。
- Before First Unlock (BFU) の重要性：電源オフ後に未解除の端末は解析がさらに難しくなる「BFU」状態となり、これも解析阻害要因になります。
- 補足事例：同じ家から押収された別のMacBook Proは指紋認証で解除され、Signalデータの一部は閲覧されたことが裁判記録にあります。つまり、端末の設定（生体認証の有無、電源状態、Lockdownの有効化）が結果を左右します。

## 実践ポイント
- まず試す（すぐできる）
  - iPhoneの「設定」→「プライバシーとセキュリティ」→「Lockdown Mode」を有効化する。
  - システムを最新のiOSに更新する。
- 端末運用の基本
  - 重要な調査や取材では、端末をロックして電源を切らずに保管するか、逆にBFUを利用するなど運用ポリシーを明確にする（状況により判断）。
  - 生体認証を使わない設定（パスコードだけにする）を検討する。生体は場面によっては端末解除を容易にする。
- 高リスク向け対策
  - 機密情報は端末単体に置かない／暗号化された外部ストレージや安全なクラウドを併用する。
  - ジャーナリストや研究者はLockdown Modeやエンドツーエンド暗号化アプリ（例：Signal）を理解し、運用ルールを整備する。
- 法的・現実的注意
  - 捜査時の取扱いや強制の法律は国によって異なるため、実際の行動は法務アドバイザーと相談してください。

以上。Lockdown Modeは万能ではないが、現実の場面で有効に働いた事例として日本のテック／報道関係者にも知っておいて損はない機能です。
