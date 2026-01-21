---
layout: post
title: "AsciiDoc Manifesto: Helping Users Understand Its Core Purpose - AsciiDoc マニフェスト：目的を明確にする宣言"
date: 2026-01-21T12:16:19.803Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/mcoderz/the_asciidoc_manifesto"
source_title: "GitHub - mcoderz/the_asciidoc_manifesto: The AsciiDoc Manifesto defines the philosophy, purpose, and principles of the AsciiDoc language and its ecosystem. It explains why AsciiDoc exists, distinguishes the language specification from its processors, and provides a shared conceptual framework for users, implementers, and contributors."
source_id: 421268391
excerpt: "AsciiDocマニフェストは仕様と処理系を分離し、ドキュメント標準化や社内導入の実践ガイドを示す必読だ"
image: "https://opengraph.githubassets.com/b9cd49bbf1e96a32b3fabbc17ff9225d76ca1cf60b5b28b8c3c436597459c8c6/mcoderz/the_asciidoc_manifesto"
---

# AsciiDoc Manifesto: Helping Users Understand Its Core Purpose - AsciiDoc マニフェスト：目的を明確にする宣言
AsciiDocの本質とエコシステムの役割を短く示す、ドキュメント文化を変える「設計思想」の案内書

## 要約
AsciiDoc Manifestoは、AsciiDoc言語の哲学・目的・原則を明文化し、言語仕様（spec）と処理系（processor）を切り分け、利用者・実装者・貢献者の共通理解を作ることを目的としたコミュニティ主導の宣言文書です。

## この記事を読むべき理由
技術ドキュメントがプロダクト価値を左右する現在、AsciiDocは「ソース管理しやすいプレーンテキスト＋豊かな表現」の選択肢として注目されています。日本のエンジニアやドキュメンテーション担当が、社内外のドキュメント標準化やオープンソース貢献を進める際の指針になるため必読です。

## 詳細解説
- 何が含まれるか：リポジトリは主文書（manifesto.adoc）、エコシステム解説（ecosystem-guide.adoc）、参考リソース集（resources.adoc）、READMEを収録。まずマニフェストを読み、目的と価値観を把握することを推奨しています。  
- 中核の主張：ドキュメントは装飾ではなく「知識の保存と伝達」であるという価値観の提示。言語仕様（何を表現できるか）と処理系（実際にHTML/PDFに変換するツール）は別物として扱うべき、という明確な区別を設けています。  
- 対象別ガイド：新規ユーザー、Working Groupメンバー、実装者それぞれに対する行動指針を用意。例：新規はマニフェスト→Asciidoctorドキュメント→Zulip参加、実装者は言語仕様を学びTCKでテスト、など。  
- 貢献フロー：小さな修正はプルリクで、哲学的・重大な変更はまずAsciDocのZulipチャネルで議論して合意を形成してからPRする、という手順を推奨。これにより共同体の合意形成が担保されます。  
- ライセンスと理念：文書はCC0（パブリックドメイン相当）で公開され、自由な利用と改変が可能。コミュニティ主導であり、現時点では公式文書化が最終目的だがまだ正式採用前である点も明記されています。

## 実践ポイント
- 今すぐやること：まずマニフェスト（manifesto.adoc）を読む。続けてecosystem-guideで「仕様と処理系の違い」を理解する。  
- 学ぶ／使う：Asciidoctor公式ドキュメントで構文を学び、既存ツールで変換ワークフローを試す。  
- 貢献する：小さな誤字修正や補足はGitHubでPR。理念的な提案や仕様議論はAsciiDocのZulipチャネルで議論を開始してからPRを作る。  
- 実務への活用：社内ドキュメントの標準化候補としてAsciiDocを提案する際は、本マニフェストの哲学（保存性・可搬性・共同体合意）を根拠にすると説得力が増します。CI/CDやバージョン管理との相性も良いため、既存のドキュメントパイプラインに組み込みやすい点を強調しましょう。  
- 互換性確認：処理系を独自に使う／作る場合はTCK（互換性テスト）で挙動を検証すること。

短くまとめると、AsciiDoc Manifestoは「言語の目的と共有ルール」を示す地図です。日本での技術文書の品質向上やオープンソース貢献を考えるなら、まずこの地図を手に取る価値があります。
