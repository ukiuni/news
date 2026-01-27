---
layout: post
title: "postmarketOS in 2026-01: monthly blog post reboot - postmarketOS 2026年1月：月次ブログ再起動"
date: 2026-01-27T12:11:22.947Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://postmarketos.org/blog/2026/01/25/pmOS-update-2026-01/"
source_title: "postmarketOS in 2026-01: monthly blog post reboot"
source_id: 1098486484
excerpt: "*postmarketOSが2026年に再編、systemd+musl対応とCSPで旧端末を蘇らせる*"
---

# postmarketOS in 2026-01: monthly blog post reboot - postmarketOS 2026年1月：月次ブログ再起動
古いスマホを「もう一度使える」未来へ──postmarketOSが2026年に描く再編と実装のハイライト

## 要約
postmarketOSが月次レポート形式を簡潔化し、2026年の重要な進展（systemdのmusl対応、インフラ強化、貢献者支援制度の始動、Phoshの設定統合など）を発表しました。

## この記事を読むべき理由
日本でも古い端末の再利用、組み込みやコンテナでの軽量Linux需要、オープンソースのメンテナンス事情に関心が高まっています。postmarketOSの取り組みは「端末の長寿命化」と「パッケージ管理／CIの整備」という観点で日本の開発者・ホビイストに直接有益です。

## 詳細解説
- ブログ方針の変更：全てのマージリクエスト列挙から「ハイライト＋貢献者一覧」に切り替え。情報の追いやすさと感謝表明の両立を図る。
- 組織／貢献者周り：
  - Alexey M.がTrusted Contributorを退任。libapk-qtやpmbootstrap等で長期貢献。
  - Antoineが新たなTrusted Contributorに。PineNote等のe-ink機器やClockworkPi等デバイスの整備を担当。
  - ほか複数の共同メンテナー就任と、各リポジトリにmaintainers.txtを置く新運用で履歴管理が明確化。
- Contributor Support Programme（CSP）：定期報告が開始。高コミットの貢献者に対する金銭支援が実運用フェーズへ。
- インフラ／CI：
  - ハードウェア自動化テストのMVPが公開。電話発信の自動テストPOCも報告。
  - loongarch64向けedgeバイナリとCIが追加。
  - pmbootstrapの複数バージョン（3.7.0–3.9.0）リリース。
  - Nightlyリポジトリ構成の再設計と、phosh/gnome/desktop向けリポジトリ追加。
  - 新チャットルーム（a11y、hwci）設置でコラボの場を拡張。
- systemd + musl対応：
  - systemdリポジトリに「muslでの実験的ビルド」を許すPRがマージ（v259に反映）。これにより、muslベースのディストロでのsystemd統合や upstream 反映が容易に。
  - Alpineの-abuildで-systemdサブパッケージ対応になり、サービスファイルを upstream 側に任せられるようになったため、forkの削減と保守負担の軽減が可能に。
- Phoshの設定アプリ統合：
  - 以前は複数あった設定アプリ群を整理。conf-tweaksバックエンドがphosh-mobile-settingsへ統合され、カスタム設定を一つのGUIで扱えるように。

## 実践ポイント
- まずはpmbootstrapで自分の端末を試す：pmbootstrapは推奨の開発ツール。最新版（3.9.0等）を使ってビルドを試すと学びが早い。
- デバイス対応状況はpmaportsで確認：PineNoteやClockworkPiなどコミュニティ端末の情報が活発。日本で手に入りやすい端末の対応状況をチェック。
- systemd+muslの恩恵を活用：Alpineや軽量環境でsystemdを使いたい場合、最新版のsystemd（v259以降）と-abuildの-systemdサブパッケージを確認すると手戻りが減る。
- 貢献したいなら：maintainers.txtやpmaportsのMRを追い、CSPで報酬対象の作業内容を確認すると参加しやすい。
- コミュニティ参加：Matrix/IRCチャネル（#postmarketos-a11y、#postmarketos-hwci等）やFOSDEM出展で直接話を聞くと最新情報が得られる。

以上。
