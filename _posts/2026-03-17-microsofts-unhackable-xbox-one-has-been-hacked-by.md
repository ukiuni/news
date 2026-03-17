---
layout: post
title: "Microsoft's 'unhackable' Xbox One has been hacked by 'Bliss' - マイクロソフトの「ハッキング不可能」と言われたXbox Oneが「Bliss」によってハックされる"
date: 2026-03-17T16:53:03.379Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.tomshardware.com/video-games/console-gaming/microsofts-unhackable-xbox-one-has-been-hacked-by-bliss-the-2013-console-finally-fell-to-voltage-glitching-allowing-the-loading-of-unsigned-code-at-every-level"
source_title: "Microsoft&rsquo;s &lsquo;unhackable&rsquo; Xbox One has been hacked by 'Bliss' &mdash; the 2013 console finally fell to voltage glitching, allowing the loading of unsigned code at every level | Tom's Hardware"
source_id: 47413876
excerpt: "電圧グリッチでXbox Oneのブートを突破、無署名コード実行が可能に"
image: "https://cdn.mos.cms.futurecdn.net/rZ7dRyfYH7ZD7yApRmNiva-1920-80.jpg"
---

# Microsoft's 'unhackable' Xbox One has been hacked by 'Bliss' - マイクロソフトの「ハッキング不可能」と言われたXbox Oneが「Bliss」によってハックされる
ついに崩れた“鉄壁”：10年以上守られたXbox Oneが電圧グリッチで突破された話

## 要約
RE//verse 2026でMarkus “Doom” Gaasedelenが発表した「Bliss」は、電圧グリッチ（Voltage Glitching）を用いてXbox Oneのシリコン上のブート経路を破り、ハイパーバイザ〜OSレベルまで署名なしコードの読み込みを可能にした脆弱性を示した。

## この記事を読むべき理由
ハードウェア層での「修正不可能」な侵害は、コンソールセキュリティの限界を示すと同時に、デジタル保存・エミュレーション・サードパーティ開発に新たな機会と倫理的・法的課題を投げかけるため、日本のエンジニアやレトロゲーム愛好者にも直接影響する話題です。

## 詳細解説
- 手法の概念：従来のリセットグリッチとは異なり、BlissはCPUの電圧を瞬間的に崩す「電圧グリッチ」を二度連続で入れることで、初期化ルーチン（メモリ保護設定など）を飛ばし、結果としてメモリコピー処理を乗っ取って攻撃者制御のコードへジャンプさせるというもの。  
- なぜ深刻か：攻撃対象がブートROMやシリコン内部の初期化処理であるため、ソフトウェア更新では対処できず「ハードウェアレベルでの完全な妥協（unpatchable）」とされる点。ハイパーバイザやセキュリティプロセッサへのアクセスにより、暗号化されたファームやゲームイメージの復号・抽出が現実的になる。  
- 余波：合法的なデジタルアーカイブやエミュレーション研究には利点がある一方、海賊版流通や不正改造の懸念も生じる。自動化するモッドチップの開発可能性も指摘されている。

## 日本市場との関連性
- レトロゲーム保存：日本国内に残るXbox One限定タイトルやリージョン限定ビルドの保存・解析に役立つ可能性がある。  
- 法的配慮：日本の著作権・不正競争防止法との関係を慎重に扱う必要があり、無断の解析・流布は問題になる。  
- 開発者視点：ハードウェアルートの防御設計や、将来のコンソール向けセキュリティ対策の議論材料になる。

## 実践ポイント
- 技術者・研究者：RE/verseや発表資料を追い、公開情報の範囲でハードウェアレベルの防御設計を学ぶ。  
- 保存・エミュ関係者：法令順守の下で正当なアーカイブ活動を検討し、コミュニティと協力する。  
- 一般ユーザー：自己の所持ハードを不正に改造しないこと。興味がある場合は発表や研究の追跡、公式声明を待つこと。
