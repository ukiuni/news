---
layout: post
title: "Migrating to GTK3 – Re: Factor - GTK3へ移行する試み（Re: Factor）"
date: 2026-02-02T09:21:49.446Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://re.factorcode.org/2025/12/migrating-to-gtk3.html"
source_title: "Migrating to GTK3 &ndash; Re: Factor"
source_id: 817224043
excerpt: "FactorのUIをGTK2/OpenGL1→GTK3/OpenGL3へ移行、描画遅延を最適化"
---

# Migrating to GTK3 – Re: Factor - GTK3へ移行する試み（Re: Factor）
魅せるUIを現代化する：古いGTK2とOpenGL 1.xからの脱却で、Linuxデスクトップ対応を一新する理由

## 要約
Factor言語のUIバックエンドをGTK2＋OpenGL 1.xからGTK3（将来的にはGTK4）＋OpenGL 3.xに移行する作業が進行中。夜間ビルドでGTK3対応が試せ、macOS側もOpenGL 3.xに移行して広く検証中だが、描画性能の微調整がまだ必要。

## この記事を読むべき理由
日本でもUbuntuやFedoraをはじめ多くのディストリでWayland＋GTK3/4が標準化されつつあり、クロスプラットフォームなデスクトップ言語/ツール（今回ならFactor）を使う開発者やUI実装者は、移行の影響と対処法を押さえておく必要があるため。

## 詳細解説
- 背景：従来のLinuxデスクトップはX11＋GTK2が中心だったが、Waylandの普及とGTK3/4への移行で環境が変化。古いlibgtkglextやOpenGL 1.x依存は維持が難しい。
- Factorの現状：FactorはプラットフォームごとにUIバックエンドを持ち、Linuxでは長らくGTK2を利用してきた。最近、GTK4への対応PRがあり、さらにGTK3にも対応させる変更を統合した。
- OpenGLの差分：旧コードはOpenGL 1.x固定の固定機構（固定機能パイプライン）を多用していたが、GTK3/4や現代のGLコンテキストではOpenGL 3.x以降のコアプロファイル対応が求められる。これに伴い、レンダリング経路をOpenGL 3.xで再実装した。
- 現状の課題：OpenGL 3.x実装は概ね動作するが、スクロール時など一部環境で遅延が見える。旧1.x経路で行われていたキャッシュが移行後に未実装な箇所が原因の可能性があり、追加の最適化が必要。
- その他：macOS側バックエンドもOpenGL 3.xに移し、相互比較とデバッグが行えるようにしている。GTK3バックエンドは夜間ビルドで試用可能。必要なら一時的にGTK2に戻すdiffも用意されている。

コード差分（GTK2に戻す例）
```diff
diff --git a/basis/bootstrap/ui/ui.factor b/basis/bootstrap/ui/ui.factor
@@
- { [ os unix? ] [ "ui.backend.gtk3" ] }
+ { [ os unix? ] [ "ui.backend.gtk2" ] }
```

## 実践ポイント
- 試す：最新版の夜間ビルドでGTK3バックエンドを検証し、Wayland／X11両環境でスクロールやウィジェット描画を確認する。
- ドライバ確認：LinuxではMesa/ドライバのOpenGL 3.x対応状況が体感性能に直結するため、環境（libepoxyなど）の整備を先に行う。
- プロファイル：描画遅延がある場合は描画キャッシュやフレームバッファ生成周りをプロファイリングして、旧1.xで行われていたキャッシュ戦略を再導入する。
- フォールバック：問題が大きければ提示されたbootstrap差分で一時的にGTK2へ戻し、段階的に移行を進める。
- 報告：実機で再現する遅延があれば、使用環境（ディストリ名、Wayland/X11、GPUドライバ、Factorバージョン）を添えて開発側へフィードバックする。
