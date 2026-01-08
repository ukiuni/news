---
  layout: post
  title: "Xmake v3.0.6 Released, Android Native Apps, Flang, AppImage/dmg Support - Xmake v3.0.6 公開、Android ネイティブアプリ・Flang・AppImage/dmg 対応"
  date: 2026-01-04T14:08:10.070Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://xmake.io/posts/xmake-update-v3.0.6.html"
  source_title: "Xmake v3.0.6 Released, Android Native Apps, Flang, AppImage/dmg Support | Xmake"
  source_id: 471295340
  excerpt: "Xmake 3.0.6でAndroid強化、bin2obj高速化とAppImage対応"
---

# Xmake v3.0.6 Released, Android Native Apps, Flang, AppImage/dmg Support - Xmake v3.0.6 公開、Android ネイティブアプリ・Flang・AppImage/dmg 対応
Androidゲームのカスタムエントリから、FortranビルドやAppImage/dmg配布まで──Xmake 3.0.6で「速さ」と「実用性」が一段と向上。

## 要約
Xmake 3.0.6はAndroidネイティブアプリの細かな設定、bin2objによる大容量アセット埋め込みの超高速化、Flangサポート、Qt向けxpackでのAppImage/dmg対応、CI向けの構文チェックなど実践的な機能強化を含むアップデートです。

## この記事を読むべき理由
日本はモバイルゲーム、組み込み系、科学技術計算、デスクトップGUIアプリの市場がいずれも重要です。本バージョンはこれら領域でのビルドフロー短縮や配布対応を直接改善するため、開発効率とデリバリー品質の向上に直結します。

## 詳細解説
- Androidネイティブアプリ対応の強化  
  android.native_appルールでSDKバージョン、AndroidManifest、リソース、keystoreやパッケージ名などを細かく指定可能に。ゲームエンジン統合などで既存のandroid_native_app_glueを無効化するオプション(native_app_glue = false)も追加され、独自のイベントループを使う場面に対応します。

  ```lua
  lua
  add_rules("android.native_app", {
    android_sdk_version = "35",
    android_manifest = "android/AndroidManifest.xml",
    android_res = "android/res",
    keystore = "android/debug.jks",
    keystore_pass = "123456",
    package_name = "com.example.custom",
    native_app_glue = false,
  })
  ```

- bin2obj：大容量バイナリ埋め込みの圧倒的高速化  
  utils.bin2objルールはバイナリを直接オブジェクト（COFF/ELF/Mach-O）化してリンクするため、従来のbin2c（Cコード生成→コンパイル）より劇的に高速。例では120MBで約1.8秒対354秒という差が報告されています。SPIR-Vやアイコン、音声データなど大規模アセットの埋め込みに最適です。

  ```lua
  lua
  add_rules("utils.bin2obj", { extensions = { ".bin", ".ico" } })
  add_files("assets/data.bin", { zeroend = true })
  ```

  C側では自動生成されたシンボルでアクセス可能（例：_binary_data_bin_start/_end）。

- Flang（LLVM Fortran）ツールチェイン対応  
  Fortranプロジェクトが容易にビルド可能に。自動検出または手動指定で利用できます。

  ```bash
  bash
  xmake f --toolchain=flang
  xmake
  ```

- QtパッケージとAppImage/dmg対応（xpack）  
  Qtアプリのデプロイパッケージをxpackで生成可能。Linux向けAppImage、macOS向けdmgをサポートし、クロスプラットフォーム配布が簡素化されます。

  ```lua
  lua
  includes("@builtin/xpack")
  add_rules("qt.widgetapp")
  xpack("qtapp"):set_formats("nsis", "dmg", "appimage", "zip")
  ```

- CI向けの高速構文チェックとデバッグ改善  
  `xmake check syntax`でコンパイラの構文チェックフラグを使い、フルビルドなしで速やかに構文エラー検出が可能。CLionプラグインの強化でLLDB/GDB-DAP対応やcompile_commands.json自動更新によりIDE統合が改善されています。

- その他ユーティリティ/改善  
  MSVCの動的デバッグサポート、binutilsのシンボル操作（readsyms、deplibs、extractlib）、CUDA 11〜13サポートなど開発実務で役立つ機能が多数追加・改善されています。

## 実践ポイント
- Androidゲームで独自エントリや独立したイベントループを使う場合、native_app_glue = falseを使い既存のGlueを替えることで統合が楽になる。署名情報やリソースの指定もxmake.luaで一元管理を。
- 大きなバイナリやSPIR-Vシェーダの埋め込みはutils.bin2objに切り替えるだけでCIやローカルビルド時間が劇的に改善する（特にアセット多数のゲーム・マルチメディアアプリで効果大）。
- Fortran（科研・数値計算）プロジェクトはFlangツールチェイン指定でxmake移行を検討すると、ビルド定義のモダン化とマルチ言語混在プロジェクトの管理が容易に。
- デスクトップ配布（Linux/macOS）ではxpackでAppImage/dmgを生成し、配布パイプラインを自動化することでユーザー体験を改善できる。
- CIには`xmake check syntax`を組み込み、無駄なビルド時間を削減してプルリクのフィードバックループを短縮する。

短くまとめると、Xmake 3.0.6は「実務で使える」改善が中心。特に日本のゲーム開発、組み込み、科学技術計算、デスクトップ配布を行うチームはアップデートの恩恵を即座に受けられます。
