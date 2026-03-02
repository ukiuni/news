---
layout: post
title: "Show HN: I built a zero-browser, pure-JS typesetting engine for bit-perfect PDFs - ブラウザ不要・純JSでビットパーフェクトPDFを作る組版エンジンを作った"
date: 2026-03-02T04:46:21.031Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/cosmiciron/vmprint"
source_title: "GitHub - cosmiciron/vmprint: A pure-JS, zero-dependency typesetting engine that yields bit-perfect PDF output across any runtime—from Cloudflare Workers to the browser. Stop using Headless Chrome to print text."
source_id: 47206082
excerpt: "ヘッドレスChrome不要、純JSでどこでもビット単位再現の出版品質PDFを生成する組版エンジン"
image: "https://opengraph.githubassets.com/cfe58a384845dcd0798d40a4251c6c321f27e277e043f2b0928a9b5d4d89ac01/cosmiciron/vmprint"
---

# Show HN: I built a zero-browser, pure-JS typesetting engine for bit-perfect PDFs - ブラウザ不要・純JSでビットパーフェクトPDFを作る組版エンジンを作った
ヘッドレスChromeにサヨナラ。どこでも同一レイアウトを保証する軽量組版エンジン「VMPrint」

## 要約
VMPrintは純JavaScript・ゼロ依存で動作する組版エンジンで、同じ入力からどのランタイムでもビット単位で同一のPDFを生成することを目指すプロジェクト。

## この記事を読むべき理由
ヘッドレスChromiumや手書きのページネーションに頼らず、サーバレス／エッジ環境で再現性の高い出版品質PDFを小さなフットプリントで作れる点は、日本のワークフロー（SaaSの帳票生成、ドキュメント公開、電子書籍下ごしらえ）に直結する利点がある。

## 詳細解説
- アーキテクチャ：レイアウト（LayoutEngine）とレンダリング（Renderer）を分離。レイアウトはフォント計測→改行→ページ構成まで行い、出力は直列化可能な Page[]（JSON）になる。レンダラーはそのJSONを受けてPDFやCanvas等に描画する。
- 決定的（deterministic）な出力：実フォントファイルからグリフ幅やカーニングを読み取り、ブラウザの推定に頼らず同一入力で同一配置を保証する設計。
- ランタイム無依存：Node/ブラウザ/Cloudflare Workersなどで同じレイアウトが得られるよう、ファイルやDOMなどの環境依存APIを持たない純TS実装。フォント管理や描画コンテキストは注入可能なプラグインとして設計。
- 多言語対応：CJK、複合スクリプト、グラフェム単位の分割、言語別のハイフネーション、スペース基準／字間基準の両方の両端揃えなどを初めから考慮。RTLは現状部分対応で今後強化予定。
- 組版機能：改ページ制御（keepWithNext, pageBreakBefore）、孤立行制御（widow/orphan）、複数ページに跨る表、ドロップキャップ、フロート回り込み、分割時の継続マーカー等をサポート。
- テスト性と運用性：Page[]をスナップショット／差分できるため、レイアウト回帰テストやCIでの差分検出が容易。ヘッドレスChromeより軽量（依存含め数MiB級）で冷スタートも高速。

## 実践ポイント
- リポジトリを試す（ローカルでPDF出力）:
```bash
git clone https://github.com/cosmiciron/vmprint.git
cd vmprint
npm install
npm run dev --prefix cli -- --input engine/tests/fixtures/regression/00-all-capabilities.json --output out.pdf
```
- APIで組み込み：LayoutEngineでページ配列を作り、RendererでPDFへ描画（最小例）。
```javascript
import { LayoutEngine, Renderer, createEngineRuntime, toLayoutConfig } from '@vmprint/engine';
const runtime = createEngineRuntime({ /* fontManager等を注入 */ });
const engine = new LayoutEngine(toLayoutConfig(doc), runtime);
await engine.waitForFonts();
const pages = engine.paginate(doc.elements);
// RendererでPDFに描画
```
- 運用のコツ：フォント管理（埋め込みするフォント）を明確にし、Page[]をCIでスナップショット化してレイアウト回帰を抑える。サーバレス（Worker等）でのバッチ生成にも向く。
- 注意点：RTL完全対応はまだ強化段階。複雑な組版ルールが必要な場合は仕様確認を。

短所と利点を把握した上で、ヘッドレスChromeからの移行や、エッジでの高再現性PDF生成を試す候補として有望。興味があればリポジトリのREADMEとドキュメントを参照して実際に動かしてみることを推奨。
