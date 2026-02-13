---
layout: post
title: "Zed editor switching graphics lib from blade to wgpu - ZedエディタがグラフィックスライブラリをBladeからwgpuへ切り替え"
date: 2026-02-13T14:43:13.353Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/zed-industries/zed/pull/46758"
source_title: "gpui: Remove blade, reimplement linux renderer with wgpu by zortax · Pull Request #46758 · zed-industries/zed · GitHub"
source_id: 47002825
excerpt: "ZedがLinuxレンダラーをwgpuへ移行、NVIDIA/Waylandのフリーズ解消に期待"
image: "https://opengraph.githubassets.com/d373bc132288b0a3e91a77f5e54e884c1318c2311de245c1771260a9c3e33c82/zed-industries/zed/pull/46758"
---

# Zed editor switching graphics lib from blade to wgpu - ZedエディタがグラフィックスライブラリをBladeからwgpuへ切り替え
ZedがLinuxレンダラーをwgpuに移行 — フリーズ改善とRustグラフィクス標準への大きな一歩

## 要約
ZedのLinux向けレンダラーで旧来のBladeライブラリを撤去し、Rust界隈で事実上の標準であるwgpu（WebGPU実装）へ差し替えるPRがマージされました（27コミット、+2,315 −2,030、2026-02-13）。NVIDIAやWaylandでのフリーズ問題解消を狙います。

## この記事を読むべき理由
- Zedはモダンなコードエディタで、UIレンダラーの安定性は開発体験に直結します。  
- 日本でもLinux（特に開発・サーバ環境やWSL、NixOS利用者）が多く、NVIDIA/Wayland周りの不具合は無視できません。  
- wgpu移行でBevyやIcedなどエコシステムの恩恵を受けやすくなり、将来的な機能拡張や互換性向上につながります。

## 詳細解説
- 背景：BladeはZedの既存Linuxレンダラーだが、設計・実装上の問題でユーザー側とサードパーティ（GPUI利用アプリ）で複数の不具合を生んでいた。特に「NVIDIA + Wayland（Smithay等）でのウィンドウフリーズ」が問題視されていた。  
- 変更内容：Bladeを削除し、Linuxプラットフォーム実装をwgpuベースに再実装。wgpuはクロスプラットフォームで、Rustのグラフィックス/GUIプロジェクトで広く採用されているため、他プロジェクトの改善や貢献の恩恵を受けやすい。  
- 技術ポイント：アダプタ選択ロジックやサーフェス作成、フォーマットサポート（例：Rgba16Unormのデバイス機能依存チェック）などレンダラ周りをwgpu APIに合わせて設計し直した。エラーハンドリングやサーフェス生成の安全性（unsafe を要する箇所）にレビューが入っている。  
- クロスプラットフォームの議論：wgpu自体はMac/Windowsでも動作するため、将来的には機能フラグで他OSにも切り替え可能だが、現状はLinux向け実装のマージ。Web（WASM）版についてはレンダラー以外の課題（ファイルシステムやバックグラウンドタスクAPI）が大きく、単純には「ブラウザで動くZed」にはならないとの指摘あり。  
- 影響範囲：PRは複数の既知Issue（#39097、#44814、#40481、#38497 など）を解決すると報告されている。レビューでも肯定的な反応が多く、メンテナは深いレビューを約束している。

## 実践ポイント
- 使っている人：Zedの最新ビルド（2026-02-13以降のマージ版）にアップデートして、NVIDIA/Waylandでのフリーズが改善されたかテストしてみる。問題が残る場合は該当Issueに再現手順を添えて報告する。  
- ビルド/開発者：ソースからビルドする場合、wgpuのFeatureやレンダラ実装（crates/gpui/src/platform/wgpu/*）を確認。Mac/Windows向けのwgpu導入は今後の議論対象なので、関連コードに目を通すと貢献のチャンスあり。  
- コントリビューション：改善案やハードウェア固有の再現手順（NVIDIAドライバー/Waylandコンポジタ環境情報）は高価値。PRの議論や関連Issue（例：#40481 #44814 等）を追うと動向が掴める。

関連リンク（元PR）：https://github.com/zed-industries/zed/pull/46758
