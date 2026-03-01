---
layout: post
title: "California introduces age verification law for all operating systems, including Linux and SteamOS — user age verified during OS account setup - カリフォルニア州、LinuxやSteamOSを含む全OSに年齢確認義務化 — OSアカウント作成時に年齢を検証"
date: 2026-03-01T17:41:59.881Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.tomshardware.com/software/operating-systems/california-introduces-age-verification-law"
source_title: "California introduces age verification law for all operating systems, including Linux and SteamOS &mdash; user age verified during OS account setup | Tom's Hardware"
source_id: 394728760
excerpt: "カリフォルニア州が全OSに年齢確認義務化、LinuxやSteamOSも対象"
image: "https://cdn.mos.cms.futurecdn.net/CBt66kAwURokqymNekYL97-1920-80.jpg"
---

# California introduces age verification law for all operating systems, including Linux and SteamOS — user age verified during OS account setup - カリフォルニア州、LinuxやSteamOSを含む全OSに年齢確認義務化 — OSアカウント作成時に年齢を検証
あなたのPCが「年齢確認」を聞いてくる日が来る――カリフォルニア新法がOSとアプリ開発の責任を変える

## 要約
カリフォルニア州の「Digital Age Assurance Act（AB 1043）」は、2027年1月1日からOS提供者にアカウント作成時の年齢収集と、アプリ開発者がリアルタイムで取得できる年齢APIの提供を義務付けます。対象はWindows/macOSだけでなくLinuxやSteamOSも含まれます。

## この記事を読むべき理由
米州の規制がグローバルなプラットフォーム運用に影響を与えるため、日本のソフトウェア事業者・開発者や一般ユーザーにも実務上の影響が及ぶ可能性があります。特にゲームやストリーミング、アプリ配信を行う企業は早めの対応が必須です。

## 詳細解説
- 対象と要件：OS提供者（「開発・ライセンス・制御」を行う者）は、アカウント作成時に年齢を取得し、4つの年齢区分（13未満・13〜15・16〜17・18以上）で分類するAPIを用意。アプリがダウンロードや起動時に要求すればリアルタイムで返す仕組みを義務化。
- 検証方法：法案は自己申告を想定しており、政府IDや顔認証は必須ではない（テキサスやユタの方式とは異なる）。  
- 法的効果と罰則：開発者がその年齢情報を受け取ると「実際の知識がある」と見なされ、子ども向けコンテンツ判断の責任が移る。罰則は過失で1人当たり最大$2,500、故意で$7,500（カリフォルニア州司法長官による執行）。
- 実装上の課題：多人数・共有アカウント、デバイス間プロファイル、プライバシー（アプリに年齢区分を渡すことによる情報露出）、オープンソース系の配布モデルが問題。特にArch/Ubuntuなど中央アカウントを持たないディストリビューションは実装困難で、CA向けに配布停止や注意書きになる可能性あり。
- 影響範囲：OSメーカー（Microsoft/Apple/Google/Valve）やアプリストア、ゲーム開発者、ストリーミング事業者が直接的対象。米州ユーザーを持つ日本企業も法適用・訴訟リスクを検討する必要あり。州知事は法改正を促す姿勢も示していますが、現時点で施行日は変わっていません。

## 実践ポイント
- 日本の開発者・事業者向け
  - CA居住ユーザーを扱うサービスは法案の動向を追い、年齢APIを受け取った際のコンテンツ対応ポリシーを整備する（ログ・同意・削除要件の確認）。  
  - ストアや配信プラットフォーム向けの仕様に年齢フラグ受け取り処理を追加し、誤受領時のフォールバックを設計する。  
  - プライバシー面で最小限の情報伝達（年齢区分のみ）と暗号化・アクセス制御を実装する。
- OSSメンテナ／一般ユーザー向け
  - ディストリビューションは中央アカウントを持たない場合、法的リスク回避のためCA向け配布ポリシーや注意書きを検討。  
  - ユーザーは家族共有機での年齢申告設定や、子ども用プロファイル・ペアレンタルコントロールの活用を見直す。

短期的には「自己申告＋APIの整備」で技術的対応は可能ですが、共有アカウントやオープンソース配布など実務上の摩擦が残ります。米州規制が先例となれば、同様の要件が他州や他国にも波及するリスクがあります。
