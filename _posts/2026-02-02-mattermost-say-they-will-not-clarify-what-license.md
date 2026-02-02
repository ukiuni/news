---
layout: post
title: "Mattermost say they will not clarify what license the project is under - Mattermost がプロジェクトのライセンスを明確化しないと表明"
date: 2026-02-02T21:21:34.491Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/mattermost/mattermost/issues/8886"
source_title: "LICENSE: _may be_ licensed to use source code; incorrect license grant. · Issue #8886 · mattermost/mattermost · GitHub"
source_id: 46861331
excerpt: "Mattermostのライセンス表記が不明で企業導入に重大リスク発生"
image: "https://opengraph.githubassets.com/25de79b160fb50ee9e260f82dae925f040280601d1601788b533c0065ada59c7/mattermost/mattermost/issues/8886"
---

# Mattermost say they will not clarify what license the project is under - Mattermost がプロジェクトのライセンスを明確化しないと表明
魅力的なタイトル: 「OSSなのにライセンス不明瞭？Mattermostの“May be licensed”表記が日本の現場に投げかける危険信号」

## 要約
Mattermost のリポジトリで LICENSE.txt に「may be licensed」といったあいまいな文言が見られ、オープンソースとしての利用許諾が不明確になっている問題が報告されている。プロジェクト側が明確化しないことで、企業利用や法的整合性にリスクが生じている。

## この記事を読むべき理由
日本の企業開発現場ではOSSのライセンス準拠が調達・セキュリティ・法務で重視されるため、主要なチャット基盤である Mattermost のライセンス不透明は導入判断やコンプライアンスに直接影響する。

## 詳細解説
- 問題点の核心: LICENSE.txt の記述に「may be licensed」といった条件付きの表現があり、誰が何をどう許諾しているのか（利用・再配布・改変の可否）が明確でない。オープンソース定義（OSS Definition）や SPDX 形式の明示と整合しない可能性がある。
- なぜ技術的に重要か: ライセンスが曖昧だと、依存関係の再配布、商用利用、バイナリ配布、サブライセンス付与などの権利範囲が不透明になり、ライセンス互換性や企業の法務リスクを増大させる。
- 典型的な原因: 文書管理ミス、複数ライセンスの混在、商用サポート契約との混同、もしくは明示的な二重ライセンス／条件付きライセンスの表現不足。
- 留意点: 問題があるのは文言そのもの（ライセンスの「付与」表現）で、コードの品質やセキュリティとは別次元の法的リスクである点。

## 実践ポイント
- 即時対応
  - 本番導入前はライセンスを明確に確認する。疑義があれば法務に相談する。
  - 重要なプロジェクトは内部でコードをベンダリング（コピーして管理）し、ライセンス状況が明確になるまで依存バージョンを固定する。
- 技術的チェック
  - scancode、FOSSA、OSS Review Toolkit などのツールでライセンススキャンを実行する。
  - リポジトリ内の LICENSE、CONTRIBUTING、README、各サブモジュール／サブパッケージのライセンスを全て確認する。
- コミュニティ対応
  - GitHub Issue や PR で明確化を要求し、回答を記録しておく。回答が得られない場合は商用版ライセンスや代替プロジェクトの検討を。
- 日本市場向けの判断基準
  - SIer／大企業では「明確なOSSライセンス（例: MIT, Apache-2.0, GPL）」が採用条件となることが多い。調達ルールに合致しない場合は採用を見送るか、ベンダーに契約で明文化してもらう。

短く言えば、コードが使えるかどうかは技術だけでなく「誰が何を許可しているか」の明確さが鍵。ライセンスが曖昧なOSSには必ず追加の確認プロセスを入れること。
