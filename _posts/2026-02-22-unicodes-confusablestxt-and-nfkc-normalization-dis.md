---
layout: post
title: "Unicode's confusables.txt and NFKC normalization disagree on 31 characters - confusables.txt と NFKC 正規化が31文字で食い違う"
date: 2026-02-22T14:33:21.394Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://paultendo.github.io/posts/unicode-confusables-nfkc-conflict/"
source_title: "confusables.txt and NFKC disagree on 31 characters"
source_id: 399435474
excerpt: "NFKC正規化とconfusablesが31文字で衝突、ユーザー名偽装を防ぐための順序とフィルタが必須"
---

# Unicode's confusables.txt and NFKC normalization disagree on 31 characters - confusables.txt と NFKC 正規化が31文字で食い違う
魅力タイトル: 「見た目と意味がズレる危険性 — ユーザー名/スラッグ検証で見落としがちなUnicodeの落とし穴」

## 要約
Unicodeの視覚的類似文字一覧(confusables.txt)とNFKC正規化が31文字で異なるマッピングを持ち、正しい順序・フィルタがないとホモグリフ検出が誤動作する可能性があります。

## この記事を読むべき理由
ユーザー名・ハンドル・スラッグを扱うサービス（GitHubやENSと同様）は、見た目でのなりすましを防ぐ必要があります。日本のサービスでも同様の攻撃が現実的で、対策の実装順序を誤ると誤検知や致命的でないにせよ信頼を損ねる不具合を招きます。

## 詳細解説
- NFKC（Normalization Form KC）は「互換表現を意味的に縮約」します（例：全角→ASCII、数学フォント→通常文字、合字→分解）。意味的・正規化の観点で優先すべき処理です。  
- confusables.txt（UTS #39）は「見た目が似ているか」を列挙するファイルで、視覚的ななりすまし検出に使われます。目的が異なるため、両者のマッピングが食い違うケースが存在します。  
- 元記事では31件の衝突を発見。代表例：
  - 長い s (ſ, U+017F)：confusables は f にマップ、NFKCは s にマップ（視覚 vs 意味の差）  
  - 多くの“数学フォント大文字 I”など（16件）：confusablesは小文字 l に見えるとするが、NFKC→I→小文字化で i になる  
  - 数字 0 / 1 のスタイル文字：視覚的には o / l に見えるが、NFKCは正しく 0 / 1 に戻す  
- 問題点：NFKCを先に実行すべきところを逆にすると、confusablesのエントリが誤った変換を行う。逆に正しい順序では一部のconfusablesエントリは「死にコード」になります。  
- 対策としては「NFKC-aware」なconfusableマップ生成。つまり confusables.txt を取り込む前に、そのソース文字を NFKC 正規化して結果と照合し、冗長・矛盾・既に解決されるものを除外するフィルタをかける。

例：NFKC フィルタの簡易ロジック（抜粋）
```javascript
const sourceChar = String.fromCodePoint(sourceCp);
const nfkcResult = sourceChar.normalize("NFKC").toLowerCase();
// NFKC が同じターゲットならスキップ（冗長）
if (nfkcResult === confusableTarget) continue;
// NFKC が別の ASCII 文字に変わるならスキップ（衝突）
if (/^[a-z0-9]$/.test(nfkcResult) && nfkcResult !== confusableTarget) continue;
// NFKC が ASCII フラグメントに展開されるならスキップ（既処理）
if (/^[a-z0-9-]+$/.test(nfkcResult)) continue;
// それ以外は保持
push({ source: sourceCp, target: confusableTarget });
```

推奨パイプライン：
入力 → 1) NFKC 正規化 → 2) NFKC フィルタ済み confusable マップ適用 → 3) 混在スクリプト拒否（mixed-script reject）

## 実践ポイント
- 実装順序は必ず「NFKC → confusableチェック → 混在スクリプト拒否」。  
- confusables.txt をそのまま使わず、NFKC に照らしてフィルタしたマップを使う（記事作者は生データ約6,565件をフィルタして約613件に削減）。  
- 既存ライブラリを使う場合は「NFKC を先にやっているか」「confusable マップが NFKC-aware か」を確認する。  
- 自動更新するスクリプトで定期的に再生成（Unicode のバージョンに合わせて）すること。  

短くまとめると：NFKC と confusables は役割が違う。両者を組み合わせるなら「NFKC を先に実行し、confusables を NFKC に合わせてフィルタする」ことが安全で実用的です。
