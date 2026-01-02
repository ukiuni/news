---
  layout: post
  title: "Canvas VM - Piet Language Runtime - Canvas VM: Piet言語ランタイム"
  date: 2026-01-01T20:59:08.007Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://www.canvasvm.com/"
  source_title: "Canvas VM - Piet Language Runtime"
  source_id: 473551283
  excerpt: "画像をアップロードして即実行、絵をそのまま高速動作するPiet VM"
  ---

# Canvas VM - Piet Language Runtime - Canvas VM: Piet言語ランタイム
魅せるコードをそのまま実行する──「絵画コンパイラ」Canvas VMが示す新しいプログラミングの愉しみ方

## 要約
Canvas VMは、Pietという「絵がプログラムになる」エソテリック言語向けの真面目なVM兼JITで、画像をアップロードして高速にバイトコード化し、WebAssemblyやネイティブで実行できます。

## この記事を読むべき理由
- 視覚的なプログラミング表現を扱う日本の教育／ホビー層やクリエイターにとって、「絵をそのまま実行する」体験は学習・デモ・作品制作の新しい手段になるため必読です。  
- また、WASM対応でブラウザ即実行、さらにx86/ARMネイティブにJIT/ネイティブ生成できるという設計は、フロントエンド→組み込みまで幅広く応用可能です。

## 詳細解説
- 基本概念：Pietは色の塊（codel）が命令となる画像ベースの言語。Canvas VMは画像を解析して自動でcodelサイズやカラーパレットを検証し、Piet作品を汎用バイトコードに変換します。
- バイトコードIR：出力される中間表現は「21種類の命令」を持つ単純かつ移植性の高いバイトコード。一度コンパイルすればプラットフォーム非依存で配布できます。
- 実行経路：ブラウザ向けはWebAssemblyで即実行。さらにJITでx86_64機械語やARMネイティブに変換して高速実行が可能。作者ページでは「Hello World」を20ステップ・100µs台で完了する例が示されています。
- 開発者向け機能：ステップデバッガ、ブレークポイント、ウォッチドッグ、I/Oバッファリングなど、遊び心だけでなくエンジニアリング品質のツール群を備えています。
- 利便性：npmパッケージやCLIツールを提供。ブラウザのUIでドラッグ＆ドロップ、あるいはコマンドラインでコンパイル→実行が可能です。

## 実践ポイント
- ブラウザで即試す：WASM版はインストール不要。Piet作品をアップロードして動作を確認できるため、ワークショップや授業の導入に最適。
- プロジェクト組込：npmパッケージを使えば既存のJS/TSプロジェクト内でPiet画像を解析・実行できる。フロントでのビジュアルスクリプト実行やアート作品のインタラクティブ化に使えます。
```javascript
// JavaScript (例)
import init, { Canvas } from 'canvas-vm-wasm';
await init();
const canvas = new Canvas(imageData, width, height, codel);
canvas.compile();
canvas.run();
console.log(canvas.output());
```
- CI/配布：一度バイトコード（.cvm）にコンパイルすれば、軽量なバイトコードを配布してターゲット環境で実行する運用が可能。ネイティブビルドでデスクトップアプリやARMデバイス向けにも対応できます。
```bash
# CLI利用例
$ pietc compile HelloWorld.png -o hello.cvm
[OK] Compiled 21 instructions
$ piet exec hello.cvm
Hello World!
```
- 教育用途での提案：色・形で制御を表現するPietは、アルゴリズム教育やビジュアルプログラミング入門に向く。日本のカリキュラムや勉強会での導入を検討すると受け入れられやすいです。

