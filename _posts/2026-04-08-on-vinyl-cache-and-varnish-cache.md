---
layout: post
title: "On Vinyl Cache and Varnish Cache - Vinyl Cache と Varnish Cache について"
date: 2026-04-08T18:13:00.427Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://vinyl-cache.org/organization/on_vinyl_cache_and_varnish_cache.html"
source_title: "On Vinyl Cache and Varnish Cache - Vinyl Cache"
source_id: 1178506804
excerpt: "Varnish分裂でVinylと企業版が並走、配布元とセキュリティ判断が急務"
---

# On Vinyl Cache and Varnish Cache - Vinyl Cache と Varnish Cache について
開発者必読：なぜ「Varnish」が「Vinyl」に生まれ変わり、選択が難しくなったのか？

## 要約
Varnish Cache の FOSS プロジェクトが「Vinyl Cache」に改名・移行し、同時に Varnish Software が別途「Varnish Cache」として企業主導の派生を公開。プロジェクトの継続性やガバナンス、配布先が分かれたため、導入・運用判断が重要になっています。

## この記事を読むべき理由
日本のサイト／CDN／リバースプロキシ運用者やパッケージ管理者は、どのソースを信頼し、どのバイナリを配布・サポートすべきかを明確にする必要があります。セキュリティ情報やアップデート配信経路が変わるため見落とすとリスクになります。

## 詳細解説
- 何が起きたか：従来の Varnish Cache FOSS チームがプロジェクト名を「Vinyl Cache」に変更し、公式サイト・リポジトリを https://vinyl-cache.org および自ホストの forgejo（https://code.vinyl-cache.org）へ移行。以前の GitHub 組織はアーカイブ済み。
- 並行する別プロジェクト：Varnish Software 側は別リポジトリで「Varnish Cache」を再展開し、商用サポートや独自の追加機能・トレードマーク方針を設定。実質的に downstream（企業版）と upstream（コミュニティ版）の関係に近いが、両者は今後別方向に進む可能性がある。
- 継続性の主張：Vinyl 側の開発チームと運用プロセスは以前とほぼ同じで、古い履歴やバグ報告も保持。従ってコミュニティとしての「継続」は Vinyl にある、という立場を示しています。
- 比喩：MySQL→MariaDB のように、歴史的な FOSS が別名で続き、企業が旧名で独自路線を取る構図と類似しています。
- 技術面の影響：リリース番号やパッチ配布、脆弱性アナウンスの発信元が分散するため、依存関係や互換性、ビルドツールチェーン（VMODs や varnishtest 等）の追跡に注意が必要。

## 実践ポイント
- 供給元を明確化：配布バイナリやソースをどのリポジトリ／組織から取得するかポリシー化する（Vinyl＝コミュニティ継続、Varnish＝企業配布）。
- セキュリティ監視：脆弱性情報やパッチがどちらから出るかを両方フォロー。パッケージ保守者は upstream URL を固定して監査ログを残す。
- 互換性検証：既存 VCL、VMOD、CI/デプロイパイプラインは両プロジェクトで差分テストし、問題がなければ明示的にどちらを採用するか決定する。
- 表示と商標：パッケージ名やドキュメントでの呼称に注意。Varnish Software のトレードマーク方針が影響する可能性があります。
- 情報源の登録：Vinyl の RSS/mailing lists と Varnish Software の告知を両方登録して、変更を見逃さない。

短くまとめると、Vinyl がコミュニティの「継続」と主張する上流、Varnish は企業主導の下流的配布です。運用者はどちらを採用するかを方針化し、セキュリティ通知と互換性テストを怠らないでください。
