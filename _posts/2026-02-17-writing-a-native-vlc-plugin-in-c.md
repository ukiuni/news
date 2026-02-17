---
layout: post
title: "Writing a native VLC plugin in C# - C#でネイティブVLCプラグインを作る"
date: 2026-02-17T05:58:02.377Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://mfkl.github.io/2026/02/11/vlc-plugin-csharp.html"
source_title: "Writing a native VLC plugin in C# - mfkl"
source_id: 439676496
excerpt: "VLCLRでC#をAOTネイティブ化しVLC用動画フィルタや字幕プラグインを実装する手順"
---

# Writing a native VLC plugin in C# - C#でネイティブVLCプラグインを作る

VLCをC#で拡張する新常識 — .NET Native AOTで本当に「ネイティブ」なVLCプラグインが作れる

## 要約
.NET Native AOTを使って、C#でVLC 4.x向けのネイティブプラグイン（動画フィルタ／字幕レンダラなど）を作る試みと、その実装フレームワーク「VLCLR」を紹介する記事です。

## この記事を読むべき理由
VLCをただ組み込むだけでなく、VLC本体のプラグインとして.NETエコシステム（ImageSharpやML等）を直接活用できる可能性は、日本の.NET開発者にとって新しい応用領域を開きます。

## 詳細解説
- 背景
  - VLCはLibVLC（組み込み向けAPI）、Luaスクリプト、そしてネイティブプラグインという複数の拡張ポイントを持つ。ネイティブプラグインはlibvlccoreに直接結びつき、字幕レンダラやフィルタなど最も強力な拡張が可能。
- アプローチ
  - .NET Native AOTでC#コードをネイティブバイナリにAhead-Of-Timeでコンパイルし、VLCが読み込めるDLLを生成する。
  - VLCLRフレームワークは、VLCの期待するバイナリレイアウト（module descriptor、vlc_entry他）をRoslynソースジェネレータで生成し、開発者は属性と少数のメソッドを実装するだけでOK。
- 実装上の要点
  - 属性ベースでモジュール定義／キャパビリティ／設定を宣言し、ベースクラスでライフサイクル（OnOpen/ProcessFrame/OnClose）を実装するだけでエントリポイント等が生成される。
  
  ```csharp
  // csharp
  [VLCModule("dotnet_overlay")]
  [VLCCapability("video filter")]
  public partial class VideoOverlayFilter : VLCVideoFilterBase {
      protected override bool OnOpen(VLCFilterContext ctx) => true;
      protected override void ProcessFrame(VLCFrame frame) { /* 直接画素を操作 */ }
  }
  ```
  - ネイティブ構造体のバイナリ互換（フィールドオフセット／アラインメント）が最も難所。ヘッダを読み込みC#側で厳密に定義する必要がある。
  - ImageSharpを使ったフレーム上書き（文字描画やアウトライン処理）は完全マネージドでAOTに向く。描画はバッファを再利用してGC発生を抑えるのが肝。
  - プロジェクト設定の例（要点）:
    - PublishAot = true、AllowUnsafeBlocks = true、AssemblyName をlib...に変更
    - DirectPInvokeでlibvlccoreとリンク、プラットフォーム固有のネイティブライブラリを指定
- パフォーマンス
  - サンプルは1080pで視認できるフレームドロップなし。ホットパスはメモリコピー＋ImageSharp描画で、バッファ再利用によりフレームごとのGC圧は発生しない。
- 現状と展望
  - 現状はProof-of-ConceptでWindows対応が主。VLC/.NETともにクロスプラットフォームなので、Linux/macOS/モバイルへ展開可能だが構造体レイアウトの検証が必要。
  - 将来的には音声フィルタ、デマクサ、.NET MLや音声認識（例：Whisper系）をVLC内で直接走らせる応用が見込める。

## 実践ポイント
- 必要条件
  - VLC 4.x（ナイトリービルド／SDK）、.NET Native AOT対応のSDK（記事はnet10.0例）、Windows環境での検証が容易。
- 試し方（短い手順）
  1. git clone https://github.com/mfkl/vlclr.git
  2. cd vlclr
  3. dotnet publish samples/VideoOverlay -c Release -r win-x64
  4. 生成された native DLL を VLC 4.x の plugins/video_filter/ にコピーして再生
- 実装の注意
  - Cヘッダを読み込みC#構造体のバイナリ互換を厳密に検証すること（小さなオフセット誤差がクラッシュやデータ破壊を招く）。
  - フレーム処理での割り当てを避け、バッファをプールしてGCを抑える。
  - ImageSharpなど完全マネージドライブラリはAOTに適している。
- 参考
  - GitHub: mfkl/vlclr（実装とサンプル、READMEに詳細手順）

短く言えば、VLCLRは「C#でVLCそのものを拡張する」ための現実的な道を開いたプロジェクトです。興味がある.NET開発者はリポジトリをクローンしてまずサンプルを動かしてみてください。
