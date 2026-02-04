---
layout: post
title: "Fitness Functions: Automating Your Architecture Decisions - フィットネス関数：アーキテクチャ決定を自動化する"
date: 2026-02-04T07:21:01.941Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://lukasniessen.medium.com/fitness-functions-automating-your-architecture-decisions-08b2fe4e5f34"
source_title: "Fitness Functions: Automating Your Architecture Decisions"
source_id: 409683711
excerpt: "フィットネス関数でCIに設計ルールを自動化し崩壊を即検知する実践法"
---

# Fitness Functions: Automating Your Architecture Decisions - フィットネス関数：アーキテクチャ決定を自動化する
アーキテクチャの“魂”をコードで守る—フィットネス関数で設計崩壊を即検知する方法

## 要約
フィットネス関数は「設計ルールを自動テスト化」して、コードが意図したアーキテクチャから逸脱するのをCI上で即座に防ぐ仕組みです。

## この記事を読むべき理由
日本でもマイクロサービス化、モノリス分割、データメッシュ採用が進む中、設計崩壊（architectural drift）は開発速度や運用コストを急速に悪化させます。人の目に頼らない自動ガバナンスはスケールする組織で必須です。

## 詳細解説
- フィットネス関数とは  
  Neal Fordらの概念で、実装が設計目標にどれだけ近いかを評価する自動テスト。ユニットテストが振る舞いを検証するのに対し、フィットネス関数は構造・依存関係・命名規約など「設計の守るべきルール」をチェックします。違反はPR段階で弾かれ、ガバナンスを「検査」から「ルール化」へシフトします。

- 三つの柱  
  1) ルールによるガバナンス（人頼みを減らす）  
  2) チームが即時に発見できる仕組み（独立監査ではなく開発時）  
  3) 継続的ガバナンス（すべてのコミットでチェック）

- 典型的なチェック例  
  - レイヤー依存：presentation が database を直接参照しない  
  - 循環依存の検出（リファクタ不能化の防止）  
  - 命名規約やファイル長、複雑度などのメトリクス  
  - ドメイン層のフレームワーク分離

- ツール例（コードでルールを書く）  
  Java: ArchUnit の例
  ```java
  // java
  @Test
  public void services_should_not_access_controllers() {
    noClasses().that().resideInAPackage("..service..")
      .should().accessClassesThat().resideInAPackage("..controller..")
      .check(importedClasses);
  }
  ```
  TypeScript: ArchUnitTS の例
  ```typescript
  // typescript
  it('presentation should not depend on database', async () => {
    const rule = projectFiles().inFolder('src/presentation/**')
      .shouldNot().dependOnFiles().inFolder('src/database/**');
    await expect(rule).toPassAsync();
  });
  ```

- コード以外への応用（データプロダクト等）  
  データカタログのメタデータに対して、「説明があるか」「SLOが定義されているか」「発見可能か」などを自動検証しダッシュボードに公開することで、分散管理下でも品質を担保できます。

- LLMを使った「曖昧基準」の自動化（2026年のトレンド）  
  「説明が十分か」「データプロダクトは一貫した概念か」など定義が難しい評価は、関数呼び出しで構造化された出力を返すLLMで半自動化できます。ただし非決定性・コスト・説明性の課題は残るため運用ポリシーが必要です。

- 運用パターン  
  - ダッシュボード化：チーム別の合否を見せると効果的  
  - 段階的厳格化：一度に大量のルールを押し付けない  
  - 例外管理：注釈や申請で一時的免除を許可し記録する

## 実践ポイント
- まず1ルール：頻出の違反を1つ選びテスト化してCIに組み込む。  
- 徐々に増やす：チームの導入障壁を下げ、全体の合格率を維持する。  
- 例外フローを設計：// @arch-ignore のように免除をトラッキングする仕組みを用意する。  
- LLMは補助的に：毎コミットではなく夜間バッチや週次で運用し、コストとブレを抑える。  
- 可視化：失敗の原因や該当箇所を分かりやすく出して、オンボーディングとリファクタの自信を高める。

これらを積み重ねれば、「設計は会議で決めるもの」から「設計はコードで守るもの」へとチーム文化を変えられます。
