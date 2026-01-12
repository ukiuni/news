---
layout: post
title: "A Developer’s Guide to Naming Things Right - 命名を正しくする開発者ガイド"
date: 2026-01-12T21:46:14.266Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://blog.stackademic.com/developer-guide-naming-conventions-a66203fd5665"
source_title: "A Developer’s Guide to Naming Things Right"
source_id: 429637056
excerpt: "命名を統一してコード検索・レビュー・オンボーディングを劇的に速くする方法"
---

# A Developer’s Guide to Naming Things Right - 命名を正しくする開発者ガイド
思わずリポジトリを開きたくなる「名前」ルール — 迷わないコードはチームの生産性を上げる

## 要約
命名は詩ではなく「開発者UX」。動詞は一意に、実装でなく能力で命名し、検索性と予測性を最優先にすると保守が劇的に楽になる。

## この記事を読むべき理由
日本のチームでは設計書やドキュメントよりもコードが事実を語ります。命名ルールを揃えるだけでコードレビュー、バグ追跡、オンボーディングが速くなり、採用・外部パートナーとの協業コストも下がります。

## 詳細解説
- 基本原則（短く厳格）
  - 一つの動詞 = 一つの意味：fetch＝常に「ネットワーク取得」、read＝「キャッシュやファイルからの読み取り」など。意味を揺らさない。
  - 実装ではなく能力で命名：loadUser() が Redis に変わっても loadUser() のまま。loadUserFromRedis() のように実装依存にしない。
  - 派手さは不要：馴染みやすさを優先。チームが名前を見て動作を予測できることが最重要。
  - grep に最適化：検索で一発で出る命名を心がける（例：ネットワークは fetch, API は apiFetch など統一）。

- よくある混乱と推奨語彙
  - ネットワーク取得：fetch / fetchUser / fetchFromNetwork
  - キャッシュ読み取り：readCached / getCached / getFromCache
  - 同期的な単純取得（ローカルメモリ）：get / getUser
  - 大きな初期化処理：load / initialize
  - 破壊的操作：set / update / delete / mutate（副作用があると明示）
  - ブール値：isEnabled, hasPermission, shouldRetry（プレフィックスで意味明確化）
  - イベントハンドラ：handleClick（処理する関数） vs onClick（イベント発火側）

- JavaScript/TypeScript の例（改善前 → 改善後）
```javascript
// JavaScript
// 悪い例（曖昧）
async function getUser(id) { /* どの層にアクセスする？ */ }

// 良い例（明確）
async function fetchUserFromApi(id) { /* ネットワーク */ }
function getCachedUser(id) { /* キャッシュ読み取り */ }
function getUserFromMemory(id) { /* メモリ取得 */ }
```

- コードベース全体での一貫性手段
  - 命名ガイドをリポジトリに置く（CONTRIBUTING.md に短い章を追加）
  - ESLint/TSLint でルール化（関数名パターン、boolean プレフィックスを強制など）
  - IDE の Rename 機能と型情報を活用して安全にリファクタ
  - PR テンプレートに「命名変更があるか」のチェックを入れる

## 実践ポイント
- 今すぐできること（30分）
  1. リポジトリのルートに「命名ガイド」を1枚書く（fetch/read/get の使い分けを明記）。
  2. 5つの代表的な関数名（API, キャッシュ, メモリ, 初期化, 削除）をチームで決める。
  3. ESLint のカスタムルールで boolean プレフィックスやハンドラ命名をチェックする。

- 中期施策（数日〜数週間）
  - 既存コードを grep して曖昧な命名をリファクタ（IDE の Rename を使う）。
  - 新人向けオンボーディングに命名ガイドを組み込む。

- ヒント
  - 「短いが説明的」を目標に。長くても意味が明確な方が良い（例：fetchUserFromApi は冗長でもOK）。
  - 命名規約は一度決めたらチームで守ること。バラバラなルールは最悪。

このガイドをリポジトリのルール化作業の起点にし、まずは「チームで1ページの命名ガイド」を作ることを推奨します。
