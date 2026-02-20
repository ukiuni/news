---
layout: post
title: "Can Regular Expressions Be Safely Reused Across Languages? - 正規表現は言語を越えて安全に再利用できるか？"
date: 2026-02-20T18:26:36.675Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.i-programmer.info/programming/176-perl/13051-can-regular-expressions-be-safely-reused-across-language-boundaries.html"
source_title: "Can Regular Expressions Be Safely Reused Across Languages?"
source_id: 402142815
excerpt: "Stack Overflowの正規表現、言語差で誤動作や性能事故に繋がる—実機テスト必須"
---

# Can Regular Expressions Be Safely Reused Across Languages? - 正規表現は言語を越えて安全に再利用できるか？
Stack Overflowでコピペした正規表現、他言語でそのまま使って大丈夫？意外な落とし穴と対策

## 要約
海外研究（ESEC/FSE ’19）と大規模実測で、開発者の多くが正規表現を再利用している一方で、言語間で挙動や性能が異なるケースが多く存在することが明らかになった。結論：安易なコピペは危険、実機でのテストが必須。

## この記事を読むべき理由
日本でもStack Overflowやライブラリから正規表現を流用する開発は日常的。業務アプリやログ処理、バリデーションで誤動作やパフォーマンス問題を起こすとインシデントに直結するため、挙動差と対処法を知っておく必要がある。

## 詳細解説
- 人的調査：159名の現役開発者のうち94%がネット上の正規表現をコピーして使い、47%は「言語間でそのまま動く」と考えていた。  
- コーパス解析：JavaScript/Java/PHP/Python/Ruby/Go/Perl/Rustの主要パッケージレジストリから合計537,806個のregexを抽出（193,524モジュール）。同一語句の重複は言語内・言語間で多数確認され、約20%のモジュールが他と同じregexを共有。約5%のモジュールはStack OverflowやRegExLib由来。  
- 挙動比較（Witness）手法：ランダム入力を各言語と複雑なregexに対して実行し、差分を3種類で分類  
  1. Match witness：マッチする／しないで言語が不一致  
  2. Substring witness：マッチはするがマッチした部分文字列が異なる  
  3. Capture witness：マッチ・部分文字列は同じだがキャプチャの切り分けが異なる  
- 主な発見：言語ペアで差分が観測される（例：JavaScript⇄JavaでMatch差異が約4%）。全体で約15%の正規表現が文書化された差異あるいは未文書の差異を示した。  
- 原因の分類：ある言語だけがサポートする機能、同じ構文が異機能を表す、同機能でも実装挙動が異なる、など。例：アンカー表記の解釈（/\Ab\Z/ が文字通り "AbZ" と解釈されるケース）、/^a/ が入力先頭と行頭で異なる扱いになる言語（Rubyなど）。  
- 余波：V8（JS）、Python、Rustの正規表現エンジンでバグが発見され、報告されている。研究の結論は「ドキュメントを読むより実測で動作を確かめるべき」。

## 実践ポイント
- コピー元を疑え：Stack Overflow等から流用する場合は必ず対象言語／実行環境でテストする。  
- 自動テストに組み込む：ユニットテストで代表的なマッチ・非マッチ・キャプチャのケースをCIで常時検証する。  
- 互換性を優先：可能ならPOSIXやECMAScriptの標準的なサブセットだけを使う（拡張機能やエンジン固有の拡張は避ける）。  
- フラグとモードを明示：^,$,m,sなどのフラグ（行単位／入力単位）の意味が言語で異なるため明示的に指定して確認する。  
- 性能対策：再帰的/バックトラックが深くなるパターンは各エンジンで爆発するので、RE2等のバックトラックを抑えるライブラリや入力サイズ制限を検討する。  
- 差異の疑いがある場合は小さな検証スイートを作り、発見した不一致はバグとして報告・記録する。

短く言えば：正規表現は「言語横断の共通語」ではない。コピペ前にテストと防護策を。
