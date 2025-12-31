---
layout: post
title: "ArchUnitTS vs eslint-plugin-import: My side project reached 200 stars on GitHub - ArchUnitTS と eslint-plugin-import：サイドプロジェクトが GitHubで200★に到達"
date: 2025-12-31T09:40:03.611Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://lukasniessen.medium.com/archunitts-vs-eslint-plugin-import-my-side-project-reached-200-stars-on-github-63629fad96ab"
source_title: "ArchUnitTS vs eslint-plugin-import: My side project reached 200 stars on GitHub"
source_id: 475757115
excerpt: "ArchUnitTSでTypeScriptの境界をCIでテスト化しNxモノレポの設計を守る"
---

# ArchUnitTS vs eslint-plugin-import: My side project reached 200 stars on GitHub - ArchUnitTS と eslint-plugin-import：サイドプロジェクトが GitHubで200★に到達
TypeScriptアーキテクチャ検証を「テスト化」する理由 — eslintだけでは守り切れない境界をCIで強制する

## 要約
ArchUnitTSはTypeScript向けのアーキテクチャ検証ライブラリで、依存関係チェックに加えコードメトリクス、Layer/Slice検証、Nx対応、HTMLレポートなどリントでは難しい「設計単位でのテスト」を提供する。

## この記事を読むべき理由
日本でも大型のTypeScriptプロジェクトやNxモノレポ運用が増えています。コード品質やモジュール境界の保証をESLintだけに頼ると見落としが出やすく、CI段階で設計規約を自動検証したいチームにとってArchUnitTSは実務的な価値があります。

## 詳細解説
ArchUnitTSは単なるimportの有無チェックを超え、設計ルールをテストとして宣言的に書ける点が特徴です。主な技術的差分は次の通り。

1. コードメトリクス解析  
   - LCOM（メソッドの結合度）、行数・メソッド数・フィールド数、サイクロマティック複雑度などを取得でき、品質ゲートに使える。カスタムメトリクスも定義可能。

2. スライス／レイヤ検証  
   - PlantUML等のアーキ図と照合する機能や、projectSlices().definedBy()で論理的なモジュール境界を定義し、層間ルールを一括検証できる。

3. Nxモノレポ対応  
   - Nxのプロジェクトグラフを読み取り、アプリケーション／ライブラリ間の境界や命名規約を検証可能。モノレポ運用での境界漏れを防止。

4. HTMLレポート生成  
   - チャート付きのダッシュボードや詳細レポートを出力し、レビューやアーキテクト会議で共有しやすい。

5. 空テスト保護  
   - 指定パターンにマッチするファイルが無い場合に失敗させる設定があり、タイプミスによる「常に成功」を防ぐ。

6. カスタムルールと高度なログ  
   - 任意のロジックでルールを定義でき、複数ログレベルやCI向けのファイル出力で調査性が高い。

7. パターンマッチやクラス解析の柔軟性  
   - フォルダ／名前／パスの組合せフィルタや、クラス単位の解析（フィールド数制限、結合度など）も可能。

一方で eslint-plugin-import が優れる点もあります：エディタでのリアルタイム表示、自動修正(--fix)、設定だけで動く手軽さ。つまり用途は補完的です。

簡単なArchUnitTSのテスト例（概念）:
```typescript
// TypeScript
it('presentation should not depend on database', async () => {
  const rule = projectFiles()
    .inFolder('src/presentation/**')
    .shouldNot()
    .dependOnFiles()
    .inFolder('src/database/**');
  await expect(rule).toPassAsync();
});
```

## 実践ポイント
- 小〜中規模なら eslint-plugin-import をまず導入してリアルタイムのインフォームを得る。  
- モノレポや大規模プロジェクト、CIで設計保証が必要なら ArchUnitTS を追加。テスト化することでリファクタ時の回帰を確実に防げる。  
- まずは1つのルール（例：presentation→databaseの依存禁止）をCIのパイプラインに組み込み、レポートをチームで確認する運用を試す。  
- Nxを使っているならプロジェクトグラフ検証を有効化して、命名規約／タイプ境界を自動チェックする。  
- 空テスト保護を有効にして、パターン指定ミスによるスルーを防ぐ。

## 引用元
- タイトル: ArchUnitTS vs eslint-plugin-import: My side project reached 200 stars on GitHub  
- URL: https://lukasniessen.medium.com/archunitts-vs-eslint-plugin-import-my-side-project-reached-200-stars-on-github-63629fad96ab
