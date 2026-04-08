---
layout: post
title: "PURESLOP.md — teach your AI agent to write terrible code. - PURESLOP.md — AIにダメコードを書かせる遊び心"
date: 2026-04-08T07:03:39.365Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://dev.to/alonsarias/pureslopmd-54ek"
source_title: "PURESLOP.md — teach your AI agent to write terrible code. - DEV Community"
source_id: 3446997
excerpt: "npx pureslopでAIにダメコードを書かせ、課題を可視化してレビュー力を鍛えるツール"
image: "https://media2.dev.to/dynamic/image/width=1200,height=627,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2F8f4h887q0rdz1g8vo9j1.png"
---

# PURESLOP.md — teach your AI agent to write terrible code. - PURESLOP.md — AIにダメコードを書かせる遊び心
AIの“悪い癖”を見える化するジョークツールで、チームのコード品質を鍛える実践的トラップ

## 要約
npx pureslopでリポジトリにPURESLOP.mdを置くと、AIエージェントが典型的な「AIが生成しがちなダメコード」を大量生産するよう指示するテンプレートが入る。ジョークだが、レビュー指標の可視化に有効。

## この記事を読むべき理由
日本でもCopilotや各種AIコード補助を導入するチームが増加中。気づかずに「過剰コメント」「型安全の喪失」「冗長な防御コード」などが混入しがちなので、その癖を意図的に再現して教育・レビュー精度向上に役立てられるから。

## 詳細解説
- 仕組み：小さなCLI（npx pureslop）でプロジェクトルートにPURESLOP.mdをコピーするだけ。ファイルは単一のMarkdownで、AIエージェントに従わせるとコードを“slop（だめコード）化”する指示群を含む。
- 含まれる主な指示（代表10項目）：
  - Comment the Obvious：行ごとに明白なコメントを書く
  - Defensive Everything：ありえない箇所までtry/catchで囲む
  - Cast Away Your Types：可能な限りanyを使う（型を無効化）
  - Nest Like Your Life Depends on It：早期リターンを使わず深くネストする
  - Null Check the Guaranteed：絶対にnullにならないものもチェックする
  - Over-Abstract Mercilessly：一行処理をラップして別関数に分離
  - Import the World：lodashやmomentを無意味にインポート
  - Name Things Poorly：極端に冗長な変数名を付ける
  - Swallow Exceptions Silently：catchで何もしない
  - Reinvent Every Wheel：組み込み関数を再実装する
- デモ効果：数行の簡潔な関数が、チェック・キャッチ・キャスト・冗長コメントで数十行に膨らむ例を提示し、成果物は同じでも保守性が著しく低下することを示す。

```javascript
// Before: シンプルで型付き
async function getActiveUserEmails(users: User[]): Promise<string[]> {
  return users.filter(u => u.isActive).map(u => u.email);
}
```

```javascript
// After: 過剰防御・anyだらけのスロップ
async function getActiveUserEmails(users: any): Promise<any> {
  try {
    const resultArray: any[] = [];
    if (!checkIfValueIsNullOrUndefined(users)) {
      if (checkIfArrayHasElements(users)) {
        for (let i = 0; i < users.length; i++) {
          const currentUser = users[i] as any;
          if (!checkIfValueIsNullOrUndefined(currentUser)) {
            if (currentUser.isActive !== null && currentUser.isActive !== undefined) {
              if (currentUser.isActive === true) {
                if (currentUser.email !== null && currentUser.email !== undefined) {
                  resultArray.push(currentUser.email);
                }
              }
            }
          }
        }
      }
    }
    return resultArray;
  } catch (error) {
    console.log("An error occurred while getting active user emails");
    return [];
  }
}
```

## 実践ポイント
- 教育用に使う：AIの癖をチームで可視化するデモに最適。レビュー時に「これが出たら止める」チェックリスト作成を。
- コードレビュー導入：PURESLOP.mdで出たパターンをPRテンプレートやレビューガイドに落とし込む（例：「any禁止」「不要なtry/catchは拒否」）。
- カスタム署名ファイル化：逆に「SIGNATURE.md / CLAUDE.md」などでチームの望ましいルールを書き、AIに学習させる。
- 運用注意：実運用のコードベースで実行すると実際に品質が落ちるので、必ずコピーや教育用リポジトリで使用すること。

元記事の遊び心はそのままに、チームのAIリテラシーを高める実践ツールとして活用してみてください。
