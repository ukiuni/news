---
layout: post
title: "[IntelliJ] Wayland By Default in 2026.1 EAP - 2026.1 EAPでWaylandがデフォルトに"
date: 2026-02-05T00:36:58.351Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://blog.jetbrains.com/platform/2026/02/wayland-by-default-in-2026-1-eap/"
source_title: "Wayland By Default in 2026.1 EAP | The JetBrains Platform Blog"
source_id: 410279435
excerpt: "IntelliJ系が2026.1でWaylandを既定化、IMEやウィンドウ挙動に影響あり"
image: "https://blog.jetbrains.com/wp-content/uploads/2026/02/JB-wayland-by-default-in-20261-eap_social.png"
---

# [IntelliJ] Wayland By Default in 2026.1 EAP - 2026.1 EAPでWaylandがデフォルトに
魅力タイトル: 「LinuxでIDEが変わる：IntelliJ系が2026.1から“ネイティブWayland”を標準サポート — 日本の開発現場で何が変わるか？」

## 要約
IntelliJ系IDEが2026.1 EAPからWaylandネイティブモードを自動で有効化。X11互換のXWaylandも残るため切替は可能だが、ウィンドウ管理やポップアップの挙動が変わる点に注意が必要。

## この記事を読むべき理由
日本でもUbuntuやFedora系、各種企業/クラウド環境でWayland採用が進んでおり、IDEの振る舞いが変わることで開発効率や日本語入力（IME）まわりに影響が出る可能性があるため、早めに理解・検証しておく価値があります。

## 詳細解説
- 何が起きるか：従来のXアプリとして動く代わりに、Wayland対応環境ではWLToolkit（ネイティブWayland）を自動選択して起動します。wl_display_connect()が成功すればWLToolkit、それ以外はXToolkitを使います。
- 目に見える違い：一般的なUIは同じに見えますが、Waylandではウィンドウ配置はウィンドウマネージャが完全に管理するため、ダイアログのセンタリングがされない、スプラッシュが中央表示されない、Search Everywhere等のポップアップがフレーム外へ出せない、などの現象が報告されています。
- デスクトップ統合：タイトルバーやシャドウ、角丸などのウィンドウ装飾がデスクトップテーマと完全一致しない場合があります。これらは多くのアプリで共通の課題で、Wayland実装側・アプリ側両方で改善が進められています。
- 安定性と機能改善：EAP段階でドラッグ＆ドロップやIMEサポート、各Wayland実装への安定性向上が行われており、多くの既知問題に修正が入っています。
- 互換性：Wayland非対応環境や互換性が必要な場合はXWayland（X.Org互換）を使えます。強制的にXToolkitを使うVMオプションも有効です。
- リモート開発：Remote DevelopmentモードでのネイティブWayland対応はまだ作業中で、当面はこれまで通りの挙動になります。
- オープンソース：WLToolkitやJetBrains Runtime関連の取り組みはオープンで、JetBrainsはOpenJDKのWayland対応プロジェクト（Wakefield等）にも貢献しています。

## 実践ポイント
- まずEAPで試す：2026.1 EAPで実際に動かして、自分の環境（日本語IME含む）で挙動を確認する。  
- 起動モード確認：Help → About の「Toolkit」行、または idea.log を確認して WLToolkit か XToolkit を確認する。  
- 必要ならX11に戻す：VMオプションに以下を追加して再起動することでX11（XToolkit）を強制できます。
```bash
-Dawt.toolkit.name=XToolkit
```
- 問題報告と追跡：不具合やIMEの課題はEAPフィードバック欄や該当Issueに投票・報告して改善に協力する。  
- 日本の現場向け注意点：会社の標準ディストリ/リモート環境（Wayland可否）、使用する日本語IME（ibus/ Mozc / fcitx 等）での動作確認を必ず行う。

以上を押さえておけば、Wayland移行による恩恵（近代的な描画や統合）を早期に享受しつつ、トラブルを最小限にできます。
