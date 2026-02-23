---
layout: post
title: "Codeigniter4 multi tenancy - Codeigniter4 マルチテナンシー"
date: 2026-02-23T09:19:13.924Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/nuelcyoung/tenantable"
source_title: "GitHub - nuelcyoung/tenantable"
source_id: 398754418
excerpt: "tenantableでサブドメイン検出と接頭辞／別DBで安全なマルチテナント化"
image: "https://opengraph.githubassets.com/4e2871ea508dc36ea4a3ed38e97af2b5aed83dd16b48ec5f81b04f053f2cdb1a/nuelcyoung/tenantable"
---

# Codeigniter4 multi tenancy - Codeigniter4 マルチテナンシー
サブドメインでテナントを自動識別、隔離までやってくれるCodeIgniter4向けパッケージ「tenantable」をわかりやすく解説

## 要約
tenantableはCodeIgniter4向けのマルチテナント支援パッケージで、サブドメイン検出／自動テナントコンテキスト／複数の隔離（共有テーブル+tenant_id・テーブル接頭辞・テナント別DB）を提供します。簡単導入でテナント境界を守りやすくします。

## この記事を読むべき理由
日本のSaaSや社内複数組織対応アプリでもマルチテナンシー設計は必須です。tenantableは手軽に導入でき、運用・セキュリティ上の落とし穴（IDORやクエリ漏れ）にも配慮した選択肢を提示します。

## 詳細解説
- 主な機能
  - サブドメインからテナント自動検出（例: tenant1.example.com）
  - モデル・クエリをテナント境界内に自動適用
  - スーパ管理者によるバイパス、CLI対応、管理用サービスとヘルパー

- サポートする隔離戦略（利点・欠点）
  1. tenant_id（共有テーブル＋tenant_id）
     - Pros: 実装が最もシンプル
     - Cons: traitを忘れたモデルや生SQLでテナント分離を破る危険あり（漏洩リスク）
  2. テーブル接頭辞（推奨）
     - Pros: tenant_1_students のように物理的に分離され漏洩リスクが少ない
     - Cons: テーブル数が増え、セットアップ・マイグレーションがやや複雑
  3. テナント別DB（最も隔離）
     - Pros: 完全分離、コンプライアンス向け
     - Cons: 最も複雑（接続管理・運用コスト増）

- 使い方（要点）
  - インストール: composer require nuelcyoung/tenantable
  - フィルターでリクエスト時にテナント判定を挟む（app/Config/Filters.php）
  - モデルでTraitを使う（例：テーブル接頭辞戦略）
```php
use nuelcyoung\tenantable\Traits\TenantTablePrefixModel;

class StudentModel extends TenantTablePrefixModel
{
    protected $table = 'students';
}
// テナントID=1なら tenant_1_students へ自動的にクエリが飛ぶ
```
  - コンフィグ例（app/Config/Tenantable.php）
    - $prefixFormat = 'tenant_{id}_{table}';
    - $baseDomain = 'example.com';
    - $separateDatabasePerTenant = true; // 別DBを使う場合

- ランタイムヘルパー
  - tenant_id(), tenant(), has_tenant(), tenant_url(), can_bypass_tenant() など
  - 管理的に手動設定：TenantManager::getInstance()->setTenantById(1)

- セキュリティ上の注意
  - tenant_id方式は漏洩リスクあり。生SQLやジョインでテナント条件を忘れるとIDOR発生。
  - 可能ならテーブル接頭辞か別DBを採用し、グローバルなバイパスログやミドルウェアを有効化する。

- 既存アプリの移行案
  - Option A（推奨）：テーブル接頭辞へ移行。既存テーブルをコピーして prefixed に置き換える。
  - Option B：全テーブルに tenant_id を追加してバックフィル。簡単だが注意が必要。

- パッケージ構成（概略）
  - Config, Database/Migrations, Filters, Middleware, Models, Services, Traits, Helpers などが揃っており、拡張や運用ツールも備える。

## 実践ポイント
- 初期推奨：多くのケースでは「テーブル接頭辞」を採用してリスクを減らす。
- 開発フロー：まずローカルでテナント用DB/サブドメインを用意して総合テストを実行。CLI挙動も確認する。
- セキュリティ対策：生SQLを避け、モデルに必ずTraitを適用。スーパ管理者バイパスは監査ログを取る。
- 既存サービス移行：マイグレーション計画を明確にし、データバックアップ→段階的切替を行う。

この記事を読めば、tenantableが提供する選択肢と現実的な運用上の注意点がつかめます。導入前に「想定テナント数」「運用負荷」「コンプライアンス要件」を整理して最適な隔離戦略を選んでください。
