---
layout: post
title: "Using Servo with Slint - ServoをSlintで使う"
date: 2026-01-19T16:52:14.026Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://slint.dev/blog/using-servo-with-slint"
source_title: "Using Servo with Slint: A Journey of Rust and Rendering — Slint Blog"
source_id: 424060651
excerpt: "SlintにServoを組み込み、GPUゼロコピーで高速安全なネイティブWeb表示を実現"
image: "https://slint.dev/blog/using-servo-with-slint/banner.jpg"
---

# Using Servo with Slint - ServoをSlintで使う
Rust×レンダリングの出会い：Slintアプリに“本物の”Webビューを組み込む方法

## 要約
Slint（Rust製UIツールキット）に同じくRustで書かれたブラウザエンジンServoを統合し、ネイティブUI内でWebコンテンツを高効率に描画・操作できるようにした取り組みの技術的要点を解説します。

## この記事を読むべき理由
Webベースの認証（OAuth）や既存のWeb資産再利用、ドキュメント表示など、ネイティブUIに「安全で高速なWeb表示」を組み込みたい日本の開発者・プロダクト担当者にとって、実用的で移植性の高い実装パターンが学べます。特にRustや組込み/クロスプラットフォーム開発に関心がある人に有益です。

## 詳細解説
- なぜServoを選んだか  
  ServoはSlintと同じくRust製で、APIやビルドの橋渡しが少なく済む点が大きな利点。モジュール設計かつ活発なコミュニティがあり、ライブラリとして埋め込みやすい点も評価されています（ただし実験的要素は残る）。

- イベントループの連携（EventLoopWaker）  
  Servoは独自スレッド／ループで動き、Slintはメインスレッドのイベントループを回すため、Servo側から「描画準備ができた」と通知する仕組みが必要です。実装ではServoのEventLoopWakerトレイトを満たすカスタムWakerを作り、smol::channelでSlint側をアンブロックして同期を取っています。これが両者を同期させる“心拍”になります。

- 描画パスと性能課題  
  初期はServoがCPUメモリ上に描画したピクセルをSlint側のイメージに毎フレームコピーするソフトウェアパスを採用。実用だが性能面でボトルネックになるため、最終目標はGPU上のテクスチャをゼロコピーで再利用することです。

- プラットフォーム別のハードウェア共有手法  
  - macOS（Metal）: Surfman経由で得たIOSurfaceを使い、MetalのネイティブAPIでMTLTextureを作り、wgpuのHAL馴染みの型に変換して再利用。座標系の差（上下反転）は軽量なWGPUレンダーパスとシェーダで反転して補正。  
  - Linux / Android（Vulkan + OpenGL interop）: Vulkanで外部メモリ付きイメージを作り、vkGetMemoryFdKHRでFDを取り出す。OpenGL側はGL_EXT_memory_object_fdでそのFDをインポートし、glTexStorageMem2DEXTでバインド。ServoのフレームをglBlitFramebufferで共有テクスチャに転送（ここで反転処理含む）。最後にそのVulkanメモリをwgpu::Textureとして扱う。Androidは既存のVulkanスタックを使えるため流用可能。  
  - Windows（DirectX）: 実装作業中で、まずはソフトウェアフォールバックで動作検証を行っている段階。

- 入力処理のマッピング  
  マウス/タッチ/キーボードイベントをSlint側からServoの入力システムにマッピング。タッチはTouchPressed/Released/MovedなどをWindowEventに追加して正確に伝搬し、キーボードはキーコード変換を行ってHTMLフォーム等で正しく入力できるようにしています。

- 結果とサポート状況  
  HTML/CSSの描画、クリック・タッチ・スクロールなどの対話、デスクトップ（macOS/Linux/Windows）とAndroidでの動作確認済み例が公開されています。WindowsのGPU高速化は進行中。

## 実践ポイント
- まずはサンプルを動かす  
  Slintリポジトリの「Servo Example」をチェックして、まずはソフトウェアレンダリング経路で動作確認。実機やエミュレータで入力やスクロールの挙動を確かめるのが速いです。

- 本番ではGPUパスを目指す  
  毎フレームCPU→GPUコピーは高コスト。macOSならIOSurface/Metal、Linux/AndroidならVK_KHR_external_memory系拡張やGL_EXT_memory_object_fdのサポートを確認してゼロコピー経路を使うべきです。

- プラットフォームの要求を把握する  
  macOSはMetal／IOSurface、LinuxはVulkan拡張、AndroidはOpenGL ESプロファイルの要件があるため、ターゲットOSで必要なドライバ／拡張が利用可能か事前確認してください。

- 入力とキー変換のテストを重視する  
  タッチ・マウス・キーボードのマッピングは微妙な差が出やすい領域。日本語入力（IME）や特殊キーの動作を含めて実機で検証しましょう。

- コードを読み、改善に貢献する  
  両プロジェクトともOSSのため、実際の実装を読んで理解し、必要なら改善やバグ報告・パッチを投げることで自分のプロジェクトにも役立ちます。

日本のプロダクトでは、既存のWeb資産やOAuthフローをネイティブアプリ内で安全かつ高速に再利用したいケースが多いはずです。本記事で紹介した実装パターンは、そうしたニーズに直結する実用的な選択肢になります。興味があればまず例を動かして、ターゲット環境でのGPUパス対応から試してみてください。
