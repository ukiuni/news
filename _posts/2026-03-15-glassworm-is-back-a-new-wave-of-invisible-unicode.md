---
layout: post
title: "Glassworm Is Back: A New Wave of Invisible Unicode Attacks Hits Repositories - Glassworm再来：リポジトリを襲う不可視Unicode攻撃の新波"
date: 2026-03-15T15:32:59.384Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.aikido.dev/blog/glassworm-returns-unicode-attack-github-npm-vscode"
source_title: "Glassworm Returns: Invisible Unicode Malware Found in 150+ GitHub Repositories"
source_id: 47387047
excerpt: "不可視UnicodeでGlasswormがリポジトリや拡張を密かに汚染、即スキャン必須"
---

# Glassworm Is Back: A New Wave of Invisible Unicode Attacks Hits Repositories - Glassworm再来：リポジトリを襲う不可視Unicode攻撃の新波
Glasswormが仕掛ける「見えないコード」の供給網攻撃 — あなたのリポジトリも狙われています

## 要約
Invisible Unicode（目に見えない文字）を使ったマルウェア「Glassworm」が再び広がり、GitHubの150以上のリポジトリに加え、npmやVS Code拡張にも波及しています。可視的な差分だけでは検出できないのが特徴です。

## この記事を読むべき理由
依存ライブラリやエディタ拡張を通じたサプライチェーン攻撃は日本の開発現場でも現実的な脅威です。見た目では分からない改ざんを防ぐための実践的対策を今すぐ確認してください。

## 詳細解説
- 攻撃手法：攻撃者はPUA（Private Use Area）や合字・Variation Selectorsなどの「不可視Unicode文字」をファイル内に埋め込み、デコーダで元のバイト列を復元してevalなどで実行します。エディタやGitの差分表示では空文字列に見えるため、レビューやlintをすり抜けます。  
- 例（デコーダ概念）：以下の例ではバックティック内が一見空だが不可視文字で埋まっており、デコードしてevalで実行する流れです。

```javascript
const s = v => [...v].map(w => (w = w.codePointAt(0),
  w >= 0xFE00 && w <= 0xFE0F ? w - 0xFE00 :
  w >= 0xE0100 && w <= 0xE01EF ? w - 0xE0100 + 16 : null))
  .filter(n => n !== null);
eval(Buffer.from(s(``)).toString('utf-8'));
```

- 規模と標的：2026年3月の波では少なくとも151件のGitHubリポジトリが一致パターンで検出され、Wasmer周りやReworm、opencode-benchなど注目リポジトリも含まれます。攻撃はnpmパッケージやVS Code拡張にも及んでいます。  
- カモフラージュ：コミットはドキュメント修正やバージョン更新など自然に見える差分で行われ、攻撃者は大規模なカスタム差分作成にLLMを活用している可能性があります。

## 実践ポイント
- まずスキャン：リポジトリ内の不可視Unicodeを検出するスクリプトでチェックする。例（追跡ファイルを検索）:

```bash
perl -nle 'print "$ARGV:$.: $_" if /[\x{FE00}-\x{FE0F}\x{E0100}-\x{E01EF}]/' $(git ls-files)
```

- CIに組み込む：コミット/PR段階で不可視文字検出を自動化し、マルウェアシグネチャやパターン（上のデコーダ類似コード）でブロックする。  
- パッケージ運用の防御：依存は固定（lockfile）、サードパーティパッケージは署名/確認、公開パッケージの突発的なバージョン増加に注意。拡張機能は公式・信頼済みソースのみ利用。  
- ツール活用：SCA／マルウェアスキャン（不可視文字検出対応）の導入や、インストール前にスキャンするラッパー（npm/yarnラッパー等）を検討する。  
- レスポンス体制：サプライチェーン被害時のロールバック、認証情報のローテーション、影響範囲（ビルド／CI／配布）を即座に評価する手順を用意する。

短くまとめると、「見えない文字」による改ざんは簡単に見逃されるため、可視的レビューに頼らず自動検出と依存管理の強化が必須です。
