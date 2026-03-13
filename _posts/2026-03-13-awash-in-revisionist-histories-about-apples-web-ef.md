---
layout: post
title: "Awash in revisionist histories about Apple's web efforts, a look at the evidence - クパチーノの慰める神話：Appleのウェブ対応を検証する"
date: 2026-03-13T23:24:39.182Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://infrequently.org/2025/09/cupertinos-comforting-myths/"
source_title: "Comforting Myths - Infrequently Noted"
source_id: 908569494
excerpt: "iPhone普及の日本で、Safariの制約がWeb機能を阻む実態を暴く検証記事"
image: "https://infrequently.org/2025/09/cupertinos-comforting-myths/webstatus-missing-features.jpg"
---

# Awash in revisionist histories about Apple's web efforts, a look at the evidence - クパチーノの慰める神話：Appleのウェブ対応を検証する

iPhone市場で「使えるWeb」と「使えないWeb」が決まる—Safariは本当に協調的か？日本の現場に迫る検証記事

## 要約
Apple（WebKit/Safari）は過去10年でChrome/Firefoxに比べて多くのWeb API導入で遅れを取り、しかもiOSでの独占的制約によりその遅れがウェブ全体の機能性に直結している。Web MIDI、Web USB、Web Bluetoothといった実運用で有効だったAPIでもAppleからの代替提案や実証的な反論がほとんど見られない。

## この記事を読むべき理由
日本は世界でもiPhone利用率が高く、iOS対応の差がユーザー体験とビジネス機会を左右する。教育現場や業務系Webアプリのユースケース（例：教室でのUSBデバイス利用）に直結する問題なので、開発者・企画者は事実関係と対策を知っておく必要がある。

## 詳細解説
- データ概況：Chromiumに実装されているがSafariにない機能が約178件、一方Safari固有は約34件。Safariは他ブラウザより「リードして同時実装する」頻度が低く、多くは数年遅れで追随する傾向がある。  
- ガバナンスの問題：iOS上の全ブラウザがWebKitを使うため、Appleの実装や方針が市場全体の“最低線”を決める。通常の競争で生じる機能淘汰が機能しない。  
- ハードケースの具体例：  
  - Web MIDI：macOS/iOSのネイティブMIDI歴は長いが、Web MIDIに対するAppleの公開での代替案や協議記録が見当たらない。  
  - Web USB：選択ダイアログや権限設計で安全性が保たれる実運用があるが、Appleは実装を拒否し、代替提案を提示していない。教育用途での有用性が示されているにも関わらず具体的解決がない。  
  - Web Bluetooth：同様に安全設計（ユーザー選択・GATT制限等）が施されているが、Apple側の公的な関与や代案提示は乏しい。  
- 結論的観察：Appleは「プライバシー/安全上の懸念」を理由に一部APIを拒否するが、拒否に対するエビデンス提示や代替設計の公開がなく、結果としてウェブの機能拡張が抑制されている。

## 実践ポイント
- iOS/Safariでの動作確認を開発フローに必須化する（モバイル優先の日本市場では特に重要）。  
- feature-detection とプログレッシブ・エンハンスメントで代替UXを設計する（可能ならpolyfillやネイティブ連携を用意）。  
- 教育・業務でのUSB/Bluetooth利用は事前にiOS対応の選択肢（ネイティブアプリ、MIDI over Webの代替等）を検討する。  
- 技術的証拠（利用実績、セキュリティ評価、ユーザー事例）を集めて、W3C/WebKitのIssueやコミュニティに提出し、公開議論を促す。  
- Web Feature Statusなどで追跡し、長期的には標準化活動や業界連携でエコシステム改善を働きかける。

以上。
