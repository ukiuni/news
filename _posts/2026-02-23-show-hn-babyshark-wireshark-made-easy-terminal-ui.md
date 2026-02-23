---
layout: post
title: "Show HN: Babyshark – Wireshark made easy (terminal UI for PCAPs) - Babyshark：Wiresharkをターミナルで手軽に"
date: 2026-02-23T22:52:43.492Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/vignesh07/babyshark"
source_title: "GitHub - vignesh07/babyshark: Flows-first PCAP TUI (case files, gorgeous UX)"
source_id: 47128535
excerpt: "TUIでPCAPを即解析、フロー優先で問題箇所を素早く特定できるBabyshark"
image: "https://opengraph.githubassets.com/f721a8404b9df6b80c46e76e07200b7714bfae15810f9b85e798ded142d89646/vignesh07/babyshark"
---

# Show HN: Babyshark – Wireshark made easy (terminal UI for PCAPs) - Babyshark：Wiresharkをターミナルで手軽に

GUI不要でPCAP解析がサクッとできる—TUI版Wireshark「Babyshark」でネットワークの「何が起きているか」を即把握

## 要約
Babysharkは「フロー優先」のターミナルUI（TUI）でPCAPを素早く探索できるツールです。オフラインPCAP閲覧と、tsharkを使ったライブキャプチャに対応し、初心者でも「何をクリックすれば次に調べるべきか」が分かる導線を提供します。

## この記事を読むべき理由
日本の現場でも、GUIのないサーバーやリモート調査、あるいは障害時の素早い切り分けが求められます。軽量なTUIで流量（フロー）ベースに把握できるBabysharkは、Wiresharkの代替または補完になり得ます。

## 詳細解説
- フロー優先（Flows-first）: パケット単位ではなく「通信フロー」を一覧して重要な会話（上位トーカー、高レイテンシ、RSTや再送など）を素早く発見できる設計。
- 主なビュー: Overview（サマリ）、Domains（サービス別）、Weird（問題候補）、Flows（フロー一覧）→ Packets → Follow stream。ドリルダウンしやすい導線が特徴。
- TUI操作: キー操作でドリルダウン（Enter）、フィルタ（/）、TCP/UDP切替（t/u）、ブックマーク（b）、レポート出力（E）などが可能。
- オフライン/ライブ両対応:
  - オフライン: .pcap / .pcapngを直接読み込んで解析。
  - ライブ: tshark（WiresharkのCLI）が必須。キャプチャ時に表示フィルタやファイル書き出しも可能。
- 出力・ケース管理: .babyshark ディレクトリにブックマークや Markdown レポートを保存。インシデントの証跡や共有が容易。
- 実装・配布: Rustで実装。GitHub Releasesにバイナリあり。ソースからcargoでビルド可能。ライブにはtsharkとキャプチャ権限が必要。
- 今後の改善予定: TCP再組立の強化、プロトコルヒント改善、パッケージ配布（Homebrew/Scoop）など。

## 実践ポイント
- 試すコマンド例（ターミナル）:
```bash
babyshark --pcap ./capture.pcap
```
```bash
babyshark --list-ifaces
```
```bash
babyshark --live en0 --dfilter "tcp.port==443" --write-pcap /tmp/live.pcapng
```
- インストール: まずはGitHub Releasesからバイナリを落とすのが手っ取り早い。ソースからはRust toolchainが必要：
```bash
cargo install --git https://github.com/vignesh07/babyshark --bin babyshark
```
- ライブ解析の注意: tsharkをインストール（macOS: brew、Ubuntu: apt）し、キャプチャ権限（sudoやdumpcap権限付与）が必要。
- 日本での使いどころ: GUIが使えないリモートサーバのトラブルシュート、ヘッドレス環境での簡易監視、インシデント対応の初動切り分けや報告書作成に有効。
- ワークフロー提案: まずOverviewで「何が多いか」を把握 → Domainsでサービスを確認 → Weirdで異常候補を抽出 → 該当フローをFollow streamし、必要ならブックマーク＆Markdownで証跡保存。

興味があればリポジトリ（https://github.com/vignesh07/babyshark）をチェックして、手元のPCAPで試してみてください。
